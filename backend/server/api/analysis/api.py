import os
import io
import json
import tempfile
import random
import asyncio
import requests
import numpy as np

from fastapi import APIRouter, UploadFile, HTTPException, Depends
from fastapi.responses import StreamingResponse

from database.adapter import MongoDBAdapter
from database.manager import get_adapter

from ml.audio.chunk import chunk_audio_parallel_with_padding
from ml.audio.classify import classify_audio_chunk

from ml.video.chunk import chunk_video_parallel_with_padding
from ml.video.classify import classify_video_chunk

from ml.feedback import generate_feedback
from ml.score import calculate_speaking_score

from globals.getter import get_global_s3_storage

from api.tags import APITags
from api.asset.utils import extract_audio

from utils.auth import generate_uuid

from dotenv import load_dotenv

load_dotenv()

AnalysisAPIRouter = APIRouter(prefix="/analysis", tags=[APITags.ANALYSIS])

CHUNK_DURATION = int(os.environ.get("ANALYSIS.CHUNK_DURATION", 5))
CHUNK_OVERLAP_DURATION = int(
    os.environ.get("ANALYSIS.CHUNK_OVERLAP_DURATION", 0)
)
SAMPLING_RATE = int(os.environ.get("ANALYSIS.SAMPLING_RATE", 20000))

def get_asset_mongodb_adapter() -> MongoDBAdapter:
    return get_adapter("asset")


# Ideally we should take it from asset_id but FUCK there is no time
# I'm taking the video input directly
@AnalysisAPIRouter.post("/")
async def analyze_audio_video(
    video_file: UploadFile
):
    try:
        # Read video file to bytes
        video_bytes = await video_file.read()
        
        # Save to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            temp_file.write(video_bytes)
            video_file_path = temp_file.name

        # Extract audio from the video
        audio_buffer = await extract_audio(video_bytes)

        # Process video chunks
        video_chunks = chunk_video_parallel_with_padding(
            video_file_path,
            chunk_duration=CHUNK_DURATION,
            overlap=CHUNK_OVERLAP_DURATION,
            fps=30,
        )

        video_data = [
            {
                "frame": np.array(chunk[0], dtype=np.float32),
                "timestep": chunk[1],
            }
            for chunk in video_chunks
        ]

        # Process the audio file
        audio_stream = io.BytesIO(audio_buffer)
        audio_chunks = chunk_audio_parallel_with_padding(
            audio_stream,
            chunk_duration=CHUNK_DURATION,
            overlap=CHUNK_OVERLAP_DURATION,
            sample_rate=SAMPLING_RATE,
        )

        audio_data = [
            {
                "audio": np.array(chunk[0], dtype=np.float32),
                "timestep": chunk[1],
            }
            for chunk in audio_chunks
        ]

        print("\n\nChunk size : ", len(audio_data), len(video_data), "\n\n")
        fps = 30

        async def generate_analysis():
            for i, (audio_chunk, video_chunk) in enumerate(
                zip(audio_data, video_data)
            ):
                print(f"Processing timestep {i}")
                audio_results = classify_audio_chunk(audio_chunk)

                video_results = classify_video_chunk(
                    video_chunk["frame"],
                    fps,
                    i,
                    frames_per_chunk=CHUNK_DURATION * fps,
                )

                feedback = generate_feedback(
                    audio_results["mean_pitch"],
                    audio_results["mean_loudness"],
                    audio_results["pitch_variation"],
                    audio_results["loudness_variation"],
                    audio_results["emotions"][0],
                )

                score = calculate_speaking_score(
                    audio_results["pitch_variation"],
                    audio_results["loudness_variation"],
                    40,
                    audio_results["silence_duration"],
                    audio_results["average_volume"],
                )

                analysis_result = {
                    "timestep": audio_results.get("timestep"),
                    "score": score,
                    "feedback": feedback,
                    "audio": {
                        "mean_pitch": audio_results.get("mean_pitch"),
                        "mean_loudness": audio_results.get("mean_loudness"),
                        "pitch_variation": audio_results.get("pitch_variation"),
                        "loudness_variation": audio_results.get("loudness_variation"),
                        "silence_duration": audio_results.get("silence_duration"),
                        "average_volume": audio_results.get("average_volume"),
                        "background_noise_level": audio_results.get("background_noise_level"),
                    },
                    "video": {
                        "emotions": video_results.get("emotions", []),
                        "frequencies": video_results.get("frequencies", []),
                    }
                }

                yield json.dumps(analysis_result) + "\n"

        return StreamingResponse(
            generate_analysis(), media_type="application/json"
        )

    except Exception as e:
        print("Error occurred while analyzing: ", e)
        raise HTTPException(status_code=500, detail="Something went wrong")

    finally:
        if os.path.exists(video_file_path):
            os.remove(video_file_path)

import os
import io
import json
import asyncio
import numpy as np

from fastapi import APIRouter, UploadFile, HTTPException, File
from fastapi.responses import StreamingResponse

from ml.audio.chunk import chunk_audio_parallel_with_padding
from ml.audio.classify import classify_audio_chunk

from api.tags import APITags

from dotenv import load_dotenv

load_dotenv()

AnalysisAPIRouter = APIRouter(prefix="/analysis", tags=[APITags.ANALYSIS])

CHUNK_DURATION = int(os.environ.get("ANALYSIS.CHUNK_DURATION", 5))
CHUNK_OVERLAP_DURATION = int(
    os.environ.get("ANALYSIS.CHUNK_OVERLAP_DURATION", 2)
)
SAMPLING_RATE = int(os.environ.get("ANALYSIS.SAMPLING_RATE", 20000))


# FastAPI Endpoint
@AnalysisAPIRouter.post("/video")
async def analyze_video(file: UploadFile = File(...)) -> StreamingResponse:
    try:
        if not (
            file.content_type.startswith("video/")
            or file.content_type.startswith("audio/")
        ):
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Please upload a video or audio file.",
            )

        # Read file content
        file_content = await file.read()
        audio_file = io.BytesIO(file_content)

        chunks = chunk_audio_parallel_with_padding(
            audio_file,
            chunk_duration=CHUNK_DURATION,
            overlap=CHUNK_OVERLAP_DURATION,
        )
        data = [
            {
                "audio": np.array(chunk[0], dtype=np.float32),
                "timestep": chunk[1],
            }
            for chunk in chunks
        ]

        def get_feedback_in_parallel(data: list):
            for chunk in data:
                res = classify_audio_chunk(chunk)
                yield json.dumps(res).encode("utf-8")
                print("res : ", res)

        return StreamingResponse(
            get_feedback_in_parallel(data), media_type="application/json"
        )

    except asyncio.CancelledError as e:
        print("Asyncio cancellation error: ", e)
    except Exception as e:
        print("An error occurred: ", e)
        raise HTTPException(status_code=500, detail="Something went wrong")

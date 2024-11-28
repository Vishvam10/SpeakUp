import io
import os
import tempfile
import cv2
import base64

import numpy as np
import noisereduce as nr

from dotenv import load_dotenv

from moviepy import VideoFileClip
from fastapi import HTTPException, status

load_dotenv()

SAMPLING_RATE = int(os.environ.get("ANALYSIS.SAMPLING_RATE", 20000))


async def generate_thumbnail_and_extract_audio(file: io.BytesIO):
    try:
        
        video_fps = 30

        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".mp4"
        ) as temp_video_file:
            temp_video_file.write(file.read())
            temp_video_file.close()

            video = VideoFileClip(temp_video_file.name)
            video_fps = video.fps

        frame = video.get_frame(0)

        thumbnail = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        thumbnail_resized = cv2.resize(thumbnail, (100, 100))

        _, buffer = cv2.imencode(".jpg", thumbnail_resized)

        thumbnail_bytes = buffer.tobytes()
        thumbnail_base64 = base64.b64encode(thumbnail_bytes).decode("utf-8")

        audio = video.audio
        audio_buffer = None

        # Write the audio to a temporary file
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".mp3"
        ) as temp_audio_file:
            audio.write_audiofile(temp_audio_file.name, codec="mp3")

            # Ensure the buffer's cursor is at the beginning
            temp_audio_file.seek(0)
            audio_buffer = temp_audio_file.read()

            temp_audio_file.close()
            # Clean up the temporary audio file
            os.remove(temp_audio_file.name)

        audio_buffer, _ = await remove_background_noise(audio_buffer)

        return (thumbnail_base64, audio_buffer, video_fps)

    except Exception as e:
        print("Generate thumbnail and extract audio failed : ", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate thumbnail: {str(e)}",
        )


async def remove_background_noise(
    audio, sr=SAMPLING_RATE, noise_profile_duration=1.0
):
    try:
        # Extract a noise profile from the start of the audio
        noise_profile = audio[: int(sr * noise_profile_duration)]

        denoised_audio = nr.reduce_noise(y=audio, sr=sr, y_noise=noise_profile)

        # Estimate background noise level in dB.
        # Adding small value to avoid log(0)
        background_noise_level = 20 * np.log10(np.std(noise_profile) + 1e-6)

        print("Background Noise Level : ", background_noise_level)

        return denoised_audio, background_noise_level

    except Exception as e:
        print(f"Error in background noise removal : {e}")
        # Returning the original audio if an error occurs
        return audio, 0

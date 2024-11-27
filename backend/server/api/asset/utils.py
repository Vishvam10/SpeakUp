import io
import os
import tempfile
import cv2
import base64
from moviepy import VideoFileClip, AudioClip
from fastapi import HTTPException, status


async def generate_thumbnail_and_extract_audio(file: io.BytesIO):

    try:
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".mp4"
        ) as temp_video_file:
            temp_video_file.write(file.read())
            temp_video_file.close()

            video = VideoFileClip(temp_video_file.name)

        frame = video.get_frame(0)

        thumbnail = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        thumbnail_resized = cv2.resize(thumbnail, (100, 100))

        _, buffer = cv2.imencode(".jpg", thumbnail_resized)

        thumbnail_bytes = buffer.tobytes()
        thumbnail_base64 = base64.b64encode(thumbnail_bytes).decode("utf-8")

        audio = video.audio
        audio_buffer = None

        # Write the audio to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_audio_file:
            audio.write_audiofile(temp_audio_file.name, codec="mp3")
            
            # Ensure the buffer's cursor is at the beginning
            temp_audio_file.seek(0)
            audio_buffer = temp_audio_file.read()

            temp_audio_file.close()
            # Clean up the temporary audio file
            os.remove(temp_audio_file.name)

        return (thumbnail_base64, audio_buffer)

    except Exception as e:
        print("Generate thumbnail and extract audio failed : ", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate thumbnail: {str(e)}",
        )

import os
import cv2
import numpy as np

from math import ceil
from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv

load_dotenv()

CHUNK_DURATION = int(os.environ.get("ANALYSIS.CHUNK_DURATION", 5))
SAMPLING_RATE = int(os.environ.get("ANALYSIS.SAMPLING_RATE", 20000))


def create_video_chunks_with_padding(
    frames, fps, start, end, chunk_duration, step_size, min_size
):
    local_chunks = []
    for i in range(start, end, int(step_size * fps)):
        chunk_end = i + int(chunk_duration * fps)
        chunk = frames[i:chunk_end]

        # Pad the chunk if it is smaller than the minimum size
        if len(chunk) < min_size:
            padding_size = min_size - len(chunk)
            chunk = np.pad(
                chunk,
                ((0, padding_size), (0, 0), (0, 0), (0, 0)),
                mode="constant",
            )

        local_chunks.append((chunk, ceil(i / fps), ceil(chunk_end / fps)))

    return local_chunks


def chunk_video_parallel_with_padding(
    video_path,
    chunk_duration=CHUNK_DURATION,
    overlap=0,
    fps=30,
    num_workers=8,
):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Unable to open video {video_path}")
        return []

    # Get the total number of frames in the video
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frames = []

    # Read all frames from the video
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)

    cap.release()

    # Calculate step size and minimum chunk size
    step_size = chunk_duration - overlap
    min_size = int(chunk_duration * fps)

    # Divide frames into sections for parallel processing
    section_size = total_frames // num_workers
    sections = [
        (
            frames,
            fps,
            i,
            min(i + section_size, total_frames),
            chunk_duration,
            step_size,
            min_size,
        )
        for i in range(0, total_frames, section_size)
    ]

    # Process each section in parallel using ThreadPoolExecutor
    chunks = []
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        results = executor.map(
            lambda args: create_video_chunks_with_padding(*args), sections
        )
        for result in results:
            chunks.extend(result)

    return chunks

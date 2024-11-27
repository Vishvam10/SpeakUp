import os
import numpy as np
import librosa
from math import ceil

from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv

load_dotenv()

CHUNK_DURATION = int(os.environ.get("ANALYSIS.CHUNK_DURATION", 5))
CHUNK_OVERLAP_DURATION = int(
    os.environ.get("ANALYSIS.CHUNK_OVERLAP_DURATION", 2)
)
SAMPLING_RATE = int(os.environ.get("ANALYSIS.SAMPLING_RATE", 20000))

def create_chunks_with_padding(audio, sr, start, end, chunk_duration, step_size, min_size):

    local_chunks = []
    for i in range(start, end, int(step_size * sr)):
        chunk_end = i + int(chunk_duration * sr)
        chunk = audio[i:chunk_end]

        if len(chunk) < min_size:
            chunk = np.pad(chunk, (0, min_size - len(chunk)), mode="constant")

        local_chunks.append((chunk, ceil(i / sr), ceil(chunk_end / sr)))
    return local_chunks

def chunk_audio_parallel_with_padding(audio_path, chunk_duration=CHUNK_DURATION, overlap=CHUNK_OVERLAP_DURATION, sample_rate=SAMPLING_RATE, num_workers=4):

    audio, sr = librosa.load(audio_path, sr=sample_rate, mono=True)
    step_size = chunk_duration - overlap
    min_size = int(chunk_duration * sr)

    # Divide the audio range into sections for parallel processing
    total_length = len(audio)
    section_size = total_length // num_workers
    sections = [(audio, sr, i, min(i + section_size, total_length), chunk_duration, step_size, min_size)
                for i in range(0, total_length, section_size)]

    # Process each section in parallel
    chunks = []
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        results = executor.map(lambda args: create_chunks_with_padding(*args), sections)
        for result in results:
            chunks.extend(result)

    return chunks
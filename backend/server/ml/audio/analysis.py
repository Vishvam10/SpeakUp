import numpy as np

from ml.audio.loudness import extract_loudness
from ml.audio.pitch import extract_pitch


def analyze_modulation_and_pitch(audio, sr):
    pitch = extract_pitch(audio, sr)
    loudness = extract_loudness(audio)

    pitch_variation = np.std(pitch)
    loudness_variation = np.std(loudness)

    return pitch, loudness, pitch_variation, loudness_variation

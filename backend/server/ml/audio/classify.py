import os
from dotenv import load_dotenv

from ml.audio.analysis import (
    analyze_modulation_and_pitch,
    analyze_silence_and_volume,
)

from globals.getter import get_global_audio_classifier


load_dotenv()

EMOTION_TOP_N_RESULTS = os.environ.get("EMOTION_TOP_N_RESULTS", 3)
CHUNK_DURATION = os.environ.get("ANALYSIS.CHUNK_DURATION", 5)
CHUNK_OVERLAP_DURATION = os.environ.get("ANALYSIS.CHUNK_OVERLAP_DURATION", 2)
SAMPLING_RATE = os.environ.get("ANALYSIS.SAMPLING_RATE", 20000)


def classify_audio_chunk(chunk):
    audio_classifier = get_global_audio_classifier()

    results = audio_classifier(chunk["audio"])

    emotions, scores = [], []
    for i in range(len(results)):
        if i < EMOTION_TOP_N_RESULTS:
            emotions.append(results[i]["label"])
            scores.append(results[i]["score"])

    mean_pitch, mean_loudness, pitch_variation, loudness_variation = (
        analyze_modulation_and_pitch(chunk["audio"], SAMPLING_RATE)
    )

    silence_duration, average_volume, background_noise_level = (
        analyze_silence_and_volume(chunk["audio"], SAMPLING_RATE)
    )

    res = {
        "timestep": chunk["timestep"],
        "emotions": emotions,
        "scores": scores,
        "mean_pitch": float(mean_pitch),
        "mean_loudness": float(mean_loudness),
        "pitch_variation": float(pitch_variation),
        "loudness_variation": float(loudness_variation),
        "silence_duration": float(silence_duration),
        "average_volume": float(average_volume),
        "background_noise_level": float(background_noise_level),
    }

    return res

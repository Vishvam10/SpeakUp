import os
import json

from typing import AsyncGenerator
from dotenv import load_dotenv

from ml.audio.analysis import analyze_modulation_and_pitch
from ml.audio.feedback import generate_feedback

from globals.getter import get_global_audio_classifier


load_dotenv()

EMOTION_TOP_N_RESULTS = os.environ.get("EMOTION_TOP_N_RESULTS", 3)
CHUNK_DURATION = os.environ.get("ANALYSIS.CHUNK_DURATION", 5)
CHUNK_OVERLAP_DURATION = os.environ.get("ANALYSIS.CHUNK_OVERLAP_DURATION", 2)
SAMPLING_RATE = os.environ.get("ANALYSIS.SAMPLING_RATE", 20000)


def classify_audio_chunk(chunk):
    audio_classifer = get_global_audio_classifier()

    # Classify emotions for each chunk of audio
    results = audio_classifer(chunk["audio"])

    emotions, scores = [], []

    for i in range(len(results)):
        if i < EMOTION_TOP_N_RESULTS:
            emotions.append(results[i]["label"])
            scores.append(results[i]["score"])

    (
        pitch,
        loudness,
        pitch_variation,
        loudness_variation,
    ) = analyze_modulation_and_pitch(chunk["audio"], SAMPLING_RATE)

    feedback = generate_feedback(
        pitch, loudness, pitch_variation, loudness_variation, emotions
    )

    res = {
        "timestep": chunk["timestep"],
        "emotion": emotions,
        "score": scores,
        "feedback": feedback,
    }

    return res


def classify_audio_stream(chunk: dict) :
    res = classify_audio_chunk(chunk)
    yield json.dumps(res).encode("utf-8")

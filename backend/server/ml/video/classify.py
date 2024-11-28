import os
import cv2
import numpy as np
from PIL import Image
from math import ceil
from globals.getter import get_global_image_classifier

from collections import Counter

# Environment variable setup
EMOTION_TOP_N_RESULTS = int(os.environ.get("EMOTION_TOP_N_RESULTS", 3))
CHUNK_DURATION = int(os.environ.get("ANALYSIS.CHUNK_DURATION", 5))


def classify_image(image) -> list:
    try:
        image_classifier = get_global_image_classifier()
        pil_image = Image.fromarray((image * 255).astype(np.uint8))
        results = image_classifier(pil_image)

        predictions = [
            {"emotion": results[i]["label"], "score": results[i]["score"]}
            for i in range(min(EMOTION_TOP_N_RESULTS, len(results)))
        ]
        return predictions
    except Exception as e:
        print(f"Error processing frame: {e}")
        return []


def classify_video_chunk(
    frames, fps, start_chunk, frames_per_chunk
) -> list[dict]:
    # The chunk results are results of a CHUNK_DURATION window size. So, in the
    # end, we will somehow give an average or something similar accumulating
    # everything (in the CHUNK_DURATION window size) into 1 data point
    emotions, scores = [], []

    # We don't care about the timesteps of the intermediate frames. We
    # want an accumulated result
    starting_timestep = ceil((start_chunk * frames_per_chunk) / fps)

    for i, frame in enumerate(frames):
        # Process every fps-th frame
        if i % fps == 0:
            frame_resized = cv2.resize(frame, (224, 224))
            normalized_frame = frame_resized / 255.0
            predictions = classify_image(normalized_frame)

            if predictions:
                emotions.extend([pred["emotion"] for pred in predictions])
                scores.extend([pred["score"] for pred in predictions])

    emotions_counter = Counter(emotions)
    emotions_list = list(emotions_counter.keys())
    frequencies = list(emotions_counter.values())

    res = {
        "timestep": starting_timestep,
        "emotions": emotions_list,
        "frequencies": frequencies,
    }

    return res

import librosa
import numpy as np

import librosa
import numpy as np


def extract_pitch(audio, sr, min_pitch=75, max_pitch=400):
    pitches, magnitudes = librosa.core.piptrack(y=audio, sr=sr)

    # Basically applying band pass filter
    filtered_pitch = []

    for t in range(pitches.shape[1]):
        valid_pitches = pitches[:, t]
        valid_pitches = valid_pitches[
            (valid_pitches >= min_pitch) & (valid_pitches <= max_pitch)
        ]

        if valid_pitches.size > 0:
            filtered_pitch.append(np.median(valid_pitches))
        else:
            filtered_pitch.append(0)

    return np.array(filtered_pitch)

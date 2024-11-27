import librosa
import numpy as np

def extract_pitch(audio, sr):
    pitches, magnitudes = librosa.core.piptrack(y=audio, sr=sr)
    pitch = [np.max(pitches[:, t]) for t in range(pitches.shape[1])]
    return np.array(pitch)

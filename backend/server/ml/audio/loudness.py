import numpy as np
import librosa

def extract_loudness(audio, ref_rms=1e-5):
    rms = librosa.feature.rms(y=audio)
    loudness_dB = 20 * np.log10(rms[0] / ref_rms)
    return loudness_dB
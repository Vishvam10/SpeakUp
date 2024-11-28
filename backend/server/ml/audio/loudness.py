import librosa

def extract_loudness(audio):
    rms = librosa.feature.rms(y=audio)
    return rms[0]
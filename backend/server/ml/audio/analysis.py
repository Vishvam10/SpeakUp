import numpy as np

from ml.audio.loudness import extract_loudness
from ml.audio.pitch import extract_pitch


# We compute everything required for the scoring function and the feedback
# function here itself since streaming such huge numpy.ndarrays (for pitch and
# modulation) for every chunk is an absolute waste of time and resources


def analyze_modulation_and_pitch(audio, sr):
    pitch = extract_pitch(audio, sr)
    loudness = extract_loudness(audio)

    mean_pitch, mean_loudness = np.mean(pitch), np.mean(loudness)

    pitch_variation = np.std(pitch)
    loudness_variation = np.std(loudness)

    return mean_pitch, mean_loudness, pitch_variation, loudness_variation


def analyze_silence_and_volume(
    audio, sr, noise_duration=1.0, silence_duration=2
):

    noise_profile = audio[: int(sr * noise_duration)]
    background_noise_level = 20 * np.log10(np.std(noise_profile) + 1e-6)

    loudness = extract_loudness(audio)

    silence_threshold = background_noise_level + silence_duration

    # Silence duration
    silent_frames = loudness < silence_threshold
    frame_duration = 1 / sr
    silence_duration = np.sum(silent_frames) * frame_duration

    # Average volume
    average_volume = np.mean(loudness)

    return silence_duration, average_volume, background_noise_level

import os

from collections import Counter

EMOTION_TOP_N_RESULTS = os.environ.get("EMOTION_TOP_N_RESULTS", 3)

def calculate_speaking_score(
    audio_emotions, video_emotions,
    pitch_variation, loudness_variation,
    words_per_minute, silence_durations,
    average_volume,
    ideal_pitch_range=(20, 100),
    ideal_loudness_range=(0.01, 0.3),
    ideal_wpm_range=(120, 160),
    ideal_volume_range=(60, 80)
):
    return 100

    # 1. Emotion Mismatch

    v_set, a_set = set(), set()

    for ae, ve in zip(audio_emotions, video_emotions) :
        pass
        
        
        
    video_set = {emotion[0] for smooth_emotion in smoothed_video_emotions for emotion in smooth_emotion}
    audio_set = {emotion[0] for smooth_emotion in smoothed_audio_emotions for emotion in smooth_emotion}

    matches = video_set & audio_set  # Intersection of emotions
    if matches:
        score += len(matches) * 2  # Reward for each match
        print("mismatch emo", score)
    else:
        score -= 5  # Small penalty for no match

    # Cap the emotion score impact between 95 and 100
    score = max(95, min(100, score))
    print("emotion score impact", score)

    # 2. Modulation (Pitch & Loudness)
    if not (ideal_pitch_range[0] <= pitch_variation <= ideal_pitch_range[1]):
        score -= 10  # Penalize unnatural pitch variation
    if not (ideal_loudness_range[0] <= loudness_variation <= ideal_loudness_range[1]):
        score -= 10  # Penalize unnatural loudness variation

    print("pitch", score)

    # 3. Speaking Speed
    if not (ideal_wpm_range[0] <= words_per_minute <= ideal_wpm_range[1]):
        score -= 10  # Penalize for too fast or too slow speech
    silence_penalty = sum([2 if s > 2 else 0 for s in silence_durations])
    score -= min(10, silence_penalty)  # Limit silence penalty impact
    print("speed", score)

    # 4. Volume
    if not (ideal_volume_range[0] <= average_volume <= ideal_volume_range[1]):
        score -= 10  # Penalize for too high or low volume
    print("volume", score)

    # Ensure the score remains within 0–100
    score = max(0, min(100, score))
    return score

# Example Usage:
smoothed_video_emotions = [[('disgust', 3), ('calm', 2)], [('disgust', 1), ('happy', 1)]]
smoothed_audio_emotions = [[('calm', 3), ('neutral', 2)], [('happy', 2), ('angry', 1)]]

pitch_variation = 50  # Std dev of pitch
loudness_variation = 0.02  # Std dev of loudness
words_per_minute = 150  # Number of words spoken per minute
silence_durations = [0.5, 1.0, 3.0, 0.8]  # Silence durations in seconds
average_volume = 65  # Average volume in dB

score = calculate_speaking_score(
    smoothed_video_emotions, smoothed_audio_emotions,
    pitch_variation, loudness_variation,
    words_per_minute, silence_durations,
    average_volume
)

print(f"Speaking Score: {score}")

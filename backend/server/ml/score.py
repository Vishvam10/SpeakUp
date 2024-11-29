import os

EMOTION_TOP_N_RESULTS = os.environ.get("EMOTION_TOP_N_RESULTS", 3)
def calculate_speaking_score(
    pitch_variation, loudness_variation,
    words_per_minute, silence_durations,
    average_volume,
    ideal_pitch_range=(20, 100),
    ideal_loudness_range=(0.01, 0.3),
    ideal_wpm_range=(120, 160),
    ideal_volume_range=(60, 80)
):
    try:
        # Ensure inputs are floats
        pitch_variation = float(pitch_variation)
        loudness_variation = float(loudness_variation)
        words_per_minute = float(words_per_minute)
        average_volume = float(average_volume)

        # Initialize score
        score = 100
        
        # Modulation (Pitch & Loudness)
        if not (ideal_pitch_range[0] <= pitch_variation <= ideal_pitch_range[1]):
            score -= 10
        if not (ideal_loudness_range[0] <= loudness_variation <= ideal_loudness_range[1]):
            score -= 10

        # Speaking Speed
        if not (ideal_wpm_range[0] <= words_per_minute <= ideal_wpm_range[1]):
            score -= 10  # Penalize for too fast or too slow speech

        silence_penalty = sum([2 if s > 2 else 0 for s in [silence_durations]])
        score -= min(10, silence_penalty)  # Limit silence penalty impact

        # Volume
        if not (ideal_volume_range[0] <= average_volume <= ideal_volume_range[1]):
            score -= 10  # Penalize for too high or low volume

        # Ensure the score remains within 0–100
        score = max(0, min(100, score))
        return score

    except ValueError as e:
        print("Invalid input type:", e)
        raise

    except TypeError as e:
        print("Type mismatch:", e)
        raise

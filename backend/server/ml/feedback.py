import numpy as np


# This will be used while streaming real-time analytics while the
# video is playing
def generate_feedback(
    mean_pitch, mean_loudness, pitch_variation, loudness_variation, emotion
):
    feedback = {}

    # Emotion-specific Modulation Feedback
    if emotion == "happy":
        feedback["modulation"] = (
            "Your speech has great variation in pitch and volume, reflecting positivity and energy. "
            "It engages the listener effectively. Keep maintaining this liveliness!"
        )
    elif emotion == "anger":
        feedback["modulation"] = (
            "Your speech has strong variation in pitch and volume, conveying intensity. "
            "While it effectively emphasizes anger, be cautious of not sounding too harsh or overwhelming."
        )
    elif emotion == "sad":
        feedback["modulation"] = (
            "Your speech is relatively flat, which is typical for a sad tone. "
            "Consider varying your pitch and volume slightly to add more emotional nuance while maintaining the somber feel."
        )
    elif emotion == "neutral":
        feedback["modulation"] = (
            "Your speech is steady and appropriate for neutral delivery. "
            "However, adding more variation in pitch and volume could make your delivery more engaging."
        )
    elif emotion == "surprise":
        feedback["modulation"] = (
            "Your speech shows dynamic variation, well-suited for a tone of surprise. "
            "Try to keep your pitch and volume shifts balanced to maintain clarity."
        )
    elif emotion == "disgust":
        feedback["modulation"] = (
            "Your speech conveys disgust effectively with controlled variation. "
            "Ensure your tone doesn't become too monotonous or overly exaggerated."
        )
    elif emotion == "fear":
        feedback["modulation"] = (
            "Your speech reflects fear with noticeable variation in pitch and volume. "
            "Maintaining a steady tone can help convey controlled anxiety if that's the goal."
        )

    # Pitch Feedback
    if emotion == "happy":
        if mean_pitch < 180:
            feedback["pitch"] = (
                "Your pitch could be slightly higher to match the excitement associated with happiness. "
                "Raising it will add more enthusiasm to your delivery."
            )
        else:
            feedback["pitch"] = (
                "Your pitch is excellent for a happy tone. It conveys energy and positivity. Great job!"
            )
    elif emotion == "anger":
        if mean_pitch < 220:
            feedback["pitch"] = (
                "For anger, your pitch is slightly low. Consider raising it to add intensity and emphasize your message."
            )
        else:
            feedback["pitch"] = (
                "Your pitch effectively conveys anger. Ensure it doesn’t become overly sharp to maintain clarity."
            )
    elif emotion == "sad":
        if mean_pitch > 150:
            feedback["pitch"] = (
                "For a sad tone, your pitch is a bit high. Lowering it slightly can help convey a more somber feel."
            )
        else:
            feedback["pitch"] = (
                "Your pitch aligns well with the sad tone. It's low and steady, which matches the emotion perfectly."
            )
    elif emotion == "neutral":
        feedback["pitch"] = (
            "Your pitch is within a neutral range, which is appropriate. Adding slight variations could make it more engaging."
        )

    # Loudness Feedback

    if mean_loudness < 0.01:
        feedback["loudness"] = (
            "Your volume is too low, making it hard for the audience to hear clearly. "
            "Increase your volume to ensure your message is heard."
        )
    elif mean_loudness > 0.3:
        feedback["loudness"] = (
            "Your volume is quite high, which may come across as overwhelming. "
            "Lowering it slightly will make your delivery more comfortable for listeners."
        )
    else:
        feedback["loudness"] = (
            "Your volume is well-balanced and appropriate for your tone. Keep up the good work!"
        )

    # Modulation (Pitch & Loudness Variation) Feedback
    if pitch_variation < 20:
        feedback["pitch_variation"] = (
            "Your pitch variation is quite low, which could make your speech sound monotonous. "
            "Try adding more variation to keep your audience engaged."
        )
    elif pitch_variation > 100:
        feedback["pitch_variation"] = (
            "Your pitch variation is too high, making your speech sound inconsistent. "
            "Balancing it can make your delivery smoother."
        )
    else:
        feedback["pitch_variation"] = (
            "Your pitch variation is excellent. It adds dynamism to your speech and keeps it interesting."
        )

    if loudness_variation < 0.01:
        feedback["loudness_variation"] = (
            "Your loudness variation is quite low, making your speech sound flat. "
            "Consider modulating your volume to emphasize key points."
        )
    elif loudness_variation > 0.1:
        feedback["loudness_variation"] = (
            "Your loudness variation is high, which adds energy to your speech. "
            "Ensure it remains controlled to maintain clarity."
        )
    else:
        feedback["loudness_variation"] = (
            "Your loudness variation is well-balanced. It keeps the audience attentive without being overwhelming."
        )

    return feedback

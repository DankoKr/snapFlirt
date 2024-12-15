from google.cloud import vision

def analyze_emotions(faces):
    """
    Detect emotions based on face annotations.
    """
    emotion_counts = {
        "joy": 0,
        "sadness": 0,
        "anger": 0,
        "fear": 0,
        "surprise": 0,
        "love": 0,
        "confidence": 0,
        "curiosity": 0,
        "calmness": 0,
    }
    for face in faces:
        if face.joy_likelihood >= vision.Likelihood.POSSIBLE:
            emotion_counts["joy"] += 1
        if face.sorrow_likelihood >= vision.Likelihood.POSSIBLE:
            emotion_counts["sadness"] += 1
        if face.anger_likelihood >= vision.Likelihood.POSSIBLE:
            emotion_counts["anger"] += 1
        if face.surprise_likelihood >= vision.Likelihood.POSSIBLE:
            emotion_counts["surprise"] += 1
        if face.joy_likelihood >= vision.Likelihood.POSSIBLE and face.sorrow_likelihood < vision.Likelihood.POSSIBLE:
            emotion_counts["love"] += 1
        if face.joy_likelihood >= vision.Likelihood.POSSIBLE:
            emotion_counts["confidence"] += 1
        if face.joy_likelihood >= vision.Likelihood.POSSIBLE and face.surprise_likelihood >= vision.Likelihood.POSSIBLE:
            emotion_counts["curiosity"] += 1
        if face.joy_likelihood >= vision.Likelihood.POSSIBLE and face.anger_likelihood < vision.Likelihood.POSSIBLE:
            emotion_counts["calmness"] += 1

    return emotion_counts

from .exercise_classifier import load_classifier, classify_exercise
from .ml_dataset import build_sequence_features
from .repetitions import detect_repetitions


def analyze_movement(sequence, movement_signal=None):
    features = build_sequence_features(sequence)
    model = load_classifier()
    exercise = classify_exercise(model, features)
    result = {"exercise": exercise}

    if movement_signal is not None:
        repetitions = detect_repetitions(movement_signal)
        result["repetitions"] = len(repetitions)
        result["rep_details"] = repetitions

    return result
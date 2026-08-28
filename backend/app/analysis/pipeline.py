from .exercise_classifier import load_classifier, classify_exercise
from .ml_dataset import build_sequence_features
from .repetitions import detect_repetitions
from .temporal import EXERCISE_MOVEMENT_FEATURES
from .features import extract_feature_series

def analyze_movement(sequence, movement_signal=None, movement_analysis=None):
    features = build_sequence_features(sequence)
    model = load_classifier()
    exercise = classify_exercise(model, features)
    result = {"exercise": exercise}
    result["analysis"] = {"sequence_frames": len(sequence), 
                          "movement_features": EXERCISE_MOVEMENT_FEATURES.get(exercise, ())}

    if movement_analysis is not None:
        result["analysis"]["feature_summary"] = {
            feature: {
                "min": min(frame[feature] for frame in movement_analysis),
                "max": max(frame[feature] for frame in movement_analysis),
            }
            for feature in EXERCISE_MOVEMENT_FEATURES.get(exercise, ())
        }

    if movement_signal is not None:
        repetitions = detect_repetitions(movement_signal)
        result["repetitions"] = len(repetitions)
        result["rep_details"] = repetitions

    return result
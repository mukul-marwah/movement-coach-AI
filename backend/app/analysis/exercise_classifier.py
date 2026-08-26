from pathlib import Path
from .ml_model import load_exercise_classifier, predict_exercise

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = PROJECT_ROOT / "models" / "exercise_classifier.joblib"

def load_classifier():
    return load_exercise_classifier(MODEL_PATH)

def classify_exercise(model, features):
    return predict_exercise(model, features)
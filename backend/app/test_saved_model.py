from pathlib import Path
from analysis.ml_model import load_exercise_classifier, predict_exercise
from analysis.ml_dataset import build_sequence_features
from analysis.mmfit import load_mmfit_pose, load_mmfit_labels, select_labeled_sequence

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_PATH = PROJECT_ROOT / "backend" / "models" / "exercise_classifier.joblib"
MMFIT_DIR = PROJECT_ROOT / "data" / "external" / "mm-fit" / "w00"

POSE_PATH = MMFIT_DIR / "w00_pose_3d.npy"
LABEL_PATH = MMFIT_DIR / "w00_labels.csv"

pose_data = load_mmfit_pose(POSE_PATH)
labels = load_mmfit_labels(LABEL_PATH)

sequence, selected_label = select_labeled_sequence(pose_data, labels, exercise="squats", occurrence=0)
features = build_sequence_features(sequence)
model = load_exercise_classifier(MODEL_PATH)
prediction = predict_exercise(model, features)

print("Saved model loaded successfully")
print("Prediction:", prediction)
print("Actual label:", labels[0])
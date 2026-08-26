from analysis.mmfit import load_mmfit_pose, load_mmfit_labels
from analysis.ml_dataset import build_ml_dataset
from analysis.ml_model import train_exercise_classifier, predict_exercise, save_exercise_classifier, load_exercise_classifier
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_DIR = PROJECT_ROOT / "backend" / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PATH = MODEL_DIR / "exercise_classifier.joblib"

MMFIT_DIR = PROJECT_ROOT / "data" / "external" / "mm-fit" / "w00"

POSE_PATH = MMFIT_DIR / "w00_pose_3d.npy"
LABEL_PATH = MMFIT_DIR / "w00_labels.csv"

pose_data = load_mmfit_pose(POSE_PATH)
labels = load_mmfit_labels(LABEL_PATH)

X, y, skipped = build_ml_dataset(pose_data, labels)
print("Skipped sequences:", len(skipped))
print("Total sequences:", len(X))
print("\nExercise distribution:")
distribution = {}
for label in y:
    distribution[label] = distribution.get(label, 0) + 1
for exercise, count in sorted(distribution.items()):
    print(f"{exercise}: {count}")
for label in skipped:
    print("Skipped:", label["exercise"], label["start_frame"], label["end_frame"])
result = train_exercise_classifier(X, y)

save_exercise_classifier(result["model"], MODEL_PATH)
loaded_model = load_exercise_classifier(MODEL_PATH)
prediction = predict_exercise(loaded_model, X[0])

print("Saved model:", MODEL_PATH)
print("Loaded model prediction:", prediction)
print("Actual label:", y[0])

print("ML EXERCISE CLASSIFIER")
print("----------------------")
print("Training sequences:", result["train_size"])
print("Testing sequences:", result["test_size"])
print("Accuracy:", f"{result['accuracy']:.2%}")
print("\nClassification report:")
print(result["report"])

predicted = predict_exercise(result["model"], X[0])
print("\nSample prediction:", predicted)
print("Actual label:", y[0])
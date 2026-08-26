from analysis.mmfit import load_mmfit_pose, load_mmfit_labels
from analysis.ml_dataset import build_ml_dataset
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MMFIT_DIR = PROJECT_ROOT / "data" / "external" / "mm-fit" / "w00"

POSE_PATH = MMFIT_DIR / "w00_pose_3d.npy"
LABEL_PATH = MMFIT_DIR / "w00_labels.csv"

pose_data = load_mmfit_pose(POSE_PATH)
labels = load_mmfit_labels(LABEL_PATH)

X, y = build_ml_dataset(pose_data, labels, sequence_limit=20,)

print("ML DATASET")
print("----------")
print("Sequences:", len(X))
print("Labels:", len(y))

print("\nExercise distribution:")

distribution = {}

for label in y:
    distribution[label] = distribution.get(label, 0) + 1

for exercise, count in sorted(distribution.items()):
    print(f"{exercise}: {count}")

print("First feature count:", len(X[0]))
print("First label:", y[0])
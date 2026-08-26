from pathlib import Path
from analysis.mmfit import load_mmfit_pose, load_mmfit_labels, select_labeled_sequence
from analysis.pipeline import analyze_movement

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MMFIT_DIR = PROJECT_ROOT / "data" / "external" / "mm-fit" / "w00"

POSE_PATH = MMFIT_DIR / "w00_pose_3d.npy"
LABEL_PATH = MMFIT_DIR / "w00_labels.csv"

pose_data = load_mmfit_pose(POSE_PATH)
labels = load_mmfit_labels(LABEL_PATH)

sequence, selected_label = select_labeled_sequence(pose_data, labels, exercise="squats", occurrence=0)
result = analyze_movement(sequence)

print("Movement pipeline result:")
print(result)
print("Expected:", selected_label["exercise"])
from analysis.mmfit import (
    load_mmfit_pose, load_mmfit_labels, select_labeled_sequence, mmfit_3d_to_movement_data
)
from analysis.features import extract_pushup_features
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MMFIT_DIR = PROJECT_ROOT / "data" / "external" / "mm-fit" / "w00"

POSE_PATH = MMFIT_DIR / "w00_pose_3d.npy"
LABEL_PATH = MMFIT_DIR / "w00_labels.csv"

pose_3d = load_mmfit_pose(POSE_PATH)
labels = load_mmfit_labels(LABEL_PATH)

pushup_sequence = select_labeled_sequence(pose_3d, labels, exercise="pushups", occurrence=0)

pushup_data = pushup_sequence[0]
pushup_label = pushup_sequence[1]

movement_data = mmfit_3d_to_movement_data(pushup_data)
features = extract_pushup_features(movement_data)

assert len(movement_data) > 0, "No Pushup movement data generated"
assert len(features) == len(movement_data), ("Feature count does not match movement-data frame count")

expected_features = {
    "left_elbow_angle",
    "right_elbow_angle",
    "left_shoulder_angle",
    "right_shoulder_angle",
    "left_body_alignment",
    "right_body_alignment",
}

assert expected_features.issubset(features[0].keys()), ("Pushup feature set missing expected features")

for frame in features:
    for name in expected_features:
        value = frame[name]
        assert isinstance(value, (int, float)), (f"{name} is not numeric")
        assert value == value, (f"{name} is NaN")

print("Real Pushup feature test: PASS")
print("Exercise:", pushup_label["exercise"])
print("Expected repetitions:", pushup_label["repetitions"])
print("Frames analyzed:", len(features))

for name in expected_features:
    values = [frame[name] for frame in features]
    print(f"{name}: " f"min={min(values):.2f}, " f"max={max(values):.2f}")
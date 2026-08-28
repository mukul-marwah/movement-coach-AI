import json
import urllib.request
from pathlib import Path
from analysis.mmfit import (load_mmfit_pose, load_mmfit_labels,
    select_labeled_sequence, mmfit_3d_to_movement_data, mmfit_squat_features)
from analysis.temporal import build_movement_signal

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MMFIT_DIR = PROJECT_ROOT / "data" / "external" / "mm-fit" / "w00"

POSE_PATH = MMFIT_DIR / "w00_pose_3d.npy"
LABEL_PATH = MMFIT_DIR / "w00_labels.csv"

pose_data = load_mmfit_pose(POSE_PATH)
labels = load_mmfit_labels(LABEL_PATH)

sequence, selected_label = select_labeled_sequence(pose_data, labels, exercise="squats", occurrence=0)
squat_data = sequence
movement_data = mmfit_3d_to_movement_data(squat_data)
features = mmfit_squat_features(movement_data)
movement_signal = build_movement_signal(features)

payload = json.dumps({"sequence": sequence.tolist(), "movement_signal": movement_signal, 
                      "movement_analysis": features}).encode("utf-8")
request = urllib.request.Request("http://127.0.0.1:8000/analyze",
    data=payload,
    headers={"Content-Type": "application/json"},
    method="POST")

with urllib.request.urlopen(request) as response:
    result = json.loads(response.read().decode("utf-8"))

print("API result:", result)
print("Expected:", selected_label["exercise"])
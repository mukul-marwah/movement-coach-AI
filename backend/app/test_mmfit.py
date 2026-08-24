from analysis.mmfit import ( load_mmfit_pose, load_mmfit_labels,
    select_labeled_sequence, mmfit_3d_to_movement_data, mmfit_squat_features)
from analysis.temporal import build_movement_signal
from analysis.repetitions import estimate_cycle_length, detect_repetitions

POSE_PATH = r"C:\Users\admin\OneDrive\Documents\movement-coach-ai\data\external\mm-fit\w00\w00_pose_3d.npy"
LABEL_PATH = r"C:\Users\admin\OneDrive\Documents\movement-coach-ai\data\external\mm-fit\w00/w00_labels.csv"

pose_3d = load_mmfit_pose(POSE_PATH)
labels = load_mmfit_labels(LABEL_PATH)
squat_sequence = select_labeled_sequence(pose_3d, labels, exercise="squats", occurrence=0)

squat_data = squat_sequence[0]

movement_data = mmfit_3d_to_movement_data(squat_data)
features = mmfit_squat_features(movement_data)
movement_signal = build_movement_signal(features)

cycle_length = estimate_cycle_length(movement_signal)
repetitions = detect_repetitions(movement_signal, cycle_length=cycle_length,)

# Results
print("MM-Fit squat repetition analysis")
print("-----------------------------")
print("Expected repetitions:", squat_sequence[1]["repetitions"])
print("Frames:", len(movement_signal),)
print("Estimated cycle length:", cycle_length,)
print("Detected repetitions:", len(repetitions))
print("First signal:", movement_signal[0])
print("Last signal:", movement_signal[-1])

for repetition in repetitions:
    print(
        f"Rep {repetition['rep']}: "
        f"frame={repetition['bottom_frame']} "
        f"time={repetition['bottom_timestamp_ms']}ms "
        f"value={repetition['bottom_value']:.2f}"
    )
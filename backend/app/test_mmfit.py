from analysis.mmfit import ( load_mmfit_pose, load_mmfit_labels,
    select_labeled_sequence, mmfit_3d_to_movement_data, mmfit_squat_features)
from analysis.temporal import build_movement_signal
from analysis.repetitions import estimate_cycle_length, detect_repetitions
from analysis.features import extract_exercise_features
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MMFIT_DIR = PROJECT_ROOT / "data" / "external" / "mm-fit" / "w00"

POSE_PATH = MMFIT_DIR / "w00_pose_3d.npy"
LABEL_PATH = MMFIT_DIR / "w00_labels.csv"

pose_3d = load_mmfit_pose(POSE_PATH)
labels = load_mmfit_labels(LABEL_PATH)
squat_sequence = select_labeled_sequence(pose_3d, labels, exercise="squats", occurrence=0)

squat_data = squat_sequence[0]

movement_data = mmfit_3d_to_movement_data(squat_data)
features = mmfit_squat_features(movement_data)
movement_signal = build_movement_signal(features)

if movement_signal:
    values = [point["value"] for point in movement_signal if point.get("value") is not None]

    if values:
        print(f"  movement_signal: " f"frames={len(movement_signal)}, "
            f"min={min(values):.2f}, " f"max={max(values):.2f}")
    else:
        print("  movement_signal: NO VALID VALUES")
else:
    print("  movement_signal: EMPTY")

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

print()
print("MM-Fit feature analysis — all exercises")
print("----------------------------------------")

MMFIT_EXERCISES = {
    "squats": "squats",
    "bicep_curls": "bicep_curls",
    "dumbbell_rows": "dumbbell_rows",
    "dumbbell_shoulder_press": "dumbbell_shoulder_press",
    "jumping_jacks": "jumping_jacks",
    "lateral_raises": "lateral_shoulder_raises",
    "lunges": "lunges",
    "pushups": "pushups",
    "situps": "situps",
    "tricep_extensions": "tricep_extensions",
}

for exercise_id, mmfit_label in MMFIT_EXERCISES.items():
    sequence = select_labeled_sequence(pose_3d, labels, exercise=mmfit_label, occurrence=0)
    exercise_data = sequence[0]
    movement_data = mmfit_3d_to_movement_data(exercise_data)
    if exercise_id == "squats":
        features = mmfit_squat_features(movement_data)
    else:
        features = extract_exercise_features(exercise_id, movement_data)

    print(f"{exercise_id}: " f"frames={len(movement_data)}, " f"features={len(features)}")

    if features:
        feature_names = [key for key in features[0] if key not in ("frame", "timestamp_ms")]

        for feature_name in feature_names:
            values = [
                frame[feature_name]for frame in features if frame.get(feature_name) is not None
            ]

            if values:
                print(
                    f"  {feature_name}: " f"min={min(values):.2f}, " f"max={max(values):.2f}"
                )
            else:
                print(f"  {feature_name}: " f"NO VALID VALUES")

    movement_signal = build_movement_signal(features, exercise_id=exercise_id)

    cycle_length = estimate_cycle_length(movement_signal)
    repetitions = detect_repetitions(movement_signal, cycle_length = cycle_length)
    print(f"  expected_repetitions={sequence[1]['repetitions']}, "
          f"cycle_length={cycle_length}, " 
          f"detected_repetitions={len(repetitions)}")
'''
    for repetition in repetitions:
        print(
            f"    Rep {repetition['rep']}: "
            f"frame={repetition['bottom_frame']} "
            f"time={repetition['bottom_timestamp_ms']}ms "
            f"value={repetition['bottom_value']:.2f}"
        )

    if movement_signal:
        values = [point["value"] for point in movement_signal if point.get("value") is not None]

        if values:
            print(f"  movement_signal: " f"frames={len(movement_signal)}, "
                  f"min={min(values):.2f}, " f"max={max(values):.2f}")
        else:
            print("  movement_signal: NO VALID VALUES")
    else:
        print("  movement_signal: EMPTY")
'''
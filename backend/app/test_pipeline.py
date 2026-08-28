from pathlib import Path
from analysis.mmfit import (load_mmfit_pose, load_mmfit_labels, select_labeled_sequence, 
                            mmfit_3d_to_movement_data, mmfit_squat_features)
from analysis.pipeline import analyze_movement
from analysis.temporal import build_movement_signal
from llm import generate_movement_coaching

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MMFIT_DIR = PROJECT_ROOT / "data" / "external" / "mm-fit" / "w00"

POSE_PATH = MMFIT_DIR / "w00_pose_3d.npy"
LABEL_PATH = MMFIT_DIR / "w00_labels.csv"

pose_data = load_mmfit_pose(POSE_PATH)
labels = load_mmfit_labels(LABEL_PATH)

sequence, selected_label = select_labeled_sequence(pose_data, labels, exercise="squats", occurrence=0)
movement_data = mmfit_3d_to_movement_data(sequence)
feature_series = mmfit_squat_features(movement_data)
movement_signal = build_movement_signal(feature_series, exercise_id="squats")
print("Sequence type:", type(sequence))
print("Sequence length:", len(sequence))

if len(sequence) > 0:
    print("First sequence item type:", type(sequence[0]))
    print("First sequence item shape:", sequence[0].shape)
    print("First sequence item:", sequence[0])
result = analyze_movement(sequence, movement_signal=movement_signal, movement_analysis=feature_series)

coaching_context = {"exercise": result["exercise"], "repetitions": result["repetitions"],
                    "feature_summary": result["analysis"]["feature_summary"],
                    "rep_details": {"first": result["rep_details"][0], 
                                    "last": result["rep_details"][-1]}}
coaching = generate_movement_coaching(coaching_context)
print("\nLLM Coaching:")
print(coaching)

print("Movement pipeline result:")
print(result)
print("Expected:", selected_label["exercise"])
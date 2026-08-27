from analysis.features import extract_exercise_features

landmarks = []

for _ in range(33):
    landmarks.append({"x": 0.0, "y": 0.0, "z": 0.0, "visibility": 1.0,})

movement_data = [
    {"frame": 0, "timestamp_ms": 0, "image_landmarks": landmarks, "world_landmarks": landmarks,}
]

exercise_ids = ["squat", "bicep_curls", "dumbbell_rows", "dumbbell_shoulder_press",
    "jumping_jacks", "lateral_raises", "lunges", "pushups", "situps", "tricep_extensions"]

for exercise_id in exercise_ids:
    features = extract_exercise_features(exercise_id, movement_data)

    assert len(features) == 1
    assert features[0]["frame"] == 0
    assert features[0]["timestamp_ms"] == 0

    print(f"{exercise_id}: PASS")

print("Feature dispatcher tests: PASS")
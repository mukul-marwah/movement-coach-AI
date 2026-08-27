from analysis.features import extract_lunge_features

landmarks = []
for _ in range(14):
    landmarks.append({"x": 0.0, "y": 0.0, "z": 0.0})

movement_data = [{"frame": 0, "timestamp_ms": 0, "world_landmarks": landmarks}]
features = extract_lunge_features(movement_data)
expected_features = {
    "left_knee_angle",
    "right_knee_angle",
    "left_hip_angle",
    "right_hip_angle",
}

assert len(features) == 1
assert expected_features.issubset(features[0].keys())

print("Lunge feature test: PASS")
print("Features generated:", len(features[0]))

for name in expected_features:
    print(f"{name}: {features[0][name]}")
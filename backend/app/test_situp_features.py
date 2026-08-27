from analysis.features import extract_situp_features

landmarks = []
for _ in range(14):
    landmarks.append({"x": 0.0, "y": 0.0, "z": 0.0})

movement_data = [{"frame": 0, "timestamp_ms": 0, "world_landmarks": landmarks}]
features = extract_situp_features(movement_data)
expected_features = {
    "left_hip_angle",
    "right_hip_angle",
    "left_body_alignment",
    "right_body_alignment",
}

assert len(features) == 1
assert expected_features.issubset(features[0].keys())

print("Situp feature test: PASS")
print("Features generated:", len(features[0]))

for name in expected_features:
    print(f"{name}: {features[0][name]}")
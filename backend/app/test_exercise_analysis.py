from analysis.exercise_analysis import analyze_feature_series
from analysis.exercises import get_exercise_definition

REQUIRED_FEATURES = (
    "left_knee_angle",
    "right_knee_angle",
    "left_hip_angle",
    "right_hip_angle",
)

def main():
    feature_series = [
        {
            "frame": 0,
            "timestamp_ms": 0,
            "left_knee_angle": 100.0,
            "right_knee_angle": 102.0,
            "left_hip_angle": 150.0,
            "right_hip_angle": 152.0,
        },
        {
            "frame": 1,
            "timestamp_ms": 100,
            "left_knee_angle": 80.0,
            "right_knee_angle": 82.0,
            "left_hip_angle": 130.0,
            "right_hip_angle": 132.0,
        },
        {
            "frame": 2,
            "timestamp_ms": 200,
            "left_knee_angle": 60.0,
            "right_knee_angle": 62.0,
            "left_hip_angle": 110.0,
            "right_hip_angle": 112.0,
        },
    ]

    result = analyze_feature_series(feature_series, REQUIRED_FEATURES)

    assert result["frame_count"] == 3
    assert result["duration_ms"] == 200

    left_knee = result["features"]["left_knee_angle"]

    assert left_knee["count"] == 3
    assert left_knee["minimum"] == 60.0
    assert left_knee["maximum"] == 100.0
    assert left_knee["range"] == 40.0

    right_knee = result["features"]["right_knee_angle"]

    assert right_knee["minimum"] == 62.0
    assert right_knee["maximum"] == 102.0
    assert right_knee["range"] == 40.0

    print("Exercise analysis tests: PASS")
    print(f"Frame count: {result['frame_count']}")
    print(f"Duration: {result['duration_ms']} ms")
    print(f"Left knee range: {left_knee['range']} degrees")
    print(f"Right knee range: {right_knee['range']} degrees")

    additional_exercises = ["bicep_curls", "dumbbell_rows", "dumbbell_shoulder_press",
    "jumping_jacks", "lateral_raises", "lunges",
    "pushups", "situps", "tricep_extensions"]

    for exercise_id in additional_exercises:
        definition = get_exercise_definition(exercise_id)

        assert definition is not None
        assert len(definition.required_features) > 0
        assert len(definition.primary_features) > 0

        feature_series = []

        for frame_number in range(3):
            frame = {"frame": frame_number, "timestamp_ms": frame_number * 100}

            for feature_index, feature_name in enumerate(definition.required_features):
                frame[feature_name] = 100.0 + frame_number + feature_index

            feature_series.append(frame)

        result = analyze_feature_series(feature_series, definition.required_features)

        assert result["frame_count"] == 3
        assert result["duration_ms"] == 200

        print(f"{definition.display_name} analysis: PASS")
        print(f"Required features: {len(definition.required_features)}")

if __name__ == "__main__":
    main()
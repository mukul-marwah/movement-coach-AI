from analysis.validation import validate_feature_series, validate_exercise_feature_series
from analysis.exercises import get_exercise_definition

REQUIRED_FEATURES = ("left_knee_angle", "right_knee_angle", "left_hip_angle", "right_hip_angle")


def main():
    valid_series = [
        {
            "frame": 0,
            "timestamp_ms": 0,
            "left_knee_angle": 100.0,
            "right_knee_angle": 101.0,
            "left_hip_angle": 150.0,
            "right_hip_angle": 151.0,
        },
        {
            "frame": 1,
            "timestamp_ms": 33,
            "left_knee_angle": 98.0,
            "right_knee_angle": 99.0,
            "left_hip_angle": 148.0,
            "right_hip_angle": 149.0,
        },
    ]

    result = validate_feature_series(valid_series, REQUIRED_FEATURES)

    assert result["valid"] is True
    assert result["reason"] is None
    assert result["missing_features"] == []

    incomplete_series = [
        {"frame": 0, "timestamp_ms": 0, "left_knee_angle": 100.0, "right_knee_angle": 101.0}
    ]

    result = validate_feature_series(incomplete_series, REQUIRED_FEATURES)

    assert result["valid"] is False
    assert result["reason"] == "missing_required_features"
    assert set(result["missing_features"]) == {
        "left_hip_angle",
        "right_hip_angle",
    }

    result = validate_feature_series([], REQUIRED_FEATURES)

    assert result["valid"] is False
    assert result["reason"] == "empty_feature_series"

    squat = get_exercise_definition("squat")

    result = validate_exercise_feature_series(valid_series, squat)

    assert result["valid"] is True
    assert result["missing_features"] == []

    print("Exercise-level validation: PASS")
    print("Feature validation tests: PASS")
    print("Valid feature series: PASS")
    print("Missing feature detection: PASS")
    print("Empty feature detection: PASS")


if __name__ == "__main__":
    main()
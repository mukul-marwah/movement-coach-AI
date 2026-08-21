from analysis.exercises import EXERCISE_DEFINITIONS, get_exercise_definition

def main():
    squat = get_exercise_definition("squat")

    assert squat is not None
    assert squat.exercise_id == "squat"
    assert squat.display_name == "Squat"

    assert "left_knee_angle" in squat.required_features
    assert "right_knee_angle" in squat.required_features
    assert "left_hip_angle" in squat.required_features
    assert "right_hip_angle" in squat.required_features

    assert squat.primary_features == squat.required_features

    assert get_exercise_definition("not_an_exercise") is None

    assert "squat" in EXERCISE_DEFINITIONS

    print("Exercise definition tests: PASS")
    print(f"Registered exercises: {len(EXERCISE_DEFINITIONS)}")
    print(f"Squat required features: {len(squat.required_features)}")

if __name__ == "__main__":
    main()
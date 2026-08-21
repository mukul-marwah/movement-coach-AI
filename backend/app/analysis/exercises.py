from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class ExerciseDefinition:
    exercise_id: str
    display_name: str
    required_features: Tuple[str, ...]
    primary_features: Tuple[str, ...]

SQUAT = ExerciseDefinition(
    exercise_id="squat",
    display_name="Squat",
    required_features=("left_knee_angle", "right_knee_angle", "left_hip_angle", "right_hip_angle"),
    primary_features=("left_knee_angle", "right_knee_angle", "left_hip_angle", "right_hip_angle")
)

EXERCISE_DEFINITIONS = {SQUAT.exercise_id: SQUAT,}


def get_exercise_definition(exercise_id):
    return EXERCISE_DEFINITIONS.get(exercise_id)
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

BICEP_CURL = ExerciseDefinition(
    exercise_id="bicep_curls",
    display_name="Bicep Curl",
    required_features=("left_elbow_angle", "right_elbow_angle",
        "left_shoulder_angle", "right_shoulder_angle"),
    primary_features=("left_elbow_angle", "right_elbow_angle")
)

DUMBBELL_ROW = ExerciseDefinition(
    exercise_id="dumbbell_rows",
    display_name="Dumbbell Row",
    required_features=("left_elbow_angle", "right_elbow_angle", "left_shoulder_angle",
        "right_shoulder_angle", "left_body_alignment", "right_body_alignment"),
    primary_features=("left_elbow_angle", "right_elbow_angle",
        "left_body_alignment", "right_body_alignment")
)

DUMBBELL_SHOULDER_PRESS = ExerciseDefinition(
    exercise_id="dumbbell_shoulder_press",
    display_name="Dumbbell Shoulder Press",
    required_features=("left_elbow_angle", "right_elbow_angle",
        "left_shoulder_angle", "right_shoulder_angle"),
    primary_features=("left_elbow_angle", "right_elbow_angle",
        "left_shoulder_angle", "right_shoulder_angle")
)

JUMPING_JACK = ExerciseDefinition(
    exercise_id="jumping_jacks",
    display_name="Jumping Jack",
    required_features=("left_shoulder_angle", "right_shoulder_angle",
        "left_hip_angle", "right_hip_angle"),
    primary_features=("left_shoulder_angle", "right_shoulder_angle",
        "left_hip_angle","right_hip_angle")
)

LATERAL_RAISE = ExerciseDefinition(
    exercise_id="lateral_raises",
    display_name="Lateral Raise",
    required_features=("left_shoulder_angle", "right_shoulder_angle",
        "left_elbow_angle", "right_elbow_angle"),
    primary_features=("left_shoulder_angle","right_shoulder_angle")
)

LUNGE = ExerciseDefinition(
    exercise_id="lunges",
    display_name="Lunge",
    required_features=("left_knee_angle", "right_knee_angle",
        "left_hip_angle", "right_hip_angle"),
    primary_features=("left_knee_angle", "right_knee_angle")
)

PUSHUP = ExerciseDefinition(
    exercise_id="pushups",
    display_name="Pushup",
    required_features=("left_elbow_angle", "right_elbow_angle", "left_shoulder_angle",
        "right_shoulder_angle", "left_body_alignment", "right_body_alignment"),
    primary_features=("left_elbow_angle", "right_elbow_angle",
        "left_body_alignment", "right_body_alignment")
)

SITUP = ExerciseDefinition(
    exercise_id="situps",
    display_name="Situp",
    required_features=("left_hip_angle", "right_hip_angle",
        "left_body_alignment", "right_body_alignment"),
    primary_features=("left_hip_angle", "right_hip_angle")
)

TRICEP_EXTENSION = ExerciseDefinition(
    exercise_id="tricep_extensions",
    display_name="Tricep Extension",
    required_features=("left_elbow_angle","right_elbow_angle",
        "left_shoulder_angle", "right_shoulder_angle"),
    primary_features= ("left_elbow_angle", "right_elbow_angle")
)

EXERCISE_DEFINITIONS = {
    SQUAT.exercise_id: SQUAT,
    BICEP_CURL.exercise_id: BICEP_CURL,
    DUMBBELL_ROW.exercise_id: DUMBBELL_ROW,
    DUMBBELL_SHOULDER_PRESS.exercise_id: DUMBBELL_SHOULDER_PRESS,
    JUMPING_JACK.exercise_id: JUMPING_JACK,
    LATERAL_RAISE.exercise_id: LATERAL_RAISE,
    LUNGE.exercise_id: LUNGE,
    PUSHUP.exercise_id: PUSHUP,
    SITUP.exercise_id: SITUP,
    TRICEP_EXTENSION.exercise_id: TRICEP_EXTENSION}

def get_exercise_definition(exercise_id):
    return EXERCISE_DEFINITIONS.get(exercise_id)
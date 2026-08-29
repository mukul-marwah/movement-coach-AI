from ..planner_validation import validate_workout_plan
from ..workout_schema import WorkoutPlanRequest
from .movement_coach import run_movement_coach
from .workout_planner import generate_workout_plan

def run_workout_planner(request: WorkoutPlanRequest):
    plan = generate_workout_plan(request)
    validated_plan = validate_workout_plan(request, plan)
    return validated_plan

def run_movement_analysis(analysis):
    return run_movement_coach(analysis)
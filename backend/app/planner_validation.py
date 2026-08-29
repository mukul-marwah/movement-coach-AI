from .workout_schema import WorkoutPlan, WorkoutPlanRequest

def validate_workout_plan(request: WorkoutPlanRequest,plan: WorkoutPlan) -> WorkoutPlan:

    if len(plan.weekly_schedule) != request.days_per_week:
        raise ValueError(f"Expected {request.days_per_week} workout days, "
                         f"got {len(plan.weekly_schedule)}")

    equipment = {item.strip().lower() for item in request.available_equipment}

    for day in plan.weekly_schedule:
        for exercise in day.exercises:
            if not exercise.name.strip():
                raise ValueError("Exercise name cannot be empty")

            if equipment:
                pass

    return plan
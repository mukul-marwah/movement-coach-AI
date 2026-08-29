from typing import Literal
from pydantic import BaseModel, Field, model_validator

class WorkoutPlanRequest(BaseModel):
    goal: Literal["general_fitness", "strength", "muscle_building", "endurance"]
    experience_level: Literal["beginner", "intermediate", "advanced"]
    days_per_week: int = Field(ge=1, le=7)
    session_duration_minutes: int = Field(ge=10, le=180)
    available_equipment: list[str] = []
    preferences: list[str] = []
    limitations: list[str] = []

class PlannedExercise(BaseModel):
    name: str
    sets: int | None = Field( default=None, ge=1, le=10)
    reps: str | None = None
    duration_seconds: int | None = Field(default=None,  ge=1)
    rest_seconds: int | None = Field(default=None, ge=0, le=600)
    notes: str | None = None

class WorkoutDay(BaseModel):
    day: str
    focus: str
    exercises: list[PlannedExercise]

class WorkoutPlan(BaseModel):
    summary: str
    weekly_schedule: list[WorkoutDay]

    @model_validator(mode="after")
    def validate_schedule(self):
        if not self.weekly_schedule:
            raise ValueError("Workout plan must contain at least one workout day")
        if len(self.weekly_schedule) > 7:
            raise ValueError("Workout plan cannot contain more than 7 workout days")

        for day in self.weekly_schedule:
            if not day.exercises:
                raise ValueError(f"Workout day '{day.day}' must contain at least one exercise")
            for exercise in day.exercises:
                if exercise.sets is None and exercise.duration_seconds is None:
                    raise ValueError(f"Exercise '{exercise.name}' needs sets or duration")
                
        return self
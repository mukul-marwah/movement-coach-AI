import numpy as np
from pydantic import BaseModel
from fastapi import FastAPI
from dotenv import load_dotenv
from app.agents.orchestrator import run_workout_planner
from app.workout_schema import WorkoutPlanRequest

load_dotenv()

app = FastAPI(title="Movement Coach AI")
class AnalyzeRequest(BaseModel):
    sequence: list[list[list[float]]]
    movement_signal: list[dict] | None = None
    movement_analysis: list[dict] | None = None

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    from app.analysis.pipeline import analyze_movement
    from app.agents.movement_coach import run_movement_coach
    sequence = np.array(request.sequence, dtype=float)
    result = analyze_movement(sequence, request.movement_signal, request.movement_analysis)
    coaching_context = {"exercise": result["exercise"], "repetitions": result.get("repetitions"), 
                        "feature_summary": result["analysis"].get("feature_summary", {}), 
                        "rep_details": result.get("rep_details", [])}
    coaching = run_movement_coach(coaching_context)
    result["coaching"] = coaching

    return result

@app.post("/plan")
def generate_plan(request: WorkoutPlanRequest):
    plan = run_workout_planner(request)
    return plan
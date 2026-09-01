from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from pydantic import BaseModel
from fastapi import FastAPI
from dotenv import load_dotenv
from app.agents.orchestrator import run_workout_planner
from app.workout_schema import WorkoutPlanRequest

load_dotenv()

app=FastAPI(title="Movement Coach AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://127.0.0.1:5173", "https://movement-coach-ai.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class AnalyzeRequest(BaseModel):
    exercise:str
    sequence:list[list[list[float]]]
    movement_signal: list[dict] | None = None
    movement_analysis: list[dict] | None = None

@app.get("/health")
def health_check():
    return {"status":"ok"}

@app.post("/analyze")
def analyze(request:AnalyzeRequest):
    from app.analysis.pipeline import analyze_movement
    from app.agents.movement_coach import run_movement_coach

    sequence=np.array(request.sequence,dtype=float)
    result = analyze_movement(sequence, request.exercise, request.movement_signal, request.movement_analysis)

    coaching_context={
        "exercise":result["exercise"],
        "repetitions":result["repetitions"],
        "feature_summary":result["analysis"]["feature_summary"],
        "rep_details":result["rep_details"]
    }

    result["coaching"]=run_movement_coach(coaching_context)
    return result

@app.post("/plan")
def generate_plan(request:WorkoutPlanRequest):
    return run_workout_planner(request)
import numpy as np
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI(title="Movement Coach AI")
class AnalyzeRequest(BaseModel):
    sequence: list[list[list[float]]]
    movement_signal: list[dict] | None = None

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    from app.analysis.pipeline import analyze_movement
    sequence = np.array(request.sequence, dtype=float)
    result = analyze_movement(sequence, request.movement_signal)
    return result
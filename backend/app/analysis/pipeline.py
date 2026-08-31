import numpy as np
from .features import extract_exercise_features,summarize_exercise_features
from .temporal import build_movement_signal,smooth_movement_signal
from .repetitions import detect_repetitions
import time

def _landmark(point):
    return {"x":float(point[0]),"y":float(point[1]),"z":float(point[2]),"visibility":float(point[3]) if len(point)>3 else 1.0}

def _movement_data(sequence):
    return [
        {
            "frame":i,
            "timestamp_ms":i*(1000/30),
            "image_landmarks":[_landmark(point) for point in frame],
            "world_landmarks":[_landmark(point) for point in frame]
        }
        for i,frame in enumerate(sequence)
    ]

def analyze_movement(sequence,exercise,movement_signal=None,movement_analysis=None):
    start=time.perf_counter()
    sequence=np.asarray(sequence,dtype=float)

    if sequence.ndim!=3 or sequence.shape[0]==0 or sequence.shape[1]==0:
        raise ValueError("Invalid pose sequence")

    print(f"sequence received: {len(sequence)} frames")

    movement_data=_movement_data(sequence)
    print(f"movement_data: {time.perf_counter()-start:.2f}s")

    feature_series=extract_exercise_features(exercise,movement_data)
    feature_summary=summarize_exercise_features(feature_series)

    raw_signal=movement_signal or build_movement_signal(feature_series,exercise)
    repetitions=detect_repetitions(raw_signal)

    signal=smooth_movement_signal(raw_signal,window_size=3)

    print(f"temporal: {time.perf_counter()-start:.2f}s")
    print(f"repetitions: {time.perf_counter()-start:.2f}s")
    print(f"detected repetitions: {len(repetitions)}")
    print(f"analysis total: {time.perf_counter()-start:.2f}s")

    return {
        "exercise":exercise,
        "repetitions":len(repetitions),
        "rep_details":repetitions,
        "analysis":{
            "sequence_frames":len(sequence),
            "feature_summary":feature_summary,
            "movement_signal":signal
        }
    }
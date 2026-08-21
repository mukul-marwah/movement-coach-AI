from typing import Any, Dict, List

MOVEMENT_FEATURES = ("left_knee_angle", "right_knee_angle", "left_hip_angle", "right_hip_angle")

def build_movement_signal(
    feature_series: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    if not feature_series:
        return []

    signal = []

    for item in feature_series:
        values = [item[name] for name in MOVEMENT_FEATURES]

        signal.append(
            {
                "frame": item["frame"],
                "timestamp_ms": item["timestamp_ms"],
                "value": sum(values) / len(values),
            }
        )

    return signal

def smooth_movement_signal(
    signal: List[Dict[str, Any]],
    window_size: int = 5,
) -> List[Dict[str, Any]]:
    if not signal:
        return []

    if window_size < 1 or window_size % 2 == 0:
        raise ValueError("window_size must be a positive odd integer")

    if len(signal) < window_size:
        return signal.copy()

    half_window = window_size // 2
    smoothed = []

    for i, item in enumerate(signal):
        start = max(0, i - half_window)
        end = min(len(signal), i + half_window + 1)

        values = [entry["value"] for entry in signal[start:end]]

        smoothed.append(
            {
                "frame": item["frame"],
                "timestamp_ms": item["timestamp_ms"],
                "value": sum(values) / len(values),
            }
        )

    return smoothed

def detect_turning_points(
    signal: List[Dict[str, Any]],
    min_prominence: float = 0.0,
) -> List[Dict[str, Any]]:
    
    if len(signal) < 3:
        return []

    turning_points = []

    for i in range(1, len(signal) - 1):
        previous_value = signal[i - 1]["value"]
        current_value = signal[i]["value"]
        next_value = signal[i + 1]["value"]

        if current_value < previous_value and current_value < next_value:
            prominence = min(
                previous_value - current_value,
                next_value - current_value,
            )
            point_type = "local_minimum"

        elif current_value > previous_value and current_value > next_value:
            prominence = min(
                current_value - previous_value,
                current_value - next_value,
            )
            point_type = "local_maximum"

        else:
            continue

        turning_points.append(
            {
                "frame": signal[i]["frame"],
                "timestamp_ms": signal[i]["timestamp_ms"],
                "value": current_value,
                "type": point_type,
                "prominence": prominence,
            }
        )

    return turning_points
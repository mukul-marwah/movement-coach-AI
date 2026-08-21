from typing import Any, Dict, List

def detect_movement_phases(
    direction_consensus: List[Dict[str, Any]],
    min_phase_frames: int = 3,
) -> List[Dict[str, Any]]:
    if not direction_consensus:
        return []

    phases = []
    current_direction = None
    current_start = None
    current_frames = []

    for item in direction_consensus:
        direction = item["dominant_direction"]

        if direction == current_direction:
            current_frames.append(item)
            continue

        if current_direction is not None:
            if len(current_frames) >= min_phase_frames:
                phases.append(
                    {
                        "phase": current_direction,
                        "start_frame": current_frames[0]["frame"],
                        "end_frame": current_frames[-1]["frame"],
                        "start_timestamp_ms": current_frames[0]["timestamp_ms"],
                        "end_timestamp_ms": current_frames[-1]["timestamp_ms"],
                        "frame_count": len(current_frames),
                    }
                )

        current_direction = direction
        current_start = item["frame"]
        current_frames = [item]

    if current_direction is not None and len(current_frames) >= min_phase_frames:
        phases.append(
            {
                "phase": current_direction,
                "start_frame": current_frames[0]["frame"],
                "end_frame": current_frames[-1]["frame"],
                "start_timestamp_ms": current_frames[0]["timestamp_ms"],
                "end_timestamp_ms": current_frames[-1]["timestamp_ms"],
                "frame_count": len(current_frames),
            }
        )

    return phases
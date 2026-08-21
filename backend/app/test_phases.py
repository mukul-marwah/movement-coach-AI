from analysis.phases import detect_movement_phases

def main():
    direction_series = [
        {"frame": 0, "timestamp_ms": 0, "dominant_direction": "decreasing"},
        {"frame": 1, "timestamp_ms": 33, "dominant_direction": "decreasing"},
        {"frame": 2, "timestamp_ms": 66, "dominant_direction": "decreasing"},
        {"frame": 3, "timestamp_ms": 99, "dominant_direction": "mixed_or_stable"},
        {"frame": 4, "timestamp_ms": 132, "dominant_direction": "mixed_or_stable"},
        {"frame": 5, "timestamp_ms": 165, "dominant_direction": "mixed_or_stable"},
        {"frame": 6, "timestamp_ms": 198, "dominant_direction": "increasing"},
        {"frame": 7, "timestamp_ms": 231, "dominant_direction": "increasing"},
        {"frame": 8, "timestamp_ms": 264, "dominant_direction": "increasing"},
    ]

    phases = detect_movement_phases(direction_series, min_phase_frames=3)

    assert len(phases) == 3

    assert phases[0]["phase"] == "decreasing"
    assert phases[0]["start_frame"] == 0
    assert phases[0]["end_frame"] == 2

    assert phases[1]["phase"] == "mixed_or_stable"
    assert phases[1]["start_frame"] == 3
    assert phases[1]["end_frame"] == 5

    assert phases[2]["phase"] == "increasing"
    assert phases[2]["start_frame"] == 6
    assert phases[2]["end_frame"] == 8

    print("Phase segmentation: PASS")
    print(f"Phases detected: {len(phases)}")

    for phase in phases:
        print(
            f"{phase['phase']}: "
            f"frames {phase['start_frame']}-{phase['end_frame']} "
            f"({phase['frame_count']} frames)"
        )

if __name__ == "__main__":
    main()
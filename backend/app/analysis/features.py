from analysis.geometry import calculate_angle, calculate_distance


def joint_angle(landmarks, first, middle, last):

    return calculate_angle(
        landmarks[first],
        landmarks[middle],
        landmarks[last],
    )


def landmark_distance(landmarks, first, second):

    return calculate_distance(
        landmarks[first],
        landmarks[second],
    )

def extract_knee_angle_series(movement_data, side="left"):
    if side not in ("left", "right"):
        raise ValueError("side must be 'left' or 'right'")

    if side == "left":
        hip_index = 23
        knee_index = 25
        ankle_index = 27
    else:
        hip_index = 24
        knee_index = 26
        ankle_index = 28

    angle_series = []

    for frame_data in movement_data:
        landmarks = frame_data["image_landmarks"]

        angle = joint_angle(landmarks, hip_index, knee_index, ankle_index)

        angle_series.append({
            "frame": frame_data["frame"],
            "timestamp_ms": frame_data["timestamp_ms"],
            "angle": angle,
        })

    return angle_series


def extract_hip_angle_series(movement_data, side="left"):
    if side not in ("left", "right"):
        raise ValueError("side must be 'left' or 'right'")

    if side == "left":
        shoulder_index = 11
        hip_index = 23
        knee_index = 25
    else:
        shoulder_index = 12
        hip_index = 24
        knee_index = 26

    angle_series = []

    for frame_data in movement_data:
        landmarks = frame_data["image_landmarks"]

        angle = joint_angle(landmarks, shoulder_index, hip_index, knee_index)

        angle_series.append({"frame": frame_data["frame"],
            "timestamp_ms": frame_data["timestamp_ms"],
            "angle": angle,
        })

    return angle_series

def extract_feature_series(movement_data):
    left_knee = extract_knee_angle_series(movement_data, side="left")
    right_knee = extract_knee_angle_series(movement_data, side="right")

    left_hip = extract_hip_angle_series(movement_data, side="left")
    right_hip = extract_hip_angle_series(movement_data, side="right")

    feature_series = []

    for i in range(len(movement_data)):
        feature_series.append({
            "frame": movement_data[i]["frame"],
            "timestamp_ms": movement_data[i]["timestamp_ms"],
            "left_knee_angle": left_knee[i]["angle"],
            "right_knee_angle": right_knee[i]["angle"],
            "left_hip_angle": left_hip[i]["angle"],
            "right_hip_angle": right_hip[i]["angle"],
        })

    return feature_series

def calculate_feature_changes(feature_series):
    if not feature_series:
        return []

    changes = []
    first_frame = feature_series[0]
    changes.append({
        "frame": first_frame["frame"],
        "timestamp_ms": first_frame["timestamp_ms"],
        "left_knee_change": 0.0,
        "right_knee_change": 0.0,
        "left_hip_change": 0.0,
        "right_hip_change": 0.0,
    })

    for i in range(1, len(feature_series)):
        previous = feature_series[i - 1]
        current = feature_series[i]

        changes.append({
            "frame": current["frame"],
            "timestamp_ms": current["timestamp_ms"],
            "left_knee_change": (current["left_knee_angle"] - previous["left_knee_angle"]),
            "right_knee_change": (current["right_knee_angle"] - previous["right_knee_angle"]),
            "left_hip_change": (current["left_hip_angle"] - previous["left_hip_angle"]),
            "right_hip_change": (current["right_hip_angle"] - previous["right_hip_angle"])
        })

    return changes

def classify_movement_direction(change, tolerance=0.5):
    if change < -tolerance:
        return "decreasing"
    if change > tolerance:
        return "increasing"

    return "stable"

def add_movement_directions(feature_changes):
    if not feature_changes:
        return []

    results = []

    for change in feature_changes:
        results.append({
            "frame": change["frame"],
            "timestamp_ms": change["timestamp_ms"],
            "left_knee_direction": classify_movement_direction(change["left_knee_change"]),
            "right_knee_direction": classify_movement_direction(change["right_knee_change"]),
            "left_hip_direction": classify_movement_direction(change["left_hip_change"]),
            "right_hip_direction": classify_movement_direction(change["right_hip_change"]),
        })

    return results

def calculate_direction_consensus(direction_data):
    if not direction_data:
        return []
    
    results = []
    direction_keys = [
        "left_knee_direction",
        "right_knee_direction",
        "left_hip_direction",
        "right_hip_direction",
    ]

    for frame in direction_data:
        directions = [frame[key] for key in direction_keys]
        increasing = directions.count("increasing")
        decreasing = directions.count("decreasing")
        stable = directions.count("stable")

        if decreasing > increasing and decreasing > stable:
            dominant = "decreasing"
        elif increasing > decreasing and increasing > stable:
            dominant = "increasing"
        else:
            dominant = "mixed_or_stable"

        results.append({
            "frame": frame["frame"],
            "timestamp_ms": frame["timestamp_ms"],
            "dominant_direction": dominant,
            "increasing_count": increasing,
            "decreasing_count": decreasing,
            "stable_count": stable,
        })

    return results
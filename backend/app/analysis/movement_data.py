def landmark_to_dict(landmark):

    return {
        "x": landmark.x, "y": landmark.y, "z": landmark.z,
        "visibility": getattr(landmark, "visibility", None),
    }


def landmarks_to_dict(landmarks):
    
    if isinstance(landmarks, dict):
        return [landmarks[idx] for idx in sorted(landmarks.keys())]

    return [
        {
            "x": lm.x, "y": lm.y, "z": lm.z,
            "visibility": getattr(lm, "visibility", None)
        } for lm in landmarks
    ]


def create_frame_data(frame_number, timestamp_ms, image_landmarks, world_landmarks):

    return {
        "frame": frame_number,
        "timestamp_ms": timestamp_ms,
        "image_landmarks": landmarks_to_dict(
            image_landmarks
        ),
        "world_landmarks": landmarks_to_dict(
            world_landmarks
        ),
    }


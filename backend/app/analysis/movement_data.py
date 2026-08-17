import cv2

def landmark_to_dict(landmark):

    return {
        "x": landmark.x, "y": landmark.y, "z": landmark.z,
        "visibility": getattr(landmark, "visibility", None),
    }


def landmarks_to_dict(landmarks):

    return [landmark_to_dict(landmark) for landmark in landmarks]


def create_frame_data(frame_number, timestamp_ms, image_landmarks, world_landmarks):

    cap = cv2.VideoCapture('squat.mp4')
    fps = cap.get(cv2.CAP_PROP_FPS)
    timestamp_ms = int(
        frame_number * 1000 / fps
    )

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


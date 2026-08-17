def extract_landmarks(pose_landmarks):

    landmarks = {}

    for index, landmark in enumerate(pose_landmarks.landmark):
        landmarks[index] = {
            "x": landmark.x,
            "y": landmark.y,
            "z": landmark.z,
            "visibility": landmark.visibility,
        }

    return landmarks
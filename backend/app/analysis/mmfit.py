import csv
import numpy as np

MMFIT_JOINTS = {
    "nose": 0,
    "neck": 1,
    "right_shoulder": 2,
    "right_elbow": 3,
    "right_wrist": 4,
    "left_shoulder": 5,
    "left_elbow": 6,
    "left_wrist": 7,
    "right_hip": 8,
    "right_knee": 9,
    "right_ankle": 10,
    "left_hip": 11,
    "left_knee": 12,
    "left_ankle": 13,
    "right_eye": 14,
    "left_eye": 15,
    "right_ear": 16,
    "left_ear": 17,
}

def load_mmfit_pose(pose_path):
    return np.load(pose_path)

def load_mmfit_labels(label_path):
    labels = []

    with open(label_path, newline="") as csv_file:
        reader = csv.reader(csv_file)

        for row in reader:
            labels.append({
                "start_frame": int(row[0]),
                "end_frame": int(row[1]),
                "repetitions": int(row[2]),
                "exercise": row[3],
            })

    return labels

def select_labeled_sequence(pose_data, labels, exercise, occurrence=0):
    matching_labels = [label for label in labels if label["exercise"] == exercise]

    if occurrence >= len(matching_labels):
        raise ValueError(f"No {exercise} sequence at occurrence {occurrence}")

    label = matching_labels[occurrence]
    frame_values = pose_data[0, :, 0]

    mask = (
        (frame_values >= label["start_frame"])
        & (frame_values <= label["end_frame"])
    )

    return pose_data[:, mask, :], label

def mmfit_3d_to_movement_data(pose_data):
    movement_data = []

    frame_values = pose_data[0, :, 0]

    for index, frame in enumerate(frame_values):
        coordinates = pose_data[:, index, :]

        landmarks = []

        for landmark_index in range(coordinates.shape[1]):
            landmarks.append({
                "x": float(coordinates[0, landmark_index]),
                "y": float(coordinates[1, landmark_index]),
                "z": float(coordinates[2, landmark_index]),
                "visibility": 1.0,
            })

        movement_data.append({
            "frame": int(frame),
            "timestamp_ms": int(round((frame - frame_values[0]) / 30.0 * 1000)),
            "image_landmarks": landmarks,
            "world_landmarks": landmarks,
        })

    return movement_data

def mmfit_squat_features(movement_data):
    from analysis.features import joint_angle

    feature_series = []

    for record in movement_data:
        landmarks = record["world_landmarks"]

        feature_series.append({
            "frame": record["frame"],
            "timestamp_ms": record["timestamp_ms"],
            "left_knee_angle": joint_angle(
                landmarks, MMFIT_JOINTS["left_hip"], MMFIT_JOINTS["left_knee"], MMFIT_JOINTS["left_ankle"]
            ),
            "right_knee_angle": joint_angle(
                landmarks, MMFIT_JOINTS["right_hip"], MMFIT_JOINTS["right_knee"], MMFIT_JOINTS["right_ankle"],
            ),
            "left_hip_angle": joint_angle(
                landmarks, MMFIT_JOINTS["left_shoulder"], MMFIT_JOINTS["left_hip"], MMFIT_JOINTS["left_knee"]
            ),
            "right_hip_angle": joint_angle(
                landmarks, MMFIT_JOINTS["right_shoulder"], MMFIT_JOINTS["right_hip"], MMFIT_JOINTS["right_knee"]
            )
        })

    return feature_series
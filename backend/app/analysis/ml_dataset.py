import numpy as np
from .mmfit import select_labeled_sequence

def build_sequence_features(sequence):
    coordinates = sequence[:, :, 1:]

    if coordinates.shape[1] == 0:
        raise ValueError("Sequence contains no frames")

    mean = np.mean(coordinates, axis=1)
    std = np.std(coordinates, axis=1)
    minimum = np.min(coordinates, axis=1)
    maximum = np.max(coordinates, axis=1)

    return np.concatenate([
        mean.flatten(),
        std.flatten(),
        minimum.flatten(),
        maximum.flatten()]).tolist()

def build_ml_dataset(pose_data, labels, sequence_limit=None):
    X = []
    y = []
    skipped = []

    for label in labels:
        if sequence_limit is not None and len(X) >= sequence_limit:
            break

        exercise = label["exercise"]
        matching_labels = [item for item in labels if item["exercise"] == exercise]

        occurrence = matching_labels.index(label)
        sequence, selected_label = select_labeled_sequence(pose_data, labels, exercise, occurrence)

        if sequence.shape[1] == 0:
            skipped.append(label)
            continue

        features = build_sequence_features(sequence)
        X.append(features)
        y.append(selected_label["exercise"])

    return X, y, skipped
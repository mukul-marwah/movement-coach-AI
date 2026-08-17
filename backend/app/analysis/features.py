from analysis.geometry import (calculate_angle, calculate_distance,)


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
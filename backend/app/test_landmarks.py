from types import SimpleNamespace
from vision.landmarks import extract_landmarks


def main():

    pose_landmarks = SimpleNamespace(landmark = [
        SimpleNamespace(x = 0.1, y = 0.2, z = 0.3, visibility = 0.9),
        SimpleNamespace(x = 0.4, y = 0.5, z = 0.6, visibility = 0.8),
    ])

    landmarks = extract_landmarks(pose_landmarks)
    print("Number of landmarks:", len(landmarks))
    print("First landmark:", landmarks[0])


if __name__ == "__main__":
    main()
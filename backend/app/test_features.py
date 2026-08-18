from analysis.features import joint_angle, landmark_distance

def main():

    landmarks = {
        0: {'x': 0, 'y': 0, 'z':0},
        1: {'x': 0, 'y': 1, 'z':0},
        2: {'x': 1, 'y': 1, 'z':0}
    }

    angle = joint_angle(landmarks, 0, 1, 2)
    distance = landmark_distance(landmarks, 0, 1)

    print(f"Joint angle: {angle:.2f} degrees")
    print(f"Landmark distance: {distance:.2f}")

if __name__ == "__main__":
    main()
from analysis.geometry import calculate_angle, calculate_distance

def main():

    point_a = {'x': 0, 'y': 1, 'z': 0}
    point_b = {'x': 0, 'y': 0, 'z': 0}
    point_c = {'x': 1, 'y': 0, 'z': 0}

    angle = calculate_angle(point_a, point_b, point_c)
    print(f"Calculated angle: {angle:.2f} degrees")

    distance = calculate_distance(point_a, point_b)
    print(f"Calculated distance: {distance:.2f}")

if __name__ == "__main__":
    main()
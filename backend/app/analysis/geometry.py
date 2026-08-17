import math

def calculate_angle(point_a, point_b, point_c):
    # To calculate the angle at point_b fomed

    vector_ba = (
        point_a['x'] - point_b['x'],
        point_a['y'] - point_b['y'],
        point_a['z'] - point_b['z'],
    )

    vector_bc = (
            point_c['x'] - point_b['x'],
            point_c['y'] - point_b['y'],
            point_c['z'] - point_b['z'],
        )

    dot_product = sum(a*b for a,b in zip(vector_ba, vector_bc))

    magnitude_ba = math.sqrt(sum(value*value for value in vector_ba))
    magnitude_bc = math.sqrt(sum(value*value for value in vector_bc))

    if magnitude_ba == 0 or magnitude_bc == 0:
        return None

    cosine_angle = (dot_product/ (magnitude_bc * magnitude_ba))

    # To prevent floating-point errors
    cosine_angle = max(-1.0, min(1.0, cosine_angle))

    angle = math.degrees(math.acos(cosine_angle))
    return angle

def calculate_distance(point_a, point_b):
    dx = point_a['x'] - point_b['x']
    dy = point_a['y'] - point_b['y']
    dz = point_a['z'] - point_b['z']

    return math.sprt(
        dx * dx + 
        dy * dy + 
        dz * dz
    )
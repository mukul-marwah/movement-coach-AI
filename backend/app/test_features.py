from vision.pose_detector import process_video
from analysis.features import (joint_angle, landmark_distance, calculate_feature_changes, 
                               classify_movement_direction, extract_knee_angle_series, 
                               extract_hip_angle_series, extract_feature_series, add_movement_directions,
                               calculate_direction_consensus)
from analysis.phases import detect_movement_phases
from analysis.temporal import build_movement_signal, smooth_movement_signal, detect_turning_points
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
video_path = PROJECT_ROOT / "data" / "test_videos" / "squat.mp4"

movement_data = process_video(video_path)

left_knee_series = extract_knee_angle_series(movement_data, side="left")
right_knee_series = extract_knee_angle_series(movement_data, side="right")
left_hip_series = extract_hip_angle_series(movement_data, side="left")
right_hip_series = extract_hip_angle_series(movement_data, side="right")

print("\nLeft knee angle series:")
print(f"Number of values: {len(left_knee_series)}")

if left_knee_series:
    print("First value:", left_knee_series[0])
    print("Last value:", left_knee_series[-1])

print("\nRight knee angle series:")
print(f"Number of values: {len(right_knee_series)}")

if right_knee_series:
    print("First value:", right_knee_series[0])
    print("Last value:", right_knee_series[-1])

print("\nLeft hip angle series:")
print(f"Number of values: {len(left_hip_series)}")

if left_hip_series:
    print("First value:", left_hip_series[0])
    print("Last value:", left_hip_series[-1])


print("\nRight hip angle series:")
print(f"Number of values: {len(right_hip_series)}")

if right_hip_series:
    print("First value:", right_hip_series[0])
    print("Last value:", right_hip_series[-1])

feature_series = extract_feature_series(
    movement_data
)

print("\nUnified feature series:")
print(f"Number of feature frames: " f"{len(feature_series)}")

if feature_series:
    print("\nFirst feature frame:")
    print(feature_series[0])

    print("\nMiddle feature frame:")
    print(feature_series[len(feature_series) // 2])

    print("\nLast feature frame:")
    print(feature_series[-1])

feature_frames = [item["frame"] for item in feature_series]
movement_frames = [item["frame"] for item in movement_data]

print("\nFeature alignment:")
print("Feature frames match movement frames:", feature_frames == movement_frames)

feature_timestamps = [item["timestamp_ms"] for item in feature_series]
movement_timestamps = [item["timestamp_ms"] for item in movement_data]

print("Feature timestamps match movement timestamps:", feature_timestamps == movement_timestamps)

required_features = {"left_knee_angle", "right_knee_angle", "left_hip_angle", "right_hip_angle",}
all_features_present = all(required_features.issubset(frame.keys()) for frame in feature_series)

print("All required features present:", all_features_present)

feature_changes = calculate_feature_changes(feature_series)

print("\nFeature changes:")
print(f"Number of change frames: " f"{len(feature_changes)}")

if feature_changes:
    print("\nFirst change:")
    print(feature_changes[0])

    print("\nSecond change:")
    print(feature_changes[1])

    print("\nLast change:")
    print(feature_changes[-1])

print("Change series length matches feature series:", len(feature_changes) == len(feature_series))

change_frames = [item["frame"] for item in feature_changes]
print("Change frames match feature frames:",change_frames == feature_frames)

print("\nMovement directions:")

for change in feature_changes[:10]:
    direction = classify_movement_direction(change["left_knee_change"])
    print(f"Frame {change['frame']}: " f"{change['left_knee_change']:.2f}° " f"→ {direction}")

movement_directions = add_movement_directions(feature_changes)
print("\nMulti-feature directions:")
for item in movement_directions[:10]:
    print(item)

direction_consensus = calculate_direction_consensus(
    movement_directions
)

movement_signal = build_movement_signal(feature_series)
smoothed_signal = smooth_movement_signal(movement_signal, window_size=5)
turning_points = detect_turning_points(smoothed_signal, min_prominence=0.0)

print("\nMOVEMENT SIGNAL")

for item in smoothed_signal[::5]:
    print(
        f"frame={item['frame']} "
        f"time={item['timestamp_ms']}ms "
        f"signal={item['value']:.2f}"
    )

print("\nTURNING POINTS")

if not turning_points:
    print("No turning points detected.")
else:
    print(f"Turning points detected: {len(turning_points)}")

    for point in turning_points:
        print(
            f"{point['type']}: "
            f"frame={point['frame']} "
            f"time={point['timestamp_ms']}ms "
            f"value={point['value']:.2f}"
        )

print("\nDirection consensus:")

for item in direction_consensus[:10]:
    print(item)

print("\nFEATURE TRAJECTORY")

for item in feature_series[::5]:
    print(
        f"frame={item['frame']} "
        f"time={item['timestamp_ms']}ms "
        f"LK={item['left_knee_angle']:.2f} "
        f"RK={item['right_knee_angle']:.2f} "
        f"LH={item['left_hip_angle']:.2f} "
        f"RH={item['right_hip_angle']:.2f}"
    )




print("\nEdge-case tests:")
print("Empty feature series:", calculate_feature_changes([]))
print("Empty direction series:", add_movement_directions([]))
print("Empty consensus series:",calculate_direction_consensus([]))

try:
    extract_knee_angle_series(movement_data,side="banana")

except ValueError as error:
    print("Invalid side correctly rejected:",error)


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


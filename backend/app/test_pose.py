from vision.pose_detector import process_video
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
video_path = PROJECT_ROOT / "data" / "test_videos" / "squat.mp4"

movement_data = process_video(video_path)

print(f"\nReturned frames: {len(movement_data)}")

if movement_data:
    first_frame = movement_data[0]
    last_frame = movement_data[-1]

    print("\nFirst frame:")
    print(f"  Frame number: {first_frame['frame']}")
    print(f"  Timestamp: {first_frame['timestamp_ms']} ms")
    print(f"  Image landmarks: " f"{len(first_frame['image_landmarks'])}")
    print(f"  World landmarks: " f"{len(first_frame['world_landmarks'])}")

    print("\nLast frame:")
    print(f"  Frame number: {last_frame['frame']}")
    print(f"  Timestamp: {last_frame['timestamp_ms']} ms")
    print(f"  Image landmarks: " f"{len(last_frame['image_landmarks'])}")
    print(f"  World landmarks: " f"{len(last_frame['world_landmarks'])}")

    frame_numbers = [frame["frame"] for frame in movement_data]

    timestamps = [frame["timestamp_ms"] for frame in movement_data]

    print("\nTemporal checks:")

    print(f"First frame number: " f"{frame_numbers[0]}")
    print(f"Last frame number: " f"{frame_numbers[-1]}")

    print(f"First timestamp: " f"{timestamps[0]} ms")
    print(f"Last timestamp: " f"{timestamps[-1]} ms")

    print("Frame numbers strictly increasing:", all(
            frame_numbers[i] < frame_numbers[i + 1] for i in range(len(frame_numbers) - 1)))
    print("Timestamps non-decreasing:", all(
            timestamps[i] <= timestamps[i + 1] for i in range(len(timestamps) - 1)))

    landmark_counts = [len(frame["image_landmarks"]) for frame in movement_data]

    print("All frames have 33 image landmarks:", all(count == 33 for count in landmark_counts))

    world_landmark_counts = [len(frame["world_landmarks"]) for frame in movement_data]

    print("World landmark counts:", sorted(set(world_landmark_counts)))
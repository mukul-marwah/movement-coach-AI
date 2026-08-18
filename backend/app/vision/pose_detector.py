import cv2
import mediapipe as mp

from vision.landmarks import extract_landmarks
from analysis.geometry import calculate_angle
from analysis.movement_data import create_frame_data

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


def process_video(video_path):

    movement_data = []
    frame_number = 0

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError(f"Could not open video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        raise ValueError("Could not determine video FPS")

    # Original video dimensions
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(f"Video resolution: {width} x {height}")

    # Resizable window
    cv2.namedWindow(
        "Movement Coach - Pose Detection",
        cv2.WINDOW_NORMAL
    )

    # Display size to preserve the video's aspect ratio
    display_width = 960
    display_height = int(
        display_width * height / width
    )

    cv2.resizeWindow(
        "Movement Coach - Pose Detection",
        display_width,
        display_height
    )

    knee_angles = []
    
    with mp_pose.Pose(
        static_image_mode=False,

        # Fastest MediaPipe pose model
        model_complexity=0,

        # Disable smoothing for maximum speed
        smooth_landmarks=False,

        enable_segmentation=False,

        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ) as pose:

        while cap.isOpened():

            success, frame = cap.read()

            if not success:
                break

            # OpenCV frame for BGR.
            # MediaPipe for RGB.
            rgb_frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            # Tell MediaPipe not to modify the image.
            rgb_frame.flags.writeable = False

            results = pose.process(rgb_frame)

            rgb_frame.flags.writeable = True

            # Draw the complete pose skeleton.
            if results.pose_landmarks:

                image_landmarks = extract_landmarks(results.pose_landmarks)
                world_landmarks = None
                if results.pose_world_landmarks:
                    world_landmarks = extract_landmarks(results.pose_world_landmarks)

                timestamp_ms = int(frame_number * 1000 / fps)

                if world_landmarks:
                    frame_data = create_frame_data(
                        frame_number,
                        timestamp_ms,
                        image_landmarks,
                        world_landmarks if world_landmarks else [],
                    )
                    movement_data.append(frame_data)

                left_knee_angle = calculate_angle(
                    image_landmarks[23],  # Left hip
                    image_landmarks[25],  # Left knee
                    image_landmarks[27],  # Left ankle
                )
                if left_knee_angle is not None:
                    knee_angles.append(left_knee_angle)

                mp_drawing.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=(
                        mp_drawing_styles
                        .get_default_pose_landmarks_style()
                    ),
                )

            # Display the original frame dimensions/aspect ratio.
            cv2.imshow(
                "Movement Coach - Pose Detection",
                frame
            )
            
            # Q = quit
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

            frame_number += 1

    

    cap.release()
    cv2.destroyAllWindows()

    print(f"Total frames analyzed: {len(knee_angles)}")

    if knee_angles:
        print(
            f"Minimum knee angle: {min(knee_angles):.2f} degrees"
        )

        print(
            f"Maximum knee angle: {max(knee_angles):.2f} degrees"
        )

    print(f"Frames stored: {len(movement_data)}")
    if movement_data:
        print(
            "Landmarks in first frame:",
            len(movement_data[0]["image_landmarks"])
        )
    return movement_data
import cv2
import mediapipe as mp


mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


def process_video(video_path):

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError(f"Could not open video: {video_path}")

    # Get the video's original dimensions
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(f"Video resolution: {width} x {height}")

    # Create a resizable window.
    # The video itself keeps its original aspect ratio.
    cv2.namedWindow(
        "Movement Coach - Pose Detection",
        cv2.WINDOW_NORMAL
    )

    # Start with a reasonable display size while
    # preserving the video's aspect ratio.
    display_width = 960
    display_height = int(
        display_width * height / width
    )

    cv2.resizeWindow(
        "Movement Coach - Pose Detection",
        display_width,
        display_height
    )

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

            # OpenCV frame is BGR.
            # MediaPipe requires RGB.
            rgb_frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            # Tell MediaPipe that it does not need
            # to modify the image.
            rgb_frame.flags.writeable = False

            results = pose.process(rgb_frame)

            rgb_frame.flags.writeable = True

            # Draw the complete pose skeleton.
            if results.pose_landmarks:

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

    cap.release()
    cv2.destroyAllWindows()
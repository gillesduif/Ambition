import mediapipe as mp
import cv2

def start_face_tracking():
    """Starts face tracking using the webcam."""
    mp_face_detection = mp.solutions.face_detection
    mp_drawing = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0)

    with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                break

            # Convert the BGR image to RGB
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Process the image
            results = face_detection.process(image)

            # Draw face detection annotations
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.detections:
                for detection in results.detections:
                    mp_drawing.draw_detection(image, detection)

            # Display the output
            cv2.imshow('Face Tracking', image)

            if cv2.waitKey(5) & 0xFF == 27:
                break

    cap.release()
    cv2.destroyAllWindows()
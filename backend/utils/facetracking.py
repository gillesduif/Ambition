import cv2
import mediapipe as mp
import os
import logging
import time

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def map_landmarks_to_image(face_landmarks, overlay, frame_width, frame_height):
    """
    Maps facial landmarks to manipulate the overlay image.
    Draws points directly on the overlay for the secondary mesh.
    """
    mesh_points = []
    for landmark in face_landmarks.landmark:
        x = int(landmark.x * frame_width)
        y = int(landmark.y * frame_height)
        mesh_points.append((x, y))
        
    # Draw connections between landmarks for a more visible mesh
    connections = mp.solutions.face_mesh.FACEMESH_TESSELATION
    for connection in connections:
        start_idx = connection[0]
        end_idx = connection[1]
        
        if start_idx < len(mesh_points) and end_idx < len(mesh_points):
            cv2.line(overlay, 
                     mesh_points[start_idx],
                     mesh_points[end_idx],
                     (255, 0, 0),  # Blue color for overlay mesh
                     1)

def draw_face_mesh_on_frame(frame, face_landmarks, color, frame_width, frame_height):
    """
    Draws face mesh on the given frame for the primary mesh.
    """
    mesh_points = []
    for landmark in face_landmarks.landmark:
        x = int(landmark.x * frame_width)
        y = int(landmark.y * frame_height)
        mesh_points.append((x, y))
        
    # Draw connections between landmarks
    connections = mp.solutions.face_mesh.FACEMESH_TESSELATION
    for connection in connections:
        start_idx = connection[0]
        end_idx = connection[1]
        
        if start_idx < len(mesh_points) and end_idx < len(mesh_points):
            cv2.line(frame, 
                     mesh_points[start_idx],
                     mesh_points[end_idx],
                     color,  # Green color for webcam mesh
                     1)

def start_dual_face_mesh():
    """
    Implements two separate face meshes:
    1. Real-time webcam feed (green mesh)
    2. Static overlay (blue mesh)
    """
    logger.info("Initializing MediaPipe Face Mesh...")
    mp_face_mesh = mp.solutions.face_mesh
    
    # Load the overlay image
    script_dir = os.path.dirname(os.path.abspath(__file__))
    overlay_path = os.path.join(script_dir, 'overlay.png')
    logger.info(f"Loading overlay image from: {overlay_path}")
    
    overlay = cv2.imread(overlay_path, cv2.IMREAD_COLOR)
    if overlay is None:
        logger.error("Failed to load overlay image. Check the file path and format.")
        return

    # Initialize face mesh with higher confidence thresholds for stability
    with mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    ) as face_mesh:
        logger.info("Face Mesh model loaded successfully.")
        
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            logger.error("Error: Unable to access webcam.")
            return

        # Process overlay image once at startup
        overlay_rgb = cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB)
        overlay_results = face_mesh.process(overlay_rgb)
        static_overlay = None
        
        if overlay_results.multi_face_landmarks:
            static_overlay = overlay.copy()
            for face_landmarks in overlay_results.multi_face_landmarks:
                map_landmarks_to_image(face_landmarks, static_overlay, 
                                    overlay.shape[1], overlay.shape[0])
        
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                logger.warning("No frame captured. Exiting...")
                break

            # Flip the frame for natural mirroring
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process the frame for face landmarks
            results = face_mesh.process(rgb_frame)

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    # Draw green mesh on webcam frame
                    draw_face_mesh_on_frame(frame, face_landmarks, 
                                         (0, 255, 0),  # Green color
                                         frame.shape[1], frame.shape[0])

            # If we have both the static overlay and current frame face detection
            if static_overlay is not None:
                # Resize static overlay to match frame size
                overlay_resized = cv2.resize(static_overlay, 
                                          (frame.shape[1], frame.shape[0]))
                # Blend the frames
                frame = cv2.addWeighted(frame, 0.7, overlay_resized, 0.3, 0)

            # Display the combined frame
            cv2.imshow('Dual Face Mesh (Green: Video, Blue: Overlay)', frame)

            if cv2.waitKey(5) & 0xFF == 27:  # Press 'Esc' to exit
                logger.info("Exiting...")
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    start_dual_face_mesh()
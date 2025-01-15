import cv2
import mediapipe as mp
import os
import logging
import numpy as np

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def create_face_mask(landmarks, image_shape):
    """Create a mask for the face region"""
    mask = np.zeros(image_shape[:2], dtype=np.uint8)
    points = []
    
    # Get face contour points
    FACE_OUTLINE = [10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288,
                   397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136,
                   172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109]
    
    for idx in FACE_OUTLINE:
        point = landmarks.landmark[idx]
        x = int(point.x * image_shape[1])
        y = int(point.y * image_shape[0])
        points.append([x, y])
    
    points = np.array(points, dtype=np.int32)
    cv2.fillPoly(mask, [points], 255)
    
    # Add some padding around the face
    kernel = np.ones((15,15), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=1)
    
    return mask

def get_face_transform(source_landmarks, target_landmarks, image_shape):
    """Calculate transformation matrix between two sets of landmarks"""
    # Select key points for stable tracking
    KEY_POINTS = [33, 133, 362, 263, 61, 291, 78, 308]
    
    source_points = []
    target_points = []
    
    for idx in KEY_POINTS:
        source = source_landmarks.landmark[idx]
        target = target_landmarks.landmark[idx]
        
        source_points.append([
            int(source.x * image_shape[1]),
            int(source.y * image_shape[0])
        ])
        target_points.append([
            int(target.x * image_shape[1]),
            int(target.y * image_shape[0])
        ])
    
    source_points = np.float32(source_points)
    target_points = np.float32(target_points)
    
    return cv2.estimateAffinePartial2D(source_points, target_points)[0]

def start_avatar_system():
    try:
        logger.info("Initializing Avatar System...")
        mp_face_mesh = mp.solutions.face_mesh
        
        # Load the avatar image
        script_dir = os.path.dirname(os.path.abspath(__file__))
        avatar_path = os.path.join(script_dir, 'overlay.png')
        logger.info(f"Loading avatar image from: {avatar_path}")
        
        avatar_original = cv2.imread(avatar_path)
        if avatar_original is None:
            logger.error("Failed to load avatar image")
            return
            
        # Initialize webcam
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            logger.error("Failed to open webcam")
            return
        
        # Get webcam dimensions
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        
        # Resize avatar to match frame height
        aspect_ratio = avatar_original.shape[1] / avatar_original.shape[0]
        avatar_width = int(frame_height * aspect_ratio)
        avatar = cv2.resize(avatar_original, (avatar_width, frame_height))
        
        with mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        ) as face_mesh:
            logger.info("Face Mesh model loaded successfully.")
            
            # Get initial avatar landmarks
            avatar_rgb = cv2.cvtColor(avatar, cv2.COLOR_BGR2RGB)
            avatar_results = face_mesh.process(avatar_rgb)
            
            if not avatar_results.multi_face_landmarks:
                logger.error("No face detected in avatar image")
                return
                
            initial_avatar_landmarks = avatar_results.multi_face_landmarks[0]
            
            # Create initial face mask for avatar
            avatar_face_mask = create_face_mask(initial_avatar_landmarks, avatar.shape)
            
            while cap.isOpened():
                success, frame = cap.read()
                if not success:
                    break
                
                frame = cv2.flip(frame, 1)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = face_mesh.process(rgb_frame)
                
                output_frame = frame.copy()
                avatar_frame = avatar.copy()
                
                if results.multi_face_landmarks:
                    webcam_landmarks = results.multi_face_landmarks[0]
                    
                    # Draw green mesh on webcam frame
                    for landmark in webcam_landmarks.landmark:
                        x = int(landmark.x * frame.shape[1])
                        y = int(landmark.y * frame.shape[0])
                        cv2.circle(output_frame, (x, y), 1, (0, 255, 0), -1)
                    
                    # Calculate transformation matrix
                    M = get_face_transform(
                        webcam_landmarks,
                        initial_avatar_landmarks,
                        avatar.shape
                    )
                    
                    if M is not None:
                        # Transform only the face region
                        face_only = cv2.bitwise_and(avatar, avatar, mask=avatar_face_mask)
                        background = cv2.bitwise_and(avatar, avatar, mask=~avatar_face_mask)
                        
                        # Warp the face region
                        warped_face = cv2.warpAffine(
                            face_only,
                            M,
                            (avatar.shape[1], avatar.shape[0]),
                            borderMode=cv2.BORDER_REPLICATE
                        )
                        
                        # Combine warped face with static background
                        warped_face_mask = cv2.warpAffine(
                            avatar_face_mask,
                            M,
                            (avatar.shape[1], avatar.shape[0]),
                            borderMode=cv2.BORDER_REPLICATE
                        )
                        avatar_frame = cv2.bitwise_and(warped_face, warped_face, mask=warped_face_mask)
                        avatar_frame += background
                        
                        # Draw blue mesh on transformed avatar face
                        for landmark in webcam_landmarks.landmark:
                            x = int(landmark.x * avatar_frame.shape[1])
                            y = int(landmark.y * avatar_frame.shape[0])
                            cv2.circle(avatar_frame, (x, y), 1, (255, 0, 0), -1)
                
                # Create side-by-side view
                debug_view = np.hstack((output_frame, avatar_frame))
                cv2.imshow('Avatar System', debug_view)
                
                if cv2.waitKey(5) & 0xFF == 27:
                    break
                
        cap.release()
        cv2.destroyAllWindows()
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)

if __name__ == "__main__":
    start_avatar_system()
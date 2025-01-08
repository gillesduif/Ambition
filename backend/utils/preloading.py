import logging
from rembg import remove
from PIL import Image
import io

def preload_rembg_model():
    """Preloads the Rembg model by processing a dummy image."""
    try:
        logging.info("Preloading Rembg model...")
        dummy_image = Image.new("RGBA", (1, 1), (255, 255, 255, 0))
        dummy_bytes = io.BytesIO()
        dummy_image.save(dummy_bytes, format="PNG")
        dummy_bytes.seek(0)
        remove(dummy_bytes.getvalue())
        logging.info("Rembg model preloaded successfully.")
    except Exception as e:
        logging.error(f"Failed to preload Rembg model: {e}")

def preload_face_tracking_model():
    """Placeholder for face tracking model preloading."""
    try:
        logging.info("Preloading Face Tracking model...")
        # Add your face tracking preloading logic here
        logging.info("Face Tracking model preloaded successfully.")
    except Exception as e:
        logging.error(f"Failed to preload Face Tracking model: {e}")

def preload_models(rembg=False, face_tracking=False):
    """Preloads specified AI models."""
    if rembg:
        preload_rembg_model()
    if face_tracking:
        preload_face_tracking_model()
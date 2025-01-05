import os

class Config:
    UPLOAD_FOLDER = os.path.join(os.getcwd(), "data/uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Limiet van 16MB
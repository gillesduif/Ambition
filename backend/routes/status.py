from flask import Blueprint, jsonify
import glob
from config import Config

status_bp = Blueprint("status", __name__)

def get_uploaded_files_count():
    return len(glob.glob(f"{Config.UPLOAD_FOLDER}/*"))

@status_bp.route("/", methods=["GET"])
def status():
    return jsonify({
        "system": "Online",
        "uploaded_files": get_uploaded_files_count(),
        "version": "1.0.0"
    }), 200
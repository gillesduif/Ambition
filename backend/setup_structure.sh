#!/bin/bash

# Maak mappen aan
mkdir -p routes utils data/uploads

# Hoofdapplicatiebestand
cat <<EOF > app.py
from flask import Flask
from flask_cors import CORS
import logging
from config import Config

# Configuratie en initialisatie
app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

# Logging instellen
logging.basicConfig(level=logging.INFO)

# Importeren van routes
from routes.home import home_bp
from routes.upload import upload_bp
from routes.status import status_bp
from routes.health import health_bp

# Blueprints registreren
app.register_blueprint(home_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(status_bp)
app.register_blueprint(health_bp)

if __name__ == "__main__":
    app.run(debug=True)
EOF

# Configuratiebestand
cat <<EOF > config.py
import os

class Config:
    UPLOAD_FOLDER = "data/uploads"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Limiet van 16MB
EOF

# Routes
cat <<EOF > routes/__init__.py
# Dit bestand laat Python de map routes herkennen als module
EOF

cat <<EOF > routes/home.py
from flask import Blueprint

home_bp = Blueprint("home", __name__)

@home_bp.route("/", methods=["GET"])
def home():
    return "Welcome to the Holonoid Backend API!"
EOF

cat <<EOF > routes/upload.py
from flask import Blueprint, request, jsonify
import os
from config import Config

upload_bp = Blueprint("upload", __name__)

@upload_bp.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400
    
    try:
        file_path = os.path.join(Config.UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        return jsonify({"message": f"File '{file.filename}' uploaded successfully!"}), 200
    except Exception as e:
        return jsonify({"error": "Failed to save the file"}), 500
EOF

cat <<EOF > routes/status.py
from flask import Blueprint, jsonify

status_bp = Blueprint("status", __name__)

@status_bp.route("/status", methods=["GET"])
def status():
    system_status = {
        "system": "Online",
        "frontend_connected": True,
        "file_status": "Idle",
    }
    return jsonify(system_status), 200
EOF

cat <<EOF > routes/health.py
from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)

@health_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "Healthy"}), 200
EOF

# Utils
cat <<EOF > utils/__init__.py
# Dit bestand laat Python de map utils herkennen als module
EOF

cat <<EOF > utils/file_helpers.py
# Helperfuncties voor bestandshandelingen
def allowed_file(filename, allowed_extensions):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions
EOF

cat <<EOF > utils/logging.py
import logging

def setup_logging():
    logging.basicConfig(level=logging.INFO)
EOF

# README
cat <<EOF > ../README.md
# Holonoid Backend
Een Flask-gebaseerde backend voor Holonoid. Ondersteunt uploaden, statuscontrole en meer.

## Structuur
- \`app.py\`: Hoofdapplicatie.
- \`routes\`: Bevat de verschillende API-routes.
- \`utils\`: Helperfuncties en logging.

## Starten
1. Zorg dat Python en Flask geïnstalleerd zijn.
2. Run de applicatie: \`python app.py\`.
EOF

echo "Structuur gegenereerd. Veel succes met je project!"

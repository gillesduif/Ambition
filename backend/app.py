import os
import logging
from flask import Flask, request, jsonify

# Configuratie en initialisatie
app = Flask(__name__)

# Logging instellen
logging.basicConfig(level=logging.INFO)

# Upload map configureren
UPLOAD_FOLDER = "data/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Home route
@app.route("/", methods=["GET"])
def home():
    return "Welcome to the Holonoid Backend API!"

# Upload route
@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        logging.error("No file provided in the request")
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        logging.error("No file selected for upload")
        return jsonify({"error": "No file selected"}), 400
    
    try:
        # Bestand opslaan
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)
        logging.info(f"File '{file.filename}' uploaded successfully")
        return jsonify({"message": f"File '{file.filename}' uploaded successfully!"}), 200
    except Exception as e:
        logging.error(f"Error while saving file: {str(e)}")
        return jsonify({"error": "Failed to save the file"}), 500

# Health check route
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "Healthy"}), 200

# Error handling (voorbeeld)
@app.errorhandler(404)
def not_found(error):
    logging.warning("404 error occurred")
    return jsonify({"error": "Endpoint not found"}), 404

# Start de applicatie
if __name__ == "__main__":
    app.run(debug=True)
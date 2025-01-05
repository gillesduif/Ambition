from flask import Blueprint, request, jsonify
import os
import logging
from werkzeug.utils import secure_filename
from rembg import remove
from PIL import Image
import io

upload_bp = Blueprint("upload", __name__)

UPLOAD_FOLDER = "data/uploads"  # Zorg ervoor dat deze map bestaat
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@upload_bp.route("", methods=["POST"])
def upload():
    logging.info("Received upload request...")
    
    # Controleer of een bestand is meegegeven
    if "file" not in request.files:
        logging.error("No file provided in the request.")
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
        logging.error("No file selected for upload.")
        return jsonify({"error": "No file selected"}), 400

    # Veilige bestandsnaam genereren
    filename = secure_filename(file.filename)
    original_path = os.path.join(UPLOAD_FOLDER, filename)
    processed_filename = f"processed_{filename.split('.')[0]}.png"
    processed_path = os.path.join(UPLOAD_FOLDER, processed_filename)

    try:
        # Bestand opslaan
        logging.info(f"Saving original file to: {original_path}")
        file.save(original_path)

        # Achtergrond verwijderen met rembg
        with open(original_path, "rb") as f:
            img_data = f.read()
            logging.info(f"Loaded image data: {len(img_data)} bytes")
            logging.info("Starting background removal...")
            output_data = remove(img_data)
            logging.info("Background removal completed.")

        # Verwerkte afbeelding opslaan
        with Image.open(io.BytesIO(output_data)) as img:
            img.save(processed_path, "PNG")
            logging.info(f"Processed image saved successfully to: {processed_path}")

        # Response retourneren
        return jsonify({
            "message": f"File '{filename}' uploaded and processed successfully!",
            "original_file": original_path,
            "processed_file": processed_path
        }), 200

    except Exception as e:
        logging.error(f"Error processing file: {e}")
        return jsonify({"error": f"Failed to process the image: {str(e)}"}), 500
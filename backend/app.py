from flask import Flask
from flask_cors import CORS
import logging
from config import Config
from rembg import remove
from PIL import Image
import io

# Configuratie en initialisatie
app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

# Logging instellen
logging.basicConfig(level=logging.INFO)

# Preloading van het rembg-model met een dummy-afbeelding
def preload_rembg_model():
    try:
        logging.info("Preloading rembg model...")
        # Maak een lege (1x1 pixel) transparante afbeelding
        dummy_image = Image.new("RGBA", (1, 1), (255, 255, 255, 0))
        dummy_bytes = io.BytesIO()
        dummy_image.save(dummy_bytes, format="PNG")
        dummy_bytes.seek(0)
        # Verwerk de dummy-afbeelding om het model te preloaden
        remove(dummy_bytes.getvalue())
        logging.info("rembg model preloaded successfully.")
    except Exception as e:
        logging.error(f"Failed to preload rembg model: {e}")

# Preload het model bij het starten van de app
preload_rembg_model()

# Importeren van routes
from routes.home import home_bp
from routes.upload import upload_bp  # Upload route inclusief achtergrondverwijdering
from routes.status import status_bp
from routes.health import health_bp

# Blueprints registreren
app.register_blueprint(home_bp, url_prefix="/")
app.register_blueprint(upload_bp, url_prefix="/upload")
app.register_blueprint(status_bp, url_prefix="/status")
app.register_blueprint(health_bp, url_prefix="/health")

if __name__ == "__main__":
    app.run(debug=True)
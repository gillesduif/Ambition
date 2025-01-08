from flask import Flask
from flask_cors import CORS
import logging
from config import Config
from utils.preloading import preload_models

# Configuratie en initialisatie
app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

# Logging instellen
logging.basicConfig(level=logging.INFO)

# Preload models (e.g., rembg, face tracking)
preload_models(rembg=True, face_tracking=True)

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
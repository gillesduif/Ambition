from flask import Blueprint, jsonify

home_bp = Blueprint("home", __name__)

@home_bp.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Welcome to the Holonoid Backend API!",
        "status": "Running smoothly",
        "version": "1.0.0"
    }), 200
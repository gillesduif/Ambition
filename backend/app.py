from flask import Flask, request, jsonify

app = Flask(__name__)

# Home route
@app.route("/", methods=["GET"])
def home():
    return "Welcome to the Holonoid Backend API!"

# Upload route
@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400
    
    # Save the file locally (you can adjust this later)
    file.save(f"data/{file.filename}")
    
    return jsonify({"message": f"File '{file.filename}' uploaded successfully!"}), 200

# Health check route
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "Healthy"}), 200

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, send_file
import requests
import os
import uuid

app = Flask(__name__)
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

MODEL_API_URL = ""  # Replace with real Render URL

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    audio = request.files.get("audio")
    model = request.files.get("model")

    if not audio or not model:
        return "Missing file", 400

    files = {
        "audio": (audio.filename, audio.stream, audio.mimetype),
        "model": (model.filename, model.stream, model.mimetype)
    }

    # Send to model API
    response = requests.post(MODEL_API_URL, files=files)

    if response.status_code != 200:
        return f"Error from model API: {response.text}", 500

    # Save returned file locally for download
    output_filename = f"output_{uuid.uuid4().hex}.wav"
    output_path = os.path.join(UPLOAD_DIR, output_filename)

    with open(output_path, "wb") as f:
        f.write(response.content)

    return send_file(output_path, as_attachment=True, download_name="cloned_audio.wav")

if __name__ == "__main__":
    app.run(debug=True)

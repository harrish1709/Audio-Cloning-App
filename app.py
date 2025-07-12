from flask import Flask, render_template, request, send_file
import requests, os, uuid

app = Flask(__name__)
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

MODEL_API_URL = "https://rvc-8lxe.onrender.com"  # Replace with your deployed API URL

@app.route("/")
def index():
    # This should match the keys in model_api.py -> MODEL_SOURCES
    available_models = ["speaker1", "speaker2","speaker3","speaker4","speaker5"]
    return render_template("index.html", models=available_models)

@app.route("/process", methods=["POST"])
def process():
    audio = request.files.get("audio")
    model_name = request.form.get("model_name")

    if not audio or not model_name:
        return "Missing audio or model_name", 400

    files = {"audio": (audio.filename, audio.stream, audio.mimetype)}
    data = {"model_name": model_name}

    try:
        response = requests.post(MODEL_API_URL, files=files, data=data, timeout=600)
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}", 500

    if response.status_code != 200:
        return f"Model API Error: {response.text}", 500

    output_filename = f"output_{uuid.uuid4().hex}.wav"
    output_path = os.path.join(UPLOAD_DIR, output_filename)

    with open(output_path, "wb") as f:
        f.write(response.content)

    return send_file(output_path, as_attachment=True, download_name="cloned_audio.wav")

if __name__ == "__main__":
    app.run(debug=True)

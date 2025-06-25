from flask import Flask, render_template, request, send_file
import os
import uuid
import torch
from fairseq.data.dictionary import Dictionary
from rvc_python.infer import RVCInference
from types import MethodType
from scipy.io import wavfile

# Allow fairseq dictionary during safe deserialization
torch.serialization.add_safe_globals([Dictionary])

app = Flask(__name__)

# Define directory paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "cloned_audio_files")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Patch RVC inference to handle output writing
def patched_infer_file(self, input_path, output_path):
    if not self.current_model:
        raise ValueError("Model not loaded.")
    model_info = self.models[self.current_model]
    file_index = model_info.get("index", "")

    result = self.vc.vc_single(
        sid=0,
        input_audio_path=input_path,
        f0_up_key=self.f0up_key,
        f0_method=self.f0method,
        file_index=file_index,
        index_rate=self.index_rate,
        filter_radius=self.filter_radius,
        resample_sr=self.resample_sr,
        rms_mix_rate=self.rms_mix_rate,
        protect=self.protect,
        f0_file="",
        file_index2=""
    )

    wav = result[0] if isinstance(result, tuple) else result
    wavfile.write(output_path, self.vc.tgt_sr, wav)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    audio = request.files.get("audio")
    model = request.files.get("model")

    if not audio or not model:
        return "Missing audio or model file", 400

    # Generate unique filenames
    input_name = f"input_{uuid.uuid4().hex}.wav"
    model_name = f"model_{uuid.uuid4().hex}.pth"
    output_name = f"cloned_{uuid.uuid4().hex}.wav"

    input_path = os.path.join(UPLOAD_DIR, input_name)
    model_path = os.path.join(UPLOAD_DIR, model_name)
    output_path = os.path.join(UPLOAD_DIR, output_name)

    # Save uploaded files
    audio.save(input_path)
    model.save(model_path)

    # Load and run inference
    rvc = RVCInference(model_path=model_path)
    rvc.infer_file = MethodType(patched_infer_file, rvc)
    rvc.set_params(f0up_key=0, index_rate=0.75)
    rvc.infer_file(input_path=input_path, output_path=output_path)

    return render_template("result.html", filename=output_name)

@app.route("/download/<filename>")
def download_file(filename):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        return "File not found.", 404
    return send_file(
        file_path,
        as_attachment=True,
        download_name="cloned_voice.wav",
        mimetype="audio/wav"
    )

if __name__ == "__main__":
    app.run(debug=True)
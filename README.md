# 🗣️ Flask Voice Cloning App (RVC Inference)

This is a web application that allows users to upload an audio clip and voice models (RVC `.pth` file), and then perform voice cloning using [RVC (Retrieval-based Voice Conversion)](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI). It uses Flask for the backend and a patched version of the RVC Python interface for inference.

---

## 🎯 Features

- Upload audio and pretrained RVC voice models.
- Clones the voice in the uploaded audio using the selected models.
- Downloads the cloned audio in `.wav` format.
- Easy-to-use web interface.

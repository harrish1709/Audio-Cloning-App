# 🗣️ Flask Voice Cloning App (RVC Inference)

This is a web application that allows users to upload an audio clip and a voice model (RVC `.pth` file), and then perform voice cloning using [RVC (Retrieval-based Voice Conversion)](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI). It uses Flask for the backend and a patched version of the RVC Python interface for inference.

---

## 🎯 Features

- Upload audio and pretrained RVC voice model.
- Clones the voice in the uploaded audio using the selected model.
- Downloads the cloned audio in `.wav` format.
- Easy-to-use web interface.

FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    python3.10 python3.10-venv python3.10-dev python3-pip \
    build-essential git ffmpeg libsndfile1 \
    && apt-get clean

RUN ln -sf /usr/bin/python3.10 /usr/bin/python

# Downgrade pip to allow legacy packages like omegaconf==2.0.5
RUN pip install --upgrade pip==23.3.1

WORKDIR /app
COPY . /app

# Install CUDA-compatible torch manually first
RUN pip install torch==2.2.2+cu121 --index-url https://download.pytorch.org/whl/cu121

# Install remaining Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
# Make sure Python can find local modules
ENV PYTHONPATH=/app
CMD ["python", "app.py"]

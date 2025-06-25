# Use a CUDA base image with Python 3.10
FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install OS dependencies
RUN apt-get update && apt-get install -y \
    python3.10 python3.10-venv python3.10-dev python3-pip \
    build-essential git ffmpeg libsndfile1 \
    && apt-get clean

# Make python3.10 the default
RUN ln -sf /usr/bin/python3.10 /usr/bin/python

# Upgrade pip and install Python deps
RUN pip install --upgrade pip

# Copy project files
WORKDIR /app
COPY . /app

# Install Python dependencies
RUN pip install torch==2.2.2+cu121 --index-url https://download.pytorch.org/whl/cu121
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]

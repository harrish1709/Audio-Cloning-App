FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    ffmpeg \
    libsndfile1 \
    git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy source code
COPY . /app

# Downgrade pip to support omegaconf 2.0.6
RUN pip install --upgrade pip==23.3.1

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Ensure local modules like rvc_python/ are found
ENV PYTHONPATH=/app

EXPOSE 5000
CMD ["python", "app.py"]

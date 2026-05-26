FROM python:3.11-slim

WORKDIR /app

# System dependencies สำหรับ EasyOCR + OpenCV
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir \
    torch==2.3.1+cpu \
    torchvision==0.18.1+cpu \
    --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY model ./model

EXPOSE 7860

CMD ["uvicorn", "src.API.server:app", "--host", "0.0.0.0", "--port", "7860"]
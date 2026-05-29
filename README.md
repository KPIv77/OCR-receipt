
# OCR-receipt


OCR-receipt for extracting, classifying, and managing information from Thai bank receipts using Optical Character Recognition (OCR) and deep learning. It features a Python backend for OCR and classification, and a React/TypeScript frontend for user interaction.

## **[🌐 Demo Website](https://ocr-receipt-ecru.vercel.app/)**

---

## Tech Stack
- **Frontend:** React, TypeScript, Vite
- **Backend:** Python, FastAPI
- **Deep Learning:** PyTorch, torchvision
- **OCR:** EasyOCR
- **Database:** PostgreSQL
- **Other:** Docker, REST API

---

## Features
- Upload receipt images and extract information (bank, amount, etc.)
- Classify receipts by bank using a trained PyTorch model
- OCR for Thai/English text using EasyOCR
- Store and manage receipt data in a PostgreSQL database
- Modern web UI with React

---

## Project Structure
```
OCR-receipt/
│
├── README.md                # Project documentation
├── Dockerfile               # Containerization for backend
├── requirements.txt         # Python dependencies
├── server_2.py              # FastAPI backend server
├── App/                     # Frontend (React/TypeScript)
│   ├── src/
│   │   ├── App.tsx
│   │   ├── api/receiptApi.ts
│   │   └── ...
│   └── ...
├── model/                   # Pretrained models for OCR/classification
│   ├── craft_mlt_25k.pth
│   ├── thai.pth
│   └── receipt_model.pth
├── src/                     # Backend source code
│   ├── main.py              # Entry point for OCR/classification
│   ├── classify_receipt.py  # Receipt bank classifier
│   ├── receipt_read.py      # OCR and info extraction
│   └── API/                 # FastAPI endpoints
│       ├── DB.py            # Database connection
│       └── server.py        # API routes
├── postgreSQL/              # Docker Compose for PostgreSQL
│   └── docker-compose.yml
└── receipt/                 # Example/test receipt images
```

---

## Backend Overview
- **main.py:** Loads models, provides `run_ocr()` for image classification and OCR.
- **classify_receipt.py:** Loads a PyTorch model to classify the bank from a receipt image.
- **receipt_read.py:** Uses EasyOCR to extract text and parse amount/bank info.
- **API/server:** FastAPI endpoints for uploading images, adding/listing receipts, and integrating with the database.

## Frontend Overview
- Located in `App/` (React + TypeScript)
- Allows users to upload receipt images, view extracted data, and interact with the backend API.

---

## Example API Endpoints
- `POST /ocr` — Upload receipt image, returns extracted info
- `POST /add` — Add receipt data to database
- `GET /list` — List all receipts

---

## Requirements
See `requirements.txt` for Python dependencies, including:
- fastapi, uvicorn, torch, torchvision, easyocr, opencv-python-headless, numpy, pillow, python-multipart, gdown, python-dotenv, psycopg2-binary, requests

---






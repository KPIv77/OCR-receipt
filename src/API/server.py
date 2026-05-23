from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

import sys, os, shutil

sys.path.append(
    os.path.join(os.path.dirname(__file__), "..")
)

from main import run_ocr

app = FastAPI()

# allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ocr")
def ocr_upload(file: UploadFile = File(...)):

    temp_path = f"/tmp/{file.filename}"

    with open(temp_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    text = run_ocr(img_path=temp_path)

    os.remove(temp_path)

    return {
        "result": text
    }
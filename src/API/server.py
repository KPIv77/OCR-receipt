from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

import sys, os, shutil
sys.path.append(
    os.path.join(os.path.dirname(__file__), "..")
)


from main import run_ocr

app = FastAPI()

# serve static files
app.mount(
    "/static",
    StaticFiles(directory="../app"),
    name="static"
)

# serve index.html at root
# เปิดหน้าเว็บ
@app.get("/")
def home():
    return FileResponse("../app/index.html")

@app.post("/ocr")
def ocr_upload(file: UploadFile = File(...)):
    # Save uploaded file to a temporary location
    temp_path = f"/tmp/{file.filename}"
    with open(temp_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    # Process the file with run_ocr() and get the text result
    text = run_ocr(img_path=temp_path)
    
    # Delete the temporary file after processing
    os.remove(temp_path)
    
    return {"result": text}

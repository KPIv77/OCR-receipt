from fastapi import FastAPI, UploadFile, File
from API.DB import get_connection
from pydantic import BaseModel
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
    allow_origins=[
        "http://localhost:5173",
        "https://ocr-receipt-ecru.vercel.app/"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Receipt(BaseModel):
    date: str
    bank: str
    detail: str
    income: int
    expenses: int



@app.get("/list")
def get_users():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT date, bank, detail, expenses
        FROM "db-main"
    """)

    rows = cursor.fetchall()

    lst = []

    for row in rows:
        lst.append({
            "date": row[0],
            "bank": row[1],
            "detail": row[2],
            "expenses": row[3]
        })

    cursor.close()
    conn.close()

    return lst

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

@app.post("/receipt")
async def create_receipt(data: Receipt):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO "db-main"
        (date, bank, detail,income, expenses)

        VALUES (%s, %s, %s, %s, %s)
    """, 
    (
        data.date,
        data.bank,
        data.detail,
        data.income,
        data.expenses
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "message": "success"
    }
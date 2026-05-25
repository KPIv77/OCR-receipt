import torch
import os

import download_model

from classify_receipt import ReceiptClassifier
from receipt_read import ReceiptRead


# Config
IMG_SIZE = 224
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
CLASS_NAMES = ["Kbank", "NEXT", "SCB"]

# Path model and image
#model_receipt = r"/home/kph/project/OCR-receipt/model/receipt_model.pth"
#image_path = r"/home/kph/project/OCR-receipt/receipt/218326_0.jpg"
#model_dir = r"/home/kph/project/OCR-receipt/model"

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

model_receipt = os.path.join(
    BASE_DIR,
    "model",
    "receipt_model.pth"
)

model_dir = os.path.join(
    BASE_DIR,
    "model"
)
CLASSIFIER = ReceiptClassifier(
    model_path=model_receipt,
    class_names=CLASS_NAMES,
    img_size=IMG_SIZE,
    device=DEVICE,
)

RECEIPT_READER = ReceiptRead(
    lang=["th", "en"],
    model_dir=model_dir,
    download_enabled=False
)

def run_ocr(img_path: str):
    # Config file classify_receipt.py 
    result = CLASSIFIER.predict(img_path)
    print(result)

    text = RECEIPT_READER.add(
        result=result,
        img_path=img_path
    )
    return text

  

import torch
from classify_receipt import ReceiptClassifier
from receipt_read import ReceiptRead

# Config
IMG_SIZE = 224
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
CLASS_NAMES = ["Kbank", "NEXT", "SCB"]

# Path model and image
model_receipt = r"/home/kph/project/OCR-receipt/model/receipt_model.pth"
#image_path = r"/home/kph/project/OCR-receipt/receipt/218326_0.jpg"
model_dir = r"/home/kph/project/OCR-receipt/model"

def run_ocr(img_path):
    # Config file classify_receipt.py 
    classifier = ReceiptClassifier(
        model_path=model_receipt,
        class_names=CLASS_NAMES,
        img_size=IMG_SIZE,
        device=DEVICE,
    )

    result = classifier.predict(img_path)
    print(result)

    receipt_read = ReceiptRead(
        lang=["th", "en"],
        model_dir=model_dir,      
        download_enabled=False
    )
    text = receipt_read.add(
        result=result,
        img_path=img_path
    )
    return text

"""
if __name__ == "__main__":
    
    text = run_ocr()
    print(text)
"""    

import os
import gdown

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

MODEL_DIR = os.path.join(BASE_DIR, "model")

os.makedirs(MODEL_DIR, exist_ok=True)

MODELS = {
    "thai.pth": os.getenv("THAI_MODEL_ID"),
    "craft_mlt_25k.pth": os.getenv("CRAFT_MODEL_ID"),
    "receipt_model.pth": os.getenv("RECEIPT_MODEL_ID"),
}

for filename, file_id in MODELS.items():

    output = os.path.join(MODEL_DIR, filename)

    if not os.path.exists(output):

        print(f"Downloading {filename}...")

        url = f"https://drive.google.com/uc?id={file_id}"

        gdown.download(url, output, quiet=False)

print("All models ready")
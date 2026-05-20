import easyocr

class ReceiptRead:

    # Read receipt
    def __init__ (
        self, 
        lang: list[str] = ["th", "en"], 
        model_dir: str = None, 
        download_enabled: bool = True
        
        ):
        self.reader = easyocr.Reader (
            lang, 
            model_storage_directory=model_dir,
            download_enabled=download_enabled
        )

    def read_img(self, img_path: str) -> str:
        
        # Read image with OCR
        results = self.reader.readtext(img_path)
        
        # Input in list[] and replace o, O by 0  
        value_row = [
            word for item in results
            for word in item[1].replace("O", "0").replace("o", "0").split()
        ]
        return value_row
    
    # Check bank
    def bank_split(self, result: dict, img_path: str) -> str:
        
        if result["bank"] == "Kbank":
            lst = self.read_img(img_path=img_path)
            return lst[-6]
        
        elif result["bank"] == "NEXT":
            return self.read_img(img_path=img_path)
        
        elif result["bank"] == "SCB":
            return self.read_img(img_path=img_path)
        
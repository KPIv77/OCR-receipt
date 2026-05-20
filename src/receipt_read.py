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

    def bank_Kb(self, img_path: str) -> str:
        results = self.reader.readtext(img_path)
        text = "\n".join([item[1] for item in results])
        return text
    
    def bank_Sc(self, img_path: str) -> str:
        results = self.reader.readtext(img_path)
        text = "\n".join([item[1] for item in results])
        return text
    
    def bank_nx(self, img_path: str) -> str:
        results = self.reader.readtext(img_path)
        text = "\n".join([item[1] for item in results])
        return text
    
    # Check bank
    def bank(self, result: dict, img_path: str) -> str:
        
        if result["bank"] == "Kbank":
            return self.bank_Kb(img_path=img_path)
        
        elif result["bank"] == "NEXT":
            return self.bank_nx(img_path=img_path)
        
        elif result["bank"] == "SCB":
            return self.bank_Sc(img_path=img_path)
        
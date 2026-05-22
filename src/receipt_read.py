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
    def bank_split(self,img_path: str) -> str:
    
        lst = self.read_img(img_path=img_path)

        # Define keywords to find the amount of money in the receipt
        keywords = {
            "จำนวนเงิน",
            "จำนวนเงิน:",
            "จานวนเงา",
            "จานวนเงา:",
            "จำนวน",
            "จำนวน:",
            "จานวน",
            "จานวน:"
        }
        
        for i in range(len(lst)):
            if lst[i] in keywords:
                try:
                    amount = lst[i+1]
                    return amount
                except IndexError:
                    return "Not found จำนวนเงิน"

        return f"{img_path}\n Not found จำนวนเงิน"

    def add(self, result: dict,img_path: str) -> str:
        
        bank = result["bank"]
        expense = self.bank_split(img_path=img_path)
        
        return {
            "Bank"  : bank,
            "Expense": expense,
        }
        
    

        
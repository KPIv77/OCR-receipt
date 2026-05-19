class ReceiptRead:

    def bank(self, result: dict) -> str:
        if result["bank"] == "Kbank":
            return "Kbank"
        
        elif result["bank"] == "NEXT":
            return "NEXT"
        
        elif result["bank"] == "SCB":
            return "SCB"
        
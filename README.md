# OCR-receipt
![label](https://img.shields.io/badge/<TEXT>-<COLOR>?style=for-the-badge)

## Project Structure
```
OCR-receipt/
│
├── README.md
├── app/
│   ├──index.html
│   ├──style.css
│   └──script.js
├── model/
│   ├──craft_mlt_25k.pth 
│   ├──thai.pth
│   └──receipt_model.pth
├── src/
│   ├──main.py 
│   ├──classify_receipt.py
│   └──receipt_read.py
└── receipt/
```

## Work Flow

### main .py
```
- Set path model and image receipt 
```

### classify_receipt.py
```
- Classify receipt bank by model receipt_model.pth
```

### receipt_read.py
```
- Use model "craft_mlt_25k.pth" and "thai.pth"
- Read info of receipt.
```






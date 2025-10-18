# fix_tesseract.py
import pytesseract

# If tesseract is not in your PATH, set the path manually
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Test
try:
    print(pytesseract.get_tesseract_version())
    print("✅ Tesseract is working!")
except:
    print("❌ Tesseract not found")
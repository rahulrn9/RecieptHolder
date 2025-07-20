
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"D:\notes\tesseract.exe"  # ✅ Windows path to Tesseract

from PIL import Image
import pdfplumber
import os

from backend.utils.helpers import extract_vendor, extract_date, extract_amount
from backend.ml.predict import predict_category  # ✅ ML-based category prediction

def parse_text_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
            print(f"[DEBUG] Extracted text length (txt): {len(text)}")
            print(f"[DEBUG] First 200 characters:\n{text[:200]}")
            return text
    except Exception as e:
        print(f"[ERROR] Text file parsing failed: {e}")
        return ""

def parse_image(file_path):
    try:
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img)
        print(f"[DEBUG] Extracted text length (img): {len(text)}")
        print(f"[DEBUG] First 200 characters:\n{text[:200]}")
        return text
    except Exception as e:
        print(f"[ERROR] Image OCR failed: {e}")
        return ""

def parse_pdf(file_path):
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        print(f"[DEBUG] Extracted text length (pdf): {len(text)}")
        print(f"[DEBUG] First 200 characters:\n{text[:200]}")
    except Exception as e:
        print(f"[ERROR] PDF parsing failed: {e}")
    return text

def extract_fields(text):
    vendor = extract_vendor(text) or "Unknown"
    date = extract_date(text) or "Unknown"
    amount = extract_amount(text) or 0.0

    # 🧠 ML Prediction with confidence
    category, confidence = predict_category(vendor, text)
    return vendor, date, amount, category, confidence

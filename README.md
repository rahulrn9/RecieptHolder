# 🧾 Receipt Analyzer (Python Full-Stack)

This is a full-stack application to extract and analyze receipt/bill data using OCR and display analytics using Streamlit.

## 🔧 Features

- Supports PDF, image, and text files
- OCR using pytesseract
- Vendor, date, and amount extraction
- SQLite storage
- Streamlit dashboard with charts
- Aggregations and data export

## 🚀 How to Run

```bash
git clone <repo>
cd receipt_uploader
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run dashboard/app.py
```

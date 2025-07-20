ReceiptHolder
A smart full-stack receipt parser and analyzer built with Python, Streamlit, OCR, and Machine Learning. This app enables users to upload receipts, automatically extracts key details, predicts categories using an ML model, syncs with Google Sheets, and visualizes spending patterns.

🔧 Features
Upload and parse receipts (.pdf, .jpg, .png, .txt)

Extracted fields: Vendor, Date, Amount

ML-based Category Prediction (Naive Bayes)

Manual category override option

Google Sheets Sync for real-time record backup

Dashboard with:

All receipt records

Spend analytics by vendor and over time

Export options (CSV/JSON)

Modern and intuitive Streamlit UI

🚀 Setup Instructions
1. Clone the Repository
bash
Copy
Edit
git clone https://github.com/rahulrn9/RecieptHolder.git
cd RecieptHolder
2. Create a Virtual Environment and Install Dependencies
bash
Copy
Edit
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

pip install -r requirements.txt
3. Install Tesseract OCR
Download and install Tesseract: https://github.com/tesseract-ocr/tesseract

Update the path in backend/parsing/parser.py:

python
Copy
Edit
pytesseract.pytesseract.tesseract_cmd = r"D:\path\to\tesseract.exe"
4. Enable Google Sheets Sync (Optional)
Go to Google Cloud Console

Create a project and enable Google Sheets API

Create a Service Account, download the .json credentials

Share access to your Google Sheet with the service account email

Replace recieptloader-xxx.json in root with your JSON key

Update backend/sync/google_sync.py:

python
Copy
Edit
GCREDS_PATH = "your-json-file.json"
SPREADSHEET_ID = "your-spreadsheet-id"
SHEET_NAME = "Receipt Data Sync"
5. Run the App
bash
Copy
Edit
streamlit run dashboard/app.py
🧠 Architecture Overview
📂 Project Structure
bash
Copy
Edit
RecieptHolder/
├── backend/
│   ├── ml/                  # ML model and predictor
│   ├── parsing/             # PDF/Image/Text parsing
│   ├── storage/             # SQLite DB logic
│   ├── ingestion/           # File validator
│   ├── sync/                # Google Sheets integration
│   └── utils/               # Vendor/Date/Amount extractors
├── dashboard/               # Streamlit app
├── data/                    # Uploaded receipts (auto-created)
├── category_model.pkl       # Trained ML model (Naive Bayes)
├── requirements.txt
├── .gitignore
└── README.md
⚙️ Data Flow
User uploads a receipt

File parsed using OCR/text extractors

Extracted text processed to find vendor, date, amount

ML model predicts category based on vendor and receipt text

Final record saved to local DB + (optionally) synced to Google Sheets

Data is displayed, summarized, and visualized on dashboard

📝 Design Choices
Modular structure: Easy-to-maintain, scalable backend

Streamlit UI: Lightweight, interactive web UI

Naive Bayes classifier: Suitable for small text-based classification

Google Sheets sync: Simple cloud integration to showcase external API skills

Manual override: Combines automation with user control

⚠️ Limitations
OCR performance depends on image quality (Tesseract isn't perfect)

Date and vendor extraction use regex-based heuristics (not NLP)

ML model trained on limited synthetic data

No login/authentication system (for simplicity)

Google Sheet integration assumes sheet structure and permissions are correct

📌 Assumptions
Receipts contain recognizable vendor names and monetary amounts

Date formats follow recognizable patterns (e.g., dd-mm-yyyy, yyyy-mm-dd)

Google Sheet is pre-shared with service account before use

The app is run locally in a virtual environment

📤 Export
Exported records available as:

CSV: receipts.csv

JSON: receipts.json

Accessible from the Export tab in the dashboard.

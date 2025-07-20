import gspread
from oauth2client.service_account import ServiceAccountCredentials

GCREDS_PATH = "recieptloader-1c1724bc0d1e.json"
SPREADSHEET_ID = "1V_FYPmg5-1rCpv4girz6CksQKG1qSS7F3yO_3pLAjDw"
SHEET_NAME = "Receipt Data Sync"

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(GCREDS_PATH, scope)
client = gspread.authorize(creds)

sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

test_row = ["TestVendor", "2025-07-20", "123.45", "TestCategory"]
sheet.append_row(test_row)
print("✅ Row inserted successfully.")

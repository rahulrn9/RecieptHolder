import gspread
from oauth2client.service_account import ServiceAccountCredentials

# === Constants ===
GCREDS_PATH = "recieptloader-1c1724bc0d1e.json"
SPREADSHEET_ID = "1V_FYPmg5-1rCpv4girz6CksQKG1qSS7F3yO_3pLAjDw"
SHEET_NAME = "Receipt Data Sync"

def sync_receipt_to_sheet(vendor, date, amount, category):
    """
    Append a new row with receipt data to the Google Sheet.
    Includes logging for easier debugging.
    """
    try:
        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(GCREDS_PATH, scope)
        client = gspread.authorize(creds)

        print("[DEBUG] Connecting to Google Sheet...")
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        sheet = spreadsheet.worksheet(SHEET_NAME)

        new_row = [vendor, date, str(amount), category]
        sheet.append_row(new_row)

        print(f"[SYNCED] ✅ Row added: {new_row}")
    except Exception as e:
        print(f"[ERROR] Google Sheet sync failed: {e}")

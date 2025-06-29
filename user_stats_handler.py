import os
import json
from datetime import date
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1mKfdSTLMrqyLu2GW_Km5ErboyPgjcyJ4q9Mqn8DkwCE'
SHEET_NAME = 'user_stats'  # 請確認你的工作表名稱

# 取得 Google Sheets 憑證
def get_credentials():
    google_credentials = os.getenv('GOOGLE_CREDENTIALS')  # 或 'GOOGLE_CREDENTIALS_USER'
    if google_credentials:
        creds_info = json.loads(google_credentials)
        creds = Credentials.from_service_account_info(creds_info, scopes=SCOPES)
        return creds
    return None

def get_service():
    creds = get_credentials()
    if not creds:
        raise Exception('No Google credentials found')
    service = build('sheets', 'v4', credentials=creds)
    return service

def safe_int(val):
    try:
        return int(val)
    except Exception:
        return 0

def get_user_stats(user_id):
    service = get_service()
    sheet = service.spreadsheets()
    range_name = f'{SHEET_NAME}!A2:E'
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=range_name).execute()
    values = result.get('values', [])
    for row in values:
        if row and row[0] == user_id:
            correct = safe_int(row[1]) if len(row) > 1 and row[1] else 0
            wrong = safe_int(row[2]) if len(row) > 2 and row[2] else 0
            correct_qids = []
            if len(row) > 3 and row[3]:
                for q in row[3].split(','):
                    try:
                        correct_qids.append(int(q))
                    except Exception:
                        pass  # 忽略非數字內容
            last_update = row[4] if len(row) > 4 else ''
            stats = {
                'correct': correct,
                'wrong': wrong,
                'correct_qids': correct_qids,
                'last_update': last_update
            }
            print(f"[DEBUG] get_user_stats for {user_id}: {stats}", flush=True)
            return stats
    # 沒有找到，回傳預設值
    stats = {
        'correct': 0,
        'wrong': 0,
        'correct_qids': [],
        'last_update': ''
    }
    print(f"[DEBUG] get_user_stats for {user_id}: {stats}", flush=True)
    return stats

def update_user_stats(user_id, correct, wrong, correct_qids):
    service = get_service()
    sheet = service.spreadsheets()
    range_name = f'{SHEET_NAME}!A2:E'
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=range_name).execute()
    values = result.get('values', [])
    correct_qids_str = ','.join(str(q) for q in correct_qids)
    today = date.today().isoformat()
    found = False
    for idx, row in enumerate(values):
        if row and row[0] == user_id:
            found = True
            row_idx = idx + 2  # A2 對應 row 2
            update_range = f'{SHEET_NAME}!A{row_idx}:E{row_idx}'
            sheet.values().update(
                spreadsheetId=SPREADSHEET_ID,
                range=update_range,
                valueInputOption='RAW',
                body={'values': [[user_id, correct, wrong, correct_qids_str, today]]}
            ).execute()
            break
    if not found:
        # 新增一行
        sheet.values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=f'{SHEET_NAME}!A:E',
            valueInputOption='RAW',
            body={'values': [[user_id, correct, wrong, correct_qids_str, today]]}
        ).execute() 
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path
import pickle
import random

# 如果修改了這些範圍，請刪除 token.pickle 文件
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SPREADSHEET_ID = '1mKfdSTLMrqyLu2GW_Km5ErboyPgjcyJ4q9Mqn8DkwCE'
RANGE_NAME = 'Sheet1!A:F'  # 假設數據在 Sheet1 的 A 到 F 列

def get_credentials():
    """獲取 Google Sheets API 憑證"""
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

def get_questions():
    """從 Google Sheets 獲取問題數據"""
    creds = get_credentials()
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME
    ).execute()
    
    values = result.get('values', [])
    if not values:
        return []
    
    # 跳過標題行，將數據轉換為字典列表
    questions = []
    for row in values[1:]:  # 跳過標題行
        if len(row) >= 6:  # 確保有足夠的列
            question = {
                'question': row[0],
                'options': row[1:5],
                'answer': row[4],
                'explanation': row[5] if len(row) > 5 else ''
            }
            questions.append(question)
    
    return questions

def get_random_question():
    """隨機獲取一個問題"""
    questions = get_questions()
    if not questions:
        return None
    return random.choice(questions) 
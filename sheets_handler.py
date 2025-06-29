import json
import os
import random
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Google Sheets 配置
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SPREADSHEET_ID = '1mKfdSTLMrqyLu2GW_Km5ErboyPgjcyJ4q9Mqn8DkwCE'
RANGE_NAME = 'Sheet1!A:F'  # 假設數據在 Sheet1 的 A 到 F 列

def get_credentials():
    """獲取 Google Sheets API 憑證"""
    try:
        # 從環境變數讀取 Google 憑證
        google_credentials = os.getenv('GOOGLE_CREDENTIALS')
        if google_credentials:
            creds_info = json.loads(google_credentials)
            creds = Credentials.from_service_account_info(creds_info)
            return creds
        else:
            print("Warning: GOOGLE_CREDENTIALS environment variable not found")
            return None
    except Exception as e:
        print(f"Error loading Google credentials: {str(e)}")
        return None

def get_questions():
    """從 Google Sheets 獲取問題數據"""
    try:
        creds = get_credentials()
        if not creds:
            print("No valid credentials found")
            return []
            
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME
        ).execute()
        
        values = result.get('values', [])
        if not values:
            print("No data found in spreadsheet")
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
        
        print(f"Loaded {len(questions)} questions from Google Sheets")
        return questions
        
    except Exception as e:
        print(f"Error getting questions from Google Sheets: {str(e)}")
        return []

def get_random_question():
    """隨機獲取一個問題"""
    questions = get_questions()
    if not questions:
        print("No questions available")
        return None
    return random.choice(questions) 
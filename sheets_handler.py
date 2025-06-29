import json
import os
import random
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Google Sheets 配置
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SPREADSHEET_ID = '1mKfdSTLMrqyLu2GW_Km5ErboyPgjcyJ4q9Mqn8DkwCE'
RANGE_NAME = 'Sheet1!A:F'  # 假設數據在 Sheet1 的 A 到 F 列

def get_test_questions():
    """返回測試問題（當 Google Sheets 不可用時）"""
    return [
        {
            'question': '人體最大的器官是什麼？',
            'options': ['心臟', '大腦', '皮膚', '肝臟'],
            'answer': '3',
            'explanation': '皮膚是人體最大的器官，佔體重的約16%。'
        },
        {
            'question': '人體有多少塊骨頭？',
            'options': ['206塊', '186塊', '226塊', '196塊'],
            'answer': '1',
            'explanation': '成人人體有206塊骨頭。'
        },
        {
            'question': '心臟位於胸腔的哪個位置？',
            'options': ['左側', '右側', '中央偏左', '中央偏右'],
            'answer': '3',
            'explanation': '心臟位於胸腔中央偏左的位置。'
        }
    ]

def get_credentials():
    """獲取 Google Sheets API 憑證"""
    try:
        # 優先使用本地 credentials.json 檔案
        if os.path.exists('credentials.json'):
            creds = Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
            print("Using local credentials.json file")
            return creds
        
        # 如果沒有本地檔案，嘗試從環境變數讀取
        google_credentials = os.getenv('GOOGLE_CREDENTIALS')
        if google_credentials:
            creds_info = json.loads(google_credentials)
            creds = Credentials.from_service_account_info(creds_info, scopes=SCOPES)
            print("Using Google credentials from environment variable")
            return creds
        
        print("No Google credentials found")
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
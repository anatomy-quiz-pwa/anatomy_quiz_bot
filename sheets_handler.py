import json
import os
import random
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Google Sheets 配置
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SPREADSHEET_ID = '1mKfdSTLMrqyLu2GW_Km5ErboyPgjcyJ4q9Mqn8DkwCE'
SHEET_NAME = '題庫'  # 工作表名稱
RANGE_NAME = f'{SHEET_NAME}!A:H'  # 範圍：題庫!A:H

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
        print("Starting to get questions from Google Sheets...")
        creds = get_credentials()
        if not creds:
            print("No valid credentials found")
            return []
        
        print("Building Google Sheets service...")
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        
        print(f"Requesting data from spreadsheet {SPREADSHEET_ID}, range {RANGE_NAME}")
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME
        ).execute()
        
        values = result.get('values', [])
        print(f"Raw data received: {len(values)} rows")
        
        if not values:
            print("No data found in spreadsheet")
            return []
        
        # 顯示前幾行資料來除錯
        print("First few rows of data:")
        for i, row in enumerate(values[:3]):
            print(f"Row {i}: {row}")
        
        # 跳過標題行，將數據轉換為字典列表
        questions = []
        for i, row in enumerate(values[1:], 1):  # 跳過標題行
            print(f"Processing row {i}: {row}")
            
            # 確保有足夠的列
            if len(row) < 8:
                print(f"Row {i} has insufficient columns: {len(row)} < 8")
                continue
            
            # 檢查必要欄位是否為空
            if not row[1] or not row[1].strip():  # 題目內容
                print(f"Row {i} has empty question content")
                continue
            
            # 檢查選項是否為空
            options = [opt.strip() for opt in row[2:6] if opt and opt.strip()]
            if len(options) < 4:
                print(f"Row {i} has insufficient options: {len(options)} < 4")
                continue
            
            # 檢查答案是否有效
            try:
                answer = int(row[6])
                if answer < 1 or answer > 4:
                    print(f"Row {i} has invalid answer: {answer}")
                    continue
            except (ValueError, TypeError):
                print(f"Row {i} has non-numeric answer: {row[6]}")
                continue
            
            question = {
                'qid': i,  # 新增唯一題目ID
                'category': row[0] if row[0] else '未分類',      # A列：題目分類
                'question': row[1].strip(),                      # B列：題目內容
                'options': options,                              # C-F列：選項1-4
                'answer': str(answer),                           # G列：正確答案
                'explanation': row[7].strip() if len(row) > 7 and row[7] else ''  # H列：補充資料
            }
            questions.append(question)
            print(f"Added question: {question['question'][:50]}...")
        
        print(f"Successfully loaded {len(questions)} questions from Google Sheets")
        return questions
        
    except Exception as e:
        print(f"Error getting questions from Google Sheets: {str(e)}")
        import traceback
        traceback.print_exc()
        return []

def get_random_question():
    """隨機獲取一個問題"""
    print("Getting random question...")
    questions = get_questions()
    if not questions:
        print("No questions available from Google Sheets, using test question")
        # 返回測試問題
        return {
            'category': '測試',
            'question': '這是一個測試問題：人體最大的器官是什麼？',
            'options': ['心臟', '大腦', '皮膚', '肝臟'],
            'answer': '3',
            'explanation': '皮膚是人體最大的器官，佔體重的約16%。'
        }
    selected = random.choice(questions)
    print(f"Selected question: {selected['question'][:50]}...")
    return selected 
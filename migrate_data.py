#!/usr/bin/env python3
"""
資料遷移腳本：從 Google Sheets 遷移到 Supabase
"""

import os
import json
from datetime import date
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_ANON_KEY

# Google Sheets 配置
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SPREADSHEET_ID = '1mKfdSTLMrqyLu2GW_Km5ErboyPgjcyJ4q9Mqn8DkwCE'

def get_google_credentials():
    """獲取 Google Sheets API 憑證"""
    try:
        if os.path.exists('credentials.json'):
            creds = Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
            print("Using local credentials.json file")
            return creds
        
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

def migrate_questions():
    """遷移題目資料"""
    print("開始遷移題目資料...")
    
    # 初始化 Supabase
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    
    # 獲取 Google Sheets 資料
    creds = get_google_credentials()
    if not creds:
        print("無法獲取 Google 憑證，跳過題目遷移")
        return
    
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    
    try:
        # 獲取題目資料
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range='題庫!A:H'
        ).execute()
        
        values = result.get('values', [])
        if not values:
            print("沒有找到題目資料")
            return
        
        print(f"找到 {len(values)-1} 個題目")
        
        # 跳過標題行，處理每個題目
        migrated_count = 0
        for i, row in enumerate(values[1:], 1):
            if len(row) < 8:
                print(f"跳過第 {i} 行：資料不完整")
                continue
            
            # 檢查必要欄位
            if not row[1] or not row[1].strip():
                print(f"跳過第 {i} 行：題目內容為空")
                continue
            
            # 檢查選項
            options = [opt.strip() for opt in row[2:6] if opt and opt.strip()]
            if len(options) < 4:
                print(f"跳過第 {i} 行：選項不完整")
                continue
            
            # 檢查答案
            try:
                answer = int(row[6])
                if answer < 1 or answer > 4:
                    print(f"跳過第 {i} 行：答案無效")
                    continue
            except (ValueError, TypeError):
                print(f"跳過第 {i} 行：答案格式錯誤")
                continue
            
            # 準備 Supabase 資料
            question_data = {
                'category': row[0] if row[0] else '未分類',
                'question': row[1].strip(),
                'option1': options[0],
                'option2': options[1],
                'option3': options[2],
                'option4': options[3],
                'correct_answer': answer,
                'explanation': row[7].strip() if len(row) > 7 and row[7] else ''
            }
            
            try:
                # 插入到 Supabase
                supabase.table('questions').insert(question_data).execute()
                migrated_count += 1
                print(f"已遷移題目 {migrated_count}: {question_data['question'][:30]}...")
            except Exception as e:
                print(f"遷移題目失敗：{str(e)}")
        
        print(f"題目遷移完成，共遷移 {migrated_count} 個題目")
        
    except Exception as e:
        print(f"遷移題目時發生錯誤：{str(e)}")

def migrate_user_stats():
    """遷移用戶統計資料"""
    print("開始遷移用戶統計資料...")
    
    # 初始化 Supabase
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    
    # 獲取 Google Sheets 資料
    creds = get_google_credentials()
    if not creds:
        print("無法獲取 Google 憑證，跳過用戶統計遷移")
        return
    
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    
    try:
        # 獲取用戶統計資料
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range='user_stats!A2:E'
        ).execute()
        
        values = result.get('values', [])
        if not values:
            print("沒有找到用戶統計資料")
            return
        
        print(f"找到 {len(values)} 個用戶統計記錄")
        
        # 處理每個用戶統計
        migrated_count = 0
        for i, row in enumerate(values):
            if not row or not row[0]:
                print(f"跳過第 {i+2} 行：用戶ID為空")
                continue
            
            user_id = row[0]
            correct = int(row[1]) if len(row) > 1 and row[1] else 0
            wrong = int(row[2]) if len(row) > 2 and row[2] else 0
            correct_qids = row[3] if len(row) > 3 and row[3] else ''
            last_update = row[4] if len(row) > 4 else date.today().isoformat()
            
            # 準備 Supabase 資料
            stats_data = {
                'user_id': user_id,
                'correct': correct,
                'wrong': wrong,
                'correct_qids': correct_qids,
                'last_update': last_update
            }
            
            try:
                # 插入到 Supabase
                supabase.table('user_stats').insert(stats_data).execute()
                migrated_count += 1
                print(f"已遷移用戶統計 {migrated_count}: {user_id}")
            except Exception as e:
                print(f"遷移用戶統計失敗 {user_id}: {str(e)}")
        
        print(f"用戶統計遷移完成，共遷移 {migrated_count} 個用戶")
        
    except Exception as e:
        print(f"遷移用戶統計時發生錯誤：{str(e)}")

def main():
    """主函數"""
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        print("錯誤：請設定 SUPABASE_URL 和 SUPABASE_ANON_KEY 環境變數")
        return
    
    print("開始資料遷移...")
    print("="*50)
    
    # 遷移題目
    migrate_questions()
    print()
    
    # 遷移用戶統計
    migrate_user_stats()
    print()
    
    print("資料遷移完成！")
    print("\n注意事項：")
    print("1. 請確認 Supabase 中已建立必要的表格")
    print("2. 建議在遷移後檢查資料完整性")
    print("3. 可以考慮保留 Google Sheets 作為備份")

if __name__ == "__main__":
    main() 
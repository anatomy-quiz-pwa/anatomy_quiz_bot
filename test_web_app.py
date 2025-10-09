#!/usr/bin/env python3
"""
測試網站版本的功能
"""

import os
import sys
import requests
import json
from supabase import create_client, Client

# 添加當前目錄到Python路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_supabase_connection():
    """測試Supabase連接"""
    print("🧪 測試Supabase連接...")
    
    SUPABASE_URL = "https://ciqlfqfgzqqgdrogedxg.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA"
    
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # 測試users表
        response = supabase.table('users').select('count', count='exact').limit(1).execute()
        print(f"   ✅ users表連接成功，共有 {response.count} 個用戶")
        
        # 測試user_stats表
        response = supabase.table('user_stats').select('count', count='exact').limit(1).execute()
        print(f"   ✅ user_stats表連接成功，共有 {response.count} 個統計記錄")
        
        # 測試questions表
        response = supabase.table('questions').select('count', count='exact').limit(1).execute()
        print(f"   ✅ questions表連接成功，共有 {response.count} 道題目")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Supabase連接失敗: {e}")
        return False

def test_web_app_endpoints():
    """測試網站端點"""
    print("\n🧪 測試網站端點...")
    
    base_url = "http://localhost:5000"
    
    endpoints = [
        ("/", "首頁"),
        ("/login", "登入頁面"),
    ]
    
    for endpoint, description in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"   ✅ {description} ({endpoint}) - 正常")
            else:
                print(f"   ⚠️ {description} ({endpoint}) - 狀態碼: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"   ❌ {description} ({endpoint}) - 連接失敗 (網站可能未啟動)")
        except Exception as e:
            print(f"   ❌ {description} ({endpoint}) - 錯誤: {e}")

def test_questions_data():
    """測試題目數據"""
    print("\n🧪 測試題目數據...")
    
    SUPABASE_URL = "https://ciqlfqfgzqqgdrogedxg.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA"
    
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # 測試獲取不同等級的題目
        for level in [1, 5, 10, 14]:
            response = supabase.table('questions').select('*').eq('level', level).limit(1).execute()
            if response.data:
                question = response.data[0]
                print(f"   ✅ 等級{level}題目: {question['question'][:30]}...")
            else:
                print(f"   ⚠️ 等級{level}: 沒有題目")
        
        # 測試題目結構
        response = supabase.table('questions').select('*').limit(1).execute()
        if response.data:
            question = response.data[0]
            required_fields = ['id', 'question', 'options', 'correct_answer', 'level', 'category']
            missing_fields = [field for field in required_fields if field not in question]
            if not missing_fields:
                print(f"   ✅ 題目數據結構完整")
            else:
                print(f"   ❌ 題目數據缺少欄位: {missing_fields}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ 測試題目數據失敗: {e}")
        return False

def test_user_data():
    """測試用戶數據"""
    print("\n🧪 測試用戶數據...")
    
    SUPABASE_URL = "https://ciqlfqfgzqqgdrogedxg.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA"
    
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # 獲取用戶統計數據
        response = supabase.table('user_stats').select('*').order('correct', desc=True).limit(5).execute()
        if response.data:
            print(f"   ✅ 獲取到 {len(response.data)} 個用戶統計記錄")
            
            for i, user in enumerate(response.data[:3], 1):
                user_id = user.get('user_id', '')
                correct = user.get('correct', 0)
                total = user.get('total', 0)
                level = user.get('level', 1)
                print(f"      第{i}名: {user_id[:10]}... - {correct}/{total} (等級{level})")
        else:
            print("   ⚠️ 沒有用戶統計數據")
        
        return True
        
    except Exception as e:
        print(f"   ❌ 測試用戶數據失敗: {e}")
        return False

def main():
    """主測試函數"""
    print("🚀 開始測試解剖學測驗網站版本")
    print("=" * 60)
    
    # 測試Supabase連接
    supabase_ok = test_supabase_connection()
    
    # 測試網站端點
    test_web_app_endpoints()
    
    # 測試題目數據
    questions_ok = test_questions_data()
    
    # 測試用戶數據
    users_ok = test_user_data()
    
    print("\n" + "=" * 60)
    print("🎉 測試完成！")
    
    if supabase_ok and questions_ok and users_ok:
        print("✅ 所有核心功能測試通過")
        print("\n📋 下一步:")
        print("1. 設置LINE Login Channel")
        print("2. 配置環境變數")
        print("3. 啟動網站: python web_app.py")
        print("4. 訪問 http://localhost:5000 進行測試")
    else:
        print("❌ 部分測試失敗，請檢查配置")

if __name__ == "__main__":
    main()

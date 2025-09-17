#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試發送歡迎訊息到指定用戶
"""

import os
import sys
import json
import requests
from datetime import datetime

# 添加當前目錄到 Python 路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 設置環境變量
os.environ['SUPABASE_URL'] = 'https://ciqlfqfgzqqgdrogedxg.supabase.co'
os.environ['SUPABASE_ANON_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA'

def send_welcome_message_to_user(user_id):
    """發送歡迎訊息到指定用戶"""
    print(f"🚀 準備發送歡迎訊息到用戶: {user_id}")
    
    try:
        from app_supabase import create_welcome_flex_message, send_line_message
        
        # 創建歡迎訊息
        welcome_flex = create_welcome_flex_message("測試用戶")
        
        # 創建完整的 Flex 訊息格式
        flex_message = {
            "type": "flex",
            "altText": "歡迎來到解剖咬一口 Beta測試版",
            "contents": welcome_flex
        }
        
        # 發送 Flex 訊息
        result = send_line_message(user_id, flex_message)
        
        if result:
            print("✅ 歡迎訊息發送成功！")
            return True
        else:
            print("❌ 歡迎訊息發送失敗")
            return False
            
    except Exception as e:
        print(f"❌ 發送歡迎訊息時發生錯誤: {e}")
        return False

def test_line_api_connection():
    """測試 LINE API 連接"""
    print("🔍 測試 LINE API 連接...")
    
    try:
        # LINE API 設定
        LINE_CHANNEL_ACCESS_TOKEN = "AhZFgYWfEMeFSDxJJhzcvJoKx78lVrfRH3cqqusfiZhug/f5wRhQTkDD9fW7+IJLA3xpoQtunFWoVKnHtaE9p+U1QVFUz1o8CQ5AnNpPicjK32KAD5Z1ouF1HNKATv/BhUHIS3OjcndnUGpOqPDYKAdB04t89/1O/w1cDnyilFU="
        
        # 測試 API 連接
        headers = {
            'Authorization': f'Bearer {LINE_CHANNEL_ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        # 簡單的 API 測試
        response = requests.get('https://api.line.me/v2/bot/info', headers=headers)
        
        if response.status_code == 200:
            print("✅ LINE API 連接正常")
            return True
        else:
            print(f"❌ LINE API 連接失敗: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ LINE API 測試失敗: {e}")
        return False

def create_welcome_message_json():
    """創建歡迎訊息的 JSON 格式"""
    print("📝 創建歡迎訊息 JSON...")
    
    try:
        from app_supabase import create_welcome_flex_message
        
        # 創建歡迎訊息
        welcome_flex = create_welcome_flex_message("測試用戶")
        
        # 完整的 LINE 訊息格式
        line_message = {
            "to": "USER_ID_PLACEHOLDER",
            "messages": [
                {
                    "type": "flex",
                    "altText": "歡迎來到解剖咬一口 Beta測試版",
                    "contents": welcome_flex
                }
            ]
        }
        
        # 保存到檔案
        with open("line_welcome_message.json", "w", encoding="utf-8") as f:
            json.dump(line_message, f, ensure_ascii=False, indent=2)
        
        print("✅ 歡迎訊息 JSON 已保存到 line_welcome_message.json")
        
        # 顯示關鍵信息
        print("\n📋 歡迎訊息摘要:")
        print(f"   - Hero 圖片 URL: {welcome_flex['body']['contents'][0]['url']}")
        print(f"   - 主標題: {welcome_flex['body']['contents'][1]['contents'][0]['text']}")
        print(f"   - 副標題: {welcome_flex['body']['contents'][1]['contents'][1]['text']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 創建歡迎訊息 JSON 失敗: {e}")
        return False

def main():
    """主測試函數"""
    print("🧪 測試歡迎訊息發送功能...")
    print("=" * 60)
    
    # 測試項目
    tests = [
        ("LINE API 連接測試", test_line_api_connection),
        ("創建歡迎訊息 JSON", create_welcome_message_json),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 執行測試: {test_name}")
        print("-" * 40)
        
        try:
            result = test_func()
            results.append((test_name, result))
            
            if result:
                print(f"✅ {test_name} 通過")
            else:
                print(f"❌ {test_name} 失敗")
                
        except Exception as e:
            print(f"❌ {test_name} 異常: {e}")
            results.append((test_name, False))
    
    # 總結測試結果
    print("\n" + "=" * 60)
    print("📊 測試結果總結:")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n總計: {passed}/{total} 個測試通過")
    
    if passed == total:
        print("\n🎉 所有測試都通過了！")
        print("\n📝 使用說明:")
        print("1. 請提供您的 LINE User ID (通常以 'U' 開頭的長字串)")
        print("2. 運行以下命令發送測試訊息:")
        print("   python -c \"from test_send_welcome import send_welcome_message_to_user; send_welcome_message_to_user('您的_USER_ID')\"")
        print("3. 或者修改 line_welcome_message.json 中的 USER_ID_PLACEHOLDER 為您的 User ID")
        print("4. 使用 LINE API 發送訊息到您的帳號")
    else:
        print("⚠️ 部分測試失敗，請檢查相關功能。")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

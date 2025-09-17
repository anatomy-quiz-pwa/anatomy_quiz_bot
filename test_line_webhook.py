#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試 LINE Webhook 和排行榜功能
"""

import requests
import json
import os

def test_line_webhook():
    """測試 LINE Webhook 端點"""
    print("🧪 測試 LINE Webhook 和排行榜功能")
    print("=" * 50)
    
    # 設置環境變量
    os.environ['LINE_CHANNEL_ACCESS_TOKEN'] = "AhZFgYWfEMeFSDxJJhzcvJoKx78lVrfRH3cqqusfiZhug/f5wRhQTkDD9fW7+IJLA3xpoQtunFWoVKnHtaE9p+U1QVFUz1o8CQ5AnNpPicjK32KAD5Z1ouF1HNKATv/BhUHIS3OjcndnUGpOqPDYKAdB04t89/1O/w1cDnyilFU="
    os.environ['LINE_CHANNEL_SECRET'] = "c025320a9328abc76bf61f36c1039756"
    os.environ['SUPABASE_URL'] = "https://ciqlfqfgzqqgdrogedxg.supabase.co"
    os.environ['SUPABASE_ANON_KEY'] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA"
    
    # 測試 LINE Webhook 端點
    webhook_url = "http://localhost:5002/webhook"
    
    # 模擬 LINE 文字訊息
    test_message = {
        "events": [
            {
                "type": "message",
                "replyToken": "test_reply_token",
                "source": {
                    "userId": "U1234567890abcdef",
                    "type": "user"
                },
                "timestamp": 1640995200000,
                "mode": "active",
                "message": {
                    "id": "test_message_id",
                    "type": "text",
                    "text": "排行榜"
                }
            }
        ],
        "destination": "U1234567890abcdef"
    }
    
    print("📤 發送測試訊息到 LINE Webhook...")
    print(f"   訊息內容: {test_message['events'][0]['message']['text']}")
    print(f"   用戶ID: {test_message['events'][0]['source']['userId']}")
    
    try:
        # 發送 POST 請求到 webhook
        response = requests.post(
            webhook_url,
            json=test_message,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"📡 響應狀態碼: {response.status_code}")
        print(f"📋 響應內容: {response.text}")
        
        if response.status_code == 200:
            print("✅ Webhook 請求成功")
        else:
            print(f"❌ Webhook 請求失敗: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 無法連接到應用服務器")
        print("💡 請確保應用正在運行在 localhost:5002")
    except Exception as e:
        print(f"❌ 請求失敗: {e}")

def test_direct_leaderboard():
    """直接測試排行榜功能"""
    print("\n🎯 直接測試排行榜功能...")
    print("=" * 50)
    
    try:
        # 導入並測試排行榜功能
        import sys
        sys.path.append('.')
        
        from app_supabase_fixed import send_leaderboard_message
        
        test_user_id = "U1234567890abcdef"
        print(f"👤 測試用戶ID: {test_user_id}")
        
        # 調用排行榜功能
        result = send_leaderboard_message(test_user_id)
        print(f"📤 發送結果: {result}")
        
        if result is None:
            print("✅ 排行榜功能執行成功")
        else:
            print(f"📊 返回結果: {result}")
            
    except Exception as e:
        print(f"❌ 直接測試失敗: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 開始測試 LINE Webhook 和排行榜功能")
    print("=" * 60)
    
    # 測試 LINE Webhook
    test_line_webhook()
    
    # 直接測試排行榜功能
    test_direct_leaderboard()
    
    print("\n" + "=" * 60)
    print("🎉 測試完成！")

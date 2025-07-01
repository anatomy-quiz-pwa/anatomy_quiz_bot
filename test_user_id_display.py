#!/usr/bin/env python3
"""
測試用戶 ID 顯示功能
"""

import sys
import os
import requests
import json
import time

def test_user_id_display():
    """測試用戶 ID 顯示功能"""
    
    # 模擬用戶發送訊息
    webhook_data = {
        "events": [
            {
                "type": "message",
                "message": {
                    "type": "text",
                    "text": "我的ID"
                },
                "replyToken": "test_reply_token_123",
                "source": {
                    "userId": "U1234567890abcdef1234567890abcdef",
                    "type": "user"
                },
                "timestamp": int(time.time() * 1000)
            }
        ]
    }
    
    try:
        print("🧪 測試用戶 ID 顯示功能...")
        print("📤 發送測試訊息到 Flask 應用...")
        
        # 發送 webhook 到本地應用程式
        response = requests.post(
            "http://localhost:5001/callback",
            headers={
                "Content-Type": "application/json",
                "X-Line-Signature": "test_signature"
            },
            data=json.dumps(webhook_data),
            timeout=10
        )
        
        print(f"📥 回應狀態碼: {response.status_code}")
        print(f"📥 回應內容: {response.text}")
        
        if response.status_code == 200:
            print("✅ 測試成功！請查看 Flask 應用的控制台輸出")
            print("🔍 你應該能看到類似這樣的輸出：")
            print("   🔍 收到訊息 - 用戶 ID: U1234567890abcdef1234567890abcdef")
            print("   📝 訊息內容: 我的ID")
        else:
            print("❌ 測試失敗")
        
        return response.status_code == 200
        
    except requests.exceptions.ConnectionError:
        print("❌ 無法連接到應用程式，請確保 app_supabase.py 正在運行")
        return False
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        return False

def test_button_click():
    """測試按鈕點擊的用戶 ID 顯示"""
    
    # 模擬用戶點擊按鈕
    webhook_data = {
        "events": [
            {
                "type": "postback",
                "postback": {
                    "data": "continue_quiz"
                },
                "replyToken": "test_reply_token_456",
                "source": {
                    "userId": "U9876543210fedcba09876543210fedcba",
                    "type": "user"
                },
                "timestamp": int(time.time() * 1000)
            }
        ]
    }
    
    try:
        print("\n🧪 測試按鈕點擊的用戶 ID 顯示...")
        print("📤 發送測試按鈕點擊到 Flask 應用...")
        
        # 發送 webhook 到本地應用程式
        response = requests.post(
            "http://localhost:5001/callback",
            headers={
                "Content-Type": "application/json",
                "X-Line-Signature": "test_signature"
            },
            data=json.dumps(webhook_data),
            timeout=10
        )
        
        print(f"📥 回應狀態碼: {response.status_code}")
        print(f"📥 回應內容: {response.text}")
        
        if response.status_code == 200:
            print("✅ 按鈕點擊測試成功！請查看 Flask 應用的控制台輸出")
            print("🔍 你應該能看到類似這樣的輸出：")
            print("   🔘 收到按鈕點擊 - 用戶 ID: U9876543210fedcba09876543210fedcba")
            print("   📝 按鈕資料: continue_quiz")
        else:
            print("❌ 按鈕點擊測試失敗")
        
        return response.status_code == 200
        
    except requests.exceptions.ConnectionError:
        print("❌ 無法連接到應用程式，請確保 app_supabase.py 正在運行")
        return False
    except Exception as e:
        print(f"❌ 按鈕點擊測試失敗: {e}")
        return False

if __name__ == "__main__":
    print("🎯 用戶 ID 顯示測試")
    print("=" * 50)
    
    # 測試文字訊息
    test_user_id_display()
    
    # 測試按鈕點擊
    test_button_click()
    
    print("\n" + "=" * 50)
    print("📋 測試完成！")
    print("💡 現在你可以在 LINE 中發送任何訊息給機器人，")
    print("   控制台會顯示你的真實用戶 ID。") 
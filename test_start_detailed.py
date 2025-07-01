#!/usr/bin/env python3
"""
詳細測試"開始"命令的腳本
"""

import requests
import json
import time

def test_start_command_detailed():
    """詳細測試開始命令"""
    print("🧪 詳細測試「開始」命令...")
    print("=" * 50)
    
    # 模擬 LINE webhook 的 POST 請求
    webhook_url = "http://127.0.0.1:5001/callback"
    
    # 模擬用戶發送"開始"訊息的 webhook 事件
    webhook_data = {
        "events": [
            {
                "type": "message",
                "mode": "active",
                "timestamp": int(time.time() * 1000),
                "source": {
                    "type": "user",
                    "userId": "test_user_123"
                },
                "webhookEventId": "test_webhook_id",
                "deliveryContext": {
                    "isRedelivery": False
                },
                "replyToken": "test_reply_token_123",
                "message": {
                    "id": "test_message_id_123",
                    "type": "text",
                    "text": "開始"
                }
            }
        ],
        "destination": "test_destination"
    }
    
    headers = {
        "Content-Type": "application/json",
        "X-Line-Signature": "test_signature"
    }
    
    print("📤 發送 webhook 請求...")
    print(f"🔗 URL: {webhook_url}")
    print(f"📝 請求內容: {json.dumps(webhook_data, indent=2, ensure_ascii=False)}")
    
    try:
        response = requests.post(
            webhook_url,
            json=webhook_data,
            headers=headers,
            timeout=10
        )
        
        print(f"📥 收到回應: {response.status_code}")
        print(f"📄 回應內容: {response.text}")
        
        if response.status_code == 200:
            print("✅ Webhook 請求成功")
            print("💡 請檢查 Flask 應用日誌是否有以下記錄:")
            print("   - '收到訊息'")
            print("   - 'Received message from test_user_123: 開始'")
            print("   - '[DEBUG] 開始指令'")
        else:
            print(f"❌ Webhook 請求失敗: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 請求失敗: {e}")

def test_other_commands():
    """測試其他命令"""
    print("\n" + "=" * 50)
    print("🧪 測試其他命令...")
    
    webhook_url = "http://127.0.0.1:5001/callback"
    
    # 測試"積分"命令
    webhook_data = {
        "events": [
            {
                "type": "message",
                "mode": "active",
                "timestamp": int(time.time() * 1000),
                "source": {
                    "type": "user",
                    "userId": "test_user_123"
                },
                "webhookEventId": "test_webhook_id_2",
                "deliveryContext": {
                    "isRedelivery": False
                },
                "replyToken": "test_reply_token_456",
                "message": {
                    "id": "test_message_id_456",
                    "type": "text",
                    "text": "積分"
                }
            }
        ],
        "destination": "test_destination"
    }
    
    headers = {
        "Content-Type": "application/json",
        "X-Line-Signature": "test_signature"
    }
    
    try:
        print("📤 測試「積分」命令...")
        response = requests.post(
            webhook_url,
            json=webhook_data,
            headers=headers,
            timeout=10
        )
        
        print(f"📥 收到回應: {response.status_code}")
        if response.status_code == 200:
            print("✅ 積分命令測試成功")
        else:
            print(f"❌ 積分命令測試失敗: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 積分命令測試失敗: {e}")

if __name__ == "__main__":
    test_start_command_detailed()
    test_other_commands() 
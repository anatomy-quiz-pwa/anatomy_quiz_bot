#!/usr/bin/env python3
import requests
import json

def test_webhook():
    """直接測試 webhook 端點"""
    url = "http://localhost:5001/callback"
    
    # 模擬 LINE 的 webhook 請求
    headers = {
        'Content-Type': 'application/json',
        'X-Line-Signature': 'test_signature'
    }
    
    # 模擬 "開始" 訊息的 webhook 事件
    webhook_data = {
        "events": [
            {
                "type": "message",
                "mode": "active",
                "timestamp": 1234567890,
                "source": {
                    "type": "user",
                    "userId": "test_user_123"
                },
                "webhookEventId": "test_event_id",
                "deliveryContext": {
                    "isRedelivery": False
                },
                "replyToken": "test_reply_token",
                "message": {
                    "id": "test_message_id",
                    "type": "text",
                    "text": "開始"
                }
            }
        ],
        "destination": "test_destination"
    }
    
    try:
        print("發送測試 webhook 請求...")
        response = requests.post(url, headers=headers, json=webhook_data)
        print(f"狀態碼: {response.status_code}")
        print(f"回應內容: {response.text}")
        
        if response.status_code == 200:
            print("✅ Webhook 端點正常回應")
        else:
            print("❌ Webhook 端點回應異常")
            
    except Exception as e:
        print(f"❌ 請求失敗: {str(e)}")

if __name__ == "__main__":
    test_webhook() 
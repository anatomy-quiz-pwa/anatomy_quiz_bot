#!/usr/bin/env python3
import requests
import json

def test_webhook():
    """測試 webhook 是否正常工作"""
    url = "http://localhost:5001/callback"
    
    # 模擬 LINE 的 MessageEvent
    webhook_data = {
        "events": [
            {
                "type": "message",
                "message": {
                    "type": "text",
                    "text": "開始"
                },
                "replyToken": "test_reply_token_123",
                "source": {
                    "userId": "test_user_123",
                    "type": "user"
                }
            }
        ]
    }
    
    headers = {
        'Content-Type': 'application/json',
        'X-Line-Signature': 'test_signature'
    }
    
    try:
        response = requests.post(url, json=webhook_data, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("測試 webhook...")
    success = test_webhook()
    print(f"測試結果: {'成功' if success else '失敗'}") 
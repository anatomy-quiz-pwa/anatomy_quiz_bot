#!/usr/bin/env python3
import requests
import json
import hmac
import hashlib
import base64

def generate_signature(body, channel_secret):
    """生成 LINE webhook 簽名"""
    hash = hmac.new(
        channel_secret.encode('utf-8'),
        body.encode('utf-8'),
        hashlib.sha256
    ).digest()
    signature = base64.b64encode(hash).decode('utf-8')
    return signature

def test_no_continue_menu():
    """測試答題後不會自動跳出「繼續每日問答」選單"""
    url = "http://localhost:5001/callback"
    
    # 從環境變數獲取 channel secret
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    channel_secret = os.getenv('LINE_CHANNEL_SECRET', '')
    if not channel_secret:
        print("❌ LINE_CHANNEL_SECRET 未設定")
        return
    
    print("🧪 測試答題後不會自動跳出「繼續每日問答」選單...")
    
    # 1. 發送「開始」指令
    print("1️⃣ 發送「開始」指令...")
    start_data = {
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
                "replyToken": "test_reply_token_start",
                "message": {
                    "id": "test_message_id",
                    "type": "text",
                    "quoteToken": "test_quote_token",
                    "text": "開始"
                }
            }
        ]
    }
    
    body = json.dumps(start_data)
    signature = generate_signature(body, channel_secret)
    
    headers = {
        'Content-Type': 'application/json',
        'X-Line-Signature': signature
    }
    
    response = requests.post(url, data=body, headers=headers)
    print(f"開始指令回應: {response.status_code}")
    
    # 等待一下
    import time
    time.sleep(2)
    
    # 2. 發送答案（假設選 A）
    print("2️⃣ 發送答案（選 A）...")
    answer_data = {
        "events": [
            {
                "type": "postback",
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
                "replyToken": "test_reply_token_answer",
                "postback": {
                    "data": "answer_0"
                }
            }
        ]
    }
    
    body = json.dumps(answer_data)
    signature = generate_signature(body, channel_secret)
    
    headers = {
        'Content-Type': 'application/json',
        'X-Line-Signature': signature
    }
    
    response = requests.post(url, data=body, headers=headers)
    print(f"答案回應: {response.status_code}")
    
    # 等待一下
    time.sleep(2)
    
    # 3. 發送任意訊息，檢查是否會自動推送選單
    print("3️⃣ 發送任意訊息，檢查是否會自動推送選單...")
    message_data = {
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
                "replyToken": "test_reply_token_message",
                "message": {
                    "id": "test_message_id",
                    "type": "text",
                    "quoteToken": "test_quote_token",
                    "text": "測試訊息"
                }
            }
        ]
    }
    
    body = json.dumps(message_data)
    signature = generate_signature(body, channel_secret)
    
    headers = {
        'Content-Type': 'application/json',
        'X-Line-Signature': signature
    }
    
    response = requests.post(url, data=body, headers=headers)
    print(f"任意訊息回應: {response.status_code}")
    
    print("✅ 測試完成！")
    print("📝 請檢查 Flask 日誌，確認：")
    print("   - 答題後只顯示結果和補充說明")
    print("   - 不會自動推送「繼續每日問答」選單")
    print("   - 對任意訊息只回覆簡單提示，不推送選單")

if __name__ == "__main__":
    test_no_continue_menu() 
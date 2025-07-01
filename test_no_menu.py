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

def test_no_menu_after_answer():
    """測試答題後不會自動跳出選單"""
    url = "http://localhost:5001/callback"
    
    # 從環境變數獲取 channel secret
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    channel_secret = os.getenv('LINE_CHANNEL_SECRET', '')
    if not channel_secret:
        print("❌ LINE_CHANNEL_SECRET 未設定")
        return
    
    print("🧪 測試答題後不會自動跳出選單...")
    
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
                    "text": "開始"
                }
            }
        ]
    }
    
    start_body = json.dumps(start_data)
    start_signature = generate_signature(start_body, channel_secret)
    
    start_headers = {
        'Content-Type': 'application/json',
        'X-Line-Signature': start_signature
    }
    
    start_response = requests.post(url, data=start_body, headers=start_headers)
    print(f"開始指令回應: {start_response.status_code}")
    
    import time
    time.sleep(2)
    
    # 2. 發送答案（假設選項 1）
    print("2️⃣ 發送答案（選項 1）...")
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
                    "data": "answer_1"
                }
            }
        ]
    }
    
    answer_body = json.dumps(answer_data)
    answer_signature = generate_signature(answer_body, channel_secret)
    
    answer_headers = {
        'Content-Type': 'application/json',
        'X-Line-Signature': answer_signature
    }
    
    answer_response = requests.post(url, data=answer_body, headers=answer_headers)
    print(f"答案回應: {answer_response.status_code}")
    
    time.sleep(2)
    
    # 3. 發送任意訊息，檢查是否會自動跳出選單
    print("3️⃣ 發送任意訊息，檢查是否會自動跳出選單...")
    random_data = {
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
                "replyToken": "test_reply_token_random",
                "message": {
                    "id": "test_message_id",
                    "type": "text",
                    "text": "測試訊息"
                }
            }
        ]
    }
    
    random_body = json.dumps(random_data)
    random_signature = generate_signature(random_body, channel_secret)
    
    random_headers = {
        'Content-Type': 'application/json',
        'X-Line-Signature': random_signature
    }
    
    random_response = requests.post(url, data=random_body, headers=random_headers)
    print(f"任意訊息回應: {random_response.status_code}")
    
    print("✅ 測試完成！請檢查 Flask 日誌確認行為。")

if __name__ == "__main__":
    test_no_menu_after_answer() 
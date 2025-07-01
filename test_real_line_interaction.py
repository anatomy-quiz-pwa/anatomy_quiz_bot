#!/usr/bin/env python3
import requests
import json
import time
from datetime import datetime

def test_line_interaction():
    """測試真實的 LINE 互動"""
    webhook_url = "http://localhost:5001/callback"
    
    # 你的真實 user_id
    user_id = "U977c24d1fec3a2bf07035504e1444911"
    
    print("🔧 開始測試 LINE 互動...")
    print(f"📡 Webhook URL: {webhook_url}")
    print(f"👤 User ID: {user_id}")
    print("-" * 50)
    
    # 測試 1: 發送 "開始" 指令
    print("1️⃣ 測試發送 '開始' 指令...")
    start_event = {
        "events": [{
            "type": "message",
            "mode": "active",
            "timestamp": int(time.time() * 1000),
            "source": {
                "type": "user",
                "userId": user_id
            },
            "webhookEventId": "test_start_001",
            "deliveryContext": {
                "isRedelivery": False
            },
            "replyToken": "test_reply_token_start",
            "message": {
                "id": "test_message_start",
                "type": "text",
                "quoteToken": "test_quote_token",
                "text": "開始"
            }
        }]
    }
    
    try:
        response = requests.post(
            webhook_url,
            json=start_event,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        print(f"✅ 開始指令回應: {response.status_code}")
        print(f"📄 回應內容: {response.text}")
    except Exception as e:
        print(f"❌ 開始指令失敗: {e}")
    
    print("-" * 50)
    
    # 等待一下讓 bot 處理
    time.sleep(2)
    
    # 測試 2: 發送答案 (假設問題 ID 為 1，選擇選項 0)
    print("2️⃣ 測試發送答案...")
    answer_event = {
        "events": [{
            "type": "postback",
            "mode": "active",
            "timestamp": int(time.time() * 1000),
            "source": {
                "type": "user",
                "userId": user_id
            },
            "webhookEventId": "test_answer_001",
            "deliveryContext": {
                "isRedelivery": False
            },
            "replyToken": "test_reply_token_answer",
            "postback": {
                "data": "answer=0&qid=1"
            }
        }]
    }
    
    try:
        response = requests.post(
            webhook_url,
            json=answer_event,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        print(f"✅ 答案回應: {response.status_code}")
        print(f"📄 回應內容: {response.text}")
    except Exception as e:
        print(f"❌ 答案失敗: {e}")
    
    print("-" * 50)
    
    # 測試 3: 查詢積分
    print("3️⃣ 測試查詢積分...")
    score_event = {
        "events": [{
            "type": "message",
            "mode": "active",
            "timestamp": int(time.time() * 1000),
            "source": {
                "type": "user",
                "userId": user_id
            },
            "webhookEventId": "test_score_001",
            "deliveryContext": {
                "isRedelivery": False
            },
            "replyToken": "test_reply_token_score",
            "message": {
                "id": "test_message_score",
                "type": "text",
                "quoteToken": "test_quote_token",
                "text": "積分"
            }
        }]
    }
    
    try:
        response = requests.post(
            webhook_url,
            json=score_event,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        print(f"✅ 積分查詢回應: {response.status_code}")
        print(f"📄 回應內容: {response.text}")
    except Exception as e:
        print(f"❌ 積分查詢失敗: {e}")
    
    print("-" * 50)
    print("🎉 測試完成！")

if __name__ == "__main__":
    test_line_interaction() 
#!/usr/bin/env python3
"""
本地測試 LINE Bot webhook 功能
模擬 LINE 的 webhook POST 請求
"""

import requests
import json
import time

# 測試用的用戶 ID - 請替換成你的真實 user_id
TEST_USER_ID = "U977c24d1fec3a2bf07035504e1444911"

def test_webhook_local():
    """測試本地 webhook 功能"""
    base_url = "http://localhost:5001"
    
    print("=== 開始測試 LINE Bot webhook 功能 ===")
    
    # 1. 測試「我的ID」指令
    print("\n1. 測試「我的ID」指令...")
    payload = {
        "events": [{
            "type": "message",
            "message": {
                "type": "text",
                "text": "我的ID"
            },
            "replyToken": "test_reply_token_1",
            "source": {
                "type": "user",
                "userId": TEST_USER_ID
            }
        }]
    }
    
    response = requests.post(f"{base_url}/callback", json=payload)
    print(f"狀態碼: {response.status_code}")
    print(f"回應: {response.text}")
    
    time.sleep(2)
    
    # 2. 測試「積分」指令
    print("\n2. 測試「積分」指令...")
    payload = {
        "events": [{
            "type": "message",
            "message": {
                "type": "text",
                "text": "積分"
            },
            "replyToken": "test_reply_token_2",
            "source": {
                "type": "user",
                "userId": TEST_USER_ID
            }
        }]
    }
    
    response = requests.post(f"{base_url}/callback", json=payload)
    print(f"狀態碼: {response.status_code}")
    print(f"回應: {response.text}")
    
    time.sleep(2)
    
    # 3. 測試「開始」指令
    print("\n3. 測試「開始」指令...")
    payload = {
        "events": [{
            "type": "message",
            "message": {
                "type": "text",
                "text": "開始"
            },
            "replyToken": "test_reply_token_3",
            "source": {
                "type": "user",
                "userId": TEST_USER_ID
            }
        }]
    }
    
    response = requests.post(f"{base_url}/callback", json=payload)
    print(f"狀態碼: {response.status_code}")
    print(f"回應: {response.text}")
    
    time.sleep(3)  # 等待更長時間，因為會發送兩條訊息
    
    # 4. 測試回答第一題（假設選擇選項 1）
    print("\n4. 測試回答第一題（選項 1）...")
    payload = {
        "events": [{
            "type": "postback",
            "postback": {
                "data": "answer_1"
            },
            "replyToken": "test_reply_token_4",
            "source": {
                "type": "user",
                "userId": TEST_USER_ID
            }
        }]
    }
    
    response = requests.post(f"{base_url}/callback", json=payload)
    print(f"狀態碼: {response.status_code}")
    print(f"回應: {response.text}")
    
    time.sleep(3)  # 等待更長時間，因為會發送結果訊息和下一題
    
    # 5. 測試回答第二題（假設選擇選項 2）
    print("\n5. 測試回答第二題（選項 2）...")
    payload = {
        "events": [{
            "type": "postback",
            "postback": {
                "data": "answer_2"
            },
            "replyToken": "test_reply_token_5",
            "source": {
                "type": "user",
                "userId": TEST_USER_ID
            }
        }]
    }
    
    response = requests.post(f"{base_url}/callback", json=payload)
    print(f"狀態碼: {response.status_code}")
    print(f"回應: {response.text}")
    
    print("\n=== 測試完成 ===")
    print("請檢查 Flask 應用程式的日誌，查看是否有錯誤訊息")
    print("同時檢查 Supabase 中的 user_stats 表，確認積分是否正確更新")

if __name__ == "__main__":
    test_webhook_local() 
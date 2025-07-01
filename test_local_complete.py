#!/usr/bin/env python3
"""
完整的本地測試腳本
模擬 LINE Bot 的完整流程，不發送實際訊息到 LINE
"""

import requests
import json
import time
import sys
import os

# 添加當前目錄到 Python 路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_webhook_without_line_api():
    """測試 webhook 處理邏輯，但不發送 LINE 訊息"""
    
    # 模擬 LINE webhook 的 POST 請求
    webhook_url = "http://127.0.0.1:5001/callback"
    
    test_cases = [
        {
            "name": "開始指令",
            "data": {
                "events": [
                    {
                        "type": "message",
                        "mode": "active",
                        "timestamp": 1234567890,
                        "source": {
                            "type": "user",
                            "userId": "U977c24d1fec3a2bf07035504e1444911"
                        },
                        "webhookEventId": "test_event_id_1",
                        "deliveryContext": {
                            "isRedelivery": False
                        },
                        "replyToken": "test_reply_token_1",
                        "message": {
                            "id": "test_message_id_1",
                            "type": "text",
                            "text": "開始"
                        }
                    }
                ],
                "destination": "test_destination"
            }
        },
        {
            "name": "積分查詢",
            "data": {
                "events": [
                    {
                        "type": "message",
                        "mode": "active",
                        "timestamp": 1234567890,
                        "source": {
                            "type": "user",
                            "userId": "U977c24d1fec3a2bf07035504e1444911"
                        },
                        "webhookEventId": "test_event_id_2",
                        "deliveryContext": {
                            "isRedelivery": False
                        },
                        "replyToken": "test_reply_token_2",
                        "message": {
                            "id": "test_message_id_2",
                            "type": "text",
                            "text": "積分"
                        }
                    }
                ],
                "destination": "test_destination"
            }
        },
        {
            "name": "我的ID",
            "data": {
                "events": [
                    {
                        "type": "message",
                        "mode": "active",
                        "timestamp": 1234567890,
                        "source": {
                            "type": "user",
                            "userId": "U977c24d1fec3a2bf07035504e1444911"
                        },
                        "webhookEventId": "test_event_id_3",
                        "deliveryContext": {
                            "isRedelivery": False
                        },
                        "replyToken": "test_reply_token_3",
                        "message": {
                            "id": "test_message_id_3",
                            "type": "text",
                            "text": "我的ID"
                        }
                    }
                ],
                "destination": "test_destination"
            }
        }
    ]
    
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'LINE-BotSDK-Python/3.17.1'
    }
    
    print("🧪 開始本地完整測試")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 測試 {i}: {test_case['name']}")
        print("-" * 40)
        
        try:
            response = requests.post(
                webhook_url,
                json=test_case['data'],
                headers=headers,
                timeout=10
            )
            
            print(f"📤 請求: {test_case['name']}")
            print(f"📥 回應狀態碼: {response.status_code}")
            print(f"📥 回應內容: {response.text}")
            
            if response.status_code == 200:
                print("✅ 測試成功")
            else:
                print("❌ 測試失敗")
                
        except Exception as e:
            print(f"❌ 請求發生錯誤: {e}")
        
        # 等待一下再進行下一個測試
        time.sleep(1)
    
    print("\n" + "=" * 60)
    print("🎯 本地測試完成！")
    print("💡 請檢查 Flask log 是否有以下訊息：")
    print("   - 收到訊息")
    print("   - [DEBUG] 收到 MessageEvent")
    print("   - [DEBUG] 開始指令 - user_id: ...")
    print("   - [DEBUG] 積分查詢 - user_id: ...")
    print("   - 資料庫查詢相關 log")

def test_answer_flow():
    """測試答題流程"""
    
    webhook_url = "http://127.0.0.1:5001/callback"
    
    # 1. 先發送「開始」指令
    start_data = {
        "events": [
            {
                "type": "message",
                "mode": "active",
                "timestamp": 1234567890,
                "source": {
                    "type": "user",
                    "userId": "U977c24d1fec3a2bf07035504e1444911"
                },
                "webhookEventId": "test_start_event",
                "deliveryContext": {
                    "isRedelivery": False
                },
                "replyToken": "test_start_reply_token",
                "message": {
                    "id": "test_start_message",
                    "type": "text",
                    "text": "開始"
                }
            }
        ],
        "destination": "test_destination"
    }
    
    # 2. 模擬選擇答案 1
    answer_data = {
        "events": [
            {
                "type": "postback",
                "mode": "active",
                "timestamp": 1234567890,
                "source": {
                    "type": "user",
                    "userId": "U977c24d1fec3a2bf07035504e1444911"
                },
                "webhookEventId": "test_answer_event",
                "deliveryContext": {
                    "isRedelivery": False
                },
                "replyToken": "test_answer_reply_token",
                "postback": {
                    "data": "answer_1"
                }
            }
        ],
        "destination": "test_destination"
    }
    
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'LINE-BotSDK-Python/3.17.1'
    }
    
    print("\n🎯 測試答題流程")
    print("=" * 60)
    
    # 測試開始指令
    print("\n📝 步驟 1: 發送「開始」指令")
    try:
        response = requests.post(webhook_url, json=start_data, headers=headers, timeout=10)
        print(f"📥 回應: {response.status_code} - {response.text}")
        time.sleep(2)
    except Exception as e:
        print(f"❌ 錯誤: {e}")
    
    # 測試答案選擇
    print("\n📝 步驟 2: 選擇答案 1")
    try:
        response = requests.post(webhook_url, json=answer_data, headers=headers, timeout=10)
        print(f"📥 回應: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ 錯誤: {e}")
    
    print("\n💡 請檢查 Flask log 是否有：")
    print("   - 收到 PostbackEvent")
    print("   - [DEBUG] 處理答案: answer_1")
    print("   - 資料庫更新相關 log")

if __name__ == "__main__":
    print("🚀 LINE Bot 本地完整測試工具")
    print("=" * 60)
    
    # 檢查 Flask 是否運行
    try:
        response = requests.get("http://127.0.0.1:5001/", timeout=5)
        if response.status_code == 200:
            print("✅ Flask 服務正在運行")
        else:
            print("❌ Flask 服務回應異常")
            sys.exit(1)
    except Exception as e:
        print("❌ Flask 服務未運行，請先啟動 Flask 應用")
        print("   執行: source venv311/bin/activate && PORT=5001 python app_supabase.py")
        sys.exit(1)
    
    # 執行測試
    test_webhook_without_line_api()
    test_answer_flow()
    
    print("\n🎉 所有測試完成！")
    print("📋 請查看 Flask log 確認功能是否正常運作") 
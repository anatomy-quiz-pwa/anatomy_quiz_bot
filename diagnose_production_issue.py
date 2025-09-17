#!/usr/bin/env python3
"""
診斷生產環境問題
"""

import requests
import json
import time

def test_webhook_with_detailed_logging():
    """測試 webhook 並記錄詳細日誌"""
    
    webhook_url = "https://anatomy-quiz-bot.onrender.com/webhook"
    
    # 測試不同的訊息
    test_messages = [
        "排行榜",
        "開始",
        "help"
    ]
    
    for i, message in enumerate(test_messages):
        print(f"\n🧪 測試 {i+1}: 發送訊息 '{message}'")
        
        webhook_data = {
            "destination": "U4d7d1202c0f2546cf9e7110edcc503ea",
            "events": [
                {
                    "type": "message",
                    "message": {
                        "type": "text",
                        "id": f"test_message_{i}",
                        "text": message
                    },
                    "webhookEventId": f"test_event_{i}",
                    "deliveryContext": {
                        "isRedelivery": False
                    },
                    "timestamp": int(time.time() * 1000),
                    "source": {
                        "type": "user",
                        "userId": "U977c24d1fec3a2bf07035504e1444911"
                    },
                    "replyToken": f"test_token_{i}",
                    "mode": "active"
                }
            ]
        }
        
        headers = {
            "Content-Type": "application/json",
            "X-Line-Signature": "test_signature"
        }
        
        try:
            response = requests.post(webhook_url, json=webhook_data, headers=headers, timeout=30)
            
            print(f"  📊 狀態碼: {response.status_code}")
            print(f"  📊 響應頭: {dict(response.headers)}")
            print(f"  📊 響應內容: {response.text[:500]}...")
            
            if response.status_code == 200:
                print(f"  ✅ 訊息 '{message}' 處理成功")
            else:
                print(f"  ❌ 訊息 '{message}' 處理失敗")
                
        except Exception as e:
            print(f"  ❌ 請求失敗: {e}")
        
        # 等待一下再發送下一個請求
        time.sleep(2)

def test_health_check():
    """測試健康檢查"""
    try:
        print("\n🏥 測試健康檢查...")
        response = requests.get("https://anatomy-quiz-bot.onrender.com/", timeout=10)
        print(f"  📊 狀態碼: {response.status_code}")
        print(f"  📊 響應內容: {response.text[:200]}...")
        
        if response.status_code == 200:
            print("  ✅ 服務正常運行")
        else:
            print("  ❌ 服務異常")
            
    except Exception as e:
        print(f"  ❌ 健康檢查失敗: {e}")

def main():
    """主函數"""
    print("🔧 診斷生產環境問題...")
    
    # 1. 健康檢查
    test_health_check()
    
    # 2. 測試 webhook
    test_webhook_with_detailed_logging()
    
    print("\n📋 診斷完成")

if __name__ == "__main__":
    main()

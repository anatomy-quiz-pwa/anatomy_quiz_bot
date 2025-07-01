#!/usr/bin/env python3
"""
簡單的 webhook 測試
"""

import sys
import os
import requests
import json
import time

def test_simple_webhook():
    """測試簡單的 webhook 請求"""
    
    # 模擬用戶發送"開始"訊息
    webhook_data = {
        "events": [
            {
                "type": "message",
                "message": {
                    "type": "text",
                    "text": "開始"
                },
                "replyToken": "test_reply_token_simple",
                "source": {
                    "userId": "U1234567890abcdef1234567890abcdef",
                    "type": "user"
                },
                "timestamp": int(time.time() * 1000)
            }
        ]
    }
    
    try:
        print("🧪 測試簡單 webhook...")
        print("📤 發送 webhook 到 Flask 應用...")
        
        # 發送 webhook 到本地應用程式，不帶簽名
        response = requests.post(
            "http://localhost:5001/callback",
            headers={
                "Content-Type": "application/json"
            },
            data=json.dumps(webhook_data)
        )
        
        print(f"📥 回應狀態碼: {response.status_code}")
        print(f"📥 回應內容: {response.text}")
        
        if response.status_code == 200:
            print("✅ 測試成功！")
            print("💡 請查看 Flask 應用的控制台輸出")
        else:
            print("❌ 測試失敗")
            
    except Exception as e:
        print(f"❌ 錯誤: {e}")

if __name__ == "__main__":
    test_simple_webhook() 
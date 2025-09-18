#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
測試積分指令的webhook處理
"""

import json
import requests
import time
from datetime import datetime

def test_webhook_score_command():
    """測試積分指令的webhook處理"""
    print("🧪 測試積分指令的webhook處理")
    print("=" * 60)
    
    # 測試用戶ID (寶的測試帳號)
    test_user_id = "U977c24d1fec3a2bf07035504e1444911"
    
    # 模擬LINE webhook的訊息格式
    webhook_data = {
        "events": [
            {
                "type": "message",
                "message": {
                    "type": "text",
                    "text": "積分"
                },
                "source": {
                    "type": "user",
                    "userId": test_user_id
                },
                "timestamp": int(time.time() * 1000),
                "replyToken": "test_reply_token_" + str(int(time.time()))
            }
        ]
    }
    
    print(f"🎯 測試用戶ID: {test_user_id}")
    print(f"📝 測試訊息: '積分'")
    print(f"⏰ 時間戳: {datetime.now().isoformat()}")
    
    # 本地測試URL
    webhook_url = "http://localhost:5000/webhook"
    
    print(f"\n📡 發送webhook請求到: {webhook_url}")
    print("📦 請求數據:")
    print(json.dumps(webhook_data, indent=2, ensure_ascii=False))
    
    try:
        response = requests.post(
            webhook_url,
            json=webhook_data,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "LineBotWebhook/1.0"
            },
            timeout=30
        )
        
        print(f"\n📊 響應狀態: {response.status_code}")
        print(f"📊 響應頭: {dict(response.headers)}")
        
        if response.text:
            print(f"📊 響應內容: {response.text}")
        
        if response.status_code == 200:
            print("✅ Webhook請求成功")
        else:
            print(f"❌ Webhook請求失敗: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 連接失敗: 本地服務器可能沒有運行")
        print("💡 請確保在另一個終端運行: python app_supabase.py")
    except requests.exceptions.Timeout:
        print("❌ 請求超時")
    except Exception as e:
        print(f"❌ 請求異常: {e}")
    
    print("\n" + "=" * 60)
    print("🔍 測試建議:")
    print("1. 確保本地服務器運行: python app_supabase.py")
    print("2. 檢查webhook URL是否正確")
    print("3. 檢查LINE Bot設定")
    print("4. 查看app.log日誌輸出")

def main():
    """主函數"""
    print("🚀 開始測試積分指令的webhook處理")
    print(f"⏰ 測試時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    test_webhook_score_command()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
測試生產環境修復
"""

import requests
import json

def test_leaderboard_webhook():
    """測試排行榜 webhook"""
    
    # 模擬 LINE webhook 請求
    webhook_url = "https://anatomy-quiz-bot.onrender.com/webhook"
    
    # 模擬真實的 LINE webhook 數據
    webhook_data = {
        "destination": "U4d7d1202c0f2546cf9e7110edcc503ea",
        "events": [
            {
                "type": "message",
                "message": {
                    "type": "text",
                    "id": "578787994795507764",
                    "text": "排行榜"
                },
                "webhookEventId": "01K52ZT07FRVEZDJ25R51G4N9X",
                "deliveryContext": {
                    "isRedelivery": False
                },
                "timestamp": 1757815832308,
                "source": {
                    "type": "user",
                    "userId": "U977c24d1fec3a2bf07035504e1444911"
                },
                "replyToken": "9e0c6cf865e8480a94d476ddd8122965",
                "mode": "active"
            }
        ]
    }
    
    headers = {
        "Content-Type": "application/json",
        "X-Line-Signature": "test_signature"
    }
    
    try:
        print("🧪 正在測試生產環境排行榜功能...")
        response = requests.post(webhook_url, json=webhook_data, headers=headers, timeout=30)
        
        print(f"📊 響應狀態碼: {response.status_code}")
        print(f"📊 響應內容: {response.text}")
        
        if response.status_code == 200:
            print("✅ 生產環境排行榜功能正常")
            return True
        else:
            print("❌ 生產環境排行榜功能異常")
            return False
            
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        return False

def main():
    """主函數"""
    print("🔧 測試生產環境排行榜修復...")
    
    success = test_leaderboard_webhook()
    
    if success:
        print("🎉 修復成功！請在 LINE Bot 中測試輸入「排行榜」")
    else:
        print("❌ 修復失敗，需要進一步檢查")
    
    return success

if __name__ == "__main__":
    main()

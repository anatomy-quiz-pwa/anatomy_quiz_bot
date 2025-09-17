#!/usr/bin/env python3
"""
深度診斷生產環境問題
"""

import requests
import json
import time

def test_production_health():
    """測試生產環境健康狀況"""
    print("🏥 測試生產環境健康狀況...")
    
    try:
        # 測試根路徑
        response = requests.get("https://anatomy-quiz-bot.onrender.com/", timeout=10)
        print(f"  📊 根路徑狀態碼: {response.status_code}")
        print(f"  📊 根路徑響應: {response.text}")
        
        # 測試 webhook 路徑
        response = requests.get("https://anatomy-quiz-bot.onrender.com/webhook", timeout=10)
        print(f"  📊 Webhook GET 狀態碼: {response.status_code}")
        print(f"  📊 Webhook GET 響應: {response.text}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 健康檢查失敗: {e}")
        return False

def test_webhook_with_minimal_payload():
    """測試 webhook 最小負載"""
    print("\n🧪 測試 webhook 最小負載...")
    
    webhook_url = "https://anatomy-quiz-bot.onrender.com/webhook"
    
    # 最小負載測試
    minimal_payload = {
        "events": []
    }
    
    headers = {
        "Content-Type": "application/json",
        "X-Line-Signature": "test_signature"
    }
    
    try:
        response = requests.post(webhook_url, json=minimal_payload, headers=headers, timeout=30)
        print(f"  📊 最小負載狀態碼: {response.status_code}")
        print(f"  📊 最小負載響應: {response.text}")
        
        if response.status_code == 200:
            print("  ✅ 最小負載測試成功")
            return True
        else:
            print("  ❌ 最小負載測試失敗")
            return False
            
    except Exception as e:
        print(f"  ❌ 最小負載測試失敗: {e}")
        return False

def test_webhook_with_simple_message():
    """測試 webhook 簡單訊息"""
    print("\n🧪 測試 webhook 簡單訊息...")
    
    webhook_url = "https://anatomy-quiz-bot.onrender.com/webhook"
    
    # 簡單訊息測試
    simple_payload = {
        "events": [
            {
                "type": "message",
                "message": {
                    "type": "text",
                    "text": "test"
                },
                "source": {
                    "type": "user",
                    "userId": "test_user"
                },
                "replyToken": "test_token"
            }
        ]
    }
    
    headers = {
        "Content-Type": "application/json",
        "X-Line-Signature": "test_signature"
    }
    
    try:
        response = requests.post(webhook_url, json=simple_payload, headers=headers, timeout=30)
        print(f"  📊 簡單訊息狀態碼: {response.status_code}")
        print(f"  📊 簡單訊息響應: {response.text}")
        
        if response.status_code == 200:
            print("  ✅ 簡單訊息測試成功")
            return True
        else:
            print("  ❌ 簡單訊息測試失敗")
            return False
            
    except Exception as e:
        print(f"  ❌ 簡單訊息測試失敗: {e}")
        return False

def test_webhook_with_leaderboard_message():
    """測試 webhook 排行榜訊息"""
    print("\n🧪 測試 webhook 排行榜訊息...")
    
    webhook_url = "https://anatomy-quiz-bot.onrender.com/webhook"
    
    # 排行榜訊息測試
    leaderboard_payload = {
        "events": [
            {
                "type": "message",
                "message": {
                    "type": "text",
                    "text": "排行榜"
                },
                "source": {
                    "type": "user",
                    "userId": "U977c24d1fec3a2bf07035504e1444911"
                },
                "replyToken": "test_leaderboard_token"
            }
        ]
    }
    
    headers = {
        "Content-Type": "application/json",
        "X-Line-Signature": "test_signature"
    }
    
    try:
        response = requests.post(webhook_url, json=leaderboard_payload, headers=headers, timeout=30)
        print(f"  📊 排行榜訊息狀態碼: {response.status_code}")
        print(f"  📊 排行榜訊息響應: {response.text}")
        
        if response.status_code == 200:
            print("  ✅ 排行榜訊息測試成功")
            return True
        else:
            print("  ❌ 排行榜訊息測試失敗")
            return False
            
    except Exception as e:
        print(f"  ❌ 排行榜訊息測試失敗: {e}")
        return False

def main():
    """主函數"""
    print("🔧 深度診斷生產環境問題...")
    
    # 1. 健康檢查
    health_ok = test_production_health()
    
    # 2. 最小負載測試
    minimal_ok = test_webhook_with_minimal_payload()
    
    # 3. 簡單訊息測試
    simple_ok = test_webhook_with_simple_message()
    
    # 4. 排行榜訊息測試
    leaderboard_ok = test_webhook_with_leaderboard_message()
    
    print("\n📋 診斷結果:")
    print(f"  🏥 健康檢查: {'✅' if health_ok else '❌'}")
    print(f"  🧪 最小負載: {'✅' if minimal_ok else '❌'}")
    print(f"  🧪 簡單訊息: {'✅' if simple_ok else '❌'}")
    print(f"  🧪 排行榜訊息: {'✅' if leaderboard_ok else '❌'}")
    
    if all([health_ok, minimal_ok, simple_ok, leaderboard_ok]):
        print("\n🎉 所有測試通過！生產環境正常運行")
    else:
        print("\n❌ 部分測試失敗，需要進一步檢查")

if __name__ == "__main__":
    main()

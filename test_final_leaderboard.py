#!/usr/bin/env python3
"""
最終排行榜功能測試
"""

import requests
import json
import time

def test_local_leaderboard():
    """測試本地排行榜功能"""
    print("🧪 測試本地排行榜功能...")
    
    webhook_data = {
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
    
    try:
        response = requests.post("http://localhost:5002/webhook", 
                               json=webhook_data, 
                               headers={"Content-Type": "application/json"}, 
                               timeout=10)
        
        print(f"  📊 本地測試狀態碼: {response.status_code}")
        print(f"  📊 本地測試響應: {response.text}")
        
        if response.status_code == 200:
            print("  ✅ 本地排行榜功能正常")
            return True
        else:
            print("  ❌ 本地排行榜功能異常")
            return False
            
    except Exception as e:
        print(f"  ❌ 本地測試失敗: {e}")
        return False

def test_production_leaderboard():
    """測試生產環境排行榜功能"""
    print("\n🧪 測試生產環境排行榜功能...")
    
    webhook_data = {
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
                "replyToken": "test_production_token"
            }
        ]
    }
    
    try:
        response = requests.post("https://anatomy-quiz-bot.onrender.com/webhook", 
                               json=webhook_data, 
                               headers={"Content-Type": "application/json"}, 
                               timeout=30)
        
        print(f"  📊 生產環境狀態碼: {response.status_code}")
        print(f"  📊 生產環境響應: {response.text}")
        
        if response.status_code == 200:
            print("  ✅ 生產環境排行榜功能正常")
            return True
        else:
            print("  ❌ 生產環境排行榜功能異常")
            return False
            
    except Exception as e:
        print(f"  ❌ 生產環境測試失敗: {e}")
        return False

def main():
    """主函數"""
    print("🎯 最終排行榜功能測試...")
    
    # 測試本地功能
    local_ok = test_local_leaderboard()
    
    # 測試生產環境
    production_ok = test_production_leaderboard()
    
    print("\n📋 測試結果:")
    print(f"  🏠 本地環境: {'✅ 正常' if local_ok else '❌ 異常'}")
    print(f"  🌐 生產環境: {'✅ 正常' if production_ok else '❌ 異常'}")
    
    if local_ok and production_ok:
        print("\n🎉 所有測試通過！排行榜功能完全正常！")
    elif local_ok:
        print("\n⚠️ 本地功能正常，但生產環境需要重啟")
        print("📋 請執行以下步驟重啟生產環境：")
        print("   cd /Users/baobaoc/Dev/anatomy_quiz_bot")
        print("   python app_supabase.py")
    else:
        print("\n❌ 需要進一步檢查問題")

if __name__ == "__main__":
    main()

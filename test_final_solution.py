#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試最終解決方案
"""

import requests
import json
import time

def test_final_solution():
    """測試最終解決方案"""
    print("🔍 測試最終解決方案...")
    
    webhook_url = "https://anatomy-quiz-bot.onrender.com/webhook"
    
    # 測試數據
    test_data = {
        "events": [
            {
                "type": "message",
                "source": {
                    "userId": "U977c24d1fec3a2bf07035504e1444911"
                },
                "message": {
                    "type": "text",
                    "text": "排行榜"
                }
            }
        ]
    }
    
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'LINE Bot SDK'
    }
    
    try:
        print(f"📤 發送請求到: {webhook_url}")
        print(f"📤 測試數據: {json.dumps(test_data, ensure_ascii=False, indent=2)}")
        
        response = requests.post(
            webhook_url, 
            json=test_data, 
            headers=headers, 
            timeout=30
        )
        
        print(f"📤 響應狀態碼: {response.status_code}")
        print(f"📤 響應內容: {response.text}")
        print(f"📤 響應標頭: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("🎉 最終解決方案成功！webhook 正常運作")
            return True
        elif response.status_code == 500:
            print("❌ 仍然返回 500 錯誤")
            return False
        else:
            print(f"⚠️ 返回狀態碼: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        return False

def test_different_keywords():
    """測試不同的關鍵字"""
    print("\n🔍 測試不同的關鍵字...")
    
    webhook_url = "https://anatomy-quiz-bot.onrender.com/webhook"
    keywords = ['排行榜', 'leaderboard', '排名', '排行']
    
    headers = {'Content-Type': 'application/json'}
    
    for keyword in keywords:
        print(f"\n📝 測試關鍵字: '{keyword}'")
        
        test_data = {
            "events": [
                {
                    "type": "message",
                    "source": {
                        "userId": "U977c24d1fec3a2bf07035504e1444911"
                    },
                    "message": {
                        "type": "text",
                        "text": keyword
                    }
                }
            ]
        }
        
        try:
            response = requests.post(
                webhook_url, 
                json=test_data, 
                headers=headers, 
                timeout=30
            )
            
            print(f"📤 狀態碼: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ 成功")
            else:
                print(f"❌ 失敗: {response.text}")
                
        except Exception as e:
            print(f"❌ 請求失敗: {e}")

def check_application_health():
    """檢查應用程式健康狀態"""
    print("\n🔍 檢查應用程式健康狀態...")
    
    base_url = "https://anatomy-quiz-bot.onrender.com"
    
    try:
        response = requests.get(base_url, timeout=10)
        print(f"📤 根路徑狀態碼: {response.status_code}")
        print(f"📤 根路徑響應: {response.text}")
        
        if response.status_code == 200:
            print("✅ 應用程式健康狀態正常")
            return True
        else:
            print(f"❌ 應用程式健康狀態異常: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 檢查應用程式健康狀態失敗: {e}")
        return False

def wait_for_deployment():
    """等待部署完成"""
    print("⏳ 等待部署完成...")
    print("💡 請確保您已經將最終解決方案上傳到 Render 並重新部署")
    
    for i in range(5):
        print(f"⏳ 等待中... ({i+1}/5)")
        time.sleep(10)
    
    print("✅ 等待完成，開始測試")

def main():
    """主函數"""
    print("🚀 測試最終解決方案")
    print("=" * 60)
    
    # 等待部署
    wait_for_deployment()
    
    # 檢查應用程式健康狀態
    health_ok = check_application_health()
    
    # 測試 webhook
    webhook_ok = test_final_solution()
    
    if webhook_ok:
        # 測試不同關鍵字
        test_different_keywords()
        
        print("\n" + "=" * 60)
        print("🎉 最終解決方案完全成功！")
        print("✅ 排行榜功能現在應該可以正常運作了")
        print("💡 用戶輸入「排行榜」、「leaderboard」、「排名」或「排行」都會收到文字訊息")
        print("📱 收到的文字訊息會顯示「🏆 排行榜功能正在測試中...請稍後再試！」")
        print("🔧 這證明了 webhook 基本功能正常，可以逐步添加更多功能")
    else:
        print("\n" + "=" * 60)
        print("❌ 最終解決方案失敗")
        print("💡 請檢查 Render 部署日誌中的具體錯誤信息")
        print("💡 建議檢查 Render 是否真的在使用我們的文件")

if __name__ == "__main__":
    main()

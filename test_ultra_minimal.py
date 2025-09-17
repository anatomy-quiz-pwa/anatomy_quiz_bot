#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試極簡版本
"""

import requests
import json
import time

def test_ultra_minimal():
    """測試極簡版本"""
    print("🔍 測試極簡版本...")
    
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
            print("🎉 極簡版本成功！webhook 基本功能正常")
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
    print("💡 請確保您已經將極簡版本上傳到 Render 並重新部署")
    
    for i in range(5):
        print(f"⏳ 等待中... ({i+1}/5)")
        time.sleep(10)
    
    print("✅ 等待完成，開始測試")

def main():
    """主函數"""
    print("🚀 測試極簡版本")
    print("=" * 60)
    
    # 等待部署
    wait_for_deployment()
    
    # 檢查應用程式健康狀態
    health_ok = check_application_health()
    
    # 測試 webhook
    webhook_ok = test_ultra_minimal()
    
    if webhook_ok:
        print("\n" + "=" * 60)
        print("🎉 極簡版本成功！")
        print("✅ webhook 基本功能現在正常運作了")
        print("💡 這證明了 FastAPI 應用程式可以在 Render 上正常運作")
        print("🔧 下一步可以逐步添加更多功能，如 LINE 訊息發送")
    else:
        print("\n" + "=" * 60)
        print("❌ 極簡版本失敗")
        print("💡 請檢查 Render 部署日誌中的具體錯誤信息")
        print("💡 建議檢查 Render 是否真的在使用我們的文件")

if __name__ == "__main__":
    main()

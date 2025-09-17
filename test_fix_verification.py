#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
驗證修復結果
"""

import requests
import json
import time

def test_webhook_after_fix():
    """測試修復後的 webhook"""
    print("🔍 測試修復後的 webhook...")
    
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
        
        if response.status_code == 200:
            print("✅ 修復成功！webhook 正常運作")
            return True
        elif response.status_code == 500:
            print("❌ 修復失敗，仍然返回 500 錯誤")
            return False
        else:
            print(f"⚠️ 返回狀態碼: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        return False

def test_basic_endpoints():
    """測試基本端點"""
    print("\n🔍 測試基本端點...")
    
    base_url = "https://anatomy-quiz-bot.onrender.com"
    
    try:
        # 測試根路徑
        response = requests.get(base_url, timeout=10)
        print(f"📤 根路徑狀態碼: {response.status_code}")
        print(f"📤 根路徑響應: {response.text}")
        
        if response.status_code == 200:
            print("✅ 應用程式正常運行")
            return True
        else:
            print(f"❌ 應用程式異常: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        return False

def wait_for_deployment():
    """等待部署完成"""
    print("⏳ 等待部署完成...")
    print("💡 請確保您已經將 Procfile 和 requirements.txt 上傳到 Render 並重新部署")
    
    for i in range(5):
        print(f"⏳ 等待中... ({i+1}/5)")
        time.sleep(10)
    
    print("✅ 等待完成，開始測試")

def main():
    """主函數"""
    print("🚀 開始驗證修復結果")
    print("=" * 60)
    
    # 等待部署
    wait_for_deployment()
    
    # 測試基本端點
    basic_ok = test_basic_endpoints()
    
    if basic_ok:
        # 測試 webhook
        webhook_ok = test_webhook_after_fix()
        
        print("\n" + "=" * 60)
        print("🏁 驗證完成")
        
        if webhook_ok:
            print("🎉 修復成功！排行榜功能應該可以正常運作了")
            print("💡 現在用戶輸入「排行榜」應該會收到 Flex Message")
        else:
            print("❌ 修復失敗，請檢查部署日誌")
    else:
        print("❌ 應用程式無法正常啟動，請檢查部署")

if __name__ == "__main__":
    main()

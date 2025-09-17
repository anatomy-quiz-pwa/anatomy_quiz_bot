#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
調試生產環境 webhook
"""

import requests
import json
import time

def test_webhook_with_detailed_logging():
    """測試 webhook 並記錄詳細日誌"""
    print("🔍 測試生產環境 webhook...")
    
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
        'User-Agent': 'LINE Bot SDK',
        'X-Line-Signature': 'test_signature'
    }
    
    try:
        print(f"📤 發送請求到: {webhook_url}")
        print(f"📤 請求標頭: {headers}")
        print(f"📤 請求數據: {json.dumps(test_data, ensure_ascii=False, indent=2)}")
        
        response = requests.post(
            webhook_url, 
            json=test_data, 
            headers=headers, 
            timeout=30
        )
        
        print(f"📤 響應狀態碼: {response.status_code}")
        print(f"📤 響應標頭: {dict(response.headers)}")
        print(f"📤 響應內容: {response.text}")
        
        if response.status_code == 200:
            print("✅ Webhook 正常運作")
            return True
        else:
            print(f"❌ Webhook 返回狀態碼: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        return False

def test_simple_webhook():
    """測試簡單的 webhook"""
    print("\n🔍 測試簡單的 webhook...")
    
    webhook_url = "https://anatomy-quiz-bot.onrender.com/webhook"
    
    # 最簡單的測試數據
    test_data = {
        "events": []
    }
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    try:
        print(f"📤 發送簡單請求到: {webhook_url}")
        
        response = requests.post(
            webhook_url, 
            json=test_data, 
            headers=headers, 
            timeout=30
        )
        
        print(f"📤 響應狀態碼: {response.status_code}")
        print(f"📤 響應內容: {response.text}")
        
        if response.status_code == 200:
            print("✅ 簡單 webhook 正常運作")
            return True
        else:
            print(f"❌ 簡單 webhook 返回狀態碼: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 簡單 webhook 測試失敗: {e}")
        return False

def test_get_webhook():
    """測試 GET webhook"""
    print("\n🔍 測試 GET webhook...")
    
    webhook_url = "https://anatomy-quiz-bot.onrender.com/webhook"
    
    try:
        print(f"📤 發送 GET 請求到: {webhook_url}")
        
        response = requests.get(webhook_url, timeout=10)
        
        print(f"📤 響應狀態碼: {response.status_code}")
        print(f"📤 響應內容: {response.text}")
        
        if response.status_code == 405:
            print("✅ GET webhook 返回 405 (預期)")
            return True
        else:
            print(f"⚠️ GET webhook 返回狀態碼: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ GET webhook 測試失敗: {e}")
        return False

def check_application_health():
    """檢查應用程式健康狀態"""
    print("\n🔍 檢查應用程式健康狀態...")
    
    base_url = "https://anatomy-quiz-bot.onrender.com"
    
    try:
        # 測試根路徑
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

def analyze_problem():
    """分析問題"""
    print("\n🔍 問題分析:")
    print("1. 應用程式已成功啟動 FastAPI 版本")
    print("2. 根路徑正常運作")
    print("3. 但 webhook 返回 500 錯誤")
    print("4. 可能的原因:")
    print("   - FastAPI 代碼中有錯誤")
    print("   - 環境變數問題")
    print("   - 依賴項問題")
    print("   - 數據庫連接問題")

def provide_solutions():
    """提供解決方案"""
    print("\n💡 解決方案:")
    print("1. 檢查 Render 部署日誌中的具體錯誤信息")
    print("2. 創建一個最簡單的 webhook 處理器進行測試")
    print("3. 檢查環境變數是否正確設置")
    print("4. 如果需要，回滾到 Flask 版本")

def main():
    """主函數"""
    print("🚀 調試生產環境 webhook")
    print("=" * 60)
    
    # 檢查應用程式健康狀態
    health_ok = check_application_health()
    
    # 測試 GET webhook
    get_ok = test_get_webhook()
    
    # 測試簡單的 webhook
    simple_ok = test_simple_webhook()
    
    # 測試完整的 webhook
    full_ok = test_webhook_with_detailed_logging()
    
    # 分析問題
    analyze_problem()
    
    # 提供解決方案
    provide_solutions()
    
    print("\n" + "=" * 60)
    if health_ok and get_ok and simple_ok and full_ok:
        print("✅ 所有測試通過")
    else:
        print("❌ 有測試失敗")
        print("💡 請檢查 Render 部署日誌中的具體錯誤信息")

if __name__ == "__main__":
    main()

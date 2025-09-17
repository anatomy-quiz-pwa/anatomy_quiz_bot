#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最終診斷
"""

import requests
import json
import time

def test_basic_webhook():
    """測試基本的 webhook"""
    print("🔍 測試基本的 webhook...")
    
    webhook_url = "https://anatomy-quiz-bot.onrender.com/webhook"
    
    # 最簡單的測試數據
    test_data = {
        "events": []
    }
    
    headers = {
        'Content-Type': 'application/json'
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
            print("✅ 基本 webhook 正常運作")
            return True
        else:
            print(f"❌ 基本 webhook 返回狀態碼: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
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
        print(f"❌ 測試失敗: {e}")
        return False

def test_root_endpoint():
    """測試根端點"""
    print("\n🔍 測試根端點...")
    
    base_url = "https://anatomy-quiz-bot.onrender.com"
    
    try:
        response = requests.get(base_url, timeout=10)
        print(f"📤 根路徑狀態碼: {response.status_code}")
        print(f"📤 根路徑響應: {response.text}")
        
        if response.status_code == 200:
            print("✅ 根端點正常運作")
            return True
        else:
            print(f"❌ 根端點返回狀態碼: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        return False

def analyze_problem():
    """分析問題"""
    print("\n🔍 問題分析:")
    print("1. 根端點正常運作 (200)")
    print("2. GET webhook 返回 405 (預期)")
    print("3. POST webhook 返回 500 (問題)")
    print("4. 可能的原因:")
    print("   - Render 沒有使用我們的文件")
    print("   - 環境變數問題")
    print("   - 依賴項問題")
    print("   - 代碼中有隱藏的錯誤")
    print("   - LINE Bot SDK 處理器覆蓋了我們的 webhook")

def provide_solutions():
    """提供解決方案"""
    print("\n💡 解決方案:")
    print("1. 檢查 Render 是否真的在使用我們的文件")
    print("2. 檢查 Render 部署日誌中的具體錯誤")
    print("3. 檢查環境變數設置")
    print("4. 檢查依賴項是否正確安裝")
    print("5. 檢查是否有其他文件在處理 webhook")
    print("6. 考慮使用不同的部署平台")

def main():
    """主函數"""
    print("🚀 最終診斷")
    print("=" * 60)
    
    # 測試根端點
    root_ok = test_root_endpoint()
    
    # 測試 GET webhook
    get_ok = test_get_webhook()
    
    # 測試基本 webhook
    webhook_ok = test_basic_webhook()
    
    # 分析問題
    analyze_problem()
    
    # 提供解決方案
    provide_solutions()
    
    print("\n" + "=" * 60)
    if root_ok and get_ok and webhook_ok:
        print("✅ 所有測試通過")
    else:
        print("❌ 有測試失敗")
        print("💡 需要進一步檢查 Render 部署日誌")
        print("💡 建議檢查 Render 是否真的在使用我們的文件")

if __name__ == "__main__":
    main()

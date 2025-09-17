#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
診斷 Render 問題
"""

import requests
import json
import time

def check_root_endpoint():
    """檢查根路徑端點"""
    print("🔍 檢查根路徑端點...")
    
    base_url = "https://anatomy-quiz-bot.onrender.com"
    
    try:
        response = requests.get(base_url, timeout=10)
        print(f"📤 根路徑狀態碼: {response.status_code}")
        print(f"📤 根路徑響應: {response.text}")
        print(f"📤 響應標頭: {dict(response.headers)}")
        
        # 檢查是否包含版本標識符
        if "super_simple_v1" in response.text:
            print("✅ 根路徑包含版本標識符，確認 Render 正在使用我們的文件")
            return True
        else:
            print("❌ 根路徑不包含版本標識符，Render 可能沒有使用我們的文件")
            return False
            
    except Exception as e:
        print(f"❌ 檢查根路徑端點失敗: {e}")
        return False

def check_webhook_endpoint():
    """檢查 webhook 端點"""
    print("\n🔍 檢查 webhook 端點...")
    
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
        
        # 檢查是否包含版本標識符
        if "super_simple_v1" in response.text:
            print("✅ webhook 響應包含版本標識符，確認 Render 正在使用我們的文件")
            return True
        else:
            print("❌ webhook 響應不包含版本標識符，Render 可能沒有使用我們的文件")
            return False
            
    except Exception as e:
        print(f"❌ 檢查 webhook 端點失敗: {e}")
        return False

def check_different_endpoints():
    """檢查不同的端點"""
    print("\n🔍 檢查不同的端點...")
    
    base_url = "https://anatomy-quiz-bot.onrender.com"
    endpoints = ["/", "/webhook", "/health", "/status", "/api", "/docs"]
    
    for endpoint in endpoints:
        try:
            url = base_url + endpoint
            print(f"\n📤 測試端點: {url}")
            
            if endpoint == "/webhook":
                # POST 請求
                test_data = {"test": "data"}
                response = requests.post(url, json=test_data, timeout=10)
            else:
                # GET 請求
                response = requests.get(url, timeout=10)
            
            print(f"📤 狀態碼: {response.status_code}")
            print(f"📤 響應內容: {response.text[:200]}...")
            
            # 檢查是否包含版本標識符
            if "super_simple_v1" in response.text:
                print("✅ 包含版本標識符")
            else:
                print("❌ 不包含版本標識符")
                
        except Exception as e:
            print(f"❌ 測試端點 {endpoint} 失敗: {e}")

def main():
    """主函數"""
    print("🚀 診斷 Render 問題")
    print("=" * 60)
    
    # 檢查根路徑端點
    root_ok = check_root_endpoint()
    
    # 檢查 webhook 端點
    webhook_ok = check_webhook_endpoint()
    
    # 檢查不同的端點
    check_different_endpoints()
    
    print("\n" + "=" * 60)
    print("📋 診斷結果:")
    
    if root_ok and webhook_ok:
        print("✅ Render 正在使用我們的文件")
        print("💡 問題可能在其他地方，如依賴項或配置")
    elif root_ok and not webhook_ok:
        print("⚠️ 根路徑正常，但 webhook 有問題")
        print("💡 可能是 webhook 處理邏輯有問題")
    elif not root_ok and not webhook_ok:
        print("❌ Render 沒有使用我們的文件")
        print("💡 請檢查 Render 部署是否成功")
        print("💡 建議重新上傳文件並重新部署")
    else:
        print("❓ 診斷結果不確定")
        print("💡 請檢查 Render 部署日誌")

if __name__ == "__main__":
    main()
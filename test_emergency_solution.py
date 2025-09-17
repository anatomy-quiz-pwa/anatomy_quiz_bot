#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試緊急解決方案
"""

import requests
import json
import time

def test_emergency_solution():
    """測試緊急解決方案"""
    print("🔍 測試緊急解決方案...")
    
    base_url = "https://anatomy-quiz-bot.onrender.com"
    
    try:
        print(f"📤 發送請求到: {base_url}")
        
        response = requests.get(base_url, timeout=10)
        print(f"📤 響應狀態碼: {response.status_code}")
        print(f"📤 響應內容: {response.text}")
        print(f"📤 響應標頭: {dict(response.headers)}")
        
        # 檢查是否包含緊急解決方案標識符
        if "EMERGENCY_SOLUTION_V6_2025_09_17" in response.text:
            print("🎉 緊急解決方案成功！Render 正在使用我們的文件")
            return True
        else:
            print("❌ 不包含緊急解決方案標識符，Render 沒有使用我們的文件")
            return False
            
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        return False

def test_webhook_with_emergency_solution():
    """測試 webhook 緊急解決方案"""
    print("\n🔍 測試 webhook 緊急解決方案...")
    
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
        
        # 檢查是否包含緊急解決方案標識符
        if "EMERGENCY_SOLUTION_V6_2025_09_17" in response.text:
            print("🎉 webhook 緊急解決方案成功！")
            return True
        else:
            print("❌ webhook 不包含緊急解決方案標識符")
            return False
            
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        return False

def wait_for_deployment():
    """等待部署完成"""
    print("⏳ 等待部署完成...")
    print("💡 請確保您已經將緊急解決方案上傳到 Render 並重新部署")
    
    for i in range(5):
        print(f"⏳ 等待中... ({i+1}/5)")
        time.sleep(10)
    
    print("✅ 等待完成，開始測試")

def main():
    """主函數"""
    print("🚀 測試緊急解決方案")
    print("=" * 60)
    
    # 等待部署
    wait_for_deployment()
    
    # 測試根路徑
    root_ok = test_emergency_solution()
    
    # 測試 webhook
    webhook_ok = test_webhook_with_emergency_solution()
    
    print("\n" + "=" * 60)
    print("📋 測試結果:")
    
    if root_ok and webhook_ok:
        print("🎉 緊急解決方案完全成功！")
        print("✅ Render 正在使用我們的文件")
        print("✅ 根路徑和 webhook 都包含版本標識符")
        print("💡 現在可以逐步添加更多功能")
    elif root_ok and not webhook_ok:
        print("⚠️ 根路徑成功，但 webhook 有問題")
        print("✅ Render 正在使用我們的文件")
        print("❌ webhook 處理邏輯有問題")
    elif not root_ok and not webhook_ok:
        print("❌ 緊急解決方案失敗")
        print("❌ Render 沒有使用我們的文件")
        print("💡 建議立即使用替代平台部署")
        print("💡 推薦平台: Railway, Heroku, Vercel, Fly.io")
        print("💡 避免繼續浪費時間在 Render 上")
    else:
        print("❓ 測試結果不確定")
        print("💡 請檢查 Render 部署日誌")

if __name__ == "__main__":
    main()

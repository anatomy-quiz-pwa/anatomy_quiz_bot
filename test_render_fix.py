#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試 Render 修復方案
"""

import requests
import json
import time

def test_render_fix():
    """測試 Render 修復方案"""
    print("🔍 測試 Render 修復方案...")
    
    base_url = "https://anatomy-quiz-bot.onrender.com"
    
    try:
        print(f"📤 發送請求到: {base_url}")
        
        response = requests.get(base_url, timeout=10)
        print(f"📤 響應狀態碼: {response.status_code}")
        print(f"📤 響應內容: {response.text}")
        print(f"📤 響應標頭: {dict(response.headers)}")
        
        # 檢查是否包含 Render 修復方案標識符
        if "RENDER_FIX_V7_2025_09_17" in response.text:
            print("🎉 Render 修復方案成功！Render 正在使用我們的文件")
            return True
        else:
            print("❌ 不包含 Render 修復方案標識符，Render 沒有使用我們的文件")
            return False
            
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        return False

def test_webhook_with_render_fix():
    """測試 webhook Render 修復方案"""
    print("\n🔍 測試 webhook Render 修復方案...")
    
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
        
        # 檢查是否包含 Render 修復方案標識符
        if "RENDER_FIX_V7_2025_09_17" in response.text:
            print("🎉 webhook Render 修復方案成功！")
            return True
        else:
            print("❌ webhook 不包含 Render 修復方案標識符")
            return False
            
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        return False

def wait_for_deployment():
    """等待部署完成"""
    print("⏳ 等待部署完成...")
    print("💡 請確保您已經將 Render 修復方案上傳到 Render 並重新部署")
    
    for i in range(5):
        print(f"⏳ 等待中... ({i+1}/5)")
        time.sleep(10)
    
    print("✅ 等待完成，開始測試")

def main():
    """主函數"""
    print("🚀 測試 Render 修復方案")
    print("=" * 60)
    
    # 等待部署
    wait_for_deployment()
    
    # 測試根路徑
    root_ok = test_render_fix()
    
    # 測試 webhook
    webhook_ok = test_webhook_with_render_fix()
    
    print("\n" + "=" * 60)
    print("📋 測試結果:")
    
    if root_ok and webhook_ok:
        print("🎉 Render 修復方案完全成功！")
        print("✅ Render 正在使用我們的文件")
        print("✅ 根路徑和 webhook 都包含版本標識符")
        print("💡 現在可以逐步添加更多功能")
    elif root_ok and not webhook_ok:
        print("⚠️ 根路徑成功，但 webhook 有問題")
        print("✅ Render 正在使用我們的文件")
        print("❌ webhook 處理邏輯有問題")
    elif not root_ok and not webhook_ok:
        print("❌ Render 修復方案失敗")
        print("❌ Render 沒有使用我們的文件")
        print("💡 請按照 Render 故障排除指南檢查：")
        print("   1. 檢查 Render 應用程式配置")
        print("   2. 檢查文件上傳")
        print("   3. 檢查部署日誌")
        print("   4. 強制重新部署")
        print("   5. 檢查環境變數")
    else:
        print("❓ 測試結果不確定")
        print("💡 請檢查 Render 部署日誌")

if __name__ == "__main__":
    main()

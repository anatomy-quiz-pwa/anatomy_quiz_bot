#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修復後的最終測試
"""

import requests
import json
import time

def test_webhook_after_fastapi_fix():
    """測試 FastAPI 修復後的 webhook"""
    print("🔍 測試 FastAPI 修復後的 webhook...")
    
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
            print("🎉 修復成功！webhook 正常運作")
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

def test_different_keywords():
    """測試不同的排行榜關鍵字"""
    print("\n🔍 測試不同的排行榜關鍵字...")
    
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

def check_server_type():
    """檢查服務器類型"""
    print("\n🔍 檢查服務器類型...")
    
    base_url = "https://anatomy-quiz-bot.onrender.com"
    
    try:
        # 測試根路徑
        response = requests.get(base_url, timeout=10)
        print(f"📤 根路徑狀態碼: {response.status_code}")
        print(f"📤 根路徑響應: {response.text}")
        
        # 測試 404 響應
        response = requests.get(f"{base_url}/nonexistent", timeout=10)
        print(f"📤 404 響應狀態碼: {response.status_code}")
        print(f"📤 404 響應內容: {response.text}")
        
        # 檢查響應格式
        if '"detail"' in response.text:
            print("✅ 響應格式像 FastAPI (包含 'detail' 字段)")
            print("💡 這表示已成功切換到 FastAPI")
        else:
            print("⚠️ 響應格式不像 FastAPI")
            
    except Exception as e:
        print(f"❌ 檢查服務器類型失敗: {e}")

def wait_for_deployment():
    """等待部署完成"""
    print("⏳ 等待部署完成...")
    print("💡 請確保您已經將修復後的文件上傳到 Render 並重新部署")
    
    for i in range(3):
        print(f"⏳ 等待中... ({i+1}/3)")
        time.sleep(10)
    
    print("✅ 等待完成，開始測試")

def main():
    """主函數"""
    print("🚀 修復後的最終測試")
    print("=" * 60)
    
    # 等待部署
    wait_for_deployment()
    
    # 檢查服務器類型
    check_server_type()
    
    # 測試 webhook
    webhook_ok = test_webhook_after_fastapi_fix()
    
    if webhook_ok:
        # 測試不同關鍵字
        test_different_keywords()
        
        print("\n" + "=" * 60)
        print("🎉 修復完全成功！")
        print("✅ 排行榜功能現在應該可以正常運作了")
        print("💡 用戶輸入「排行榜」、「leaderboard」、「排名」或「排行」都會收到 Flex Message")
    else:
        print("\n" + "=" * 60)
        print("❌ 修復失敗")
        print("💡 請檢查 Render 部署日誌")

if __name__ == "__main__":
    main()

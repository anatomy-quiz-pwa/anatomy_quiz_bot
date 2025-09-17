#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
診斷當前問題
"""

import requests
import json
import time

def test_webhook_with_leaderboard_keyword():
    """測試排行榜關鍵字"""
    print("🔍 測試排行榜關鍵字...")
    
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
            print("✅ Webhook 返回 200")
            return True
        else:
            print(f"❌ Webhook 返回狀態碼: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        return False

def test_different_keywords():
    """測試不同的關鍵字"""
    print("\n🔍 測試不同的關鍵字...")
    
    webhook_url = "https://anatomy-quiz-bot.onrender.com/webhook"
    keywords = ['排行榜', '開始', '出題', 'test']
    
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

def check_server_response_format():
    """檢查服務器響應格式"""
    print("\n🔍 檢查服務器響應格式...")
    
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
        else:
            print("⚠️ 響應格式不像 FastAPI")
            
    except Exception as e:
        print(f"❌ 檢查服務器響應格式失敗: {e}")

def analyze_problem():
    """分析問題"""
    print("\n🔍 問題分析:")
    print("1. 從日誌可以看出，應用程式確實收到了「排行榜」訊息")
    print("2. 但是發送的是一個遊戲開始的 Flex Message，而不是排行榜")
    print("3. 這表示代碼邏輯有問題")
    print("4. 可能的原因:")
    print("   - FastAPI 代碼沒有正確處理排行榜關鍵字")
    print("   - 仍然在使用 LINE Bot SDK 的處理器")
    print("   - 代碼邏輯錯誤")

def provide_solutions():
    """提供解決方案"""
    print("\n💡 解決方案:")
    print("1. 檢查 FastAPI 代碼是否正確處理排行榜關鍵字")
    print("2. 確保沒有其他文件在處理 webhook")
    print("3. 檢查 Render 是否正確使用了我們的 FastAPI 版本")
    print("4. 如果需要，創建一個簡單的測試版本")

def main():
    """主函數"""
    print("🚀 診斷當前問題")
    print("=" * 60)
    
    # 檢查服務器響應格式
    check_server_response_format()
    
    # 測試 webhook
    webhook_ok = test_webhook_with_leaderboard_keyword()
    
    # 測試不同關鍵字
    test_different_keywords()
    
    # 分析問題
    analyze_problem()
    
    # 提供解決方案
    provide_solutions()
    
    print("\n" + "=" * 60)
    if webhook_ok:
        print("✅ Webhook 正常運作，但邏輯有問題")
    else:
        print("❌ Webhook 有問題")

if __name__ == "__main__":
    main()

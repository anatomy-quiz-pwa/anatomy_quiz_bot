#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試生產環境 webhook 問題
"""

import requests
import json

def test_webhook_with_different_payloads():
    """測試不同格式的 webhook 請求"""
    print("🔍 測試不同格式的 webhook 請求...")
    
    webhook_url = "https://anatomy-quiz-bot.onrender.com/webhook"
    
    # 測試 1: 基本 LINE webhook 格式
    test_cases = [
        {
            "name": "基本 LINE webhook",
            "data": {
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
        },
        {
            "name": "簡化 LINE webhook",
            "data": {
                "events": [
                    {
                        "type": "message",
                        "source": {
                            "userId": "U977c24d1fec3a2bf07035504e1444911"
                        },
                        "message": {
                            "type": "text",
                            "text": "排行榜"
                        },
                        "replyToken": "test_reply_token"
                    }
                ]
            }
        },
        {
            "name": "Facebook Messenger 格式",
            "data": {
                "object": "page",
                "entry": [
                    {
                        "messaging": [
                            {
                                "sender": {
                                    "id": "U977c24d1fec3a2bf07035504e1444911"
                                },
                                "message": {
                                    "text": "排行榜"
                                }
                            }
                        ]
                    }
                ]
            }
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 測試 {i}: {test_case['name']}")
        
        try:
            headers = {'Content-Type': 'application/json'}
            response = requests.post(
                webhook_url, 
                json=test_case['data'], 
                headers=headers, 
                timeout=30
            )
            
            print(f"📤 狀態碼: {response.status_code}")
            print(f"📤 響應內容: {response.text[:200]}...")
            
            if response.status_code == 200:
                print("✅ 請求成功")
            else:
                print(f"❌ 請求失敗: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 請求異常: {e}")

def test_webhook_validation():
    """測試 webhook 驗證"""
    print("\n🔍 測試 webhook 驗證...")
    
    webhook_url = "https://anatomy-quiz-bot.onrender.com/webhook"
    
    # 測試 GET 請求（應該返回 405）
    try:
        response = requests.get(webhook_url, timeout=10)
        print(f"📤 GET 請求狀態碼: {response.status_code}")
        if response.status_code == 405:
            print("✅ GET 請求正確返回 405 Method Not Allowed")
        else:
            print(f"⚠️ GET 請求返回意外狀態碼: {response.status_code}")
    except Exception as e:
        print(f"❌ GET 請求失敗: {e}")
    
    # 測試空 POST 請求
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(webhook_url, json={}, headers=headers, timeout=10)
        print(f"📤 空 POST 請求狀態碼: {response.status_code}")
        print(f"📤 響應內容: {response.text}")
    except Exception as e:
        print(f"❌ 空 POST 請求失敗: {e}")

def test_webhook_with_headers():
    """測試不同 headers 的 webhook 請求"""
    print("\n🔍 測試不同 headers 的 webhook 請求...")
    
    webhook_url = "https://anatomy-quiz-bot.onrender.com/webhook"
    
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
    
    header_tests = [
        {"Content-Type": "application/json"},
        {"Content-Type": "application/json; charset=utf-8"},
        {"Content-Type": "application/json", "User-Agent": "LINE Bot SDK"},
        {}  # 無 headers
    ]
    
    for i, headers in enumerate(header_tests, 1):
        print(f"\n📝 測試 headers {i}: {headers}")
        
        try:
            response = requests.post(
                webhook_url, 
                json=test_data, 
                headers=headers, 
                timeout=30
            )
            
            print(f"📤 狀態碼: {response.status_code}")
            print(f"📤 響應內容: {response.text[:100]}...")
            
        except Exception as e:
            print(f"❌ 請求失敗: {e}")

def main():
    """主函數"""
    print("🚀 開始測試生產環境 webhook 問題")
    print("=" * 60)
    
    # 1. 測試 webhook 驗證
    test_webhook_validation()
    
    # 2. 測試不同格式的請求
    test_webhook_with_different_payloads()
    
    # 3. 測試不同 headers
    test_webhook_with_headers()
    
    print("\n" + "=" * 60)
    print("🏁 測試完成")
    
    print("\n💡 如果所有測試都返回 500 錯誤，可能的原因：")
    print("  1. 生產環境應用程式崩潰")
    print("  2. 環境變數配置問題")
    print("  3. 依賴項缺失")
    print("  4. 代碼錯誤")
    print("  5. 數據庫連接問題")
    print("\n🔧 建議檢查：")
    print("  1. Render 部署日誌")
    print("  2. 環境變數設置")
    print("  3. 應用程式啟動狀態")

if __name__ == "__main__":
    main()

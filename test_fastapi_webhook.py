#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試 FastAPI webhook 處理器
"""

import sys
import os
sys.path.append('/Users/baobaoc/Dev/anatomy_quiz_bot')

from fastapi.testclient import TestClient
from app_supabase import app

def test_webhook_endpoint():
    """測試 webhook 端點"""
    print("🔍 測試 FastAPI webhook 端點...")
    
    client = TestClient(app)
    
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
    
    try:
        print(f"📤 發送測試數據: {test_data}")
        
        response = client.post("/webhook", json=test_data)
        
        print(f"📤 響應狀態碼: {response.status_code}")
        print(f"📤 響應內容: {response.text}")
        
        if response.status_code == 200:
            print("✅ FastAPI webhook 處理器正常運作")
            return True
        else:
            print(f"❌ FastAPI webhook 處理器返回狀態碼: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        return False

def test_different_keywords():
    """測試不同的關鍵字"""
    print("\n🔍 測試不同的關鍵字...")
    
    client = TestClient(app)
    keywords = ['排行榜', '開始', '出題', 'test']
    
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
            response = client.post("/webhook", json=test_data)
            print(f"📤 狀態碼: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ 成功")
            else:
                print(f"❌ 失敗: {response.text}")
                
        except Exception as e:
            print(f"❌ 請求失敗: {e}")

def test_root_endpoint():
    """測試根端點"""
    print("\n🔍 測試根端點...")
    
    client = TestClient(app)
    
    try:
        response = client.get("/")
        print(f"📤 根端點狀態碼: {response.status_code}")
        print(f"📤 根端點響應: {response.text}")
        
        if response.status_code == 200:
            print("✅ 根端點正常運作")
            return True
        else:
            print(f"❌ 根端點返回狀態碼: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 測試根端點失敗: {e}")
        return False

def main():
    """主函數"""
    print("🚀 測試 FastAPI webhook 處理器")
    print("=" * 60)
    
    # 測試根端點
    root_ok = test_root_endpoint()
    
    # 測試 webhook 端點
    webhook_ok = test_webhook_endpoint()
    
    # 測試不同關鍵字
    test_different_keywords()
    
    print("\n" + "=" * 60)
    if root_ok and webhook_ok:
        print("✅ FastAPI webhook 處理器正常運作")
        print("💡 問題可能在於 Render 部署或環境變數")
    else:
        print("❌ FastAPI webhook 處理器有問題")
        print("💡 需要修復代碼")

if __name__ == "__main__":
    main()

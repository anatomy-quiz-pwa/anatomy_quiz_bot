#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試極簡版本
"""

import sys
import os
sys.path.append('/Users/baobaoc/Dev/anatomy_quiz_bot')

from fastapi.testclient import TestClient
from app_supabase import app

def test_extreme_simple_webhook():
    """測試極簡版本的 webhook"""
    print("🔍 測試極簡版本的 webhook...")
    
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
            print("✅ 極簡版本 webhook 正常運作")
            return True
        else:
            print(f"❌ 極簡版本 webhook 返回狀態碼: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        return False

def test_empty_webhook():
    """測試空的 webhook"""
    print("\n🔍 測試空的 webhook...")
    
    client = TestClient(app)
    
    # 空的測試數據
    test_data = {
        "events": []
    }
    
    try:
        print(f"📤 發送空測試數據: {test_data}")
        
        response = client.post("/webhook", json=test_data)
        
        print(f"📤 響應狀態碼: {response.status_code}")
        print(f"📤 響應內容: {response.text}")
        
        if response.status_code == 200:
            print("✅ 空 webhook 正常運作")
            return True
        else:
            print(f"❌ 空 webhook 返回狀態碼: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        return False

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
    print("🚀 測試極簡版本")
    print("=" * 60)
    
    # 測試根端點
    root_ok = test_root_endpoint()
    
    # 測試空的 webhook
    empty_ok = test_empty_webhook()
    
    # 測試完整的 webhook
    webhook_ok = test_extreme_simple_webhook()
    
    print("\n" + "=" * 60)
    if root_ok and empty_ok and webhook_ok:
        print("✅ 極簡版本所有測試通過")
        print("💡 可以部署到 Render 進行測試")
    else:
        print("❌ 有測試失敗")
        print("💡 需要進一步修復")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
測試 LINE Bot 的重置和開始功能
"""

import requests
import json
import time

def test_line_reset_and_start():
    """測試重置和開始功能"""
    test_user_id = "test_user_123"
    
    print("🧪 測試 LINE Bot 重置和開始功能...")
    
    # 1. 測試重置指令
    print(f"\n1️⃣ 測試重置指令...")
    reset_payload = {
        "events": [{
            "type": "message",
            "message": {
                "type": "text",
                "text": "重置"
            },
            "source": {
                "type": "user",
                "userId": test_user_id
            },
            "replyToken": "test_reply_token_reset"
        }]
    }
    
    try:
        response = requests.post(
            "http://localhost:5001/callback",
            json=reset_payload,
            headers={"Content-Type": "application/json"}
        )
        print(f"   重置指令回應: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ 重置指令成功")
        else:
            print(f"   ❌ 重置指令失敗")
    except Exception as e:
        print(f"   ❌ 重置指令錯誤: {e}")
    
    # 等待一下
    time.sleep(2)
    
    # 2. 測試開始指令
    print(f"\n2️⃣ 測試開始指令...")
    start_payload = {
        "events": [{
            "type": "message",
            "message": {
                "type": "text",
                "text": "開始"
            },
            "source": {
                "type": "user",
                "userId": test_user_id
            },
            "replyToken": "test_reply_token_start"
        }]
    }
    
    try:
        response = requests.post(
            "http://localhost:5001/callback",
            json=start_payload,
            headers={"Content-Type": "application/json"}
        )
        print(f"   開始指令回應: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ 開始指令成功")
        else:
            print(f"   ❌ 開始指令失敗")
    except Exception as e:
        print(f"   ❌ 開始指令錯誤: {e}")
    
    # 3. 檢查資料庫狀態
    print(f"\n3️⃣ 檢查資料庫狀態...")
    try:
        from debug_supabase import debug_user_stats
        debug_user_stats()
    except Exception as e:
        print(f"   檢查資料庫狀態失敗: {e}")
    
    print(f"\n🎉 測試完成！")

if __name__ == "__main__":
    test_line_reset_and_start() 
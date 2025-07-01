#!/usr/bin/env python3
"""
只測試重置功能
"""

import requests
import json
import time

def test_reset_only():
    """只測試重置功能"""
    test_user_id = "test_user_123"
    
    print("🧪 只測試重置功能...")
    
    # 1. 檢查重置前狀態
    print(f"\n1️⃣ 檢查重置前狀態...")
    try:
        from debug_supabase import debug_user_stats
        debug_user_stats()
    except Exception as e:
        print(f"   檢查失敗: {e}")
    
    # 2. 執行重置
    print(f"\n2️⃣ 執行重置...")
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
        print(f"   重置回應: {response.status_code}")
    except Exception as e:
        print(f"   重置錯誤: {e}")
    
    # 等待一下
    time.sleep(3)
    
    # 3. 檢查重置後狀態
    print(f"\n3️⃣ 檢查重置後狀態...")
    try:
        from debug_supabase import debug_user_stats
        debug_user_stats()
    except Exception as e:
        print(f"   檢查失敗: {e}")
    
    print(f"\n🎉 測試完成！")

if __name__ == "__main__":
    test_reset_only() 
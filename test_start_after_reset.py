#!/usr/bin/env python3
"""
測試重置後的開始指令
"""

import requests
import json
import time

def test_start_after_reset():
    """測試重置後的開始指令"""
    test_user_id = "test_user_123"
    
    print("🧪 測試重置後的開始指令...")
    
    # 1. 先重置
    print(f"\n1️⃣ 先執行重置...")
    try:
        from supabase_user_stats_handler import reset_user_stats
        reset_success = reset_user_stats(test_user_id)
        print(f"   重置結果: {reset_success}")
    except Exception as e:
        print(f"   重置失敗: {e}")
    
    # 等待一下
    time.sleep(2)
    
    # 2. 檢查重置後狀態
    print(f"\n2️⃣ 檢查重置後狀態...")
    try:
        from supabase_user_stats_handler import get_user_stats
        stats = get_user_stats(test_user_id)
        print(f"   重置後統計: {stats}")
    except Exception as e:
        print(f"   檢查失敗: {e}")
    
    # 3. 測試開始指令
    print(f"\n3️⃣ 測試開始指令...")
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
    
    # 4. 檢查開始指令後的狀態
    print(f"\n4️⃣ 檢查開始指令後的狀態...")
    try:
        from supabase_user_stats_handler import get_user_stats
        stats = get_user_stats(test_user_id)
        print(f"   開始指令後統計: {stats}")
    except Exception as e:
        print(f"   檢查失敗: {e}")
    
    print(f"\n🎉 測試完成！")

if __name__ == "__main__":
    test_start_after_reset() 
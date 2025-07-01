#!/usr/bin/env python3
"""
測試完整的問答流程
"""

import requests
import json
import time

def test_full_quiz_flow():
    """測試完整的問答流程"""
    test_user_id = "test_user_123"
    
    print("🧪 測試完整的問答流程...")
    
    # 1. 先重置
    print(f"\n1️⃣ 先重置...")
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
    
    # 3. 模擬開始指令
    print(f"\n3️⃣ 模擬開始指令...")
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
    except Exception as e:
        print(f"   開始指令錯誤: {e}")
    
    # 等待一下
    time.sleep(3)
    
    # 4. 檢查開始指令後狀態
    print(f"\n4️⃣ 檢查開始指令後狀態...")
    try:
        from supabase_user_stats_handler import get_user_stats
        stats = get_user_stats(test_user_id)
        print(f"   開始指令後統計: {stats}")
    except Exception as e:
        print(f"   檢查失敗: {e}")
    
    # 5. 模擬回答正確答案
    print(f"\n5️⃣ 模擬回答正確答案...")
    answer_payload = {
        "events": [{
            "type": "postback",
            "postback": {
                "data": "answer_3"  # 假設答案是 3
            },
            "source": {
                "type": "user",
                "userId": test_user_id
            },
            "replyToken": "test_reply_token_answer"
        }]
    }
    
    try:
        response = requests.post(
            "http://localhost:5001/callback",
            json=answer_payload,
            headers={"Content-Type": "application/json"}
        )
        print(f"   回答指令回應: {response.status_code}")
    except Exception as e:
        print(f"   回答指令錯誤: {e}")
    
    # 等待一下
    time.sleep(3)
    
    # 6. 檢查回答後狀態
    print(f"\n6️⃣ 檢查回答後狀態...")
    try:
        from supabase_user_stats_handler import get_user_stats
        stats = get_user_stats(test_user_id)
        print(f"   回答後統計: {stats}")
    except Exception as e:
        print(f"   檢查失敗: {e}")
    
    # 7. 檢查積分
    print(f"\n7️⃣ 檢查積分...")
    try:
        from main_supabase import get_user_correct_wrong
        correct, wrong = get_user_correct_wrong(test_user_id)
        print(f"   積分: 正確={correct}, 錯誤={wrong}")
    except Exception as e:
        print(f"   檢查失敗: {e}")
    
    print(f"\n🎉 完整流程測試完成！")

if __name__ == "__main__":
    test_full_quiz_flow() 
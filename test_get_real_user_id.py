#!/usr/bin/env python3
"""
模擬獲取真實 LINE 用戶 ID
"""

import sys
import os
import requests
import json
import time

def test_get_real_user_id():
    """測試獲取真實用戶 ID"""
    
    # 模擬用戶發送「我的ID」指令
    webhook_data = {
        "events": [
            {
                "type": "message",
                "message": {
                    "type": "text",
                    "text": "我的ID"
                },
                "replyToken": "test_reply_token_123",
                "source": {
                    "userId": "U1234567890abcdef1234567890abcdef",  # 模擬真實 LINE 用戶 ID
                    "type": "user"
                },
                "timestamp": int(time.time() * 1000)
            }
        ]
    }
    
    try:
        # 發送 webhook 到本地應用程式
        response = requests.post(
            "http://localhost:5001/callback",
            headers={
                "Content-Type": "application/json",
                "X-Line-Signature": "test_signature"
            },
            data=json.dumps(webhook_data),
            timeout=10
        )
        
        print(f"Webhook 回應狀態碼: {response.status_code}")
        print(f"Webhook 回應內容: {response.text}")
        
        return response.status_code == 200
        
    except requests.exceptions.ConnectionError:
        print("❌ 無法連接到應用程式，請確保 app_supabase.py 正在運行")
        return False
    except Exception as e:
        print(f"Webhook 測試失敗: {e}")
        return False

def test_real_user_stats():
    """測試真實用戶的統計資料"""
    try:
        from supabase_user_stats_handler import get_user_stats, add_correct_answer
        from supabase_quiz_handler import get_questions
        
        # 使用模擬的真實用戶 ID
        real_user_id = "U1234567890abcdef1234567890abcdef"
        
        print(f"=== 測試真實用戶 {real_user_id} ===")
        
        # 獲取初始統計
        initial_stats = get_user_stats(real_user_id)
        print(f"初始統計: {initial_stats}")
        
        # 獲取題目
        questions = get_questions()
        print(f"總題目數: {len(questions)}")
        
        # 檢查可用題目
        available = [q for q in questions if q["qid"] not in initial_stats["correct_qids"]]
        print(f"可用題目數: {len(available)}")
        
        if available:
            # 選擇第一個可用題目
            question = available[0]
            print(f"選擇題目: qid={question['qid']}")
            
            # 模擬答對
            success = add_correct_answer(real_user_id, question['qid'])
            print(f"添加正確答案: {success}")
            
            # 獲取更新後的統計
            updated_stats = get_user_stats(real_user_id)
            print(f"更新後統計: {updated_stats}")
            
            return True
        else:
            print("❌ 沒有可用題目")
            return False
        
    except Exception as e:
        print(f"測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 測試真實用戶 ID...")
    
    # 測試獲取用戶 ID
    print("\n1. 測試獲取用戶 ID...")
    if test_get_real_user_id():
        print("✅ 用戶 ID 測試成功")
    else:
        print("❌ 用戶 ID 測試失敗")
    
    # 測試真實用戶統計
    print("\n2. 測試真實用戶統計...")
    if test_real_user_stats():
        print("✅ 真實用戶統計測試成功")
    else:
        print("❌ 真實用戶統計測試失敗") 
#!/usr/bin/env python3
"""
直接測試 LINE Bot 功能，不通過 webhook
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main_supabase import send_question, handle_answer, get_user_stats, get_user_correct_wrong
from config import LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET

# 測試用的用戶 ID
TEST_USER_ID = "U977c24d1fec3a2bf07035504e1444911"

def test_direct():
    """直接測試功能"""
    print("=== 直接測試 LINE Bot 功能 ===")
    
    # 1. 檢查初始狀態
    print("\n1. 檢查初始狀態...")
    try:
        correct, wrong = get_user_correct_wrong(TEST_USER_ID)
        print(f"初始積分: 正確 {correct}, 錯誤 {wrong}")
    except Exception as e:
        print(f"檢查積分失敗: {e}")
    
    # 2. 發送第一題
    print("\n2. 發送第一題...")
    try:
        send_question(TEST_USER_ID)
        print("第一題已發送")
    except Exception as e:
        print(f"發送第一題失敗: {e}")
    
    # 3. 模擬回答第一題（選項 1）
    print("\n3. 模擬回答第一題（選項 1）...")
    try:
        handle_answer(TEST_USER_ID, 1)
        print("第一題答案已處理")
    except Exception as e:
        print(f"處理第一題答案失敗: {e}")
    
    # 4. 檢查更新後的狀態
    print("\n4. 檢查更新後的狀態...")
    try:
        correct, wrong = get_user_correct_wrong(TEST_USER_ID)
        print(f"更新後積分: 正確 {correct}, 錯誤 {wrong}")
    except Exception as e:
        print(f"檢查更新後積分失敗: {e}")
    
    # 5. 發送第二題
    print("\n5. 發送第二題...")
    try:
        send_question(TEST_USER_ID)
        print("第二題已發送")
    except Exception as e:
        print(f"發送第二題失敗: {e}")
    
    # 6. 模擬回答第二題（選項 2）
    print("\n6. 模擬回答第二題（選項 2）...")
    try:
        handle_answer(TEST_USER_ID, 2)
        print("第二題答案已處理")
    except Exception as e:
        print(f"處理第二題答案失敗: {e}")
    
    # 7. 最終檢查
    print("\n7. 最終檢查...")
    try:
        correct, wrong = get_user_correct_wrong(TEST_USER_ID)
        print(f"最終積分: 正確 {correct}, 錯誤 {wrong}")
    except Exception as e:
        print(f"最終檢查失敗: {e}")
    
    print("\n=== 測試完成 ===")

if __name__ == "__main__":
    test_direct() 
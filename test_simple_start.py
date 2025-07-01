#!/usr/bin/env python3
"""
簡單測試"開始"命令的核心功能
"""

import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

def test_start_command_core():
    """測試開始命令的核心功能"""
    print("🧪 測試「開始」命令的核心功能...")
    
    try:
        # 測試 get_user_correct_wrong 函數
        from main_supabase import get_user_correct_wrong, get_user_question_count
        
        user_id = "test_user_123"
        
        print(f"📊 測試用戶統計功能...")
        correct, wrong = get_user_correct_wrong(user_id)
        print(f"   正確答案: {correct}")
        print(f"   錯誤答案: {wrong}")
        print(f"   總計: {correct + wrong}")
        
        print(f"📊 測試今日挑戰次數...")
        today_count = get_user_question_count(user_id)
        print(f"   今日挑戰次數: {today_count}")
        
        # 測試 send_question 函數
        print(f"📝 測試發送題目功能...")
        from main_supabase import send_question
        
        # 在本地測試模式下發送題目
        send_question(user_id)
        print("   ✅ 題目發送測試完成")
        
        print("✅ 核心功能測試完成")
        
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        import traceback
        traceback.print_exc()

def test_safe_functions():
    """測試安全發送函數"""
    print("\n🧪 測試安全發送函數...")
    
    try:
        from app_supabase import safe_reply_message, safe_push_message
        from linebot.models import TextSendMessage
        
        # 測試 safe_reply_message
        test_message = TextSendMessage(text="測試回覆訊息")
        result = safe_reply_message("test_reply_token", test_message)
        print(f"📤 safe_reply_message 結果: {result}")
        
        # 測試 safe_push_message
        test_message2 = TextSendMessage(text="測試推送訊息")
        result2 = safe_push_message("test_user_123", test_message2)
        print(f"📤 safe_push_message 結果: {result2}")
        
        print("✅ 安全發送函數測試完成")
        
    except Exception as e:
        print(f"❌ 安全發送函數測試失敗: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_start_command_core()
    test_safe_functions() 
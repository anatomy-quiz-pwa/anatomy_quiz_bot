#!/usr/bin/env python3
"""
測試 user_states 問題
"""

def test_user_states():
    """測試 user_states 問題"""
    test_user_id = "test_user_123"
    
    print("🧪 測試 user_states 問題...")
    
    # 1. 先重置
    print(f"\n1️⃣ 先重置...")
    try:
        from supabase_user_stats_handler import reset_user_stats
        reset_success = reset_user_stats(test_user_id)
        print(f"   重置結果: {reset_success}")
    except Exception as e:
        print(f"   重置失敗: {e}")
    
    # 2. 檢查 user_states
    print(f"\n2️⃣ 檢查 user_states...")
    try:
        from main_supabase import user_states
        print(f"   當前 user_states: {user_states}")
        if test_user_id in user_states:
            print(f"   用戶 {test_user_id} 在 user_states 中")
            print(f"   用戶狀態: {user_states[test_user_id]}")
        else:
            print(f"   用戶 {test_user_id} 不在 user_states 中")
    except Exception as e:
        print(f"   檢查失敗: {e}")
    
    # 3. 模擬發送題目（設置 user_states）
    print(f"\n3️⃣ 模擬發送題目...")
    try:
        from main_supabase import user_states, get_questions, send_question
        questions = get_questions()
        print(f"   題目數量: {len(questions)}")
        
        # 直接調用 send_question
        send_question(test_user_id)
        print(f"   send_question 調用完成")
        
        # 檢查 user_states
        print(f"   調用後 user_states: {user_states}")
        if test_user_id in user_states:
            print(f"   用戶 {test_user_id} 在 user_states 中")
            print(f"   用戶狀態: {user_states[test_user_id]}")
        else:
            print(f"   用戶 {test_user_id} 不在 user_states 中")
    except Exception as e:
        print(f"   模擬失敗: {e}")
    
    # 4. 模擬回答（如果 user_states 存在）
    print(f"\n4️⃣ 模擬回答...")
    try:
        from main_supabase import user_states, handle_answer
        if test_user_id in user_states:
            print(f"   用戶狀態存在，模擬回答...")
            handle_answer(test_user_id, 3)
            print(f"   handle_answer 調用完成")
        else:
            print(f"   用戶狀態不存在，跳過回答")
    except Exception as e:
        print(f"   回答失敗: {e}")
    
    # 5. 檢查最終狀態
    print(f"\n5️⃣ 檢查最終狀態...")
    try:
        from supabase_user_stats_handler import get_user_stats
        stats = get_user_stats(test_user_id)
        print(f"   最終統計: {stats}")
    except Exception as e:
        print(f"   檢查失敗: {e}")
    
    print(f"\n🎉 user_states 測試完成！")

if __name__ == "__main__":
    test_user_states() 
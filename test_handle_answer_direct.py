#!/usr/bin/env python3
"""
直接測試 handle_answer 函數
"""

def test_handle_answer_direct():
    """直接測試 handle_answer 函數"""
    test_user_id = "test_user_123"
    
    print("🧪 直接測試 handle_answer 函數...")
    
    # 1. 先重置
    print(f"\n1️⃣ 先重置...")
    try:
        from supabase_user_stats_handler import reset_user_stats
        reset_success = reset_user_stats(test_user_id)
        print(f"   重置結果: {reset_success}")
    except Exception as e:
        print(f"   重置失敗: {e}")
    
    # 2. 檢查重置後狀態
    print(f"\n2️⃣ 檢查重置後狀態...")
    try:
        from supabase_user_stats_handler import get_user_stats
        stats = get_user_stats(test_user_id)
        print(f"   重置後統計: {stats}")
    except Exception as e:
        print(f"   檢查失敗: {e}")
    
    # 3. 設置用戶狀態（模擬已經發送題目）
    print(f"\n3️⃣ 設置用戶狀態...")
    try:
        from main_supabase import user_states, get_questions
        questions = get_questions()
        # 選擇第一題
        question = questions[0]
        print(f"   選擇題目: qid={question['qid']}, 題目={question['question'][:30]}...")
        
        # 設置用戶狀態
        user_states[test_user_id] = {
            'current_question': question,
            'answered': False
        }
        print(f"   用戶狀態已設置: {user_states[test_user_id]}")
    except Exception as e:
        print(f"   設置失敗: {e}")
    
    # 4. 直接調用 handle_answer
    print(f"\n4️⃣ 直接調用 handle_answer...")
    try:
        from main_supabase import handle_answer
        # 假設答案是 3
        handle_answer(test_user_id, 3)
        print(f"   handle_answer 調用完成")
    except Exception as e:
        print(f"   調用失敗: {e}")
    
    # 5. 檢查處理後狀態
    print(f"\n5️⃣ 檢查處理後狀態...")
    try:
        from supabase_user_stats_handler import get_user_stats
        stats = get_user_stats(test_user_id)
        print(f"   處理後統計: {stats}")
    except Exception as e:
        print(f"   檢查失敗: {e}")
    
    # 6. 檢查積分
    print(f"\n6️⃣ 檢查積分...")
    try:
        from main_supabase import get_user_correct_wrong
        correct, wrong = get_user_correct_wrong(test_user_id)
        print(f"   積分: 正確={correct}, 錯誤={wrong}")
    except Exception as e:
        print(f"   檢查失敗: {e}")
    
    print(f"\n🎉 直接測試完成！")

if __name__ == "__main__":
    test_handle_answer_direct() 
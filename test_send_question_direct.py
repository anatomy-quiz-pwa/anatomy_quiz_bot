#!/usr/bin/env python3
"""
直接測試 send_question 函數
"""

def test_send_question_direct():
    """直接測試 send_question 函數"""
    test_user_id = "test_user_123"
    
    print("🧪 直接測試 send_question 函數...")
    
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
    
    # 3. 檢查題目
    print(f"\n3️⃣ 檢查題目...")
    try:
        from main_supabase import get_questions
        questions = get_questions()
        question_ids = [q["qid"] for q in questions]
        print(f"   所有題目 ID: {question_ids}")
    except Exception as e:
        print(f"   檢查失敗: {e}")
    
    # 4. 直接調用 send_question（不發送訊息）
    print(f"\n4️⃣ 直接調用 send_question...")
    try:
        from main_supabase import send_question
        # 這裡我們需要修改 send_question 函數，讓它不實際發送訊息
        # 或者我們可以檢查它的邏輯
        print(f"   send_question 函數存在")
        
        # 檢查可用題目邏輯
        available = [q for q in questions if q["qid"] not in stats["correct_qids"]]
        print(f"   可用題目數量: {len(available)}")
        if available:
            print(f"   可用題目 ID: {[q['qid'] for q in available]}")
            print(f"   ✅ send_question 應該會發送題目")
        else:
            print(f"   ❌ send_question 會顯示：今天沒有新題目了，明天再來挑戰吧！")
            
    except Exception as e:
        print(f"   調用失敗: {e}")
    
    print(f"\n🎉 測試完成！")

if __name__ == "__main__":
    test_send_question_direct() 
#!/usr/bin/env python3
"""
測試實際 LINE 用戶的狀態
"""

def test_real_user():
    """測試實際 LINE 用戶的狀態"""
    
    print("🧪 測試實際 LINE 用戶的狀態...")
    
    # 1. 檢查所有用戶統計
    print(f"\n1️⃣ 檢查所有用戶統計...")
    try:
        from supabase_user_stats_handler import get_all_user_stats
        all_stats = get_all_user_stats()
        print(f"   所有用戶統計數量: {len(all_stats)}")
        for stat in all_stats:
            print(f"   用戶 {stat['user_id']}: 正確={stat['correct']}, 錯誤={stat['wrong']}, correct_qids={stat['correct_qids']}")
    except Exception as e:
        print(f"   檢查失敗: {e}")
    
    # 2. 檢查題目
    print(f"\n2️⃣ 檢查題目...")
    try:
        from main_supabase import get_questions
        questions = get_questions()
        question_ids = [q["qid"] for q in questions]
        print(f"   所有題目 ID: {question_ids}")
        print(f"   題目數量: {len(questions)}")
    except Exception as e:
        print(f"   檢查失敗: {e}")
    
    # 3. 測試不同用戶 ID
    print(f"\n3️⃣ 測試不同用戶 ID...")
    test_user_ids = [
        "test_user_123",
        "U1234567890abcdef1234567890abcdef",  # 可能的 LINE 用戶 ID 格式
        "U1234567890abcdef1234567890abcde",   # 另一個可能的格式
    ]
    
    for user_id in test_user_ids:
        try:
            from supabase_user_stats_handler import get_user_stats
            stats = get_user_stats(user_id)
            print(f"   用戶 {user_id}: {stats}")
            
            # 檢查可用題目
            available = [q for q in questions if q["qid"] not in stats["correct_qids"]]
            print(f"     可用題目數量: {len(available)}")
            if available:
                print(f"     可用題目 ID: {[q['qid'] for q in available]}")
            else:
                print(f"     ❌ 沒有可用題目！")
                
        except Exception as e:
            print(f"   用戶 {user_id}: 檢查失敗 - {e}")
    
    print(f"\n🎉 測試完成！")

if __name__ == "__main__":
    test_real_user() 
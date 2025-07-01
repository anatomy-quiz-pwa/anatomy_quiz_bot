#!/usr/bin/env python3
"""
直接測試 send_question 函數
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main_supabase import send_question, get_user_stats, get_questions

def test_send_question():
    """測試 send_question 函數"""
    test_user_id = "test_user_123"
    
    print("🧪 直接測試 send_question 函數...")
    
    # 1. 檢查用戶統計
    print(f"\n1️⃣ 檢查用戶統計...")
    stats = get_user_stats(test_user_id)
    print(f"   用戶統計: {stats}")
    
    # 2. 檢查題目
    print(f"\n2️⃣ 檢查題目...")
    questions = get_questions()
    question_ids = [q["qid"] for q in questions]
    print(f"   所有題目 ID: {question_ids}")
    
    # 3. 檢查可用題目
    print(f"\n3️⃣ 檢查可用題目...")
    available = [q for q in questions if q["qid"] not in stats["correct_qids"]]
    print(f"   可用題目數量: {len(available)}")
    if available:
        print(f"   可用題目 ID: {[q['qid'] for q in available]}")
    else:
        print(f"   ❌ 沒有可用題目！")
        print(f"   原因：所有題目 ID {question_ids} 都在已答對列表 {stats['correct_qids']} 中")
    
    # 4. 測試 send_question（不實際發送訊息）
    print(f"\n4️⃣ 測試 send_question 邏輯...")
    if not available:
        print(f"   ❌ send_question 會顯示：今天沒有新題目了，明天再來挑戰吧！")
        return False
    else:
        print(f"   ✅ send_question 會發送題目")
        return True

if __name__ == "__main__":
    test_send_question() 
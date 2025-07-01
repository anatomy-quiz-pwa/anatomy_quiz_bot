#!/usr/bin/env python3
"""
測試多個題目的回答流程
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main_supabase import send_question, handle_answer, user_states
from supabase_user_stats_handler import reset_user_stats, get_user_stats
from supabase_quiz_handler import get_questions

def test_multiple_questions():
    """測試回答多個題目"""
    user_id = "test_user_123"
    
    print("🧪 測試回答多個題目...")
    
    # 1. 重置用戶
    print("\n1️⃣ 重置用戶...")
    reset_user_stats(user_id)
    stats = get_user_stats(user_id)
    print(f"   重置後統計: {stats}")
    
    # 2. 獲取所有題目
    print("\n2️⃣ 獲取所有題目...")
    questions = get_questions()
    question_ids = [q["qid"] for q in questions]
    print(f"   所有題目 ID: {question_ids}")
    
    # 3. 模擬回答多個題目
    for i in range(min(3, len(questions))):  # 回答前3題
        print(f"\n3️⃣ 回答第 {i+1} 題...")
        
        # 選擇題目
        question = questions[i]
        print(f"   選擇題目: qid={question['qid']}, 題目={question['question'][:30]}...")
        
        # 設置用戶狀態
        user_states[user_id] = {
            'current_question': question,
            'answered': False
        }
        
        # 回答正確答案
        correct_answer = int(question['answer'])
        print(f"   正確答案: {correct_answer}")
        
        # 調用 handle_answer
        handle_answer(user_id, correct_answer)
        
        # 檢查狀態
        stats = get_user_stats(user_id)
        print(f"   回答後統計: {stats}")
        
        # 清理用戶狀態，準備下一題
        if user_id in user_states:
            del user_states[user_id]
    
    # 4. 最終檢查
    print(f"\n4️⃣ 最終檢查...")
    stats = get_user_stats(user_id)
    print(f"   最終統計: {stats}")
    
    # 5. 檢查可用題目
    print(f"\n5️⃣ 檢查可用題目...")
    available_questions = [q for q in questions if q["qid"] not in stats["correct_qids"]]
    print(f"   已答對題目 ID: {stats['correct_qids']}")
    print(f"   剩餘可用題目數: {len(available_questions)}")
    print(f"   剩餘可用題目 ID: {[q['qid'] for q in available_questions]}")
    
    print("\n🎉 多題目測試完成！")

if __name__ == "__main__":
    test_multiple_questions() 
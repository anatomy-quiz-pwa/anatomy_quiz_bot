#!/usr/bin/env python3
"""
測試題目重複出現功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main_supabase import send_question, handle_answer, user_states
from supabase_user_stats_handler import reset_user_stats, get_user_stats
from supabase_quiz_handler import get_questions

def test_repeat_questions():
    """測試題目重複出現"""
    user_id = "test_user_123"
    
    print("🧪 測試題目重複出現功能...")
    
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
    
    # 3. 模擬回答所有題目
    print("\n3️⃣ 回答所有題目...")
    for i in range(len(questions)):
        print(f"\n   回答第 {i+1} 題...")
        
        # 模擬 send_question
        import random
        question = random.choice(questions)  # 從所有題目中隨機選擇
        print(f"   選中題目: qid={question['qid']}, 題目={question['question'][:30]}...")
        
        # 設置用戶狀態
        user_states[user_id] = {
            'current_question': question,
            'answered': False
        }
        
        # 模擬正確回答
        correct_answer = int(question['answer'])
        print(f"   正確答案: {correct_answer}")
        
        # 調用 handle_answer
        handle_answer(user_id, correct_answer)
        
        # 檢查統計
        stats = get_user_stats(user_id)
        print(f"   回答後統計: {stats}")
    
    # 4. 測試重複回答
    print("\n4️⃣ 測試重複回答...")
    for i in range(3):  # 再回答3題
        print(f"\n   重複回答第 {i+1} 題...")
        
        # 模擬 send_question（現在應該可以重複選擇）
        question = random.choice(questions)  # 從所有題目中隨機選擇
        print(f"   選中題目: qid={question['qid']}, 題目={question['question'][:30]}...")
        
        # 設置用戶狀態
        user_states[user_id] = {
            'current_question': question,
            'answered': False
        }
        
        # 模擬正確回答
        correct_answer = int(question['answer'])
        print(f"   正確答案: {correct_answer}")
        
        # 調用 handle_answer
        handle_answer(user_id, correct_answer)
        
        # 檢查統計
        stats = get_user_stats(user_id)
        print(f"   回答後統計: {stats}")
    
    # 5. 最終檢查
    print("\n5️⃣ 最終檢查...")
    stats = get_user_stats(user_id)
    print(f"   最終統計: {stats}")
    
    # 檢查 correct_qids 是否包含重複的 ID
    correct_qids = stats['correct_qids']
    unique_qids = set(correct_qids)
    print(f"   已答對題目 ID: {correct_qids}")
    print(f"   唯一題目 ID: {list(unique_qids)}")
    print(f"   總答對次數: {len(correct_qids)}")
    print(f"   唯一題目數: {len(unique_qids)}")
    
    if len(correct_qids) > len(unique_qids):
        print("✅ 成功！題目可以重複出現")
    else:
        print("❌ 失敗！題目沒有重複出現")
    
    print("\n🎉 重複題目測試完成！")

if __name__ == "__main__":
    test_repeat_questions() 
#!/usr/bin/env python3
"""
測試題目資料和 add_correct_answer 調用
"""

import sys
import os

# 添加當前目錄到 Python 路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_question_data():
    """測試題目資料結構"""
    try:
        from supabase_quiz_handler import get_questions
        from supabase_user_stats_handler import add_correct_answer, get_user_stats
        
        print("=== 測試題目資料 ===")
        
        # 獲取所有題目
        questions = get_questions()
        print(f"總題目數: {len(questions)}")
        
        # 檢查每個題目的結構
        for i, question in enumerate(questions):
            print(f"\n題目 {i+1}:")
            print(f"  qid: {question.get('qid')} (類型: {type(question.get('qid'))})")
            print(f"  問題: {question.get('question', '')[:50]}...")
            print(f"  選項: {question.get('options', [])}")
            print(f"  答案: {question.get('answer')}")
        
        # 測試 add_correct_answer 調用
        print("\n=== 測試 add_correct_answer 調用 ===")
        test_user_id = "test_user_123"
        
        # 獲取初始統計
        initial_stats = get_user_stats(test_user_id)
        print(f"初始統計: {initial_stats}")
        
        # 使用第一個題目的 qid
        if questions:
            first_question = questions[0]
            question_id = first_question.get('qid')
            print(f"使用題目 ID: {question_id} (類型: {type(question_id)})")
            
            # 調用 add_correct_answer
            success = add_correct_answer(test_user_id, question_id)
            print(f"add_correct_answer 結果: {success}")
            
            # 獲取更新後的統計
            updated_stats = get_user_stats(test_user_id)
            print(f"更新後統計: {updated_stats}")
            
            # 檢查 correct_qids 是否包含該題目 ID
            if question_id in updated_stats['correct_qids']:
                print("✅ 題目 ID 已正確添加到 correct_qids")
            else:
                print("❌ 題目 ID 未添加到 correct_qids")
                print(f"  期望: {question_id}")
                print(f"  實際: {updated_stats['correct_qids']}")
        
        return True
        
    except Exception as e:
        print(f"測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_question_data() 
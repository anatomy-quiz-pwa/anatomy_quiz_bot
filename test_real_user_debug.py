#!/usr/bin/env python3
"""
檢查實際 LINE 用戶的統計資料
"""

import sys
import os

# 添加當前目錄到 Python 路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_real_user_stats():
    """檢查實際 LINE 用戶的統計資料"""
    try:
        from supabase_user_stats_handler import get_user_stats, get_all_user_stats
        from supabase_quiz_handler import get_questions
        
        print("=== 檢查所有用戶統計 ===")
        
        # 獲取所有用戶統計
        all_stats = get_all_user_stats()
        print(f"總用戶數: {len(all_stats)}")
        
        for i, user_stat in enumerate(all_stats):
            print(f"\n用戶 {i+1}:")
            print(f"  user_id: {user_stat.get('user_id')}")
            print(f"  correct: {user_stat.get('correct')}")
            print(f"  wrong: {user_stat.get('wrong')}")
            print(f"  correct_qids: {user_stat.get('correct_qids')}")
            print(f"  last_update: {user_stat.get('last_update')}")
        
        print("\n=== 檢查題目資料 ===")
        questions = get_questions()
        question_ids = [q['qid'] for q in questions]
        print(f"所有題目 ID: {question_ids}")
        
        # 檢查每個用戶的可用題目
        for user_stat in all_stats:
            user_id = user_stat.get('user_id')
            correct_qids_str = user_stat.get('correct_qids', '')
            
            # 解析 correct_qids
            correct_qids = []
            if correct_qids_str:
                for qid in correct_qids_str.split(','):
                    try:
                        correct_qids.append(int(qid.strip()))
                    except (ValueError, TypeError):
                        pass
            
            available_qids = [qid for qid in question_ids if qid not in correct_qids]
            
            print(f"\n用戶 {user_id}:")
            print(f"  已答對題目: {correct_qids}")
            print(f"  可用題目: {available_qids}")
            print(f"  可用題目數: {len(available_qids)}")
            
            if len(available_qids) == 0:
                print(f"  ❌ 沒有可用題目！")
            else:
                print(f"  ✅ 有 {len(available_qids)} 個可用題目")
        
        return True
        
    except Exception as e:
        print(f"檢查失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    check_real_user_stats() 
#!/usr/bin/env python3
"""
獲取真實的 LINE 用戶 ID
"""

import sys
import os

# 添加當前目錄到 Python 路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_all_users():
    """檢查所有用戶並顯示他們的統計"""
    try:
        from supabase_user_stats_handler import get_all_user_stats
        from supabase_quiz_handler import get_questions
        
        print("=== 當前資料庫中的所有用戶 ===")
        
        # 獲取所有用戶統計
        all_stats = get_all_user_stats()
        print(f"總用戶數: {len(all_stats)}")
        
        if len(all_stats) == 0:
            print("❌ 資料庫中沒有任何用戶記錄")
            print("💡 請在 LINE 中發送任何訊息給機器人，然後再檢查")
            return
        
        # 獲取題目
        questions = get_questions()
        question_ids = [q['qid'] for q in questions]
        
        for i, user_stat in enumerate(all_stats):
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
            
            print(f"\n用戶 {i+1}: {user_id}")
            print(f"  正確答案數: {user_stat.get('correct', 0)}")
            print(f"  錯誤答案數: {user_stat.get('wrong', 0)}")
            print(f"  已答對題目: {correct_qids}")
            print(f"  可用題目: {available_qids}")
            print(f"  可用題目數: {len(available_qids)}")
            
            if len(available_qids) == 0:
                print(f"  ❌ 沒有可用題目！")
            else:
                print(f"  ✅ 有 {len(available_qids)} 個可用題目")
        
        print(f"\n=== 所有題目 ID ===")
        print(f"題目 ID: {question_ids}")
        
        print(f"\n=== 使用說明 ===")
        print("1. 在 LINE 中發送 '我的ID' 給機器人，獲取你的真實用戶 ID")
        print("2. 如果沒有新題目，發送 '重置' 來清除你的統計資料")
        print("3. 發送 '開始' 來開始新的問答")
        
    except Exception as e:
        print(f"檢查失敗: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_all_users() 
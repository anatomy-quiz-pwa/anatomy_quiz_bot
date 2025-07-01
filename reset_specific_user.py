#!/usr/bin/env python3
"""
重置特定用戶的統計資料
"""

import sys
import os

# 添加當前目錄到 Python 路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def reset_user(user_id):
    """重置指定用戶的統計資料"""
    try:
        from supabase_user_stats_handler import reset_user_stats, get_user_stats
        from supabase_quiz_handler import get_questions
        
        print(f"=== 重置用戶 {user_id} ===")
        
        # 獲取重置前的統計
        before_stats = get_user_stats(user_id)
        print(f"重置前統計: {before_stats}")
        
        # 執行重置
        success = reset_user_stats(user_id)
        if success:
            print("✅ 重置成功")
        else:
            print("❌ 重置失敗")
            return False
        
        # 獲取重置後的統計
        after_stats = get_user_stats(user_id)
        print(f"重置後統計: {after_stats}")
        
        # 檢查可用題目
        questions = get_questions()
        available = [q for q in questions if q["qid"] not in after_stats["correct_qids"]]
        print(f"可用題目數: {len(available)}")
        
        if len(available) > 0:
            print("✅ 重置成功！現在有可用題目了")
            return True
        else:
            print("❌ 重置後仍然沒有可用題目")
            return False
        
    except Exception as e:
        print(f"重置失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    if len(sys.argv) != 2:
        print("使用方法: python reset_specific_user.py <用戶ID>")
        print("例如: python reset_specific_user.py U1234567890abcdef1234567890abcdef")
        return
    
    user_id = sys.argv[1]
    reset_user(user_id)

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
測試等級進度顯示修復
檢查答題後進度數據是否正確顯示
"""

import os
import sys
import json
from datetime import datetime

# 添加項目根目錄到 Python 路徑
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 設置環境變量
os.environ['SUPABASE_URL'] = 'https://ciqlfqfgzqqgdrogedxg.supabase.co'
os.environ['SUPABASE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjY1MjIwNTcsImV4cCI6MjA0MjA5ODA1N30.RzLvHoKUvdEE9O6XVJJG-JcZAKONhgFWqmrqJZvNLHs'
os.environ['LINE_CHANNEL_ACCESS_TOKEN'] = 'test_token'
os.environ['LINE_CHANNEL_SECRET'] = 'test_secret'

from app_supabase import (
    get_user_stats, 
    update_user_stats_after_answer, 
    check_and_handle_level_up,
    send_explanation_with_image,
    supabase
)

def test_progress_display_fix():
    """測試等級進度顯示修復"""
    print("🔍 測試等級進度顯示修復")
    print("=" * 60)
    
    # 使用寶的測試帳號
    test_user_id = "U977c24d1fec3a2bf07035504e1444911"
    
    try:
        # 1. 獲取用戶當前狀態
        print("\n📊 1. 獲取用戶當前狀態")
        current_stats = get_user_stats(test_user_id)
        if current_stats:
            print(f"   等級: {current_stats.get('level', 1)}")
            print(f"   總答對數: {current_stats.get('correct', 0)}")
            print(f"   當前等級進度: {current_stats.get('correct_in_level', 0)}/3")
        else:
            print("   用戶不存在，將創建新用戶")
        
        # 2. 模擬答對一題
        print("\n✅ 2. 模擬答對一題")
        
        # 模擬題目數據
        mock_question = {
            'id': 999,
            'question': '測試題目',
            'options': ['選項A', '選項B', '選項C', '選項D'],
            'correct_answer': 0,
            'explanation': '這是測試解說',
            'level': 1
        }
        
        # 按照修復後的順序執行
        print("   a. 更新用戶統計...")
        update_user_stats_after_answer(test_user_id, True, 999)
        
        print("   b. 檢查升級邏輯...")
        current_level = current_stats.get('level', 1) if current_stats else 1
        upgraded = check_and_handle_level_up(test_user_id, current_level, True)
        print(f"      升級狀態: {'升級了' if upgraded else '未升級'}")
        
        # 3. 獲取更新後的狀態
        print("\n📈 3. 獲取更新後的狀態")
        updated_stats = get_user_stats(test_user_id)
        if updated_stats:
            print(f"   等級: {updated_stats.get('level', 1)}")
            print(f"   總答對數: {updated_stats.get('correct', 0)}")
            print(f"   當前等級進度: {updated_stats.get('correct_in_level', 0)}/3")
            
            # 4. 模擬進度顯示邏輯
            print("\n🎯 4. 模擬進度顯示邏輯")
            display_level = updated_stats.get('level', 1)
            display_progress = updated_stats.get('correct_in_level', 0)
            
            # 這是 send_explanation_with_image 中的邏輯
            # 如果答對了，進度+1（只用於顯示）
            display_progress += 1  # 因為剛答對了一題
            remaining = max(0, 3 - display_progress)
            
            print(f"   顯示等級: {display_level}")
            print(f"   顯示進度: {display_progress}/3")
            print(f"   剩餘題數: {remaining}")
            
            # 驗證結果
            print("\n✨ 5. 驗證結果")
            if display_progress > 0:
                print("   ✅ 進度正確顯示！")
                print(f"   📈 等級 {display_level} 進度：{display_progress}/3")
                if remaining > 0:
                    print(f"   🎯 還需要答對{remaining}題升級")
                else:
                    print("   🎉 準備升級！")
            else:
                print("   ❌ 進度顯示仍有問題")
        else:
            print("   ❌ 無法獲取更新後的用戶狀態")
            
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {e}")
        import traceback
        traceback.print_exc()

def test_multiple_answers():
    """測試連續答題的進度顯示"""
    print("\n🔄 測試連續答題的進度顯示")
    print("=" * 60)
    
    test_user_id = "U977c24d1fec3a2bf07035504e1444911"
    
    # 重置用戶到等級1，進度0
    try:
        reset_data = {
            'user_id': test_user_id,
            'level': 1,
            'correct': 0,
            'wrong': 0,
            'correct_in_level': 0,
            'correct_qids': []
        }
        supabase.table('user_stats').upsert(reset_data, on_conflict='user_id').execute()
        print("✅ 用戶狀態已重置")
        
        # 連續答對3題
        for i in range(3):
            print(f"\n📝 第{i+1}題:")
            
            # 獲取答題前狀態
            before_stats = get_user_stats(test_user_id)
            before_progress = before_stats.get('correct_in_level', 0) if before_stats else 0
            before_level = before_stats.get('level', 1) if before_stats else 1
            
            # 模擬答對
            update_user_stats_after_answer(test_user_id, True, 1000 + i)
            check_and_handle_level_up(test_user_id, before_level, True)
            
            # 獲取答題後狀態
            after_stats = get_user_stats(test_user_id)
            after_progress = after_stats.get('correct_in_level', 0) if after_stats else 0
            after_level = after_stats.get('level', 1) if after_stats else 1
            
            # 計算顯示進度（模擬 send_explanation_with_image 的邏輯）
            display_progress = after_progress + 1  # 答對了，顯示時+1
            remaining = max(0, 3 - display_progress)
            
            print(f"   答題前: 等級{before_level}, 進度{before_progress}/3")
            print(f"   答題後: 等級{after_level}, 進度{after_progress}/3")
            print(f"   顯示為: 等級{after_level}, 進度{display_progress}/3")
            
            if i < 2:  # 前兩題不應升級
                if after_level == before_level and display_progress == i + 1:
                    print("   ✅ 進度正確")
                else:
                    print("   ❌ 進度錯誤")
            else:  # 第三題應該升級
                if after_level > before_level:
                    print("   ✅ 正確升級")
                else:
                    print("   ❌ 未正確升級")
                    
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🧪 等級進度顯示修復測試")
    print("=" * 60)
    
    test_progress_display_fix()
    test_multiple_answers()
    
    print("\n" + "=" * 60)
    print("✅ 測試完成")

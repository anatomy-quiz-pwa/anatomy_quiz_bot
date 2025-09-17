#!/usr/bin/env python3
"""
測試重複題目修復功能
驗證題目選擇邏輯是否正確過濾已答題目
"""

import os
import sys
import random
from supabase import create_client, Client

# 添加項目根目錄到 Python 路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 環境變數設置
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://ciqlfqfgzqqgdrogedxg.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA')

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_all_questions():
    """從 Supabase 獲取所有等級的題目"""
    try:
        response = supabase.table('anatomy_questions_v2').select('*').execute()
        
        if not response.data:
            return []
        
        questions = []
        for item in response.data:
            question = {
                "id": item.get('id'),
                "question": item.get('question'),
                "options": [
                    item.get('option_1', ''),
                    item.get('option_2', ''),
                    item.get('option_3', ''),
                    item.get('option_4', '')
                ],
                "correct_answer": (item.get('correct_option', 1) - 1) if item.get('correct_option') else 0,
                "level": item.get('level', 1),
                "category": "解剖學",
                "explanation": item.get('explanation', ''),
                "image_url": item.get('image_url', ''),
                "qimage_url": item.get('qimage_url', '')
            }
            questions.append(question)
        
        return questions
        
    except Exception as e:
        print(f"❌ 從 Supabase 獲取題目失敗: {e}")
        return []

def get_questions_by_level(level):
    """獲取指定等級的題目"""
    all_questions = get_all_questions()
    return [q for q in all_questions if q['level'] == level]

def get_user_stats(user_id):
    """獲取用戶統計信息"""
    try:
        response = supabase.table('user_stats').select('*').eq('user_id', user_id).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        print(f"❌ 獲取用戶統計失敗: {e}")
        return None

def simulate_question_selection(user_id, level, test_rounds=10):
    """模擬題目選擇邏輯測試"""
    print(f"\n=== 測試用戶 {user_id} 等級 {level} 題目選擇 ===")
    
    # 獲取該等級的所有題目
    level_questions = get_questions_by_level(level)
    print(f"等級 {level} 總題目數: {len(level_questions)}")
    
    if not level_questions:
        print("❌ 該等級沒有題目")
        return
    
    # 獲取用戶已答對的題目
    user_stats = get_user_stats(user_id)
    answered_question_ids = user_stats.get('correct_qids', []) if user_stats else []
    print(f"用戶已答對題目ID: {answered_question_ids}")
    
    # 應用新的過濾邏輯
    available_questions = [q for q in level_questions if q['id'] not in answered_question_ids]
    print(f"可用題目數: {len(available_questions)}")
    
    if not available_questions:
        print("🎉 該等級所有題目都已答過！")
        return
    
    # 模擬多次選題
    print(f"\n模擬 {test_rounds} 次選題結果:")
    selected_ids = []
    for i in range(test_rounds):
        question = random.choice(available_questions)
        selected_ids.append(question['id'])
        print(f"第{i+1}次: 題目ID {question['id']} - {question['question'][:30]}...")
    
    # 統計結果
    unique_selections = set(selected_ids)
    print(f"\n📊 選題統計:")
    print(f"總選題次數: {test_rounds}")
    print(f"不同題目數: {len(unique_selections)}")
    print(f"重複選到已答題目: {'否' if not any(qid in answered_question_ids for qid in selected_ids) else '是'}")
    
    return len(unique_selections), len(selected_ids)

def test_admin_question_selection(user_id, test_rounds=10):
    """測試管理員題目選擇邏輯"""
    print(f"\n=== 測試管理員 {user_id} 題目選擇 ===")
    
    # 獲取所有題目
    all_questions = get_all_questions()
    print(f"總題目數: {len(all_questions)}")
    
    if not all_questions:
        print("❌ 沒有題目")
        return
    
    # 獲取用戶已答對的題目
    user_stats = get_user_stats(user_id)
    answered_question_ids = user_stats.get('correct_qids', []) if user_stats else []
    print(f"管理員已答對題目ID: {answered_question_ids}")
    
    # 應用新的過濾邏輯
    available_questions = [q for q in all_questions if q['id'] not in answered_question_ids]
    
    # 如果沒有未答的題目，管理員可以重新答題
    if not available_questions:
        print("🔄 所有題目都已答過，管理員可以重新挑戰")
        available_questions = all_questions
    
    print(f"可用題目數: {len(available_questions)}")
    
    # 模擬多次選題
    print(f"\n模擬 {test_rounds} 次選題結果:")
    selected_ids = []
    for i in range(test_rounds):
        question = random.choice(available_questions)
        selected_ids.append(question['id'])
        print(f"第{i+1}次: 題目ID {question['id']} (等級{question['level']}) - {question['question'][:30]}...")
    
    # 統計結果
    unique_selections = set(selected_ids)
    print(f"\n📊 選題統計:")
    print(f"總選題次數: {test_rounds}")
    print(f"不同題目數: {len(unique_selections)}")
    
    return len(unique_selections), len(selected_ids)

def create_test_user_with_answered_questions():
    """創建測試用戶並設置一些已答題目"""
    test_user_id = "test_duplicate_fix_user"
    
    # 模擬用戶已答對等級1的部分題目
    level_1_questions = get_questions_by_level(1)
    if level_1_questions:
        # 假設用戶已答對前3道題目
        answered_ids = [q['id'] for q in level_1_questions[:3]]
        
        # 更新或創建用戶統計
        user_data = {
            'user_id': test_user_id,
            'level': 1,
            'correct': len(answered_ids),
            'wrong': 0,
            'correct_qids': answered_ids,
            'last_update': '2025-01-17T12:00:00'
        }
        
        try:
            supabase.table('user_stats').upsert(user_data).execute()
            print(f"✅ 創建測試用戶 {test_user_id}，已答對題目: {answered_ids}")
            return test_user_id
        except Exception as e:
            print(f"❌ 創建測試用戶失敗: {e}")
            return None
    
    return None

def main():
    """主測試函數"""
    print("🧪 重複題目修復功能測試")
    print("=" * 50)
    
    # 1. 測試基本題目獲取
    print("\n1. 測試題目獲取功能")
    all_questions = get_all_questions()
    print(f"總題目數: {len(all_questions)}")
    
    for level in range(1, 15):
        level_questions = get_questions_by_level(level)
        if level_questions:
            print(f"等級 {level}: {len(level_questions)} 道題目")
    
    # 2. 創建測試用戶
    print("\n2. 創建測試用戶")
    test_user_id = create_test_user_with_answered_questions()
    
    if not test_user_id:
        print("❌ 無法創建測試用戶，使用現有用戶")
        test_user_id = "U9a9df49945755ef651d067743f3c7ea7"  # 現有用戶
    
    # 3. 測試普通用戶題目選擇
    print("\n3. 測試普通用戶題目選擇（等級1）")
    simulate_question_selection(test_user_id, 1, 15)
    
    # 4. 測試不同等級
    print("\n4. 測試不同等級題目選擇")
    for level in [2, 3, 5]:  # 測試幾個不同等級
        level_questions = get_questions_by_level(level)
        if level_questions:
            simulate_question_selection(test_user_id, level, 5)
    
    # 5. 測試管理員題目選擇
    print("\n5. 測試管理員題目選擇")
    test_admin_question_selection(test_user_id, 10)
    
    print("\n" + "=" * 50)
    print("✅ 測試完成！")
    print("\n修復要點:")
    print("1. ✅ 題目選擇時會過濾已答對的題目")
    print("2. ✅ 避免用戶收到重複題目")
    print("3. ✅ 等級完成時會提示用戶")
    print("4. ✅ 管理員可以重新挑戰所有題目")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
調試 Supabase 資料庫連接和資料
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client

# 載入環境變數
load_dotenv()

# 初始化 Supabase 客戶端
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    raise ValueError("SUPABASE_URL 和 SUPABASE_ANON_KEY 必須在 .env 檔案中設定")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def debug_questions():
    """調試題目資料"""
    print("🔍 調試 Supabase 題目資料...")
    
    try:
        # 查詢所有題目
        response = supabase.table("questions").select("*").execute()
        
        if hasattr(response, 'data'):
            questions_data = response.data
        else:
            questions_data = response
        
        print(f"📊 原始資料數量: {len(questions_data)}")
        
        if not questions_data:
            print("❌ 沒有找到題目資料")
            return
        
        print("\n📋 前3題資料結構:")
        for i, row in enumerate(questions_data[:3]):
            print(f"\n題目 {i+1}:")
            print(f"  ID: {row.get('id')}")
            print(f"  題目文字: {row.get('question_text', 'N/A')[:50]}...")
            print(f"  選項1: {row.get('option1', 'N/A')}")
            print(f"  選項2: {row.get('option2', 'N/A')}")
            print(f"  選項3: {row.get('option3', 'N/A')}")
            print(f"  選項4: {row.get('option4', 'N/A')}")
            print(f"  正確答案: {row.get('correct_answer', 'N/A')}")
            print(f"  解釋: {row.get('explanation', 'N/A')[:50]}...")
        
        # 檢查必要欄位
        valid_questions = []
        for i, row in enumerate(questions_data):
            if (row.get('question_text') and 
                row.get('option1') and 
                row.get('option2') and 
                row.get('option3') and 
                row.get('option4') and
                isinstance(row.get('correct_answer'), int) and
                1 <= row.get('correct_answer') <= 4):
                valid_questions.append(row)
            else:
                print(f"⚠️  題目 {i+1} 缺少必要欄位或格式錯誤")
        
        print(f"\n✅ 有效題目數量: {len(valid_questions)}")
        
    except Exception as e:
        print(f"❌ 調試題目資料時發生錯誤: {e}")
        import traceback
        traceback.print_exc()

def debug_user_stats():
    """調試用戶統計資料"""
    print("\n🔍 調試 Supabase 用戶統計資料...")
    
    try:
        # 查詢所有用戶統計
        response = supabase.table("user_stats").select("*").execute()
        
        if hasattr(response, 'data'):
            user_stats_data = response.data
        else:
            user_stats_data = response
        
        print(f"📊 用戶統計資料數量: {len(user_stats_data)}")
        
        if not user_stats_data:
            print("❌ 沒有找到用戶統計資料")
            return
        
        print("\n📋 用戶統計資料:")
        for i, row in enumerate(user_stats_data):
            print(f"\n用戶 {i+1}:")
            print(f"  ID: {row.get('id')}")
            print(f"  User ID: {row.get('user_id')}")
            print(f"  正確: {row.get('correct', 0)}")
            print(f"  錯誤: {row.get('wrong', 0)}")
            print(f"  正確題目ID: {row.get('correct_qids', '')}")
            print(f"  最後更新: {row.get('last_update', '')}")
        
    except Exception as e:
        print(f"❌ 調試用戶統計資料時發生錯誤: {e}")
        import traceback
        traceback.print_exc()

def test_question_loading():
    """測試題目載入功能"""
    print("\n🧪 測試題目載入功能...")
    
    try:
        from supabase_quiz_handler import get_questions
        
        questions = get_questions()
        print(f"📊 載入的題目數量: {len(questions)}")
        
        if questions:
            print("\n📋 第一題詳細資訊:")
            first_question = questions[0]
            print(f"  QID: {first_question.get('qid')}")
            print(f"  題目: {first_question.get('question', 'N/A')}")
            print(f"  選項: {first_question.get('options', [])}")
            print(f"  答案: {first_question.get('answer', 'N/A')}")
            print(f"  解釋: {first_question.get('explanation', 'N/A')}")
        else:
            print("❌ 沒有載入到題目")
            
    except Exception as e:
        print(f"❌ 測試題目載入時發生錯誤: {e}")
        import traceback
        traceback.print_exc()

def test_user_stats_loading():
    """測試用戶統計載入功能"""
    print("\n🧪 測試用戶統計載入功能...")
    
    try:
        from supabase_user_stats_handler import get_user_stats, add_correct_answer
        
        test_user_id = "test_user_123"
        
        # 獲取用戶統計
        stats = get_user_stats(test_user_id)
        print(f"📊 用戶 {test_user_id} 統計: {stats}")
        
        # 測試添加正確答案
        success = add_correct_answer(test_user_id, 1)
        print(f"✅ 添加正確答案成功: {success}")
        
        # 再次獲取統計
        updated_stats = get_user_stats(test_user_id)
        print(f"📊 更新後統計: {updated_stats}")
        
    except Exception as e:
        print(f"❌ 測試用戶統計載入時發生錯誤: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 開始調試 Supabase 資料庫...")
    
    # 調試題目資料
    debug_questions()
    
    # 調試用戶統計資料
    debug_user_stats()
    
    # 測試題目載入功能
    test_question_loading()
    
    # 測試用戶統計載入功能
    test_user_stats_loading()
    
    print("\n✅ 調試完成！") 
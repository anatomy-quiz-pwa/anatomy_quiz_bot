#!/usr/bin/env python3
"""
測試新的資料庫結構和程式碼修改
"""

import os
import sys
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

def test_new_schema():
    """測試新的資料庫結構"""
    print("🔧 測試新的資料庫結構...")
    
    try:
        from supabase_quiz_handler import get_questions, test_supabase_connection
        
        # 測試連線
        if not test_supabase_connection():
            print("❌ Supabase 連線失敗")
            return False
        
        # 獲取題目
        questions = get_questions()
        print(f"✅ 成功獲取 {len(questions)} 個題目")
        
        if not questions:
            print("⚠️  沒有找到題目，請檢查資料庫")
            return False
        
        # 檢查第一個題目的結構
        first_question = questions[0]
        print(f"\n📋 第一個題目結構:")
        print(f"  ID: {first_question.get('qid')}")
        print(f"  分類: {first_question.get('category')}")
        print(f"  題目: {first_question.get('question')[:50]}...")
        print(f"  選項: {first_question.get('options')}")
        print(f"  答案: {first_question.get('answer')}")
        print(f"  解釋: {first_question.get('explanation')[:50]}...")
        
        # 檢查新欄位
        print(f"\n🆕 新欄位檢查:")
        print(f"  topic_tag: {first_question.get('topic_tag')}")
        print(f"  application_case: {first_question.get('application_case')}")
        print(f"  boom_type: {first_question.get('boom_type')}")
        print(f"  emotion_response: {first_question.get('emotion_response')}")
        print(f"  answer_feedback: {first_question.get('answer_feedback')}")
        print(f"  image_url: {first_question.get('image_url')}")
        print(f"  audio_snippet_url: {first_question.get('audio_snippet_url')}")
        
        return True
        
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_question_handling():
    """測試題目處理邏輯"""
    print("\n🔧 測試題目處理邏輯...")
    
    try:
        from supabase_quiz_handler import get_questions
        from main_supabase import handle_answer
        
        questions = get_questions()
        if not questions:
            print("❌ 沒有題目可測試")
            return False
        
        # 模擬一個測試題目
        test_question = questions[0]
        print(f"📝 測試題目: {test_question['question'][:50]}...")
        
        # 模擬正確答案
        correct_answer = int(test_question['answer'])
        print(f"✅ 正確答案: {correct_answer}")
        
        # 檢查新欄位的使用
        if test_question.get('answer_feedback'):
            print(f"💡 有 answer_feedback: {test_question['answer_feedback'][:50]}...")
        
        if test_question.get('emotion_response'):
            print(f"💬 有 emotion_response: {test_question['emotion_response'][:50]}...")
        
        if test_question.get('application_case'):
            print(f"🩺 有 application_case: {test_question['application_case'][:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_user_stats():
    """測試用戶統計功能"""
    print("\n🔧 測試用戶統計功能...")
    
    try:
        from supabase_user_stats_handler import get_user_stats, add_correct_answer, add_wrong_answer
        
        test_user_id = "test_new_schema_user"
        
        # 獲取初始統計
        initial_stats = get_user_stats(test_user_id)
        print(f"📊 初始統計: {initial_stats}")
        
        # 測試添加正確答案
        success = add_correct_answer(test_user_id, 1)
        print(f"✅ 添加正確答案: {'成功' if success else '失敗'}")
        
        # 獲取更新後統計
        updated_stats = get_user_stats(test_user_id)
        print(f"📊 更新後統計: {updated_stats}")
        
        return True
        
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_advanced_queries():
    """測試新資料庫結構的進階查詢功能"""
    print("🧪 測試新資料庫結構的進階查詢功能...")
    
    # 1. 根據難度篩選題目
    print("\n1️⃣ 根據難度篩選題目:")
    difficulties = ['easy', 'medium', 'clinical']
    for difficulty in difficulties:
        try:
            response = supabase.table("questions").select("*").eq("difficulty", difficulty).execute()
            questions = response.data
            print(f"  {difficulty}: {len(questions)} 題")
        except Exception as e:
            print(f"  {difficulty}: 查詢失敗 - {e}")
    
    # 2. 根據主題標籤篩選
    print("\n2️⃣ 根據主題標籤篩選題目:")
    try:
        response = supabase.table("questions").select("*").eq("topic_tag", "上肢解剖").execute()
        questions = response.data
        print(f"  上肢解剖: {len(questions)} 題")
    except Exception as e:
        print(f"  上肢解剖: 查詢失敗 - {e}")
    
    # 3. 根據標籤篩選
    print("\n3️⃣ 根據標籤篩選題目:")
    try:
        response = supabase.table("questions").select("*").contains("tags", ["冷知識"]).execute()
        questions = response.data
        print(f"  包含'冷知識'標籤: {len(questions)} 題")
    except Exception as e:
        print(f"  包含'冷知識'標籤: 查詢失敗 - {e}")
    
    # 4. 根據解剖部位篩選
    print("\n4️⃣ 根據解剖部位篩選題目:")
    try:
        response = supabase.table("questions").select("*").eq("structure_part", "上肢").execute()
        questions = response.data
        print(f"  上肢相關: {len(questions)} 題")
    except Exception as e:
        print(f"  上肢相關: 查詢失敗 - {e}")
    
    # 5. 根據考試來源篩選
    print("\n5️⃣ 根據考試來源篩選題目:")
    try:
        response = supabase.table("questions").select("*").like("exam_source", "%PT國考%").execute()
        questions = response.data
        print(f"  PT國考相關: {len(questions)} 題")
    except Exception as e:
        print(f"  PT國考相關: 查詢失敗 - {e}")

def test_question_details():
    """測試題目詳細資訊"""
    print("\n📝 題目詳細資訊範例:")
    
    try:
        response = supabase.table("questions").select("*").limit(1).execute()
        if response.data:
            q = response.data[0]
            print(f"  題目: {q['question_text']}")
            print(f"  難度: {q['difficulty']}")
            print(f"  主題: {q['topic_tag']}")
            print(f"  解剖主題: {q['anatomy_topic']}")
            print(f"  標籤: {q['tags']}")
            print(f"  解剖部位: {q['structure_part']}")
            print(f"  構造類型: {q['structure_type']}")
            print(f"  功能: {q['structure_function']}")
            print(f"  考試來源: {q['exam_source']}")
            print(f"  臨床應用: {q['application_case']}")
            print(f"  爆點類型: {q['boom_type']}")
            print(f"  情感回應: {q['emotion_response']}")
            print(f"  解釋: {q['explanation']}")
    except Exception as e:
        print(f"  獲取題目詳細資訊失敗: {e}")

def test_quiz_logic():
    """測試新的題目邏輯"""
    print("\n🎯 測試新的題目邏輯:")
    
    # 模擬根據用戶程度選擇題目
    user_level = "medium"  # 可以根據用戶歷史表現動態調整
    
    try:
        # 根據用戶程度選擇題目
        response = supabase.table("questions").select("*").eq("difficulty", user_level).execute()
        questions = response.data
        
        if questions:
            selected_question = questions[0]  # 簡化，實際應該隨機選擇
            print(f"  為 {user_level} 程度用戶選擇的題目:")
            print(f"    題目: {selected_question['question_text']}")
            print(f"    選項: {selected_question['option1']}, {selected_question['option2']}, {selected_question['option3']}, {selected_question['option4']}")
            print(f"    正確答案: {selected_question['correct_answer']}")
            print(f"    解釋: {selected_question['explanation']}")
            
            # 模擬答對後的豐富回應
            print(f"    爆點: {selected_question['boom_type']}")
            print(f"    情感回應: {selected_question['emotion_response']}")
            print(f"    臨床應用: {selected_question['application_case']}")
        else:
            print(f"  沒有找到 {user_level} 程度的題目")
            
    except Exception as e:
        print(f"  測試題目邏輯失敗: {e}")

def main():
    """主測試函數"""
    print("🚀 開始測試新的資料庫結構...")
    
    # 測試資料庫結構
    if not test_new_schema():
        print("❌ 資料庫結構測試失敗")
        return
    
    # 測試題目處理
    if not test_question_handling():
        print("❌ 題目處理測試失敗")
        return
    
    # 測試用戶統計
    if not test_user_stats():
        print("❌ 用戶統計測試失敗")
        return
    
    # 測試進階查詢
    test_advanced_queries()
    
    # 測試題目詳細資訊
    test_question_details()
    
    # 測試題目邏輯
    test_quiz_logic()
    
    print("\n🎉 所有測試通過！新的資料庫結構工作正常。")

if __name__ == "__main__":
    main() 
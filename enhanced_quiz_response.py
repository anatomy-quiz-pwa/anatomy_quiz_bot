#!/usr/bin/env python3
import os
import random
from supabase import create_client, Client
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 初始化 Supabase 客戶端
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    raise ValueError("SUPABASE_URL 和 SUPABASE_ANON_KEY 必須在 .env 檔案中設定")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def get_enhanced_question(user_level="medium", topic=None):
    """根據用戶程度和主題獲取增強版題目"""
    try:
        query = supabase.table("questions").select("*")
        
        # 根據用戶程度篩選
        if user_level:
            query = query.eq("difficulty", user_level)
        
        # 根據主題篩選（如果指定）
        if topic:
            query = query.eq("topic_tag", topic)
        
        response = query.execute()
        questions = response.data
        
        if not questions:
            # 如果沒有找到符合條件的題目，返回隨機題目
            response = supabase.table("questions").select("*").execute()
            questions = response.data
        
        if questions:
            return random.choice(questions)
        else:
            return None
            
    except Exception as e:
        print(f"獲取增強題目失敗: {e}")
        return None

def create_enhanced_response(question, is_correct, user_answer):
    """創建增強版的答題回應"""
    if not question:
        return "抱歉，無法獲取題目資訊。"
    
    # 基礎回應
    response_parts = []
    
    if is_correct:
        response_parts.append("🎉 答對了！")
    else:
        correct_answer = question['correct_answer']
        response_parts.append(f"❌ 答錯了！正確答案是：{correct_answer}")
    
    # 添加解釋
    if question.get('explanation'):
        response_parts.append(f"\n📚 {question['explanation']}")
    
    # 添加爆點
    if question.get('boom_type'):
        response_parts.append(f"\n💥 {question['boom_type']}")
    
    # 添加情感回應
    if question.get('emotion_response'):
        response_parts.append(f"\n💭 {question['emotion_response']}")
    
    # 添加臨床應用
    if question.get('application_case'):
        response_parts.append(f"\n🩺 臨床應用：{question['application_case']}")
    
    # 添加難度資訊
    difficulty_emoji = {
        'easy': '🟢',
        'medium': '🟡', 
        'clinical': '🔴'
    }
    difficulty = question.get('difficulty', 'medium')
    response_parts.append(f"\n{difficulty_emoji.get(difficulty, '🟡')} 難度：{difficulty}")
    
    # 添加標籤
    if question.get('tags'):
        tags_text = ', '.join(question['tags'])
        response_parts.append(f"\n🏷️ 標籤：{tags_text}")
    
    # 添加考試來源
    if question.get('exam_source'):
        response_parts.append(f"\n📖 來源：{question['exam_source']}")
    
    return '\n'.join(response_parts)

def create_question_message(question):
    """創建增強版的題目訊息"""
    if not question:
        return "抱歉，無法獲取題目。"
    
    message_parts = []
    
    # 題目
    message_parts.append(f"📝 {question['question_text']}")
    
    # 選項
    options = [
        question.get('option1', ''),
        question.get('option2', ''),
        question.get('option3', ''),
        question.get('option4', '')
    ]
    
    for i, option in enumerate(options, 1):
        message_parts.append(f"{i}. {option}")
    
    # 難度指示
    difficulty = question.get('difficulty', 'medium')
    difficulty_emoji = {
        'easy': '🟢',
        'medium': '🟡',
        'clinical': '🔴'
    }
    message_parts.append(f"\n{difficulty_emoji.get(difficulty, '🟡')} 難度：{difficulty}")
    
    # 主題
    if question.get('topic_tag'):
        message_parts.append(f"📚 主題：{question['topic_tag']}")
    
    return '\n'.join(message_parts)

def simulate_enhanced_quiz():
    """模擬增強版的問答流程"""
    print("🎯 模擬增強版問答流程...")
    
    # 模擬不同程度的用戶
    user_levels = ['easy', 'medium', 'clinical']
    
    for level in user_levels:
        print(f"\n👤 模擬 {level} 程度用戶:")
        
        # 獲取題目
        question = get_enhanced_question(user_level=level)
        if not question:
            print("  無法獲取題目")
            continue
        
        print(f"  題目: {question['question_text']}")
        print(f"  難度: {question['difficulty']}")
        print(f"  主題: {question['topic_tag']}")
        
        # 模擬答對
        print("\n  ✅ 模擬答對:")
        correct_response = create_enhanced_response(question, True, None)
        print(f"  {correct_response}")
        
        # 模擬答錯
        print("\n  ❌ 模擬答錯:")
        wrong_response = create_enhanced_response(question, False, 2)
        print(f"  {wrong_response}")
        
        print("-" * 50)

def test_topic_based_questions():
    """測試根據主題篩選題目"""
    print("\n🎯 測試根據主題篩選題目:")
    
    try:
        # 獲取上肢解剖相關題目
        response = supabase.table("questions").select("*").eq("topic_tag", "上肢解剖").execute()
        questions = response.data
        
        if questions:
            print(f"  找到 {len(questions)} 個上肢解剖相關題目")
            for i, q in enumerate(questions, 1):
                print(f"  {i}. {q['question_text'][:50]}...")
        else:
            print("  沒有找到上肢解剖相關題目")
            
    except Exception as e:
        print(f"  測試主題篩選失敗: {e}")

def test_difficulty_based_questions():
    """測試根據難度篩選題目"""
    print("\n🎯 測試根據難度篩選題目:")
    
    difficulties = ['easy', 'medium', 'clinical']
    
    for difficulty in difficulties:
        try:
            response = supabase.table("questions").select("*").eq("difficulty", difficulty).execute()
            questions = response.data
            
            print(f"  {difficulty}: {len(questions)} 題")
            if questions:
                sample = questions[0]
                print(f"    範例: {sample['question_text'][:40]}...")
                
        except Exception as e:
            print(f"  {difficulty}: 查詢失敗 - {e}")

if __name__ == "__main__":
    print("🚀 開始測試增強版問答功能...")
    
    # 測試增強版問答流程
    simulate_enhanced_quiz()
    
    # 測試主題篩選
    test_topic_based_questions()
    
    # 測試難度篩選
    test_difficulty_based_questions()
    
    print("\n✨ 增強版功能測試完成！") 
#!/usr/bin/env python3
"""
向新的資料庫結構添加示例題目
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

def add_sample_questions():
    """添加示例題目到新的資料庫結構"""
    
    sample_questions = [
        {
            "question_text": "人體最大的器官是什麼？",
            "option1": "心臟",
            "option2": "大腦", 
            "option3": "皮膚",
            "option4": "肝臟",
            "correct_answer": 3,
            "topic_tag": "基礎解剖｜器官系統",
            "application_case": "皮膚是人體最大的器官，佔體重的約16%，具有保護、調節體溫、感覺等功能。",
            "boom_type": "冷知識",
            "emotion_response": "你知道嗎？皮膚不只是保護層，它還是我們最大的器官！",
            "explanation": "皮膚是人體最大的器官，佔體重的約16%，具有保護、調節體溫、感覺等功能。",
            "image_url": "https://example.com/skin_organ.png",
            "audio_snippet_url": None
        },
        {
            "question_text": "心臟位於胸腔的哪個位置？",
            "option1": "左側",
            "option2": "右側",
            "option3": "中央偏左",
            "option4": "中央偏右",
            "correct_answer": 3,
            "topic_tag": "循環系統｜心臟",
            "application_case": "心臟位於胸腔中央偏左，這在臨床上對於心臟聽診、心電圖檢查等都很重要。",
            "boom_type": "常見錯誤",
            "emotion_response": "很多人以為心臟在左邊，其實它在中央偏左的位置！",
            "explanation": "心臟位於胸腔中央偏左的位置，不是完全在左側。",
            "image_url": "https://example.com/heart_position.png",
            "audio_snippet_url": None
        },
        {
            "question_text": "人體有多少塊骨頭？",
            "option1": "206塊",
            "option2": "186塊",
            "option3": "226塊",
            "option4": "196塊",
            "correct_answer": 1,
            "topic_tag": "骨骼系統｜骨頭數量",
            "application_case": "成人有206塊骨頭，但嬰兒有更多骨頭，因為有些骨頭會隨著成長融合。",
            "boom_type": "基礎知識",
            "emotion_response": "206塊骨頭組成了我們的身體支架，每一塊都有它的作用！",
            "explanation": "成人人體有206塊骨頭，但嬰兒有更多骨頭，因為有些骨頭會隨著成長融合。",
            "image_url": "https://example.com/skeleton_count.png",
            "audio_snippet_url": None
        },
        {
            "question_text": "大腦的主要功能是什麼？",
            "option1": "只負責思考",
            "option2": "只負責記憶",
            "option3": "控制身體所有功能",
            "option4": "只負責視覺",
            "correct_answer": 3,
            "topic_tag": "神經系統｜大腦",
            "application_case": "大腦是神經系統的中樞，控制身體的所有功能，包括思考、記憶、運動、感覺等。",
            "boom_type": "重要概念",
            "emotion_response": "大腦是我們身體的指揮中心，控制著一切！",
            "explanation": "大腦是神經系統的中樞，控制身體的所有功能，包括思考、記憶、運動、感覺等。",
            "image_url": "https://example.com/brain_functions.png",
            "audio_snippet_url": None
        },
        {
            "question_text": "肺的主要功能是什麼？",
            "option1": "消化食物",
            "option2": "過濾血液",
            "option3": "氣體交換",
            "option4": "產生血液",
            "correct_answer": 3,
            "topic_tag": "呼吸系統｜肺臟",
            "application_case": "肺的主要功能是進行氣體交換，將氧氣吸入血液，將二氧化碳排出體外。",
            "boom_type": "基礎功能",
            "emotion_response": "每一次呼吸都是肺在為我們工作，感謝它們！",
            "explanation": "肺的主要功能是進行氣體交換，將氧氣吸入血液，將二氧化碳排出體外。",
            "image_url": "https://example.com/lung_function.png",
            "audio_snippet_url": None
        }
    ]
    
    print("🚀 開始添加示例題目...")
    
    for i, question in enumerate(sample_questions, 1):
        try:
            # 插入題目到資料庫
            response = supabase.table("questions").insert(question).execute()
            
            if hasattr(response, 'data'):
                inserted_data = response.data
            else:
                inserted_data = response
            
            if inserted_data:
                print(f"✅ 成功添加第 {i} 題: {question['question_text'][:30]}...")
            else:
                print(f"❌ 添加第 {i} 題失敗")
                
        except Exception as e:
            print(f"❌ 添加第 {i} 題時發生錯誤: {e}")
    
    print("\n🎉 示例題目添加完成！")

def check_existing_questions():
    """檢查現有題目"""
    try:
        response = supabase.table("questions").select("count", count="exact").execute()
        count = response.count if hasattr(response, 'count') else len(response.data)
        print(f"📊 目前資料庫中有 {count} 個題目")
        
        # 顯示前幾個題目
        response = supabase.table("questions").select("*").limit(3).execute()
        questions = response.data if hasattr(response, 'data') else response
        
        print("\n📋 前3個題目:")
        for i, q in enumerate(questions, 1):
            print(f"  {i}. {q['question_text'][:50]}...")
            print(f"     分類: {q.get('topic_tag', '未分類')}")
            print(f"     答案: {q.get('correct_answer', 'N/A')}")
            if q.get('explanation'):
                print(f"     解釋: {q['explanation'][:50]}...")
            print()
            
    except Exception as e:
        print(f"❌ 檢查題目時發生錯誤: {e}")

def main():
    """主函數"""
    print("🔧 檢查現有題目...")
    check_existing_questions()
    
    print("\n" + "="*50)
    
    # 詢問是否要添加示例題目
    response = input("是否要添加示例題目？(y/n): ").lower().strip()
    
    if response == 'y':
        add_sample_questions()
        print("\n" + "="*50)
        print("🔧 添加後的題目狀態:")
        check_existing_questions()
    else:
        print("跳過添加示例題目")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
import os
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

def init_new_schema():
    """初始化新的資料庫結構"""
    print("🔧 初始化新的資料庫結構...")
    
    # 刪除舊的 questions 表（如果存在）
    try:
        supabase.table("questions").delete().neq("id", 0).execute()
        print("✅ 已清空舊的 questions 表")
    except Exception as e:
        print(f"⚠️ 清空舊表時出現警告: {e}")
    
    # 添加示例題目
    sample_questions = [
        {
            "question_text": "「解剖鼻煙壺」最常在什麼部位被找到？",
            "option1": "手腕外側",
            "option2": "手腕內側", 
            "option3": "手肘外側",
            "option4": "手肘內側",
            "correct_answer": 1,
            "application_case": "腕部疼痛評估時的重要解剖標記",
            "boom_type": "解剖學冷知識",
            "emotion_response": "原來手腕還有這麼有趣的地方！",
            "explanation": "解剖鼻煙壺位於手腕外側，是重要的解剖標記，用於定位橈動脈和評估腕部疼痛。",
            "difficulty": "medium",
            "topic_tag": "上肢解剖",
            "anatomy_topic": "腕部解剖",
            "tags": ["冷知識", "圖像輔助"],
            "structure_part": "上肢",
            "structure_type": "解剖標記",
            "structure_function": "定位",
            "exam_source": "108年PT國考"
        },
        {
            "question_text": "當你把大拇指伸直，鼻煙壺的邊界會由哪一組肌腱構成？",
            "option1": "伸拇長肌和伸拇短肌",
            "option2": "伸拇長肌和展拇長肌",
            "option3": "伸拇短肌和展拇短肌", 
            "option4": "伸拇長肌和展拇短肌",
            "correct_answer": 2,
            "application_case": "手部肌腱損傷的診斷",
            "boom_type": "臨床應用",
            "emotion_response": "肌腱的排列原來這麼精妙！",
            "explanation": "鼻煙壺的邊界由伸拇長肌和展拇長肌構成，這個解剖關係對於診斷手部肌腱損傷很重要。",
            "difficulty": "clinical",
            "topic_tag": "肌腱解剖",
            "anatomy_topic": "手部肌腱",
            "tags": ["臨床應用", "肌腱"],
            "structure_part": "上肢",
            "structure_type": "肌腱",
            "structure_function": "運動",
            "exam_source": "109年PT國考"
        },
        {
            "question_text": "以下哪個動作**最容易誘發鼻煙壺區域的疼痛**？",
            "option1": "握拳",
            "option2": "伸腕",
            "option3": "拇指外展",
            "option4": "拇指內收",
            "correct_answer": 3,
            "application_case": "腕部疼痛的體位檢查",
            "boom_type": "臨床技巧",
            "emotion_response": "體位檢查的奧秘！",
            "explanation": "拇指外展動作最容易誘發鼻煙壺區域的疼痛，這是診斷該區域病變的重要體位檢查。",
            "difficulty": "clinical",
            "topic_tag": "體位檢查",
            "anatomy_topic": "腕部檢查",
            "tags": ["體位檢查", "疼痛評估"],
            "structure_part": "上肢",
            "structure_type": "檢查技巧",
            "structure_function": "診斷",
            "exam_source": "110年PT國考"
        },
        {
            "question_text": "鼻煙壺下方的骨頭是？",
            "option1": "舟狀骨",
            "option2": "月狀骨",
            "option3": "三角骨",
            "option4": "豌豆骨",
            "correct_answer": 1,
            "application_case": "腕部骨折的診斷",
            "boom_type": "解剖學基礎",
            "emotion_response": "骨頭的位置關係真有趣！",
            "explanation": "鼻煙壺下方是舟狀骨，這個解剖關係對於診斷舟狀骨骨折很重要。",
            "difficulty": "medium",
            "topic_tag": "骨骼解剖",
            "anatomy_topic": "腕骨",
            "tags": ["骨骼", "骨折"],
            "structure_part": "上肢",
            "structure_type": "骨骼",
            "structure_function": "支撐",
            "exam_source": "111年PT國考"
        },
        {
            "question_text": "解剖鼻煙壺可作為下列哪一個結構的觸診標記？",
            "option1": "尺動脈",
            "option2": "橈動脈",
            "option3": "正中神經",
            "option4": "尺神經",
            "correct_answer": 2,
            "application_case": "動脈搏動的觸診",
            "boom_type": "臨床技能",
            "emotion_response": "觸診技巧的應用！",
            "explanation": "解剖鼻煙壺是觸診橈動脈的重要標記，在急救和血管評估中非常有用。",
            "difficulty": "easy",
            "topic_tag": "血管解剖",
            "anatomy_topic": "動脈觸診",
            "tags": ["觸診", "血管"],
            "structure_part": "上肢",
            "structure_type": "血管",
            "structure_function": "循環",
            "exam_source": "112年PT國考"
        }
    ]
    
    # 插入示例題目
    for i, question in enumerate(sample_questions):
        try:
            response = supabase.table("questions").insert(question).execute()
            print(f"✅ 已添加題目 {i+1}: {question['question_text'][:30]}...")
        except Exception as e:
            print(f"❌ 添加題目 {i+1} 失敗: {e}")
    
    print(f"🎉 成功初始化資料庫，添加了 {len(sample_questions)} 個示例題目")

def test_new_schema():
    """測試新的資料庫結構"""
    print("\n🧪 測試新的資料庫結構...")
    
    try:
        # 測試查詢
        response = supabase.table("questions").select("*").execute()
        questions = response.data
        
        print(f"✅ 成功查詢到 {len(questions)} 個題目")
        
        if questions:
            print("\n📝 第一個題目範例:")
            q = questions[0]
            print(f"  題目: {q['question_text']}")
            print(f"  選項1: {q['option1']}")
            print(f"  選項2: {q['option2']}")
            print(f"  選項3: {q['option3']}")
            print(f"  選項4: {q['option4']}")
            print(f"  正確答案: {q['correct_answer']}")
            print(f"  解釋: {q['explanation']}")
            print(f"  難度: {q['difficulty']}")
            print(f"  主題: {q['topic_tag']}")
            print(f"  標籤: {q['tags']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        return False

if __name__ == "__main__":
    print("🚀 開始初始化新的資料庫結構...")
    
    # 初始化
    init_new_schema()
    
    # 測試
    test_new_schema()
    
    print("\n✨ 初始化完成！") 
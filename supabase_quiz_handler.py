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

def get_questions():
    """從 Supabase 獲取所有題目"""
    print(f"🔍 進入 get_questions function", flush=True)
    try:
        print(f"🔍 get_questions: 開始從 Supabase 獲取題目", flush=True)
        
        # 查詢所有題目
        print(f"🔍 get_questions: 執行 supabase.table('questions').select('*').execute()", flush=True)
        response = supabase.table("questions").select("*").execute()
        print(f"🔍 get_questions: Supabase 查詢完成，response 類型: {type(response)}", flush=True)
        
        if hasattr(response, 'data'):
            questions_data = response.data
            print(f"🔍 get_questions: 使用 response.data，長度: {len(questions_data) if questions_data else 0}", flush=True)
        else:
            questions_data = response
            print(f"🔍 get_questions: 直接使用 response，長度: {len(questions_data) if questions_data else 0}", flush=True)
        
        if not questions_data:
            print(f"🔍 get_questions: Supabase questions 表格中沒有資料", flush=True)
            return []
        
        print(f"🔍 get_questions: 原始資料接收: {len(questions_data)} 題", flush=True)
        
        # 轉換為與原 Google Sheets 格式相容的格式
        questions = []
        for i, row in enumerate(questions_data):
            try:
                print(f"🔍 get_questions: 處理第 {i} 行資料", flush=True)
                
                # 檢查必要欄位
                if not row.get('question_text') or not row.get('option1') or not row.get('option2') or not row.get('option3') or not row.get('option4'):
                    print(f"🔍 get_questions: 第 {i} 行缺少必要欄位", flush=True)
                    continue
                
                # 檢查正確答案是否有效
                correct_answer = row.get('correct_answer')
                if not isinstance(correct_answer, int) or correct_answer < 1 or correct_answer > 4:
                    print(f"🔍 get_questions: 第 {i} 行正確答案無效: {correct_answer}", flush=True)
                    continue
                
                # 構建解釋文字，包含新的欄位資訊
                explanation_parts = []
                if row.get('explanation'):
                    explanation_parts.append(row['explanation'])
                if row.get('application_case'):
                    explanation_parts.append(f"臨床應用：{row['application_case']}")
                if row.get('boom_type'):
                    explanation_parts.append(f"💥 {row['boom_type']}")
                if row.get('emotion_response'):
                    explanation_parts.append(f"💭 {row['emotion_response']}")
                
                explanation = " | ".join(explanation_parts) if explanation_parts else ""
                
                question = {
                    'qid': row['id'],  # 直接使用 Supabase 的 id
                    'category': row.get('topic_tag', '未分類'),
                    'question': row.get('question_text', '').strip(),
                    'options': [
                        row.get('option1', '').strip(),
                        row.get('option2', '').strip(),
                        row.get('option3', '').strip(),
                        row.get('option4', '').strip()
                    ],
                    'answer': str(correct_answer),
                    'explanation': explanation,
                    # 新增欄位
                    'topic_tag': row.get('topic_tag'),
                    'application_case': row.get('application_case'),
                    'boom_type': row.get('boom_type'),
                    'emotion_response': row.get('emotion_response'),
                    'image_url': row.get('image_url'),
                    'audio_snippet_url': row.get('audio_snippet_url'),
                    'difficulty': row.get('difficulty', 'medium'),
                    'mission_group': row.get('mission_group'),
                    'variant_of': row.get('variant_of'),
                    'anatomy_topic': row.get('anatomy_topic'),
                    'tags': row.get('tags', []),
                    'structure_part': row.get('structure_part'),
                    'structure_type': row.get('structure_type'),
                    'structure_function': row.get('structure_function'),
                    'exam_source': row.get('exam_source')
                }
                questions.append(question)
                print(f"🔍 get_questions: 已添加題目: {question['question'][:50]}...", flush=True)
                
            except Exception as e:
                print(f"🛑 get_questions: 處理第 {i} 行時發生錯誤: {e}", flush=True)
                continue
        
        print(f"🔍 get_questions: 成功從 Supabase 載入 {len(questions)} 題", flush=True)
        return questions
        
    except Exception as e:
        print(f"🛑 get_questions 發生錯誤: {str(e)}", flush=True)
        import traceback
        traceback.print_exc()
        return []

def get_random_question():
    """隨機獲取一個問題"""
    print("Getting random question from Supabase...")
    questions = get_questions()
    if not questions:
        print("No questions available from Supabase, using test question")
        # 返回測試問題
        return {
            'qid': 999,
            'category': '測試',
            'question': '這是一個測試問題：人體最大的器官是什麼？',
            'options': ['心臟', '大腦', '皮膚', '肝臟'],
            'answer': '3',
            'explanation': '皮膚是人體最大的器官，佔體重的約16%。'
        }
    selected = random.choice(questions)
    print(f"Selected question: {selected['question'][:50]}...")
    return selected

def get_test_questions():
    """返回測試問題（當 Supabase 不可用時）"""
    return [
        {
            'qid': 1,
            'category': '基礎解剖',
            'question': '人體最大的器官是什麼？',
            'options': ['心臟', '大腦', '皮膚', '肝臟'],
            'answer': '3',
            'explanation': '皮膚是人體最大的器官，佔體重的約16%。'
        },
        {
            'qid': 2,
            'category': '骨骼系統',
            'question': '人體有多少塊骨頭？',
            'options': ['206塊', '186塊', '226塊', '196塊'],
            'answer': '1',
            'explanation': '成人人體有206塊骨頭。'
        },
        {
            'qid': 3,
            'category': '循環系統',
            'question': '心臟位於胸腔的哪個位置？',
            'options': ['左側', '右側', '中央偏左', '中央偏右'],
            'answer': '3',
            'explanation': '心臟位於胸腔中央偏左的位置。'
        }
    ]

# 測試函數
def test_supabase_connection():
    """測試 Supabase 連線"""
    try:
        print("Testing Supabase connection...")
        response = supabase.table("questions").select("count", count="exact").execute()
        print(f"Connection successful! Found {response.count} questions")
        return True
    except Exception as e:
        print(f"Supabase connection failed: {e}")
        return False

if __name__ == "__main__":
    # 測試連線
    if test_supabase_connection():
        questions = get_questions()
        print(f"Retrieved {len(questions)} questions")
        if questions:
            print("Sample question:")
            print(questions[0])
    else:
        print("Using test questions")
        test_questions = get_test_questions()
        print(f"Test questions: {len(test_questions)}") 
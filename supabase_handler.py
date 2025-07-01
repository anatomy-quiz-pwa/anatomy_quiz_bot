import os
import random
from datetime import date
from typing import List, Dict, Optional
from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_ANON_KEY

# 初始化 Supabase 客戶端
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

class SupabaseHandler:
    def __init__(self):
        self.supabase = supabase
    
    # ==================== 題目相關操作 ====================
    
    def get_all_questions(self) -> List[Dict]:
        """從 Supabase 獲取所有題目"""
        try:
            print("Fetching questions from Supabase...")
            response = self.supabase.table('questions').select('*').execute()
            questions = response.data
            
            # 轉換資料格式以符合現有程式
            formatted_questions = []
            for q in questions:
                formatted_question = {
                    'qid': q.get('id'),
                    'category': q.get('category', '未分類'),
                    'question': q.get('question', ''),
                    'options': [
                        q.get('option1', ''),
                        q.get('option2', ''),
                        q.get('option3', ''),
                        q.get('option4', '')
                    ],
                    'answer': str(q.get('correct_answer', 1)),
                    'explanation': q.get('explanation', '')
                }
                formatted_questions.append(formatted_question)
            
            print(f"Successfully loaded {len(formatted_questions)} questions from Supabase")
            return formatted_questions
            
        except Exception as e:
            print(f"Error fetching questions from Supabase: {str(e)}")
            return self.get_test_questions()
    
    def get_random_question(self) -> Dict:
        """隨機獲取一個題目"""
        print("Getting random question from Supabase...")
        questions = self.get_all_questions()
        if not questions:
            print("No questions available from Supabase, using test question")
            return self.get_test_question()
        
        selected = random.choice(questions)
        print(f"Selected question: {selected['question'][:50]}...")
        return selected
    
    def get_test_questions(self) -> List[Dict]:
        """返回測試問題（當 Supabase 不可用時）"""
        return [
            {
                'qid': 1,
                'category': '測試',
                'question': '人體最大的器官是什麼？',
                'options': ['心臟', '大腦', '皮膚', '肝臟'],
                'answer': '3',
                'explanation': '皮膚是人體最大的器官，佔體重的約16%。'
            },
            {
                'qid': 2,
                'category': '測試',
                'question': '人體有多少塊骨頭？',
                'options': ['206塊', '186塊', '226塊', '196塊'],
                'answer': '1',
                'explanation': '成人人體有206塊骨頭。'
            },
            {
                'qid': 3,
                'category': '測試',
                'question': '心臟位於胸腔的哪個位置？',
                'options': ['左側', '右側', '中央偏左', '中央偏右'],
                'answer': '3',
                'explanation': '心臟位於胸腔中央偏左的位置。'
            }
        ]
    
    def get_test_question(self) -> Dict:
        """返回單個測試問題"""
        return self.get_test_questions()[0]
    
    # ==================== 用戶統計相關操作 ====================
    
    def get_user_stats(self, user_id: str) -> Dict:
        """獲取用戶統計資料"""
        try:
            print(f"Fetching stats for user {user_id} from Supabase...")
            response = self.supabase.table('user_stats').select('*').eq('user_id', user_id).execute()
            
            if response.data:
                user_data = response.data[0]
                correct_qids = user_data.get('correct_qids', [])
                if isinstance(correct_qids, str):
                    # 如果是字串格式，轉換為列表
                    correct_qids = [int(q.strip()) for q in correct_qids.split(',') if q.strip().isdigit()]
                
                stats = {
                    'correct': user_data.get('correct', 0),
                    'wrong': user_data.get('wrong', 0),
                    'correct_qids': correct_qids,
                    'last_update': user_data.get('last_update', '')
                }
            else:
                # 沒有找到用戶資料，回傳預設值
                stats = {
                    'correct': 0,
                    'wrong': 0,
                    'correct_qids': [],
                    'last_update': ''
                }
            
            print(f"[DEBUG] get_user_stats for {user_id}: {stats}", flush=True)
            return stats
            
        except Exception as e:
            print(f"Error fetching user stats from Supabase: {str(e)}")
            # 回傳預設值
            return {
                'correct': 0,
                'wrong': 0,
                'correct_qids': [],
                'last_update': ''
            }
    
    def update_user_stats(self, user_id: str, correct: int, wrong: int, correct_qids: List[int]):
        """更新用戶統計資料"""
        try:
            print(f"Updating stats for user {user_id} in Supabase...")
            correct_qids_str = ','.join(str(q) for q in correct_qids)
            today = date.today().isoformat()
            
            # 檢查用戶是否已存在
            response = self.supabase.table('user_stats').select('id').eq('user_id', user_id).execute()
            
            if response.data:
                # 更新現有用戶資料
                self.supabase.table('user_stats').update({
                    'correct': correct,
                    'wrong': wrong,
                    'correct_qids': correct_qids_str,
                    'last_update': today
                }).eq('user_id', user_id).execute()
                print(f"Updated existing user stats for {user_id}")
            else:
                # 新增用戶資料
                self.supabase.table('user_stats').insert({
                    'user_id': user_id,
                    'correct': correct,
                    'wrong': wrong,
                    'correct_qids': correct_qids_str,
                    'last_update': today
                }).execute()
                print(f"Created new user stats for {user_id}")
                
        except Exception as e:
            print(f"Error updating user stats in Supabase: {str(e)}")
    
    def get_total_stats(self) -> Dict:
        """獲取總體統計資料"""
        try:
            response = self.supabase.table('user_stats').select('correct, wrong').execute()
            total_correct = sum(row.get('correct', 0) for row in response.data)
            total_wrong = sum(row.get('wrong', 0) for row in response.data)
            
            return {
                'total_correct': total_correct,
                'total_wrong': total_wrong,
                'total_attempts': total_correct + total_wrong
            }
        except Exception as e:
            print(f"Error fetching total stats from Supabase: {str(e)}")
            return {
                'total_correct': 0,
                'total_wrong': 0,
                'total_attempts': 0
            }

# 建立全域實例
supabase_handler = SupabaseHandler() 
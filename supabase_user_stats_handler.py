import os
from datetime import date
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

def safe_int(val):
    """安全地轉換為整數"""
    try:
        return int(val)
    except (ValueError, TypeError):
        return 0

def get_user_stats(user_id):
    """從 Supabase 獲取用戶統計資料"""
    try:
        print(f"Getting user stats for {user_id} from Supabase...")
        
        # 查詢用戶統計資料
        response = supabase.table("user_stats").select("*").eq("user_id", user_id).execute()
        
        if hasattr(response, 'data'):
            user_data = response.data
        else:
            user_data = response
        
        if user_data and len(user_data) > 0:
            user_row = user_data[0]
            
            # 解析正確題目ID列表
            correct_qids = []
            correct_qids_str = user_row.get('correct_qids', '')
            if correct_qids_str:
                for qid in correct_qids_str.split(','):
                    try:
                        correct_qids.append(int(qid.strip()))
                    except (ValueError, TypeError):
                        pass  # 忽略非數字內容
            
            stats = {
                'correct': safe_int(user_row.get('correct', 0)),
                'wrong': safe_int(user_row.get('wrong', 0)),
                'correct_qids': correct_qids,
                'last_update': user_row.get('last_update', '')
            }
            print(f"[DEBUG] get_user_stats for {user_id}: {stats}", flush=True)
            return stats
        else:
            # 沒有找到用戶資料，回傳預設值
            stats = {
                'correct': 0,
                'wrong': 0,
                'correct_qids': [],
                'last_update': ''
            }
            print(f"[DEBUG] get_user_stats for {user_id}: {stats} (new user)", flush=True)
            return stats
            
    except Exception as e:
        print(f"Error getting user stats from Supabase: {str(e)}")
        import traceback
        traceback.print_exc()
        # 回傳預設值
        stats = {
            'correct': 0,
            'wrong': 0,
            'correct_qids': [],
            'last_update': ''
        }
        return stats

def update_user_stats(user_id, correct, wrong, correct_qids):
    """更新用戶統計資料到 Supabase"""
    try:
        print(f"Updating user stats for {user_id} in Supabase...")
        print(f"[DEBUG] update_user_stats: correct_qids = {correct_qids}", flush=True)
        
        # 準備資料
        correct_qids_str = ','.join(str(q) for q in correct_qids)
        today = date.today().isoformat()
        
        # 檢查用戶是否已存在
        response = supabase.table("user_stats").select("id").eq("user_id", user_id).execute()
        
        if hasattr(response, 'data'):
            existing_data = response.data
        else:
            existing_data = response
        
        if existing_data and len(existing_data) > 0:
            # 更新現有用戶資料
            user_id_in_db = existing_data[0]['id']
            update_data = {
                'correct': correct,
                'wrong': wrong,
                'correct_qids': correct_qids_str,
                'last_update': today
            }
            
            response = supabase.table("user_stats").update(update_data).eq("id", user_id_in_db).execute()
            print(f"Updated existing user stats for {user_id}")
            
        else:
            # 新增用戶資料
            new_data = {
                'user_id': user_id,
                'correct': correct,
                'wrong': wrong,
                'correct_qids': correct_qids_str,
                'last_update': today
            }
            
            response = supabase.table("user_stats").insert(new_data).execute()
            print(f"Created new user stats for {user_id}")
        
        return True
        
    except Exception as e:
        print(f"Error updating user stats in Supabase: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def add_correct_answer(user_id, question_id=None):
    """為用戶添加一個正確答案"""
    try:
        print(f"Adding correct answer for user {user_id}, question_id: {question_id}")
        print(f"[DEBUG] add_correct_answer: question_id = {question_id}", flush=True)
        
        # 獲取當前用戶統計
        current_stats = get_user_stats(user_id)
        
        # 更新統計資料
        new_correct = current_stats['correct'] + 1
        new_wrong = current_stats['wrong']
        new_correct_qids = current_stats['correct_qids'].copy()  # 複製列表避免修改原列表
        
        # 如果有 question_id，添加到正確題目列表中
        print(f"[DEBUG] add_correct_answer: 檢查 question_id={question_id}, 當前 correct_qids={new_correct_qids}", flush=True)
        if question_id is not None and question_id not in new_correct_qids:
            new_correct_qids.append(question_id)
            print(f"[DEBUG] add_correct_answer: 已添加 question_id={question_id} 到 correct_qids", flush=True)
        else:
            print(f"[DEBUG] add_correct_answer: question_id={question_id} 已存在或為 None，不添加", flush=True)
        
        # 更新到資料庫
        success = update_user_stats(user_id, new_correct, new_wrong, new_correct_qids)
        
        if success:
            print(f"Successfully added correct answer for user {user_id}")
        else:
            print(f"Failed to add correct answer for user {user_id}")
            
        return success
        
    except Exception as e:
        print(f"🛑 add_correct_answer 發生錯誤：{e}")
        import traceback
        traceback.print_exc()
        return False

def add_wrong_answer(user_id):
    """為用戶添加一個錯誤答案"""
    try:
        print(f"Adding wrong answer for user {user_id}")
        
        # 獲取當前用戶統計
        current_stats = get_user_stats(user_id)
        
        # 更新統計資料
        new_correct = current_stats['correct']
        new_wrong = current_stats['wrong'] + 1
        new_correct_qids = current_stats['correct_qids']  # 保持不變
        
        # 更新到資料庫
        success = update_user_stats(user_id, new_correct, new_wrong, new_correct_qids)
        
        if success:
            print(f"Successfully added wrong answer for user {user_id}")
        else:
            print(f"Failed to add wrong answer for user {user_id}")
            
        return success
        
    except Exception as e:
        print(f"🛑 add_wrong_answer 發生錯誤：{e}")
        import traceback
        traceback.print_exc()
        return False

def get_all_user_stats():
    """獲取所有用戶統計資料（用於管理員功能）"""
    try:
        print("Getting all user stats from Supabase...")
        
        response = supabase.table("user_stats").select("*").execute()
        
        if hasattr(response, 'data'):
            all_stats = response.data
        else:
            all_stats = response
        
        print(f"Retrieved {len(all_stats)} user stats")
        return all_stats
        
    except Exception as e:
        print(f"Error getting all user stats: {str(e)}")
        return []

def reset_user_stats(user_id):
    """重置用戶統計資料（完全歸零）"""
    try:
        print(f"Resetting user stats for {user_id} in Supabase...")
        
        # 刪除用戶的統計資料
        response = supabase.table("user_stats").delete().eq("user_id", user_id).execute()
        
        print(f"Successfully reset user stats for {user_id}")
        return True
        
    except Exception as e:
        print(f"Error resetting user stats for {user_id}: {e}")
        return False

# 測試函數
def test_supabase_user_stats():
    """測試 Supabase 用戶統計功能"""
    try:
        print("Testing Supabase user stats functionality...")
        
        # 測試獲取用戶統計
        test_user_id = "test_user_123"
        stats = get_user_stats(test_user_id)
        print(f"Initial stats for {test_user_id}: {stats}")
        
        # 測試添加正確答案
        success = add_correct_answer(test_user_id)
        print(f"Add correct answer success: {success}")
        
        # 再次獲取統計
        updated_stats = get_user_stats(test_user_id)
        print(f"Updated stats for {test_user_id}: {updated_stats}")
        
        return True
        
    except Exception as e:
        print(f"Supabase user stats test failed: {e}")
        return False

if __name__ == "__main__":
    # 測試功能
    if test_supabase_user_stats():
        print("Supabase user stats test passed!")
    else:
        print("Supabase user stats test failed!") 
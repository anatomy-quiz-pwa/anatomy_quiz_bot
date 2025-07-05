import os
from datetime import date
from supabase import create_client, Client
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 初始化 Supabase 客戶端
SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "").strip()

# 防呆驗證
print(f"[DEBUG] Render 實際讀到的 URL: {repr(SUPABASE_URL)}")
print(f"[DEBUG] Render 實際讀到的 KEY: {repr(SUPABASE_ANON_KEY[:20] if SUPABASE_ANON_KEY else 'None')}...")

if any(c in SUPABASE_URL for c in ["\n", "\r", " ", "\t"]):
    raise ValueError(f"❌ SUPABASE_URL 含有非法字元：{repr(SUPABASE_URL)}")

if any(c in SUPABASE_ANON_KEY for c in ["\n", "\r", " ", "\t"]):
    raise ValueError(f"❌ SUPABASE_ANON_KEY 含有非法字元：{repr(SUPABASE_ANON_KEY[:20])}...")

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
    print(f"🔍 進入 get_user_stats function - user_id: {user_id}", flush=True)
    print(f"[DEBUG] 使用 SUPABASE_URL: {repr(SUPABASE_URL)}", flush=True)
    try:
        print(f"🔍 get_user_stats: 開始查詢 Supabase...", flush=True)
        
        # 查詢用戶統計資料
        print(f"🔍 get_user_stats: 執行 supabase.table('user_stats').select('*').eq('user_id', {user_id}).execute()", flush=True)
        response = supabase.table("user_stats").select("*").eq("user_id", user_id).execute()
        print(f"🔍 get_user_stats: Supabase 查詢完成，response 類型: {type(response)}", flush=True)
        
        if hasattr(response, 'data'):
            user_data = response.data
            print(f"🔍 get_user_stats: 使用 response.data，長度: {len(user_data) if user_data else 0}", flush=True)
        else:
            user_data = response
            print(f"🔍 get_user_stats: 直接使用 response，長度: {len(user_data) if user_data else 0}", flush=True)
        
        if user_data and len(user_data) > 0:
            user_row = user_data[0]
            print(f"🔍 get_user_stats: 找到用戶資料: {user_row}", flush=True)
            
            # 解析正確題目ID列表
            correct_qids = []
            correct_qids_str = user_row.get('correct_qids', '')
            print(f"🔍 get_user_stats: correct_qids_str = '{correct_qids_str}'", flush=True)
            
            # 防呆：若錯誤為字串型態（如 "EMPTY"），強制轉為空陣列
            if isinstance(correct_qids_str, str) and correct_qids_str.strip().upper() in ['EMPTY', 'NULL', 'NONE', '']:
                correct_qids = []
                print(f"🔍 get_user_stats: 檢測到特殊字串 '{correct_qids_str}'，強制轉為空陣列", flush=True)
            elif correct_qids_str:
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
            print(f"🔍 get_user_stats: 成功返回統計資料: {stats}", flush=True)
            return stats
        else:
            # 沒有找到用戶資料，回傳預設值
            stats = {
                'correct': 0,
                'wrong': 0,
                'correct_qids': [],
                'last_update': ''
            }
            print(f"🔍 get_user_stats: 新用戶，返回預設統計資料: {stats}", flush=True)
            return stats
            
    except Exception as e:
        print(f"🛑 get_user_stats 發生錯誤: {str(e)}", flush=True)
        import traceback
        traceback.print_exc()
        # 回傳預設值
        stats = {
            'correct': 0,
            'wrong': 0,
            'correct_qids': [],
            'last_update': ''
        }
        print(f"🔍 get_user_stats: 錯誤後返回預設統計資料: {stats}", flush=True)
        return stats

def update_user_stats(user_id, correct, wrong, correct_qids):
    """更新用戶統計資料到 Supabase"""
    print(f"🔍 進入 update_user_stats function - user_id: {user_id}, correct: {correct}, wrong: {wrong}", flush=True)
    try:
        print(f"🔍 update_user_stats: 開始更新用戶統計", flush=True)
        print(f"🔍 update_user_stats: correct_qids = {correct_qids}", flush=True)
        
        # 準備資料
        correct_qids_str = ','.join(str(q) for q in correct_qids)
        today = date.today().isoformat()
        print(f"🔍 update_user_stats: correct_qids_str = '{correct_qids_str}', today = '{today}'", flush=True)
        
        # 檢查用戶是否已存在
        print(f"🔍 update_user_stats: 檢查用戶是否存在", flush=True)
        response = supabase.table("user_stats").select("id").eq("user_id", user_id).execute()
        print(f"🔍 update_user_stats: 查詢用戶存在性完成，response 類型: {type(response)}", flush=True)
        
        if hasattr(response, 'data'):
            existing_data = response.data
            print(f"🔍 update_user_stats: 使用 response.data，長度: {len(existing_data) if existing_data else 0}", flush=True)
        else:
            existing_data = response
            print(f"🔍 update_user_stats: 直接使用 response，長度: {len(existing_data) if existing_data else 0}", flush=True)
        
        if existing_data and len(existing_data) > 0:
            # 更新現有用戶資料
            user_id_in_db = existing_data[0]['id']
            update_data = {
                'correct': correct,
                'wrong': wrong,
                'correct_qids': correct_qids_str,
                'last_update': today
            }
            print(f"🔍 update_user_stats: 更新現有用戶資料，id={user_id_in_db}, data={update_data}", flush=True)
            
            response = supabase.table("user_stats").update(update_data).eq("id", user_id_in_db).execute()
            print(f"🔍 update_user_stats: 成功更新現有用戶統計 {user_id}", flush=True)
            
        else:
            # 新增用戶資料
            new_data = {
                'user_id': user_id,
                'correct': correct,
                'wrong': wrong,
                'correct_qids': correct_qids_str,
                'last_update': today
            }
            print(f"🔍 update_user_stats: 新增用戶資料: {new_data}", flush=True)
            
            response = supabase.table("user_stats").insert(new_data).execute()
            print(f"🔍 update_user_stats: 成功創建新用戶統計 {user_id}", flush=True)
        
        return True
        
    except Exception as e:
        print(f"🛑 update_user_stats 發生錯誤: {str(e)}", flush=True)
        import traceback
        traceback.print_exc()
        return False

def add_correct_answer(user_id, question_id=None):
    """為用戶添加一個正確答案"""
    print(f"🔍 進入 add_correct_answer function - user_id: {user_id}, question_id: {question_id}", flush=True)
    try:
        print(f"🔍 add_correct_answer: 開始處理正確答案", flush=True)
        
        # 獲取當前用戶統計
        print(f"🔍 add_correct_answer: 準備獲取當前用戶統計", flush=True)
        current_stats = get_user_stats(user_id)
        print(f"🔍 add_correct_answer: 當前統計 = {current_stats}", flush=True)
        
        # 更新統計資料
        new_correct = current_stats['correct'] + 1
        new_wrong = current_stats['wrong']
        new_correct_qids = current_stats['correct_qids'].copy()  # 複製列表避免修改原列表
        
        print(f"🔍 add_correct_answer: 更新統計 - new_correct={new_correct}, new_wrong={new_wrong}", flush=True)
        
        # 允許題目重複出現，不再記錄具體的題目 ID
        print(f"🔍 add_correct_answer: 題目重複模式，不記錄 question_id={question_id}", flush=True)
        # 保持 correct_qids 為空列表，只記錄總答對次數
        new_correct_qids = []
        
        # 更新到資料庫
        print(f"🔍 add_correct_answer: 準備更新資料庫", flush=True)
        success = update_user_stats(user_id, new_correct, new_wrong, new_correct_qids)
        
        if success:
            print(f"🔍 add_correct_answer: 成功添加正確答案給用戶 {user_id}", flush=True)
        else:
            print(f"🛑 add_correct_answer: 添加正確答案失敗，用戶 {user_id}", flush=True)
            
        return success
        
    except Exception as e:
        print(f"🛑 add_correct_answer 發生錯誤：{e}", flush=True)
        import traceback
        traceback.print_exc()
        return False

def add_wrong_answer(user_id):
    """為用戶添加一個錯誤答案"""
    print(f"🔍 進入 add_wrong_answer function - user_id: {user_id}", flush=True)
    try:
        print(f"🔍 add_wrong_answer: 開始處理錯誤答案", flush=True)
        
        # 獲取當前用戶統計
        print(f"🔍 add_wrong_answer: 準備獲取當前用戶統計", flush=True)
        current_stats = get_user_stats(user_id)
        print(f"🔍 add_wrong_answer: 當前統計 = {current_stats}", flush=True)
        
        # 更新統計資料
        new_correct = current_stats['correct']
        new_wrong = current_stats['wrong'] + 1
        new_correct_qids = current_stats['correct_qids']  # 保持不變
        
        print(f"🔍 add_wrong_answer: 更新統計 - new_correct={new_correct}, new_wrong={new_wrong}", flush=True)
        
        # 更新到資料庫
        print(f"🔍 add_wrong_answer: 準備更新資料庫", flush=True)
        success = update_user_stats(user_id, new_correct, new_wrong, new_correct_qids)
        
        if success:
            print(f"🔍 add_wrong_answer: 成功添加錯誤答案給用戶 {user_id}", flush=True)
        else:
            print(f"🛑 add_wrong_answer: 添加錯誤答案失敗，用戶 {user_id}", flush=True)
            
        return success
        
    except Exception as e:
        print(f"🛑 add_wrong_answer 發生錯誤：{e}", flush=True)
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
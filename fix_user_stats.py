#!/usr/bin/env python3
"""
修正用戶統計中的 correct_qids 資料
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

def fix_user_stats():
    """修正用戶統計資料"""
    print("🔧 修正用戶統計資料...")
    
    try:
        # 獲取所有用戶統計
        response = supabase.table("user_stats").select("*").execute()
        
        if hasattr(response, 'data'):
            user_stats_data = response.data
        else:
            user_stats_data = response
        
        print(f"📊 找到 {len(user_stats_data)} 個用戶統計")
        
        for user_stat in user_stats_data:
            user_id = user_stat['user_id']
            correct_qids_str = user_stat.get('correct_qids', '')
            
            print(f"\n👤 處理用戶: {user_id}")
            print(f"   原始 correct_qids: {correct_qids_str}")
            
            # 檢查 correct_qids 是否包含無效的 ID
            if correct_qids_str:
                qids = []
                for qid_str in correct_qids_str.split(','):
                    try:
                        qid = int(qid_str.strip())
                        # 檢查這個 ID 是否在實際題目中存在
                        question_response = supabase.table("questions").select("id").eq("id", qid).execute()
                        if hasattr(question_response, 'data'):
                            question_data = question_response.data
                        else:
                            question_data = question_response
                        
                        if question_data:
                            qids.append(qid)
                            print(f"   ✅ 保留有效題目 ID: {qid}")
                        else:
                            print(f"   ❌ 移除無效題目 ID: {qid}")
                    except (ValueError, TypeError):
                        print(f"   ❌ 移除無效格式: {qid_str}")
                
                # 更新為有效的題目 ID
                new_correct_qids_str = ','.join(str(q) for q in qids)
                
                if new_correct_qids_str != correct_qids_str:
                    print(f"   更新 correct_qids: {new_correct_qids_str}")
                    
                    # 更新資料庫
                    update_data = {
                        'correct_qids': new_correct_qids_str
                    }
                    
                    supabase.table("user_stats").update(update_data).eq("user_id", user_id).execute()
                    print(f"   ✅ 已更新用戶 {user_id} 的 correct_qids")
                else:
                    print(f"   ✅ 用戶 {user_id} 的 correct_qids 無需修正")
            else:
                print(f"   ✅ 用戶 {user_id} 沒有 correct_qids，無需修正")
        
        print("\n✅ 用戶統計修正完成！")
        
    except Exception as e:
        print(f"❌ 修正用戶統計時發生錯誤: {e}")
        import traceback
        traceback.print_exc()

def reset_test_user():
    """重置測試用戶的統計資料"""
    print("\n🔄 重置測試用戶統計...")
    
    try:
        test_user_id = "test_user_123"
        
        # 刪除測試用戶的統計資料
        response = supabase.table("user_stats").delete().eq("user_id", test_user_id).execute()
        print(f"✅ 已刪除測試用戶 {test_user_id} 的統計資料")
        
        # 創建新的統計資料
        new_stats = {
            'user_id': test_user_id,
            'correct': 0,
            'wrong': 0,
            'correct_qids': '',
            'last_update': '2025-07-01'
        }
        
        response = supabase.table("user_stats").insert(new_stats).execute()
        print(f"✅ 已創建測試用戶 {test_user_id} 的新統計資料")
        
    except Exception as e:
        print(f"❌ 重置測試用戶時發生錯誤: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 開始修正用戶統計資料...")
    
    # 修正用戶統計
    fix_user_stats()
    
    # 重置測試用戶
    reset_test_user()
    
    print("\n✅ 所有修正完成！") 
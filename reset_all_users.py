#!/usr/bin/env python3
"""
重置所有用戶進度腳本
直接清空所有用戶的 correct_qids
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client

# 載入環境變數
load_dotenv()

# 初始化 Supabase 客戶端
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")
supabase: Client = create_client(url, key)

def reset_all_users_progress():
    """重置所有用戶的進度"""
    try:
        print("🔄 正在重置所有用戶的進度...")
        
        # 先獲取所有用戶
        users_result = supabase.table('user_stats').select('user_id').execute()
        
        if not users_result.data:
            print("📊 目前沒有用戶統計資料")
            return True
        
        print(f"找到 {len(users_result.data)} 個用戶")
        
        # 逐個更新每個用戶的 correct_qids
        updated_count = 0
        for user in users_result.data:
            user_id = user.get('user_id')
            if user_id:
                try:
                    result = supabase.table('user_stats').update({
                        'correct_qids': []
                    }).eq('user_id', user_id).execute()
                    
                    if result.data:
                        updated_count += 1
                        print(f"✅ 已重置用戶 {user_id} 的進度")
                except Exception as e:
                    print(f"❌ 重置用戶 {user_id} 時發生錯誤: {e}")
        
        print(f"\n✅ 成功重置 {updated_count} 個用戶的進度")
        
        # 顯示重置後的狀態
        print("\n📊 重置後的用戶統計:")
        print("-" * 60)
        final_result = supabase.table('user_stats').select('*').execute()
        for user in final_result.data:
            user_id = user.get('user_id', 'N/A')
            correct = user.get('correct', 0)
            wrong = user.get('wrong', 0)
            correct_qids = user.get('correct_qids', [])
            print(f"用戶: {user_id}")
            print(f"  正確: {correct}, 錯誤: {wrong}")
            print(f"  已答對題目: {correct_qids}")
            print("-" * 60)
        
        return True
            
    except Exception as e:
        print(f"❌ 重置所有用戶進度時發生錯誤: {e}")
        return False

if __name__ == "__main__":
    print("🔄 用戶進度重置工具")
    print("=" * 50)
    
    # 直接重置所有用戶
    reset_all_users_progress()
    
    print("\n✅ 重置完成！現在可以重新測試題目了。") 
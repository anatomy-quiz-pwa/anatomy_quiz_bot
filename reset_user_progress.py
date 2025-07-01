#!/usr/bin/env python3
"""
重置用戶進度腳本
清空用戶的 correct_qids，讓用戶可以重新回答所有題目
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

def reset_user_progress(user_id: str):
    """重置指定用戶的進度"""
    try:
        # 更新用戶統計，清空 correct_qids
        result = supabase.table('user_stats').update({
            'correct_qids': []
        }).eq('user_id', user_id).execute()
        
        if result.data:
            print(f"✅ 成功重置用戶 {user_id} 的進度")
            print(f"   已清空 correct_qids")
            return True
        else:
            print(f"❌ 用戶 {user_id} 不存在或重置失敗")
            return False
            
    except Exception as e:
        print(f"❌ 重置用戶 {user_id} 進度時發生錯誤: {e}")
        return False

def reset_all_users_progress():
    """重置所有用戶的進度"""
    try:
        # 更新所有用戶統計，清空 correct_qids
        result = supabase.table('user_stats').update({
            'correct_qids': []
        }).execute()
        
        if result.data:
            print(f"✅ 成功重置所有用戶的進度")
            print(f"   已清空 {len(result.data)} 個用戶的 correct_qids")
            return True
        else:
            print(f"❌ 重置所有用戶進度失敗")
            return False
            
    except Exception as e:
        print(f"❌ 重置所有用戶進度時發生錯誤: {e}")
        return False

def show_user_stats():
    """顯示所有用戶的統計資訊"""
    try:
        result = supabase.table('user_stats').select('*').execute()
        
        if result.data:
            print(f"\n📊 當前用戶統計 (共 {len(result.data)} 個用戶):")
            print("-" * 60)
            for user in result.data:
                user_id = user.get('user_id', 'N/A')
                correct = user.get('correct', 0)
                wrong = user.get('wrong', 0)
                correct_qids = user.get('correct_qids', [])
                print(f"用戶: {user_id}")
                print(f"  正確: {correct}, 錯誤: {wrong}")
                print(f"  已答對題目: {correct_qids}")
                print("-" * 60)
        else:
            print("📊 目前沒有用戶統計資料")
            
    except Exception as e:
        print(f"❌ 獲取用戶統計時發生錯誤: {e}")

if __name__ == "__main__":
    print("🔄 用戶進度重置工具")
    print("=" * 50)
    
    # 顯示當前狀態
    show_user_stats()
    
    print("\n請選擇操作:")
    print("1. 重置特定用戶進度")
    print("2. 重置所有用戶進度")
    print("3. 只顯示統計資訊")
    
    choice = input("\n請輸入選項 (1/2/3): ").strip()
    
    if choice == "1":
        user_id = input("請輸入要重置的用戶ID: ").strip()
        if user_id:
            reset_user_progress(user_id)
        else:
            print("❌ 用戶ID不能為空")
    
    elif choice == "2":
        confirm = input("確定要重置所有用戶的進度嗎？(y/N): ").strip().lower()
        if confirm == 'y':
            reset_all_users_progress()
        else:
            print("❌ 操作已取消")
    
    elif choice == "3":
        print("✅ 操作完成")
    
    else:
        print("❌ 無效的選項")
    
    # 顯示重置後的狀態
    print("\n" + "=" * 50)
    show_user_stats() 
#!/usr/bin/env python3
"""
檢查用戶統計數據
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import SUPABASE_URL, SUPABASE_ANON_KEY
from supabase import create_client, Client

# 初始化 Supabase 客戶端
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def check_user_stats(user_id):
    """檢查特定用戶的統計數據"""
    try:
        # 查詢用戶統計
        response = supabase.table('user_stats').select('*').eq('user_id', user_id).execute()
        
        if response.data:
            stats = response.data[0]
            print(f"用戶 {user_id} 的統計數據:")
            print(f"  正確答案數: {stats['correct']}")
            print(f"  錯誤答案數: {stats['wrong']}")
            print(f"  正確題目ID: {stats['correct_qids']}")
            print(f"  最後更新: {stats['last_update']}")
        else:
            print(f"用戶 {user_id} 沒有統計數據")
            
        # 查詢今日答題記錄
        from datetime import datetime
        today = datetime.now().strftime('%Y-%m-%d')
        
        daily_response = supabase.table('user_daily').select('*').eq('user_id', user_id).eq('date', today).execute()
        
        if daily_response.data:
            daily = daily_response.data[0]
            print(f"\n今日答題記錄:")
            print(f"  今日答題數: {daily['today_count']}")
            print(f"  日期: {daily['date']}")
        else:
            print(f"\n今日沒有答題記錄")
            
    except Exception as e:
        print(f"查詢失敗: {e}")

def list_all_users():
    """列出所有用戶的統計數據"""
    try:
        response = supabase.table('user_stats').select('*').execute()
        
        print("所有用戶統計數據:")
        for user in response.data:
            print(f"  用戶 {user['user_id']}: 正確 {user['correct']}, 錯誤 {user['wrong']}")
            
    except Exception as e:
        print(f"查詢失敗: {e}")

if __name__ == "__main__":
    # 檢查你的真實用戶
    real_user_id = "U977c24d1fec3a2bf07035504e1444911"
    check_user_stats(real_user_id)
    
    print("\n" + "="*50 + "\n")
    
    # 列出所有用戶
    list_all_users() 
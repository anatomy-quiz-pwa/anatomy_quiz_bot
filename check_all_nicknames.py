#!/usr/bin/env python3
"""
檢查所有用戶的暱稱記錄
"""
import os
from supabase import create_client, Client
import json

# Supabase 配置
SUPABASE_URL = "https://ciqlfqfgzqqgdrogedxg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA"

def main():
    print("🔍 檢查所有用戶的暱稱記錄...")
    
    try:
        # 創建 Supabase 客戶端
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Supabase 連接成功")
        
        # 1. 查找所有有暱稱的用戶
        print("\n📋 步驟1: 查找所有有暱稱的用戶...")
        users_response = supabase.table('users').select('line_user_id, game_nickname').not_.is_('game_nickname', 'null').execute()
        
        print(f"✅ 找到 {len(users_response.data)} 個有暱稱的用戶:")
        for user in users_response.data:
            user_id = user.get('line_user_id', 'Unknown')
            nickname = user.get('game_nickname', 'None')
            print(f"   - {user_id}: {nickname}")
        
        # 2. 查找包含「濛」字的暱稱
        print(f"\n🔍 步驟2: 查找包含「濛」字的暱稱...")
        meng_users = [user for user in users_response.data if user.get('game_nickname') and '濛' in user.get('game_nickname')]
        
        if meng_users:
            print(f"✅ 找到 {len(meng_users)} 個包含「濛」字的暱稱:")
            for user in meng_users:
                user_id = user.get('line_user_id')
                nickname = user.get('game_nickname')
                print(f"   - {user_id}: {nickname}")
                
                # 檢查該用戶的統計資料
                stats_response = supabase.table('user_stats').select('*').eq('user_id', user_id).execute()
                if stats_response.data:
                    stats = stats_response.data[0]
                    correct = stats.get('correct', 0)
                    wrong = stats.get('wrong', 0)
                    level = stats.get('level', 1)
                    print(f"     📊 統計: 答對{correct}題, 答錯{wrong}題, 等級{level}")
                else:
                    print(f"     📊 沒有統計資料")
        else:
            print("❌ 沒有找到包含「濛」字的暱稱")
        
        # 3. 查找包含「小」字的暱稱
        print(f"\n🔍 步驟3: 查找包含「小」字的暱稱...")
        xiao_users = [user for user in users_response.data if user.get('game_nickname') and '小' in user.get('game_nickname')]
        
        if xiao_users:
            print(f"✅ 找到 {len(xiao_users)} 個包含「小」字的暱稱:")
            for user in xiao_users:
                user_id = user.get('line_user_id')
                nickname = user.get('game_nickname')
                print(f"   - {user_id}: {nickname}")
                
                # 檢查該用戶的統計資料
                stats_response = supabase.table('user_stats').select('*').eq('user_id', user_id).execute()
                if stats_response.data:
                    stats = stats_response.data[0]
                    correct = stats.get('correct', 0)
                    wrong = stats.get('wrong', 0)
                    level = stats.get('level', 1)
                    print(f"     📊 統計: 答對{correct}題, 答錯{wrong}題, 等級{level}")
                else:
                    print(f"     📊 沒有統計資料")
        
        # 4. 查找最近有活動的用戶統計
        print(f"\n📊 步驟4: 查找最近有活動的用戶統計...")
        recent_stats = supabase.table('user_stats').select('*').gt('correct', 0).order('last_update', desc=True).limit(10).execute()
        
        print(f"✅ 最近有活動的前10個用戶:")
        for i, stats in enumerate(recent_stats.data, 1):
            user_id = stats.get('user_id')
            correct = stats.get('correct', 0)
            wrong = stats.get('wrong', 0)
            level = stats.get('level', 1)
            last_update = stats.get('last_update', 'Unknown')
            
            # 查找該用戶的暱稱
            user_response = supabase.table('users').select('game_nickname').eq('line_user_id', user_id).execute()
            nickname = user_response.data[0].get('game_nickname') if user_response.data else '無暱稱'
            
            print(f"   {i}. {user_id} ({nickname}): 答對{correct}題, 答錯{wrong}題, 等級{level}, 最後更新: {last_update}")
        
    except Exception as e:
        print(f"❌ 檢查過程中發生錯誤: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

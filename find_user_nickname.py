#!/usr/bin/env python3
"""
查找用户昵称
"""

import os
from supabase import create_client, Client

# Supabase 配置
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://ciqlfqfgzqqgdrogedxg.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA')

def find_user_nickname():
    """查找用户昵称"""
    try:
        # 创建 Supabase 客户端
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        print("🔍 查找所有用户昵称...")
        
        # 获取所有用户数据
        response = supabase.table('users').select('line_user_id, game_nickname, display_name').execute()
        
        if response.data:
            print(f"✅ 找到 {len(response.data)} 个用户")
            print("\n📊 所有用户昵称:")
            for i, user in enumerate(response.data):
                game_nickname = user.get('game_nickname', 'N/A')
                display_name = user.get('display_name', 'N/A')
                line_user_id = user.get('line_user_id', 'N/A')
                print(f"  {i+1}. 游戏昵称: '{game_nickname}' | 显示名称: '{display_name}' | 用户ID: {line_user_id}")
                
            # 查找包含 "保" 的昵称
            print("\n🔍 查找包含 '保' 的昵称:")
            for user in response.data:
                game_nickname = user.get('game_nickname', '')
                if '保' in game_nickname:
                    print(f"  ✅ 找到: '{game_nickname}' (用户ID: {user.get('line_user_id')})")
                    
        else:
            print("❌ 没有找到任何用户")
            
    except Exception as e:
        print(f"❌ 错误: {e}")

if __name__ == "__main__":
    find_user_nickname()

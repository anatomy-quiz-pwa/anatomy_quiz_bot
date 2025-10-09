#!/usr/bin/env python3
"""
测试用户昵称是否存在
"""

import os
from supabase import create_client, Client

# Supabase 配置
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://ciqlfqfgzqqgdrogedxg.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA')

def test_user_nickname():
    """测试用户昵称"""
    try:
        # 创建 Supabase 客户端
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # 测试昵称
        test_nicknames = ['保保', '寶', '寶寶', 'Bao', 'bao']
        
        print("🔍 检查用户昵称...")
        
        for nickname in test_nicknames:
            print(f"\n📝 检查昵称: {nickname}")
            
            # 查询用户
            response = supabase.table('users').select('*').eq('nickname', nickname).execute()
            
            if response.data:
                print(f"✅ 找到用户: {response.data[0]}")
            else:
                print(f"❌ 未找到昵称为 '{nickname}' 的用户")
        
        # 显示所有用户
        print("\n📊 所有用户列表:")
        all_users = supabase.table('users').select('user_id, nickname, line_id').execute()
        
        if all_users.data:
            for user in all_users.data:
                print(f"  - 昵称: {user.get('nickname', 'N/A')}, 用户ID: {user.get('user_id', 'N/A')}")
        else:
            print("❌ 没有找到任何用户")
            
    except Exception as e:
        print(f"❌ 错误: {e}")

if __name__ == "__main__":
    test_user_nickname()

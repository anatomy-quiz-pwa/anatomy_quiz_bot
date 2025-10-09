#!/usr/bin/env python3
"""
检查 users 表结构
"""

import os
from supabase import create_client, Client

# Supabase 配置
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://ciqlfqfgzqqgdrogedxg.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA')

def check_users_table():
    """检查 users 表结构"""
    try:
        # 创建 Supabase 客户端
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        print("🔍 检查 users 表...")
        
        # 获取所有用户数据
        response = supabase.table('users').select('*').limit(5).execute()
        
        if response.data:
            print(f"✅ 找到 {len(response.data)} 个用户")
            print("\n📊 用户数据结构:")
            for i, user in enumerate(response.data):
                print(f"  用户 {i+1}: {user}")
        else:
            print("❌ 没有找到任何用户")
            
        # 尝试不同的字段名
        print("\n🔍 尝试不同的字段名...")
        
        # 检查可能的字段名
        possible_fields = ['nickname', 'name', 'display_name', 'user_name', 'line_name']
        
        for field in possible_fields:
            try:
                response = supabase.table('users').select(field).limit(1).execute()
                print(f"✅ 字段 '{field}' 存在")
            except Exception as e:
                print(f"❌ 字段 '{field}' 不存在: {e}")
                
    except Exception as e:
        print(f"❌ 错误: {e}")

if __name__ == "__main__":
    check_users_table()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試排行榜 Supabase 連接
"""

import os
from supabase import create_client, Client

# Supabase 配置
SUPABASE_URL = 'https://ciqlfqfgzqqgdrogedxg.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA'

print("🔍 測試排行榜 Supabase 連接...")
print("=" * 60)

# 1. 測試 Supabase 連接
print("\n1️⃣ 測試 Supabase 連接...")
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Supabase 客戶端創建成功")
except Exception as e:
    print(f"❌ Supabase 客戶端創建失敗: {e}")
    exit(1)

# 2. 測試 user_stats 表
print("\n2️⃣ 測試 user_stats 表...")
try:
    response = supabase.table('user_stats').select('*').limit(5).execute()
    if response.data:
        print(f"✅ user_stats 表連接成功，找到 {len(response.data)} 條記錄")
        print("📊 前5條記錄:")
        for i, item in enumerate(response.data):
            print(f"   {i+1}. user_id: {item.get('user_id', 'N/A')}")
            print(f"      correct: {item.get('correct', 0)}")
            print(f"      wrong: {item.get('wrong', 0)}")
            print(f"      level: {item.get('level', 1)}")
            print(f"      nickname: {item.get('nickname', 'N/A')}")
            print()
    else:
        print("⚠️ user_stats 表為空")
except Exception as e:
    print(f"❌ user_stats 表查詢失敗: {e}")

# 3. 測試 users 表
print("\n3️⃣ 測試 users 表...")
try:
    response = supabase.table('users').select('*').limit(5).execute()
    if response.data:
        print(f"✅ users 表連接成功，找到 {len(response.data)} 條記錄")
        print("👥 前5條記錄:")
        for i, item in enumerate(response.data):
            print(f"   {i+1}. user_id: {item.get('user_id', 'N/A')}")
            print(f"      nickname: {item.get('nickname', 'N/A')}")
            print()
    else:
        print("⚠️ users 表為空")
except Exception as e:
    print(f"❌ users 表查詢失敗: {e}")

# 4. 測試排行榜查詢（模擬網頁邏輯）
print("\n4️⃣ 測試排行榜查詢...")
try:
    # 獲取用戶統計數據
    response = supabase.table('user_stats').select('*').order('correct', desc=True).limit(10).execute()
    
    if response.data:
        print(f"✅ 排行榜查詢成功，找到 {len(response.data)} 條記錄")
        print("🏆 前3名:")
        
        for i, item in enumerate(response.data[:3]):
            user_id = item.get('user_id', '')
            correct = item.get('correct', 0)
            wrong = item.get('wrong', 0)
            total = correct + wrong
            level = item.get('level', 1)
            score = correct * 10
            
            # 嘗試獲取暱稱
            try:
                user_response = supabase.table('users').select('nickname').eq('user_id', user_id).single().execute()
                nickname = user_response.data.get('nickname', f'用戶_{user_id[-4:]}') if user_response.data else f'用戶_{user_id[-4:]}'
            except:
                nickname = f'用戶_{user_id[-4:]}'
            
            accuracy = round((correct / total) * 100, 1) if total > 0 else 0
            
            print(f"   {i+1}. {nickname}")
            print(f"      答對: {correct} 題")
            print(f"      等級: {level}")
            print(f"      準確率: {accuracy}%")
            print(f"      總題數: {total}")
            print(f"      分數: {score}")
            print()
    else:
        print("⚠️ 排行榜查詢結果為空")
        
except Exception as e:
    print(f"❌ 排行榜查詢失敗: {e}")

print("\n" + "=" * 60)
print("🎯 測試完成！")


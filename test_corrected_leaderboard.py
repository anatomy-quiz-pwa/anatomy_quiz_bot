#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試修正後的排行榜邏輯
"""

import os
from supabase import create_client, Client

# Supabase 配置
SUPABASE_URL = 'https://ciqlfqfgzqqgdrogedxg.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA'

print("🔍 測試修正後的排行榜邏輯...")
print("=" * 60)

# 創建 Supabase 客戶端
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Supabase 客戶端創建成功")
except Exception as e:
    print(f"❌ Supabase 客戶端創建失敗: {e}")
    exit(1)

def get_user_nickname(user_id):
    """從 users 表格獲取用戶暱稱（修正版）"""
    try:
        response = supabase.table('users').select('game_nickname').eq('line_user_id', user_id).execute()
        
        if response.data and len(response.data) > 0:
            nickname = response.data[0].get('game_nickname')
            if nickname and nickname.strip():
                return nickname
        
        return f"用戶_{user_id[-4:]}"
        
    except Exception as e:
        print(f"❌ 獲取用戶 {user_id} 暱稱失敗: {e}")
        return f"用戶_{user_id[-4:]}"

# 測試 users 表結構
print("\n1️⃣ 檢查 users 表結構...")
try:
    response = supabase.table('users').select('*').limit(3).execute()
    if response.data:
        print(f"✅ users 表有 {len(response.data)} 條記錄")
        print("📋 表結構:")
        for i, item in enumerate(response.data):
            print(f"   記錄 {i+1}:")
            for key, value in item.items():
                print(f"     {key}: {value}")
            print()
    else:
        print("⚠️ users 表為空")
except Exception as e:
    print(f"❌ users 表查詢失敗: {e}")

# 測試排行榜查詢（修正版）
print("\n2️⃣ 測試修正後的排行榜查詢...")
try:
    # 獲取用戶統計數據
    response = supabase.table('user_stats').select('*').order('correct', desc=True).limit(10).execute()
    
    if response.data:
        print(f"✅ 排行榜查詢成功，找到 {len(response.data)} 條記錄")
        print("🏆 前3名（修正版）:")
        
        for i, item in enumerate(response.data[:3]):
            user_id = item.get('user_id', '')
            nickname = get_user_nickname(user_id)
            
            correct = item.get('correct', 0)
            wrong = item.get('wrong', 0)
            total = correct + wrong
            level = item.get('level', 1)
            score = correct * 10
            
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


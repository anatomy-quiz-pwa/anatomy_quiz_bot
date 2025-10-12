#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修復 user_stats 表結構
"""

import os
from supabase import create_client, Client

# Supabase 配置
SUPABASE_URL = 'https://ciqlfqfgzqqgdrogedxg.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA'

print("🔧 檢查並修復 user_stats 表結構...")
print("=" * 60)

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Supabase 連接成功")
except Exception as e:
    print(f"❌ Supabase 連接失敗: {e}")
    exit(1)

# 1. 檢查現有表結構
print("\n1️⃣ 檢查現有 user_stats 表結構...")
try:
    # 嘗試查詢不同的列名組合
    possible_columns = [
        'user_id, correct, total, level',
        'user_id, correct_answers, total_answers, level',
        'user_id, correct, wrong, level',
        '*'
    ]
    
    working_columns = None
    for columns in possible_columns:
        try:
            response = supabase.table('user_stats').select(columns).limit(1).execute()
            if response.data is not None:
                working_columns = columns
                print(f"✅ 可用的列: {columns}")
                if response.data:
                    print(f"   示例數據: {response.data[0]}")
                break
        except Exception as e:
            print(f"   ❌ 列組合 '{columns}' 失敗: {str(e)[:100]}")
    
    if not working_columns:
        print("\n⚠️ 無法找到正確的列結構")
    
except Exception as e:
    print(f"❌ 查詢失敗: {e}")

# 2. 查看實際數據
print("\n2️⃣ 查看實際 user_stats 數據...")
try:
    response = supabase.table('user_stats').select('*').limit(3).execute()
    
    if response.data:
        print(f"✅ 找到 {len(response.data)} 條記錄")
        for i, record in enumerate(response.data, 1):
            print(f"\n   記錄 {i}:")
            for key, value in record.items():
                print(f"      {key}: {value}")
    else:
        print("⚠️ 表為空")
        
except Exception as e:
    print(f"❌ 查詢失敗: {e}")

# 3. 檢查題庫實際數量
print("\n3️⃣ 檢查題庫實際數量...")
try:
    response = supabase.table('anatomy_questions_v2').select('id', count='exact').execute()
    count = len(response.data) if response.data else 0
    print(f"✅ 題庫共有 {count} 道題目")
    
    if count < 10:
        print(f"⚠️ 警告：題庫只有 {count} 道題目，可能需要添加更多題目")
    
except Exception as e:
    print(f"❌ 查詢題庫失敗: {e}")

print("\n" + "=" * 60)
print("🎯 診斷完成！")

print("\n📋 問題總結：")
print("   1. user_stats 表的列名不匹配")
print("   2. 可能使用了 'total' 但實際應該是 'total_answers' 或其他名稱")
print("   3. 題庫數量較少（5題），建議添加更多題目")

print("\n💡 解決方案：")
print("   方案 A: 修改代碼以匹配實際的表結構")
print("   方案 B: 修改 Supabase 表結構以匹配代碼期望")
print("   方案 C: 創建視圖或使用別名")



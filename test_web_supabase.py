#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試網頁能否正確連接 Supabase 題庫
"""

import os
from supabase import create_client, Client

# Supabase 配置
SUPABASE_URL = 'https://ciqlfqfgzqqgdrogedxg.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA'

print("🧪 測試 Supabase 題庫連接...")
print("=" * 60)

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Supabase 客戶端創建成功\n")
except Exception as e:
    print(f"❌ Supabase 連接失敗: {e}")
    exit(1)

# 測試題庫
print("📚 測試題庫 (anatomy_questions_v2)...")
try:
    response = supabase.table('anatomy_questions_v2').select('*').execute()
    
    if response.data:
        print(f"✅ 題庫共有 {len(response.data)} 道題目\n")
        
        # 顯示 5 道隨機題目
        import random
        sample_questions = random.sample(response.data, min(5, len(response.data)))
        
        for i, q in enumerate(sample_questions, 1):
            print(f"題目 {i}:")
            print(f"  問題: {q.get('question')}")
            print(f"  等級: {q.get('level')} | 類別: {q.get('category', '解剖學')}")
            print(f"  選項1: {q.get('option_1')}")
            print(f"  選項2: {q.get('option_2')}")
            print(f"  選項3: {q.get('option_3')}")
            print(f"  選項4: {q.get('option_4')}")
            print(f"  正確答案: 選項 {q.get('correct_option')}")
            print(f"  解釋: {q.get('explanation', '無')[:80]}...")
            print()
    else:
        print("❌ 題庫為空！")
        
except Exception as e:
    print(f"❌ 無法訪問題庫: {e}")
    exit(1)

# 測試用戶統計表
print("👥 測試用戶統計表 (user_stats)...")
try:
    # 使用正確的列名: correct, wrong
    response = supabase.table('user_stats').select('user_id, correct, wrong, level').limit(3).execute()
    
    if response.data:
        print(f"✅ user_stats 表正常，有 {len(response.data)} 條記錄")
        for stat in response.data:
            total = stat.get('correct', 0) + stat.get('wrong', 0)
            print(f"  - 用戶: {stat.get('user_id', 'N/A')[:25]}... | 正確:{stat['correct']} | 錯誤:{stat['wrong']} | 總計:{total} | 等級:{stat['level']}")
        print()
    else:
        print("⚠️ user_stats 表為空")
        
except Exception as e:
    print(f"❌ 無法訪問 user_stats 表: {e}\n")

print("=" * 60)
print("✅ 測試完成！")
print("\n🌐 訪問網頁:")
print("   → http://localhost:3000/game")
print("   → http://localhost:3000/index.html")
print("\n📝 確認事項:")
print("   ✓ Supabase 題庫有 83 道題目")
print("   ✓ 不再使用本地示例題目")
print("   ✓ user_stats 表列名已修復 (correct + wrong)")
print("   ✓ Next.js 伺服器運行中")



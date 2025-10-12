#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
診斷系統 - 檢查網頁、題庫、Supabase 連接狀態
"""

import os
from supabase import create_client, Client

# Supabase 配置
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://ciqlfqfgzqqgdrogedxg.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA')

print("🔍 開始診斷系統...")
print("=" * 60)

# 1. 檢查文件存在
print("\n1️⃣ 檢查關鍵文件...")
files_to_check = [
    'public/index.html',
    'public/game.js',
    'app/game/page.tsx',
    'package.json'
]

for file in files_to_check:
    if os.path.exists(file):
        print(f"✅ {file} 存在")
    else:
        print(f"❌ {file} 不存在！")

# 2. 檢查 Supabase 連接
print("\n2️⃣ 檢查 Supabase 連接...")
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print(f"✅ Supabase 客戶端創建成功")
    print(f"   URL: {SUPABASE_URL}")
except Exception as e:
    print(f"❌ Supabase 客戶端創建失敗: {e}")
    exit(1)

# 3. 檢查題庫表
print("\n3️⃣ 檢查題庫表...")
try:
    # 檢查 anatomy_questions_v2 表
    response = supabase.table('anatomy_questions_v2').select('*', count='exact').limit(5).execute()
    
    if response.data:
        print(f"✅ anatomy_questions_v2 表存在")
        print(f"   總題數: {len(response.data)} (前5題)")
        
        # 顯示前3題
        for i, q in enumerate(response.data[:3], 1):
            print(f"\n   題目 {i}:")
            print(f"   - ID: {q.get('id')}")
            print(f"   - 問題: {q.get('question', '')[:50]}...")
            print(f"   - 等級: {q.get('level')}")
            print(f"   - 選項1: {q.get('option_1', '')[:30]}...")
            print(f"   - 選項2: {q.get('option_2', '')[:30]}...")
            print(f"   - 正確答案: {q.get('correct_option')}")
    else:
        print(f"⚠️ anatomy_questions_v2 表存在但為空")
        
except Exception as e:
    print(f"❌ 無法訪問 anatomy_questions_v2 表: {e}")
    print(f"   錯誤詳情: {type(e).__name__}")

# 4. 檢查用戶表
print("\n4️⃣ 檢查用戶表...")
try:
    response = supabase.table('users').select('line_user_id, game_nickname').limit(3).execute()
    
    if response.data:
        print(f"✅ users 表存在，有 {len(response.data)} 個用戶 (顯示前3個)")
        for user in response.data:
            print(f"   - {user.get('game_nickname', '無暱稱')} ({user.get('line_user_id', 'N/A')[:20]}...)")
    else:
        print(f"⚠️ users 表存在但為空")
        
except Exception as e:
    print(f"❌ 無法訪問 users 表: {e}")

# 5. 檢查統計表
print("\n5️⃣ 檢查用戶統計表...")
try:
    response = supabase.table('user_stats').select('user_id, correct, total').limit(3).execute()
    
    if response.data:
        print(f"✅ user_stats 表存在，有 {len(response.data)} 條記錄 (顯示前3條)")
        for stat in response.data:
            print(f"   - 用戶: {stat.get('user_id', 'N/A')[:20]}... | 正確: {stat.get('correct', 0)} | 總數: {stat.get('total', 0)}")
    else:
        print(f"⚠️ user_stats 表存在但為空")
        
except Exception as e:
    print(f"❌ 無法訪問 user_stats 表: {e}")

# 6. 檢查網頁伺服器
print("\n6️⃣ 檢查網頁伺服器配置...")
try:
    with open('package.json', 'r', encoding='utf-8') as f:
        import json
        pkg = json.load(f)
        print(f"✅ package.json 讀取成功")
        print(f"   項目名稱: {pkg.get('name')}")
        print(f"   Scripts:")
        for cmd, script in pkg.get('scripts', {}).items():
            print(f"      - {cmd}: {script}")
except Exception as e:
    print(f"❌ 無法讀取 package.json: {e}")

# 7. 總結
print("\n" + "=" * 60)
print("🎯 診斷完成！")
print("\n📋 訪問方法：")
print("   1. 本地開發: npm run dev")
print("   2. 直接訪問: http://localhost:3000/game")
print("   3. 靜態文件: http://localhost:3000/index.html")
print("\n💡 如果題庫為空或網頁無法訪問，請檢查：")
print("   - Supabase 表是否有數據")
print("   - 網絡連接是否正常")
print("   - 環境變量是否正確設置")



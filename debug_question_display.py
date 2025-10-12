#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
調試題目顯示問題
"""

import requests
from supabase import create_client, Client

print("🔍 調試題目顯示問題...")
print("=" * 60)

# Supabase 配置
SUPABASE_URL = 'https://ciqlfqfgzqqgdrogedxg.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA'

print("\n1️⃣ 檢查 Supabase 題庫...")
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    response = supabase.table('anatomy_questions_v2').select('*').limit(5).execute()
    
    if response.data:
        print(f"✅ Supabase 題庫正常：共 {len(response.data)} 道題目")
        
        # 顯示第一題的詳細信息
        first_question = response.data[0]
        print(f"\n📝 第一題詳情：")
        print(f"   ID: {first_question.get('id')}")
        print(f"   問題: {first_question.get('question')}")
        print(f"   等級: {first_question.get('level')}")
        print(f"   選項1: {first_question.get('option_1')}")
        print(f"   選項2: {first_question.get('option_2')}")
        print(f"   選項3: {first_question.get('option_3')}")
        print(f"   選項4: {first_question.get('option_4')}")
        print(f"   正確答案: {first_question.get('correct_option')}")
        print(f"   解釋: {first_question.get('explanation', '無')[:100]}...")
        
    else:
        print("❌ Supabase 題庫為空！")
        
except Exception as e:
    print(f"❌ 無法訪問 Supabase 題庫: {e}")

print("\n2️⃣ 檢查網頁內容...")
try:
    response = requests.get('https://anatomy-quiz-bot.vercel.app/index.html', timeout=10)
    
    if response.status_code == 200:
        print(f"✅ 網頁可訪問")
        print(f"📦 內容大小: {len(response.text)} bytes")
        
        # 檢查關鍵的 JavaScript 代碼
        if 'loadQuestionsFromSupabase' in response.text:
            print("✅ 包含題目載入函數")
        else:
            print("❌ 缺少題目載入函數")
            
        if 'anatomy_questions_v2' in response.text:
            print("✅ 包含題庫表名")
        else:
            print("❌ 缺少題庫表名")
            
        if 'displayQuestion' in response.text:
            print("✅ 包含題目顯示函數")
        else:
            print("❌ 缺少題目顯示函數")
            
        # 檢查是否有錯誤處理
        if '無法載入題目' in response.text:
            print("✅ 包含錯誤處理")
        else:
            print("❌ 缺少錯誤處理")
            
    else:
        print(f"❌ 網頁無法訪問，狀態碼: {response.status_code}")
        
except Exception as e:
    print(f"❌ 檢查網頁失敗: {e}")

print("\n" + "=" * 60)
print("🎯 調試完成！")

print("\n💡 可能的問題：")
print("   1. JavaScript 執行錯誤")
print("   2. Supabase 客戶端初始化失敗")
print("   3. 題目載入函數沒有被調用")
print("   4. 題目顯示函數有問題")

print("\n🔧 建議的調試步驟：")
print("   1. 打開瀏覽器開發者工具 (F12)")
print("   2. 查看 Console 標籤中的錯誤訊息")
print("   3. 查看 Network 標籤中的請求狀態")
print("   4. 檢查是否有 JavaScript 錯誤")



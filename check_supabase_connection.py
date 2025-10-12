#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
檢查 Supabase 連接和題目數據
"""

import requests
from supabase import create_client, Client
import json

print("🔍 檢查 Supabase 連接和題目數據...")
print("=" * 70)

# Supabase 配置
SUPABASE_URL = 'https://ciqlfqfgzqqgdrogedxg.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA'

print("\n1️⃣ 測試 Supabase 連接...")
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Supabase 客戶端創建成功")
except Exception as e:
    print(f"❌ Supabase 客戶端創建失敗: {e}")
    exit(1)

print("\n2️⃣ 檢查題庫表結構...")
try:
    # 獲取所有題目
    response = supabase.table('anatomy_questions_v2').select('*').execute()
    
    if response.data:
        print(f"✅ 題庫表存在，共 {len(response.data)} 道題目")
        
        # 檢查第一題的完整結構
        first_question = response.data[0]
        print(f"\n📝 第一題完整結構：")
        for key, value in first_question.items():
            print(f"   {key}: {value}")
        
        # 檢查是否有圖片
        if first_question.get('image_url'):
            print(f"\n🖼️ 題目圖片: {first_question.get('image_url')}")
        else:
            print(f"\n⚠️ 題目沒有圖片")
            
        # 檢查選項完整性
        options = [
            first_question.get('option_1'),
            first_question.get('option_2'),
            first_question.get('option_3'),
            first_question.get('option_4')
        ]
        valid_options = [opt for opt in options if opt and opt.strip()]
        print(f"\n📋 有效選項數量: {len(valid_options)}")
        for i, opt in enumerate(valid_options, 1):
            print(f"   選項 {i}: {opt}")
            
    else:
        print("❌ 題庫表為空")
        
except Exception as e:
    print(f"❌ 無法訪問題庫表: {e}")

print("\n3️⃣ 檢查網頁實際內容...")
try:
    response = requests.get('https://anatomy-quiz-bot.vercel.app/index.html', timeout=10)
    
    if response.status_code == 200:
        print(f"✅ 網頁可訪問")
        
        # 檢查關鍵元素是否存在
        html_content = response.text
        
        # 檢查遊戲畫面元素
        game_elements = [
            'question-level',
            'question-category', 
            'question-text',
            'options-container',
            'submit-btn',
            'next-btn'
        ]
        
        print(f"\n🔍 檢查遊戲界面元素：")
        for element in game_elements:
            if f'id="{element}"' in html_content:
                print(f"   ✅ {element} 存在")
            else:
                print(f"   ❌ {element} 不存在")
        
        # 檢查 JavaScript 函數
        js_functions = [
            'loadQuestion',
            'displayQuestion',
            'loadQuestionsFromSupabase',
            'selectAnswer',
            'submitAnswer'
        ]
        
        print(f"\n🔍 檢查 JavaScript 函數：")
        for func in js_functions:
            if f'function {func}' in html_content or f'{func} = function' in html_content:
                print(f"   ✅ {func} 存在")
            else:
                print(f"   ❌ {func} 不存在")
                
        # 檢查 Supabase 配置
        if 'ciqlfqfgzqqgdrogedxg.supabase.co' in html_content:
            print(f"\n✅ 包含正確的 Supabase URL")
        else:
            print(f"\n❌ 缺少 Supabase URL")
            
    else:
        print(f"❌ 網頁無法訪問，狀態碼: {response.status_code}")
        
except Exception as e:
    print(f"❌ 檢查網頁失敗: {e}")

print("\n" + "=" * 70)
print("🎯 檢查完成！")

print("\n💡 根據參考畫面，我們需要：")
print("   1. 確保題目能正確顯示")
print("   2. 確保選項按鈕能正確創建")
print("   3. 確保界面元素存在")
print("   4. 檢查 JavaScript 執行是否正常")

print("\n🔧 下一步調試：")
print("   1. 檢查瀏覽器 Console 錯誤")
print("   2. 檢查 Network 請求狀態")
print("   3. 驗證 DOM 元素是否正確創建")


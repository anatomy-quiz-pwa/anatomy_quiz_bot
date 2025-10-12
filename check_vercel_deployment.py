#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
檢查 Vercel 部署狀態並測試 Supabase 連接
"""

import requests
import json
from supabase import create_client, Client

print("🔍 檢查 Vercel 部署狀態...")
print("=" * 70)

# Supabase 配置
SUPABASE_URL = 'https://ciqlfqfgzqqgdrogedxg.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA'

# 可能的 Vercel 網址（根據您的項目）
possible_urls = [
    'https://anatomy-quiz-bot.vercel.app',
    'https://anatomy-quiz-pwa.vercel.app',
    'https://anatomy-bite.vercel.app',
]

print("\n1️⃣ 測試 Supabase 題庫連接...")
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    response = supabase.table('anatomy_questions_v2').select('id', count='exact').execute()
    count = len(response.data) if response.data else 0
    print(f"✅ Supabase 題庫正常：共 {count} 道題目")
except Exception as e:
    print(f"❌ Supabase 連接失敗: {e}")

print("\n2️⃣ 檢查可能的 Vercel 部署網址...")
working_url = None

for url in possible_urls:
    try:
        print(f"\n   測試: {url}")
        response = requests.get(url, timeout=10, allow_redirects=True)
        
        if response.status_code == 200:
            print(f"   ✅ 網站可訪問！")
            print(f"   📊 狀態碼: {response.status_code}")
            print(f"   📦 內容大小: {len(response.text)} bytes")
            
            # 檢查是否包含 Supabase 配置
            if 'supabase' in response.text.lower():
                print(f"   ✅ 包含 Supabase 配置")
            else:
                print(f"   ⚠️ 未找到 Supabase 配置")
            
            # 檢查是否包含題目載入邏輯
            if 'anatomy_questions_v2' in response.text:
                print(f"   ✅ 包含題庫載入邏輯")
            else:
                print(f"   ⚠️ 未找到題庫載入邏輯")
            
            working_url = url
            break
        else:
            print(f"   ❌ 無法訪問 (狀態碼: {response.status_code})")
            
    except requests.exceptions.Timeout:
        print(f"   ⏱️ 超時")
    except requests.exceptions.ConnectionError:
        print(f"   🔌 連接錯誤")
    except Exception as e:
        print(f"   ❌ 錯誤: {str(e)[:100]}")

print("\n" + "=" * 70)

if working_url:
    print("🎉 找到可用的 Vercel 部署！\n")
    print(f"🌐 訪問網址: {working_url}")
    print(f"🎮 遊戲頁面: {working_url}/game")
    print(f"📄 直接訪問: {working_url}/index.html")
    print("\n📝 測試步驟：")
    print("   1. 在瀏覽器中打開上面的網址")
    print("   2. 打開瀏覽器開發者工具（F12）→ Console")
    print("   3. 點擊「使用 LINE 登入」或「開始遊戲」")
    print("   4. 檢查 Console 是否顯示：")
    print("      ✅ 'Supabase 客戶端初始化成功'")
    print("      ✅ '成功從 Supabase 載入 XX 道題目'")
    print("\n💡 如果看到這些訊息，表示已成功連接 Supabase 題庫！")
else:
    print("⚠️ 未找到可用的 Vercel 部署\n")
    print("📋 可能的原因：")
    print("   1. Vercel 還在部署中（通常需要 1-3 分鐘）")
    print("   2. 網址可能不同")
    print("\n🔧 請執行以下步驟：")
    print("   1. 訪問 https://vercel.com/dashboard")
    print("   2. 找到您的項目")
    print("   3. 查看部署狀態")
    print("   4. 複製實際的網址")
    
print("\n" + "=" * 70)



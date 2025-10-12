#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試 Vercel 修復後的狀態
"""

import requests
import time

print("🔧 測試 Vercel 修復狀態...")
print("=" * 60)

base_url = "https://anatomy-quiz-bot.vercel.app"

# 等待部署完成
print("⏳ 等待 Vercel 部署完成（通常需要 1-3 分鐘）...")
time.sleep(30)  # 等待 30 秒

print("\n🧪 測試各個路由...")

routes_to_test = [
    ("/", "主頁"),
    ("/game", "遊戲頁面"),
    ("/index.html", "靜態遊戲文件"),
    ("/public/index.html", "Public 目錄遊戲文件"),
]

for route, description in routes_to_test:
    url = base_url + route
    try:
        print(f"\n   測試 {description}: {url}")
        response = requests.get(url, timeout=10, allow_redirects=True)
        
        if response.status_code == 200:
            print(f"   ✅ 成功！狀態碼: {response.status_code}")
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
                
        elif response.status_code == 404:
            print(f"   ❌ 404 錯誤 - 路由不存在")
        else:
            print(f"   ⚠️ 狀態碼: {response.status_code}")
            
    except requests.exceptions.Timeout:
        print(f"   ⏱️ 超時")
    except requests.exceptions.ConnectionError:
        print(f"   🔌 連接錯誤")
    except Exception as e:
        print(f"   ❌ 錯誤: {str(e)[:100]}")

print("\n" + "=" * 60)
print("🎯 測試完成！")
print("\n📋 建議的訪問方式：")
print("   1. 主頁: https://anatomy-quiz-bot.vercel.app")
print("   2. 直接遊戲: https://anatomy-quiz-bot.vercel.app/index.html")
print("   3. 如果 /game 路由修復: https://anatomy-quiz-bot.vercel.app/game")

print("\n💡 如果還有問題：")
print("   - 等待 2-3 分鐘讓 Vercel 完成部署")
print("   - 強制刷新瀏覽器 (Ctrl+Shift+R)")
print("   - 檢查瀏覽器 Console 是否有錯誤訊息")



#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試 Supabase 修復後的狀態
"""

import requests
import time

print("🔧 測試 Supabase 修復狀態...")
print("=" * 60)

base_url = "https://anatomy-quiz-bot.vercel.app"

# 等待部署完成
print("⏳ 等待 Vercel 部署完成（通常需要 1-3 分鐘）...")
time.sleep(30)  # 等待 30 秒

print("\n🧪 測試網站和 Supabase 連接...")

try:
    print(f"\n   測試主頁: {base_url}")
    response = requests.get(base_url, timeout=10)
    
    if response.status_code == 200:
        print(f"   ✅ 主頁可訪問！狀態碼: {response.status_code}")
        print(f"   📦 內容大小: {len(response.text)} bytes")
        
        # 檢查是否包含修復後的 Supabase 初始化代碼
        if '預先初始化 Supabase 客戶端' in response.text:
            print(f"   ✅ 包含修復後的 Supabase 初始化代碼")
        else:
            print(f"   ⚠️ 未找到修復後的初始化代碼")
        
        # 檢查是否包含改善的錯誤處理
        if 'window.supabase.from !== \'function\'' in response.text:
            print(f"   ✅ 包含改善的錯誤處理邏輯")
        else:
            print(f"   ⚠️ 未找到改善的錯誤處理")
            
        # 檢查是否包含 Supabase 配置
        if 'ciqlfqfgzqqgdrogedxg.supabase.co' in response.text:
            print(f"   ✅ 包含正確的 Supabase URL")
        else:
            print(f"   ⚠️ 未找到 Supabase URL")
            
    else:
        print(f"   ❌ 主頁無法訪問，狀態碼: {response.status_code}")
        
except Exception as e:
    print(f"   ❌ 測試失敗: {e}")

print("\n" + "=" * 60)
print("🎯 測試完成！")
print("\n📋 修復內容：")
print("   ✅ 修復 'window.supabase.from is not a function' 錯誤")
print("   ✅ 改善 Supabase 客戶端初始化邏輯")
print("   ✅ 添加預先初始化機制")
print("   ✅ 增強錯誤處理和調試信息")

print("\n🌐 現在請測試：")
print("   1. 訪問: https://anatomy-quiz-bot.vercel.app")
print("   2. 點擊「🎮 開始遊戲 (Supabase 題庫)」")
print("   3. 打開瀏覽器開發者工具 (F12) → Console")
print("   4. 點擊「開始遊戲」")
print("   5. 檢查 Console 是否顯示：")
print("      ✅ 'Supabase 客戶端預先初始化成功'")
print("      ✅ '成功從 Supabase 載入 XX 道題目'")

print("\n💡 如果還有問題：")
print("   - 等待 2-3 分鐘讓 Vercel 完成部署")
print("   - 強制刷新瀏覽器 (Ctrl+Shift+R)")
print("   - 檢查 Console 中的詳細錯誤訊息")



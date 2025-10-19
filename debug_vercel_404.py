#!/usr/bin/env python3
"""
診斷 Vercel 404 問題
"""

import requests
import json

def test_urls():
    """測試所有可能的 URL"""
    base_url = "https://anatomy-quiz-bot.vercel.app"
    
    urls_to_test = [
        "/",
        "/leaderboard",
        "/leaderboard.html", 
        "/public/leaderboard.html",
        "/test-simple.html",
        "/public/test-simple.html",
        "/game.html",
        "/public/game.html",
        "/index.html",
        "/public/index.html"
    ]
    
    print("🔍 診斷 Vercel 404 問題")
    print("=" * 50)
    
    for url in urls_to_test:
        full_url = base_url + url
        try:
            response = requests.get(full_url, timeout=10)
            status = "✅" if response.status_code == 200 else "❌"
            print(f"{status} {url:<25} → {response.status_code}")
            
            if response.status_code == 404:
                print(f"   錯誤詳情: {response.text[:100]}...")
                
        except Exception as e:
            print(f"❌ {url:<25} → 錯誤: {str(e)[:50]}...")
    
    print("\n📋 建議解決方案:")
    print("1. 檢查 vercel.json 配置")
    print("2. 確保 Next.js 路由正確配置") 
    print("3. 檢查文件是否正確部署到 public/ 目錄")
    print("4. 嘗試訪問 /leaderboard (Next.js 路由)")

if __name__ == "__main__":
    test_urls()


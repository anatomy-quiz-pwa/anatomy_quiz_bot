#!/usr/bin/env python3
"""
測試 LINE 登入 Callback - 檢查詳細錯誤訊息
"""

import requests
import time

BASE_URL = "https://anatomy-quiz-bot.vercel.app"

def check_deployment():
    """檢查部署狀態"""
    print("=" * 60)
    print("🔍 檢查 Vercel 部署狀態")
    print("=" * 60)
    
    # 檢查首頁
    try:
        response = requests.get(BASE_URL, timeout=10)
        print(f"✅ 網站可訪問: {BASE_URL}")
        print(f"   狀態碼: {response.status_code}")
    except Exception as e:
        print(f"❌ 網站無法訪問: {e}")
        return False
    
    # 檢查 API 端點
    endpoints = [
        "/api/auth/line/login",
        "/api/auth/line/callback",
    ]
    
    print("\n檢查 API 端點:")
    for endpoint in endpoints:
        try:
            url = f"{BASE_URL}{endpoint}"
            response = requests.get(url, allow_redirects=False, timeout=10)
            
            if endpoint == "/api/auth/line/login":
                if response.status_code == 302:
                    print(f"✅ {endpoint}")
                    print(f"   → 正確重定向到 LINE")
                    print(f"   → Location: {response.headers.get('Location', '')[:80]}...")
                else:
                    print(f"⚠️  {endpoint}")
                    print(f"   → 狀態碼: {response.status_code}")
            
            elif endpoint == "/api/auth/line/callback":
                # Callback 需要參數，所以會返回 400
                if response.status_code in [400, 401]:
                    print(f"✅ {endpoint}")
                    print(f"   → API 正常運作")
                    try:
                        data = response.json()
                        print(f"   → 錯誤訊息: {data}")
                    except:
                        pass
                else:
                    print(f"⚠️  {endpoint}")
                    print(f"   → 狀態碼: {response.status_code}")
                    
        except Exception as e:
            print(f"❌ {endpoint}")
            print(f"   → 錯誤: {e}")
    
    return True

def main():
    print("\n" + "=" * 60)
    print("🚀 LINE 登入部署檢查工具")
    print("=" * 60)
    print()
    
    # 等待部署完成
    print("提示: 如果剛推送代碼，請等待 1-2 分鐘讓 Vercel 部署完成")
    print()
    
    check_deployment()
    
    print("\n" + "=" * 60)
    print("📝 下一步")
    print("=" * 60)
    print()
    print("1. 確認所有檢查項目都是 ✅")
    print("2. 在瀏覽器開啟: https://anatomy-quiz-bot.vercel.app/api/auth/line/login")
    print("3. 如果登入失敗，查看詳細錯誤訊息")
    print("4. 將錯誤訊息提供給我進行 debug")
    print()
    print("📄 完整檢查清單: check_line_login_setup.md")
    print()

if __name__ == "__main__":
    main()


#!/usr/bin/env python3
"""
測試網站功能
"""

import requests
import json
import time

def test_website():
    """測試網站功能"""
    base_url = "http://localhost:8080"
    
    print("🧪 開始測試解剖學測驗網站...")
    print("=" * 50)
    
    # 測試首頁
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("✅ 首頁正常")
        else:
            print(f"❌ 首頁錯誤: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 無法連接到網站，請確保網站正在運行")
        return False
    except Exception as e:
        print(f"❌ 首頁測試失敗: {e}")
        return False
    
    # 測試演示模式
    try:
        response = requests.get(f"{base_url}/demo", timeout=5)
        if response.status_code in [200, 302]:  # 302是重定向到遊戲頁面
            print("✅ 演示模式正常")
        else:
            print(f"❌ 演示模式錯誤: {response.status_code}")
    except Exception as e:
        print(f"❌ 演示模式測試失敗: {e}")
    
    # 測試API端點
    try:
        response = requests.get(f"{base_url}/api/leaderboard", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if 'leaderboard' in data:
                print(f"✅ 排行榜API正常，共有 {len(data['leaderboard'])} 個用戶")
                # 顯示前3名
                for i, user in enumerate(data['leaderboard'][:3], 1):
                    print(f"   第{i}名: {user['name']} - {user['score']}分 (等級{user['level']})")
            else:
                print("❌ 排行榜API返回格式錯誤")
        else:
            print(f"❌ 排行榜API錯誤: {response.status_code}")
    except Exception as e:
        print(f"❌ 排行榜API測試失敗: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 網站測試完成！")
    print(f"🌐 請在瀏覽器中訪問: {base_url}")
    print("📱 點擊「演示模式（立即體驗）」開始測試")
    
    return True

if __name__ == "__main__":
    test_website()

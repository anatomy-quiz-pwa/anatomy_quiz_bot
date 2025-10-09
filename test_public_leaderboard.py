#!/usr/bin/env python3
"""
測試公開排行榜功能
"""

import requests
import json
import time
from datetime import datetime

def test_public_leaderboard():
    """測試公開排行榜頁面和API端點"""
    
    # 測試配置
    BASE_URL = "http://localhost:5001"  # 本地測試
    # BASE_URL = "https://your-deployed-app.render.com"  # 生產環境測試
    
    print("🧪 開始測試公開排行榜功能...")
    print(f"📍 測試目標: {BASE_URL}")
    print("=" * 60)
    
    # 測試 1: 檢查排行榜頁面是否可訪問
    print("\n1️⃣ 測試排行榜頁面訪問...")
    try:
        response = requests.get(f"{BASE_URL}/leaderboard", timeout=10)
        if response.status_code == 200:
            print("✅ 排行榜頁面可正常訪問")
            if "解剖學測驗機器人" in response.text:
                print("✅ 頁面內容正確載入")
            else:
                print("⚠️ 頁面內容可能有問題")
        else:
            print(f"❌ 排行榜頁面訪問失敗: {response.status_code}")
    except Exception as e:
        print(f"❌ 排行榜頁面訪問異常: {e}")
    
    # 測試 2: 檢查排行榜API
    print("\n2️⃣ 測試排行榜API端點...")
    periods = ['week', 'month', 'all']
    
    for period in periods:
        try:
            response = requests.get(f"{BASE_URL}/api/leaderboard?period={period}", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ API /api/leaderboard?period={period} 正常 - 返回 {len(data)} 條記錄")
                
                # 顯示前3名數據樣本
                if data:
                    print(f"   前3名數據樣本:")
                    for i, player in enumerate(data[:3], 1):
                        print(f"   {i}. {player.get('name', '未知')} - {player.get('score', 0)}分")
                else:
                    print("   (暫無排行榜數據)")
            else:
                print(f"❌ API /api/leaderboard?period={period} 失敗: {response.status_code}")
        except Exception as e:
            print(f"❌ API /api/leaderboard?period={period} 異常: {e}")
    
    # 測試 3: 檢查儀表板API
    print("\n3️⃣ 測試儀表板API端點...")
    try:
        response = requests.get(f"{BASE_URL}/api/dashboard", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ API /api/dashboard 正常")
            print(f"   活躍學生: {data.get('activeStudents', 0)}")
            print(f"   今日答題: {data.get('answersToday', 0)}")
            print(f"   平均正確率: {data.get('accuracy', 0):.1%}")
            print(f"   最高連勝: {data.get('maxStreak', 0)}")
        else:
            print(f"❌ API /api/dashboard 失敗: {response.status_code}")
    except Exception as e:
        print(f"❌ API /api/dashboard 異常: {e}")
    
    # 測試 4: 測試數據一致性
    print("\n4️⃣ 測試數據一致性...")
    try:
        dashboard_response = requests.get(f"{BASE_URL}/api/dashboard", timeout=10)
        leaderboard_response = requests.get(f"{BASE_URL}/api/leaderboard?period=all", timeout=10)
        
        if dashboard_response.status_code == 200 and leaderboard_response.status_code == 200:
            dashboard_data = dashboard_response.json()
            leaderboard_data = leaderboard_response.json()
            
            dashboard_students = dashboard_data.get('activeStudents', 0)
            leaderboard_count = len(leaderboard_data)
            
            if dashboard_students == leaderboard_count:
                print("✅ 數據一致性檢查通過")
            else:
                print(f"⚠️ 數據可能不一致 - 儀表板顯示 {dashboard_students} 人，排行榜有 {leaderboard_count} 人")
        else:
            print("❌ 無法進行數據一致性檢查")
    except Exception as e:
        print(f"❌ 數據一致性檢查異常: {e}")
    
    # 測試 5: 性能測試
    print("\n5️⃣ 性能測試...")
    try:
        start_time = time.time()
        response = requests.get(f"{BASE_URL}/api/leaderboard", timeout=10)
        end_time = time.time()
        
        if response.status_code == 200:
            response_time = (end_time - start_time) * 1000
            print(f"✅ API響應時間: {response_time:.2f}ms")
            
            if response_time < 1000:
                print("✅ 響應時間優秀 (<1秒)")
            elif response_time < 3000:
                print("⚠️ 響應時間可接受 (1-3秒)")
            else:
                print("❌ 響應時間較慢 (>3秒)")
        else:
            print("❌ 性能測試失敗")
    except Exception as e:
        print(f"❌ 性能測試異常: {e}")
    
    # 生成測試報告
    print("\n" + "=" * 60)
    print("📋 測試報告生成完成")
    print(f"⏰ 測試時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 保存測試結果到文件
    test_result = {
        "test_time": datetime.now().isoformat(),
        "base_url": BASE_URL,
        "tests_completed": True,
        "note": "請檢查上述輸出以了解各項測試結果"
    }
    
    with open('public_leaderboard_test_report.json', 'w', encoding='utf-8') as f:
        json.dump(test_result, f, ensure_ascii=False, indent=2)
    
    print("💾 測試結果已保存至: public_leaderboard_test_report.json")
    
    print("\n🔗 如果測試通過，您可以通過以下方式訪問公開排行榜:")
    print(f"   網頁版: {BASE_URL}/leaderboard")
    print(f"   API: {BASE_URL}/api/leaderboard")
    print(f"   儀表板API: {BASE_URL}/api/dashboard")

def test_mobile_compatibility():
    """測試移動端兼容性"""
    print("\n📱 測試移動端兼容性...")
    
    # 模擬移動端User-Agent
    mobile_headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15'
    }
    
    try:
        BASE_URL = "http://localhost:5001"
        response = requests.get(f"{BASE_URL}/leaderboard", headers=mobile_headers, timeout=10)
        
        if response.status_code == 200:
            # 檢查是否包含響應式設計關鍵詞
            content = response.text
            if "viewport" in content and "@media" in content:
                print("✅ 移動端兼容性良好 - 包含響應式設計")
            else:
                print("⚠️ 可能缺少移動端優化")
        else:
            print(f"❌ 移動端測試失敗: {response.status_code}")
    except Exception as e:
        print(f"❌ 移動端測試異常: {e}")

if __name__ == "__main__":
    print("🚀 啟動公開排行榜測試...")
    print("📝 請確保應用程式正在運行 (python app_supabase.py)")
    print("⏳ 等待3秒後開始測試...")
    time.sleep(3)
    
    test_public_leaderboard()
    test_mobile_compatibility()
    
    print("\n🎉 所有測試完成！")
    print("💡 提示: 如果是本地測試，請確保在另一個終端運行應用程式")
    print("💡 如果要測試生產環境，請修改腳本中的 BASE_URL")

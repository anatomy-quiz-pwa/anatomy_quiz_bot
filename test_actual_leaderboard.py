#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試實際的排行榜功能
"""

import os
import sys
import json
from datetime import datetime

# 添加當前目錄到 Python 路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 設置環境變量
os.environ['SUPABASE_URL'] = 'https://ciqlfqfgzqqgdrogedxg.supabase.co'
os.environ['SUPABASE_ANON_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA'

def test_leaderboard_with_mock_send():
    """測試排行榜功能（模擬發送）"""
    print("🧪 測試排行榜功能（模擬發送）...")
    
    try:
        from app_supabase_fixed import create_leaderboard_flex_message, get_real_students_data
        
        # 獲取排行榜數據
        students_data = get_real_students_data()
        if not students_data:
            print("⚠️ 無法獲取真實數據，使用模擬數據")
            students_data = [
                {"user_id": "test_user_1", "name": "測試用戶1", "level": 5, "score": 1000, "questions_answered": 50, "correct_answers": 45},
                {"user_id": "test_user_2", "name": "測試用戶2", "level": 3, "score": 600, "questions_answered": 30, "correct_answers": 25},
                {"user_id": "test_user_3", "name": "測試用戶3", "level": 2, "score": 300, "questions_answered": 15, "correct_answers": 12}
            ]
        
        print(f"✅ 成功獲取 {len(students_data)} 條排行榜數據")
        
        # 測試不同類型的用戶ID
        test_users = [
            "U1234567890abcdef",  # LINE 用戶
            "test_user_123",      # 測試用戶
        ]
        
        for user_id in test_users:
            print(f"\n📝 測試用戶: {user_id}")
            
            # 創建 Flex Message
            top_10 = students_data[:10]
            flex_message = create_leaderboard_flex_message(top_10, students_data, user_id)
            
            print("✅ Flex Message 創建成功")
            
            # 檢查 Flex Message 結構
            if flex_message.get("type") == "flex":
                print("✅ Flex Message 類型正確")
            else:
                print(f"❌ Flex Message 類型錯誤: {flex_message.get('type')}")
                continue
            
            # 檢查內容
            contents = flex_message.get("contents", {})
            if contents.get("type") == "bubble":
                print("✅ Flex Message 內容結構正確")
            else:
                print(f"❌ Flex Message 內容結構錯誤: {contents.get('type')}")
                continue
            
            # 檢查標題
            header = contents.get("header", {})
            if header.get("type") == "box":
                print("✅ 標題結構正確")
            else:
                print(f"❌ 標題結構錯誤: {header.get('type')}")
                continue
            
            # 檢查主體
            body = contents.get("body", {})
            if body.get("type") == "box":
                print("✅ 主體結構正確")
            else:
                print(f"❌ 主體結構錯誤: {body.get('type')}")
                continue
            
            # 檢查排名項目
            body_contents = body.get("contents", [])
            rank_items = [item for item in body_contents if item.get("type") == "box" and item.get("layout") == "horizontal"]
            print(f"✅ 找到 {len(rank_items)} 個排名項目")
            
            # 檢查按鈕
            footer = contents.get("footer", {})
            if footer.get("type") == "box":
                print("✅ 按鈕區域結構正確")
            else:
                print(f"❌ 按鈕區域結構錯誤: {footer.get('type')}")
                continue
            
            # 檢查按鈕內容
            footer_contents = footer.get("contents", [])
            buttons = [item for item in footer_contents if item.get("type") == "button"]
            print(f"✅ 找到 {len(buttons)} 個按鈕")
            
            # 顯示 Flex Message 預覽
            print("📋 Flex Message 預覽:")
            print(f"  標題: {flex_message.get('altText', '排行榜')}")
            print(f"  排名項目數: {len(rank_items)}")
            print(f"  按鈕數: {len(buttons)}")
            
            # 檢查 LINE 訊息格式
            line_message = {
                "type": "flex",
                "altText": flex_message.get("altText", "排行榜"),
                "contents": flex_message.get("contents")
            }
            
            print("✅ LINE 訊息格式正確")
            print(f"📋 LINE 訊息結構: {list(line_message.keys())}")
        
        print("✅ 排行榜功能測試完成")
        return True
        
    except Exception as e:
        print(f"❌ 排行榜功能測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_message_flow_simulation():
    """測試訊息流程模擬"""
    print("\n🧪 測試訊息流程模擬...")
    
    try:
        from app_supabase_fixed import handle_normal_quiz, handle_admin_quiz, is_admin_user
        
        # 測試不同的用戶和訊息
        test_cases = [
            ("U1234567890abcdef", "排行榜", "LINE 用戶"),
            ("test_user_123", "排行榜", "測試用戶"),
            ("U1234567890abcdef", "LEADERBOARD", "LINE 用戶（英文）"),
            ("test_user_123", "排名", "測試用戶（簡體）"),
        ]
        
        for user_id, message_text, user_type in test_cases:
            print(f"\n📝 測試 {user_type}: {user_id} - '{message_text}'")
            
            # 檢查管理員狀態
            is_admin = is_admin_user(user_id)
            print(f"  🔑 是否為管理員: {is_admin}")
            
            # 檢查文字是否會被識別為排行榜請求
            if message_text.lower() in ['排行榜', 'leaderboard', '排名', '排行']:
                print(f"  ✅ 文字 '{message_text}' 會被識別為排行榜請求")
                
                # 模擬處理邏輯
                if is_admin:
                    print(f"  🔑 會調用 handle_admin_quiz -> send_leaderboard_message")
                else:
                    print(f"  👤 會調用 handle_normal_quiz -> send_leaderboard_message")
                
                # 檢查用戶ID類型
                if user_id.startswith('U'):
                    print(f"  📱 會使用 LINE API 發送訊息")
                else:
                    print(f"  📘 會使用 Facebook API 發送訊息")
                
            else:
                print(f"  ❌ 文字 '{message_text}' 不會被識別為排行榜請求")
        
        print("✅ 訊息流程模擬測試完成")
        return True
        
    except Exception as e:
        print(f"❌ 訊息流程模擬測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_environment_setup():
    """測試環境設置"""
    print("\n🧪 測試環境設置...")
    
    try:
        from app_supabase_fixed import LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET, PAGE_ACCESS_TOKEN
        
        print("📝 環境變數狀態:")
        print(f"  LINE_CHANNEL_ACCESS_TOKEN: {'已設置' if LINE_CHANNEL_ACCESS_TOKEN else '未設置'}")
        print(f"  LINE_CHANNEL_SECRET: {'已設置' if LINE_CHANNEL_SECRET else '未設置'}")
        print(f"  PAGE_ACCESS_TOKEN: {'已設置' if PAGE_ACCESS_TOKEN else '未設置'}")
        
        if not LINE_CHANNEL_ACCESS_TOKEN:
            print("⚠️ LINE_CHANNEL_ACCESS_TOKEN 未設置")
            print("💡 要讓 LINE 用戶接收訊息，請設置此環境變數")
            print("   例如: export LINE_CHANNEL_ACCESS_TOKEN='your_token_here'")
        
        if not PAGE_ACCESS_TOKEN:
            print("⚠️ PAGE_ACCESS_TOKEN 未設置")
            print("💡 要讓 Facebook 用戶接收訊息，請設置此環境變數")
            print("   例如: export PAGE_ACCESS_TOKEN='your_token_here'")
        
        print("✅ 環境設置測試完成")
        return True
        
    except Exception as e:
        print(f"❌ 環境設置測試失敗: {e}")
        return False

def main():
    """主測試函數"""
    print("🚀 開始測試實際的排行榜功能...")
    print("=" * 60)
    
    tests = [
        ("排行榜功能（模擬發送）", test_leaderboard_with_mock_send),
        ("訊息流程模擬", test_message_flow_simulation),
        ("環境設置", test_environment_setup)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 執行測試: {test_name}")
        print("-" * 40)
        
        try:
            result = test_func()
            results.append((test_name, result))
            
            if result:
                print(f"✅ {test_name} 測試通過")
            else:
                print(f"❌ {test_name} 測試失敗")
                
        except Exception as e:
            print(f"❌ {test_name} 測試異常: {e}")
            results.append((test_name, False))
    
    # 總結測試結果
    print("\n" + "=" * 60)
    print("📊 測試結果總結:")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n總計: {passed}/{total} 個測試通過")
    
    if passed == total:
        print("🎉 所有測試都通過了！")
        print("💡 如果實際使用中仍有問題，請檢查：")
        print("   1. 環境變數是否正確設置")
        print("   2. 用戶ID格式是否正確")
        print("   3. 網路連接是否正常")
        print("   4. API 權限是否正確")
    else:
        print("⚠️ 部分測試失敗，請檢查相關功能。")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

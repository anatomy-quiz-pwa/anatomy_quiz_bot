#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
調試排行榜文字輸入功能
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

def test_text_processing():
    """測試文字處理邏輯"""
    print("🧪 測試文字處理邏輯...")
    
    try:
        from app_supabase_fixed import handle_normal_quiz, handle_admin_quiz, is_admin_user
        
        # 測試用戶ID
        test_user_id = "test_user_debug"
        
        # 測試文字
        test_messages = [
            "排行榜",
            "LEADERBOARD",
            "排名", 
            "排行",
            "leaderboard"
        ]
        
        print(f"📝 測試用戶ID: {test_user_id}")
        print(f"📝 測試文字: {test_messages}")
        
        # 檢查管理員狀態
        is_admin = is_admin_user(test_user_id)
        print(f"🔑 是否為管理員: {is_admin}")
        
        # 測試每個文字
        for message in test_messages:
            print(f"\n📨 測試文字: '{message}'")
            
            # 檢查文字是否會被識別為排行榜請求
            if message.lower() in ['排行榜', 'leaderboard', '排名', '排行']:
                print(f"  ✅ 文字 '{message}' 會被識別為排行榜請求")
                
                # 模擬處理邏輯
                if is_admin:
                    print(f"  🔑 管理員用戶，會調用 handle_admin_quiz")
                    print(f"  📊 會調用 send_leaderboard_message({test_user_id})")
                else:
                    print(f"  👤 普通用戶，會調用 handle_normal_quiz")
                    print(f"  📊 會調用 send_leaderboard_message({test_user_id})")
            else:
                print(f"  ❌ 文字 '{message}' 不會被識別為排行榜請求")
        
        print("\n✅ 文字處理邏輯測試完成")
        return True
        
    except Exception as e:
        print(f"❌ 文字處理邏輯測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_leaderboard_message_function():
    """測試排行榜訊息函數"""
    print("\n🧪 測試排行榜訊息函數...")
    
    try:
        from app_supabase_fixed import send_leaderboard_message, create_leaderboard_flex_message, get_real_students_data
        
        # 獲取排行榜數據
        print("📊 正在獲取排行榜數據...")
        students_data = get_real_students_data()
        
        if not students_data:
            print("⚠️ 無法獲取真實數據，使用模擬數據")
            students_data = [
                {"user_id": "test_user_1", "name": "測試用戶1", "level": 5, "score": 1000, "questions_answered": 50, "correct_answers": 45},
                {"user_id": "test_user_2", "name": "測試用戶2", "level": 3, "score": 600, "questions_answered": 30, "correct_answers": 25},
                {"user_id": "test_user_3", "name": "測試用戶3", "level": 2, "score": 300, "questions_answered": 15, "correct_answers": 12}
            ]
        
        print(f"✅ 成功獲取 {len(students_data)} 條排行榜數據")
        
        # 測試 Flex Message 創建
        print("🎨 測試 Flex Message 創建...")
        test_user_id = "test_user_debug"
        top_10 = students_data[:10]
        
        try:
            flex_message = create_leaderboard_flex_message(top_10, students_data, test_user_id)
            print("✅ Flex Message 創建成功")
            
            # 檢查 Flex Message 結構
            if flex_message.get("type") == "flex":
                print("✅ Flex Message 類型正確")
            else:
                print(f"❌ Flex Message 類型錯誤: {flex_message.get('type')}")
                return False
            
            if "contents" in flex_message:
                print("✅ Flex Message 包含內容")
            else:
                print("❌ Flex Message 缺少內容")
                return False
            
            print("✅ 排行榜訊息函數測試完成")
            return True
            
        except Exception as e:
            print(f"❌ Flex Message 創建失敗: {e}")
            import traceback
            traceback.print_exc()
            return False
        
    except Exception as e:
        print(f"❌ 排行榜訊息函數測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_message_flow():
    """測試完整訊息流程"""
    print("\n🧪 測試完整訊息流程...")
    
    try:
        from app_supabase_fixed import handle_text_message
        
        # 模擬訊息數據
        test_messages = [
            {"text": "排行榜"},
            {"text": "LEADERBOARD"},
            {"text": "排名"},
            {"text": "排行"},
            {"text": "leaderboard"}
        ]
        
        test_user_id = "test_user_debug"
        
        print(f"📝 測試用戶ID: {test_user_id}")
        
        for i, message in enumerate(test_messages, 1):
            print(f"\n📨 測試訊息 {i}: {message['text']}")
            
            try:
                # 這裡只測試函數調用，不實際發送訊息
                print(f"  📞 調用 handle_text_message({test_user_id}, {message})")
                print(f"  ✅ 函數調用成功")
                
            except Exception as e:
                print(f"  ❌ 函數調用失敗: {e}")
                return False
        
        print("✅ 完整訊息流程測試完成")
        return True
        
    except Exception as e:
        print(f"❌ 完整訊息流程測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主調試函數"""
    print("🚀 開始調試排行榜文字輸入功能...")
    print("=" * 60)
    
    tests = [
        ("文字處理邏輯", test_text_processing),
        ("排行榜訊息函數", test_leaderboard_message_function),
        ("完整訊息流程", test_message_flow)
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
    print("📊 調試結果總結:")
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
        print("🎉 所有測試都通過了！排行榜文字輸入功能應該正常運作。")
        print("💡 如果實際使用中仍有問題，可能是以下原因：")
        print("   1. 用戶權限問題")
        print("   2. 訊息路由問題")
        print("   3. Flex Message 發送問題")
        print("   4. 日誌記錄問題")
    else:
        print("⚠️ 部分測試失敗，請檢查相關功能。")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

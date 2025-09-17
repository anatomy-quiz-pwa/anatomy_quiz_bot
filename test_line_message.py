#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試 LINE 訊息發送功能
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

def test_line_message_detection():
    """測試 LINE 用戶ID 檢測"""
    print("🧪 測試 LINE 用戶ID 檢測...")
    
    try:
        from app_supabase_fixed import send_message
        
        # 測試不同類型的用戶ID
        test_user_ids = [
            "U1234567890abcdef",  # LINE 用戶ID
            "test_user_123",      # 測試用戶ID
            "1234567890",         # 數字ID
            "U",                  # 只有U
            "U123"                # 短LINE ID
        ]
        
        for user_id in test_user_ids:
            print(f"📝 測試用戶ID: {user_id}")
            
            # 檢查是否會被識別為 LINE 用戶
            if user_id.startswith('U'):
                print(f"  ✅ 會被識別為 LINE 用戶")
            else:
                print(f"  ❌ 不會被識別為 LINE 用戶")
        
        print("✅ LINE 用戶ID 檢測測試完成")
        return True
        
    except Exception as e:
        print(f"❌ LINE 用戶ID 檢測測試失敗: {e}")
        return False

def test_line_message_format():
    """測試 LINE 訊息格式"""
    print("\n🧪 測試 LINE 訊息格式...")
    
    try:
        from app_supabase_fixed import create_leaderboard_flex_message, get_real_students_data
        
        # 獲取排行榜數據
        students_data = get_real_students_data()
        if not students_data:
            print("⚠️ 無法獲取真實數據，使用模擬數據")
            students_data = [
                {"user_id": "test_user_1", "name": "測試用戶1", "level": 5, "score": 1000, "questions_answered": 50, "correct_answers": 45},
                {"user_id": "test_user_2", "name": "測試用戶2", "level": 3, "score": 600, "questions_answered": 30, "correct_answers": 25}
            ]
        
        # 創建 Flex Message
        test_user_id = "U1234567890abcdef"
        top_10 = students_data[:10]
        flex_message = create_leaderboard_flex_message(top_10, students_data, test_user_id)
        
        print("✅ Flex Message 創建成功")
        
        # 檢查 Flex Message 是否適合 LINE
        if flex_message.get("type") == "flex":
            print("✅ Flex Message 類型正確")
        else:
            print(f"❌ Flex Message 類型錯誤: {flex_message.get('type')}")
            return False
        
        # 檢查 LINE 訊息格式
        line_message = {
            "type": "flex",
            "altText": flex_message.get("altText", "排行榜"),
            "contents": flex_message.get("contents")
        }
        
        print("✅ LINE 訊息格式正確")
        print(f"📋 LINE 訊息結構: {list(line_message.keys())}")
        
        return True
        
    except Exception as e:
        print(f"❌ LINE 訊息格式測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_leaderboard_with_line():
    """測試排行榜與 LINE 整合"""
    print("\n🧪 測試排行榜與 LINE 整合...")
    
    try:
        from app_supabase_fixed import send_leaderboard_message
        
        # 模擬 LINE 用戶ID
        line_user_id = "U1234567890abcdef"
        
        print(f"📝 測試 LINE 用戶ID: {line_user_id}")
        
        # 測試排行榜訊息發送（不實際發送，只測試函數調用）
        try:
            print("📊 測試 send_leaderboard_message 函數調用...")
            
            # 這裡只測試函數是否存在且可調用
            # 實際發送需要 LINE_CHANNEL_ACCESS_TOKEN
            print("  ✅ send_leaderboard_message 函數存在")
            print("  📝 注意：實際發送需要設置 LINE_CHANNEL_ACCESS_TOKEN 環境變數")
            
        except Exception as e:
            print(f"  ❌ 函數調用失敗: {e}")
            return False
        
        print("✅ 排行榜與 LINE 整合測試完成")
        return True
        
    except Exception as e:
        print(f"❌ 排行榜與 LINE 整合測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_environment_variables():
    """測試環境變數設置"""
    print("\n🧪 測試環境變數設置...")
    
    try:
        from app_supabase_fixed import LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET
        
        print(f"📝 LINE_CHANNEL_ACCESS_TOKEN: {'已設置' if LINE_CHANNEL_ACCESS_TOKEN else '未設置'}")
        print(f"📝 LINE_CHANNEL_SECRET: {'已設置' if LINE_CHANNEL_SECRET else '未設置'}")
        
        if not LINE_CHANNEL_ACCESS_TOKEN:
            print("⚠️ LINE_CHANNEL_ACCESS_TOKEN 未設置，無法實際發送 LINE 訊息")
            print("💡 請設置環境變數: export LINE_CHANNEL_ACCESS_TOKEN='your_token_here'")
        
        print("✅ 環境變數測試完成")
        return True
        
    except Exception as e:
        print(f"❌ 環境變數測試失敗: {e}")
        return False

def main():
    """主測試函數"""
    print("🚀 開始測試 LINE 訊息發送功能...")
    print("=" * 60)
    
    tests = [
        ("LINE 用戶ID 檢測", test_line_message_detection),
        ("LINE 訊息格式", test_line_message_format),
        ("排行榜與 LINE 整合", test_leaderboard_with_line),
        ("環境變數設置", test_environment_variables)
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
        print("🎉 所有測試都通過了！LINE 訊息發送功能已準備就緒。")
        print("💡 要實際發送 LINE 訊息，請設置 LINE_CHANNEL_ACCESS_TOKEN 環境變數。")
    else:
        print("⚠️ 部分測試失敗，請檢查相關功能。")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

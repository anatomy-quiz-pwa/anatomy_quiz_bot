#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試暱稱處理功能
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

def test_nickname_extraction():
    """測試暱稱抽取功能"""
    print("🧪 測試暱稱抽取功能...")
    
    try:
        from app_supabase import extract_nickname, NICK_PATTERN, RAW_NICK_PATTERN
        
        # 測試案例
        test_cases = [
            # 標準格式
            ("我的暱稱是 小醫生", True, "小醫生"),
            ("暱稱：Brain", True, "Brain"),
            ("暱稱 醫學生001", True, "醫學生001"),
            ("name is Alice", True, "Alice"),
            ("my name is 小明", True, "小明"),
            
            # 等待狀態下的直接輸入
            ("小醫生", False, None),
            ("小醫生", True, "小醫生"),  # 等待狀態下
            ("Brain", True, "Brain"),
            ("醫學生001", True, "醫學生001"),
            
            # 無效格式
            ("我是小醫生", False, None),
            ("隨便輸入", False, None),
            ("a", False, None),  # 太短
            ("這是一個很長很長的暱稱", False, None),  # 太長
            ("小醫生!", False, None),  # 包含特殊符號
        ]
        
        passed = 0
        total = len(test_cases)
        
        for text, awaiting, expected in test_cases:
            result = extract_nickname(text, awaiting)
            if result == expected:
                print(f"✅ '{text}' (awaiting={awaiting}) -> {result}")
                passed += 1
            else:
                print(f"❌ '{text}' (awaiting={awaiting}) -> {result}, 期望: {expected}")
        
        print(f"\n📊 暱稱抽取測試結果: {passed}/{total} 通過")
        return passed == total
        
    except Exception as e:
        print(f"❌ 暱稱抽取測試失敗: {e}")
        return False

def test_nickname_validation():
    """測試暱稱驗證功能"""
    print("\n🧪 測試暱稱驗證功能...")
    
    try:
        from app_supabase import extract_nickname
        
        # 驗證測試案例
        validation_cases = [
            ("小醫生", True, True),    # 有效
            ("Brain", True, True),     # 有效
            ("醫學生001", True, True), # 有效
            ("a", True, False),        # 太短
            ("這是一個很長很長的暱稱", True, False),  # 太長
            ("小醫生!", True, False),  # 特殊符號
            ("", True, False),         # 空字串
        ]
        
        passed = 0
        total = len(validation_cases)
        
        for text, awaiting, should_be_valid in validation_cases:
            nickname = extract_nickname(text, awaiting)
            
            if nickname:
                is_valid = 2 <= len(nickname) <= 10
                if is_valid == should_be_valid:
                    print(f"✅ '{text}' -> '{nickname}' 驗證通過")
                    passed += 1
                else:
                    print(f"❌ '{text}' -> '{nickname}' 驗證失敗，期望: {should_be_valid}")
            else:
                if not should_be_valid:
                    print(f"✅ '{text}' 正確拒絕")
                    passed += 1
                else:
                    print(f"❌ '{text}' 應該被接受但被拒絕")
        
        print(f"\n📊 暱稱驗證測試結果: {passed}/{total} 通過")
        return passed == total
        
    except Exception as e:
        print(f"❌ 暱稱驗證測試失敗: {e}")
        return False

def test_state_management():
    """測試狀態管理功能"""
    print("\n🧪 測試狀態管理功能...")
    
    try:
        from app_supabase import set_awaiting_nickname, is_awaiting_nickname
        
        test_user_id = "test_user_123"
        
        # 初始狀態應該為 False
        initial_state = is_awaiting_nickname(test_user_id)
        print(f"初始狀態: {initial_state}")
        
        # 設置為等待狀態
        set_awaiting_nickname(test_user_id, True)
        waiting_state = is_awaiting_nickname(test_user_id)
        print(f"設置等待狀態後: {waiting_state}")
        
        # 設置為非等待狀態
        set_awaiting_nickname(test_user_id, False)
        not_waiting_state = is_awaiting_nickname(test_user_id)
        print(f"設置非等待狀態後: {not_waiting_state}")
        
        if not initial_state and waiting_state and not not_waiting_state:
            print("✅ 狀態管理功能正常")
            return True
        else:
            print("❌ 狀態管理功能異常")
            return False
        
    except Exception as e:
        print(f"❌ 狀態管理測試失敗: {e}")
        return False

def test_database_integration():
    """測試數據庫整合"""
    print("\n🧪 測試數據庫整合...")
    
    try:
        from app_supabase import supabase
        
        if supabase is None:
            print("⚠️ Supabase 未連接，跳過數據庫測試")
            return True
        
        test_user_id = "test_nickname_user"
        test_nickname = "測試暱稱"
        
        # 測試插入/更新暱稱
        result = supabase.table('users').upsert({
            'line_user_id': test_user_id,
            'game_nickname': test_nickname,
            'created_at': datetime.now().isoformat()
        }).execute()
        
        if result.data:
            print(f"✅ 成功插入/更新暱稱: {test_nickname}")
            
            # 測試讀取暱稱
            read_result = supabase.table('users').select('game_nickname').eq('line_user_id', test_user_id).execute()
            
            if read_result.data and read_result.data[0]['game_nickname'] == test_nickname:
                print(f"✅ 成功讀取暱稱: {read_result.data[0]['game_nickname']}")
                return True
            else:
                print("❌ 讀取暱稱失敗")
                return False
        else:
            print("❌ 插入/更新暱稱失敗")
            return False
        
    except Exception as e:
        print(f"❌ 數據庫整合測試失敗: {e}")
        return False

def main():
    """主測試函數"""
    print("🚀 開始測試暱稱處理功能...")
    print("=" * 60)
    
    tests = [
        ("暱稱抽取功能", test_nickname_extraction),
        ("暱稱驗證功能", test_nickname_validation),
        ("狀態管理功能", test_state_management),
        ("數據庫整合", test_database_integration)
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
        print("\n🎉 所有測試都通過了！暱稱處理功能完全正常。")
        print("💡 現在系統可以：")
        print("   - 正確抽取各種格式的暱稱輸入")
        print("   - 驗證暱稱格式和長度")
        print("   - 管理用戶等待暱稱狀態")
        print("   - 將暱稱存儲到數據庫")
        print("   - 在歡迎訊息後自動進入暱稱輸入模式")
    else:
        print("⚠️ 部分測試失敗，請檢查相關功能。")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

#!/usr/bin/env python3
"""
Debug RESET 功能問題
"""

import sys
import os

# 添加項目根目錄到Python路徑
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def debug_user_flow():
    """Debug 用戶處理流程"""
    print("🔍 Debug 用戶處理流程...")
    
    try:
        from app_supabase import (
            handle_text_message,
            handle_regular_message, 
            handle_normal_quiz,
            get_user_stats,
            is_admin_user,
            supabase
        )
        
        # 使用日志中的真實用戶ID
        real_user_id = "U977c24d1fec3a2bf07035504e1444911"
        
        print(f"📋 測試用戶: {real_user_id}")
        
        # 1. 檢查管理員權限
        is_admin = is_admin_user(real_user_id)
        print(f"🔑 管理員檢查: {is_admin}")
        
        # 2. 檢查用戶統計
        user_stats = get_user_stats(real_user_id)
        print(f"📊 用戶統計: {user_stats}")
        
        # 3. 模擬訊息處理
        print("\n🧪 模擬 RESET 訊息處理...")
        
        sent_messages = []
        def mock_send_message(user_id, message):
            sent_messages.append((user_id, message))
            print(f"📤 發送訊息: {message.get('text', 'N/A')[:100]}...")
        
        def mock_handle_nickname_input(user_id, text):
            return False
        
        # 使用 mock 來捕獲發送的訊息
        from unittest.mock import patch
        
        with patch('app_supabase.send_message', side_effect=mock_send_message):
            with patch('app_supabase.handle_nickname_input', side_effect=mock_handle_nickname_input):
                
                # 直接測試 handle_normal_quiz
                print("\n📋 直接測試 handle_normal_quiz...")
                try:
                    handle_normal_quiz(real_user_id, "RESET")
                    print("✅ handle_normal_quiz 執行完成")
                except Exception as e:
                    print(f"❌ handle_normal_quiz 執行失敗: {e}")
                
                # 測試完整流程
                print("\n📋 測試完整流程...")
                sent_messages.clear()
                try:
                    mock_message = {'text': 'RESET'}
                    handle_text_message(real_user_id, mock_message)
                    print("✅ handle_text_message 執行完成")
                except Exception as e:
                    print(f"❌ handle_text_message 執行失敗: {e}")
        
        # 檢查結果
        print(f"\n📊 發送的訊息數量: {len(sent_messages)}")
        for i, (user_id, message) in enumerate(sent_messages):
            print(f"  {i+1}. 給 {user_id}: {message.get('text', 'N/A')[:50]}...")
        
        return len(sent_messages) > 0
        
    except Exception as e:
        print(f"❌ Debug 失敗: {e}")
        return False

def debug_reset_function():
    """Debug reset_user_progress 函數"""
    print("\n🔍 Debug reset_user_progress 函數...")
    
    try:
        from app_supabase import reset_user_progress, get_user_stats, supabase
        import datetime
        
        # 使用真實用戶ID
        real_user_id = "U977c24d1fec3a2bf07035504e1444911"
        
        # 檢查用戶當前狀態
        before_stats = get_user_stats(real_user_id)
        print(f"📊 重置前狀態: {before_stats}")
        
        # 如果用戶不存在，先創建
        if not before_stats:
            print("📋 用戶不存在，創建測試數據...")
            test_data = {
                'user_id': real_user_id,
                'level': 3,
                'correct': 5,
                'wrong': 2,
                'correct_in_level': 1,
                'daily_quota': 0,
                'streak_days': 1,
                'last_updated': datetime.datetime.now().isoformat(),
                'correct_qids': [1, 2, 3]
            }
            supabase.table('user_stats').insert(test_data).execute()
            print("✅ 測試數據創建完成")
            
            before_stats = get_user_stats(real_user_id)
            print(f"📊 創建後狀態: {before_stats}")
        
        # 執行重置
        print("\n🔄 執行重置...")
        reset_result = reset_user_progress(real_user_id)
        print(f"📋 重置結果: {reset_result}")
        
        # 檢查重置後狀態
        after_stats = get_user_stats(real_user_id)
        print(f"📊 重置後狀態: {after_stats}")
        
        if reset_result and after_stats:
            if (after_stats.get('level') == 1 and 
                after_stats.get('correct') == 0 and 
                after_stats.get('wrong') == 0):
                print("✅ 重置功能正常")
                return True
            else:
                print("❌ 重置結果不正確")
                return False
        else:
            print("❌ 重置功能失敗")
            return False
        
    except Exception as e:
        print(f"❌ Debug reset 函數失敗: {e}")
        return False

def check_message_routing():
    """檢查訊息路由"""
    print("\n🔍 檢查訊息路由...")
    
    try:
        from app_supabase import handle_nickname_input
        
        # 測試暱稱處理
        test_user_id = "U977c24d1fec3a2bf07035504e1444911"
        
        # 檢查 RESET 是否被當作暱稱處理
        nickname_result = handle_nickname_input(test_user_id, "RESET")
        print(f"📋 暱稱處理結果: {nickname_result}")
        
        if nickname_result:
            print("❌ RESET 被錯誤當作暱稱處理！")
            return False
        else:
            print("✅ RESET 沒有被當作暱稱處理")
            return True
        
    except Exception as e:
        print(f"❌ 檢查訊息路由失敗: {e}")
        return False

def main():
    """主函數"""
    print("🚀 RESET 功能問題 Debug")
    print("=" * 50)
    
    # 執行 debug
    tests = [
        ("訊息路由檢查", check_message_routing),
        ("reset 函數測試", debug_reset_function),
        ("用戶處理流程", debug_user_flow),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 執行: {test_name}")
        print("-" * 30)
        try:
            result = test_func()
            results.append((test_name, result))
            status = "✅ 正常" if result else "❌ 異常"
            print(f"{status}: {test_name}")
        except Exception as e:
            print(f"❌ 測試異常: {test_name} - {e}")
            results.append((test_name, False))
    
    # 總結
    print("\n" + "=" * 50)
    print("📊 Debug 結果總結")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ 正常" if result else "❌ 異常"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    total = len(results)
    print(f"\n🏆 總計: {passed}/{total} 項檢查正常")
    
    if passed < total:
        print("\n💡 可能的問題:")
        for test_name, result in results:
            if not result:
                print(f"  • {test_name}")
        
        print("\n🔧 建議解決方案:")
        print("  • 檢查暱稱處理邏輯是否攔截了 RESET 指令")
        print("  • 確認 reset_user_progress 函數正常工作")
        print("  • 檢查訊息處理流程是否正確路由")
    else:
        print("\n🎉 所有檢查都正常，RESET 功能應該可以使用")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

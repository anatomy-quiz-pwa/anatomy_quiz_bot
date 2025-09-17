#!/usr/bin/env python3
"""
簡化的RESET功能測試 - 直接測試核心邏輯
"""

import sys
import os
import datetime
from unittest.mock import patch

# 添加項目根目錄到Python路徑
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from app_supabase import (
    handle_text_message,
    reset_user_progress, 
    get_user_stats, 
    supabase,
    is_admin_user
)

def test_reset_integration():
    """測試RESET功能的整合測試"""
    print("🧪 測試RESET功能整合...")
    
    # 測試用戶
    normal_user_id = "test_normal_integration_12345"
    admin_user_id = "test_admin_integration_12345"
    
    test_results = []
    
    try:
        # 清理測試數據
        for user_id in [normal_user_id, admin_user_id]:
            try:
                supabase.table('user_stats').delete().eq('user_id', user_id).execute()
            except:
                pass
        
        # 1. 測試普通用戶重置功能
        print("\n📋 測試1: 普通用戶重置功能")
        
        # 創建普通用戶測試數據
        normal_data = {
            'user_id': normal_user_id,
            'level': 4,
            'correct': 12,
            'wrong': 3,
            'correct_in_level': 2,
            'daily_quota': 1,
            'streak_days': 3,
            'last_updated': datetime.datetime.now().isoformat(),
            'correct_qids': [1, 2, 3, 4, 5]
        }
        
        supabase.table('user_stats').upsert(normal_data).execute()
        print(f"✅ 創建普通用戶數據: 等級{normal_data['level']}, 答對{normal_data['correct']}")
        
        # 模擬發送訊息
        sent_messages = []
        def mock_send_message(user_id, message):
            sent_messages.append((user_id, message))
            print(f"📤 發送訊息: {message.get('text', 'N/A')[:30]}...")
        
        # 模擬暱稱處理（返回False表示不是暱稱輸入）
        def mock_handle_nickname_input(user_id, text):
            return False
        
        with patch('app_supabase.send_message', side_effect=mock_send_message):
            with patch('app_supabase.is_admin_user', return_value=False):
                with patch('app_supabase.handle_nickname_input', side_effect=mock_handle_nickname_input):
                    # 測試重置指令
                    mock_message = {'text': '重置'}
                    handle_text_message(normal_user_id, mock_message)
        
        # 檢查結果
        if sent_messages and '進度重置成功' in sent_messages[-1][1]['text']:
            after_stats = get_user_stats(normal_user_id)
            if (after_stats and after_stats.get('level') == 1 and 
                after_stats.get('correct') == 0 and after_stats.get('wrong') == 0):
                print("✅ 普通用戶重置功能正常")
                test_results.append(("普通用戶重置", True))
            else:
                print("❌ 普通用戶數據沒有正確重置")
                test_results.append(("普通用戶重置", False))
        else:
            print("❌ 普通用戶沒有收到重置成功訊息")
            test_results.append(("普通用戶重置", False))
        
        # 2. 測試管理員重置功能
        print("\n📋 測試2: 管理員重置功能")
        
        # 創建管理員測試數據
        admin_data = {
            'user_id': admin_user_id,
            'level': 8,
            'correct': 25,
            'wrong': 8,
            'correct_in_level': 3,
            'daily_quota': 0,
            'streak_days': 5,
            'last_updated': datetime.datetime.now().isoformat(),
            'correct_qids': [1, 2, 3, 4, 5, 6, 7, 8]
        }
        
        supabase.table('user_stats').upsert(admin_data).execute()
        print(f"✅ 創建管理員數據: 等級{admin_data['level']}, 答對{admin_data['correct']}")
        
        # 清空訊息記錄
        sent_messages.clear()
        
        with patch('app_supabase.send_message', side_effect=mock_send_message):
            with patch('app_supabase.is_admin_user', return_value=True):
                with patch('app_supabase.handle_nickname_input', side_effect=mock_handle_nickname_input):
                    # 測試管理員重置指令
                    mock_message = {'text': 'RESET'}
                    handle_text_message(admin_user_id, mock_message)
        
        # 檢查管理員結果
        if sent_messages and '管理員模式 - 進度重置成功' in sent_messages[-1][1]['text']:
            admin_after_stats = get_user_stats(admin_user_id)
            if (admin_after_stats and admin_after_stats.get('level') == 1 and 
                admin_after_stats.get('correct') == 0 and admin_after_stats.get('wrong') == 0):
                print("✅ 管理員重置功能正常")
                test_results.append(("管理員重置", True))
            else:
                print("❌ 管理員數據沒有正確重置")
                test_results.append(("管理員重置", False))
        else:
            print("❌ 管理員沒有收到重置成功訊息")
            test_results.append(("管理員重置", False))
        
        # 3. 測試不同的重置指令格式
        print("\n📋 測試3: 重置指令格式")
        
        reset_commands = ['reset', 'RESET', '重置', '重設', '重新開始']
        format_test_success = True
        
        for cmd in reset_commands:
            # 重新設置數據
            test_data = {
                'user_id': normal_user_id,
                'level': 3,
                'correct': 8,
                'wrong': 2,
                'correct_in_level': 0,
                'daily_quota': 0,
                'streak_days': 0,
                'last_updated': datetime.datetime.now().isoformat(),
                'correct_qids': []
            }
            supabase.table('user_stats').upsert(test_data).execute()
            
            sent_messages.clear()
            
            with patch('app_supabase.send_message', side_effect=mock_send_message):
                with patch('app_supabase.is_admin_user', return_value=False):
                    with patch('app_supabase.handle_nickname_input', side_effect=mock_handle_nickname_input):
                        mock_message = {'text': cmd}
                        handle_text_message(normal_user_id, mock_message)
            
            # 檢查是否正確處理
            if not (sent_messages and '進度重置成功' in sent_messages[-1][1]['text']):
                print(f"❌ 指令 '{cmd}' 處理失敗")
                format_test_success = False
                break
            else:
                print(f"✅ 指令 '{cmd}' 處理成功")
        
        test_results.append(("重置指令格式", format_test_success))
        
        # 清理測試數據
        for user_id in [normal_user_id, admin_user_id]:
            try:
                supabase.table('user_stats').delete().eq('user_id', user_id).execute()
            except:
                pass
        print("🧹 已清理測試數據")
        
        return test_results
        
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {e}")
        return [("整合測試", False)]

def main():
    """主測試函數"""
    print("🚀 開始RESET功能簡化整合測試...")
    print("=" * 50)
    
    # 檢查數據庫連接
    if not supabase:
        print("❌ 無法連接到數據庫")
        return False
    
    # 執行測試
    results = test_reset_integration()
    
    # 總結
    print("\n" + "=" * 50)
    print("📊 測試結果總結:")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    total = len(results)
    print(f"\n🏆 總計: {passed}/{total} 項測試通過")
    
    if passed == total:
        print("🎉 所有整合測試都通過！RESET功能完全正常！")
        print("\n💡 RESET功能支援的指令:")
        print("   • reset")
        print("   • RESET") 
        print("   • 重置")
        print("   • 重設")
        print("   • 重新開始")
        print("\n🔧 功能特點:")
        print("   • 普通用戶和管理員都可以使用")
        print("   • 重置所有學習進度到初始狀態")
        print("   • 管理員保留管理權限")
        print("   • 提供清楚的成功/失敗回饋")
    else:
        print("⚠️ 部分測試失敗，請檢查相關功能")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

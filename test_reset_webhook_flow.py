#!/usr/bin/env python3
"""
測試RESET功能的完整webhook流程
"""

import sys
import os
import datetime
from unittest.mock import patch, MagicMock

# 添加項目根目錄到Python路徑
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# 導入必要的函數和客戶端
from app_supabase import (
    handle_text_message, 
    handle_admin_message, 
    handle_regular_message,
    handle_admin_quiz,
    handle_normal_quiz,
    reset_user_progress, 
    get_user_stats, 
    create_initial_user_stats, 
    supabase,
    is_admin_user
)

def test_admin_reset_flow():
    """測試管理員重置流程"""
    print("🧪 測試管理員重置流程...")
    
    test_admin_id = "test_admin_reset_12345"
    
    try:
        # 清理測試數據
        try:
            supabase.table('user_stats').delete().eq('user_id', test_admin_id).execute()
        except:
            pass
        
        # 創建管理員測試數據
        test_data = {
            'user_id': test_admin_id,
            'level': 8,
            'correct': 25,
            'wrong': 8,
            'correct_in_level': 3,
            'daily_quota': 1,
            'streak_days': 7,
            'last_updated': datetime.datetime.now().isoformat(),
            'correct_qids': [1, 2, 3, 4, 5, 6, 7, 8]
        }
        
        supabase.table('user_stats').upsert(test_data).execute()
        print(f"✅ 已創建管理員測試數據")
        
        # 模擬管理員發送重置指令
        with patch('app_supabase.send_message') as mock_send:
            with patch('app_supabase.is_admin_user', return_value=True):
                # 測試各種重置指令
                reset_commands = ['reset', 'RESET', '重置', '重設', '重新開始']
                
                for cmd in reset_commands:
                    print(f"  測試指令: '{cmd}'")
                    
                    # 模擬訊息處理
                    mock_message = {'text': cmd}
                    handle_text_message(test_admin_id, mock_message)
                    
                    # 檢查是否調用了發送訊息
                    assert mock_send.called, f"指令 '{cmd}' 沒有觸發訊息發送"
                    
                    # 檢查發送的訊息內容
                    sent_message = mock_send.call_args[0][1]
                    assert '進度重置成功' in sent_message['text'], f"指令 '{cmd}' 沒有發送正確的重置訊息"
                    
                    mock_send.reset_mock()
        
        # 驗證數據是否被重置
        after_stats = get_user_stats(test_admin_id)
        assert after_stats.get('level') == 1, "等級沒有被重置為1"
        assert after_stats.get('correct') == 0, "答對數沒有被重置為0"
        assert after_stats.get('wrong') == 0, "答錯數沒有被重置為0"
        
        print("✅ 管理員重置流程測試通過")
        
        # 清理測試數據
        supabase.table('user_stats').delete().eq('user_id', test_admin_id).execute()
        return True
        
    except Exception as e:
        print(f"❌ 管理員重置流程測試失敗: {e}")
        return False

def test_normal_user_reset_flow():
    """測試普通用戶重置流程"""
    print("\n🧪 測試普通用戶重置流程...")
    
    test_user_id = "test_normal_reset_12345"
    
    try:
        # 清理測試數據
        try:
            supabase.table('user_stats').delete().eq('user_id', test_user_id).execute()
        except:
            pass
        
        # 創建普通用戶測試數據
        test_data = {
            'user_id': test_user_id,
            'level': 3,
            'correct': 8,
            'wrong': 3,
            'correct_in_level': 2,
            'daily_quota': 2,
            'streak_days': 2,
            'last_updated': datetime.datetime.now().isoformat(),
            'correct_qids': [1, 2, 3, 4, 5]
        }
        
        supabase.table('user_stats').upsert(test_data).execute()
        print(f"✅ 已創建普通用戶測試數據")
        
        # 模擬普通用戶發送重置指令
        with patch('app_supabase.send_message') as mock_send:
            with patch('app_supabase.is_admin_user', return_value=False):
                with patch('app_supabase.check_daily_question_limit', return_value={'can_answer': True}):
                    # 測試重置指令
                    mock_message = {'text': '重置'}
                    handle_text_message(test_user_id, mock_message)
                    
                    # 檢查是否調用了發送訊息
                    assert mock_send.called, "重置指令沒有觸發訊息發送"
                    
                    # 檢查發送的訊息內容
                    sent_message = mock_send.call_args[0][1]
                    assert '進度重置成功' in sent_message['text'], "沒有發送正確的重置訊息"
        
        # 驗證數據是否被重置
        after_stats = get_user_stats(test_user_id)
        assert after_stats.get('level') == 1, "等級沒有被重置為1"
        assert after_stats.get('correct') == 0, "答對數沒有被重置為0"
        assert after_stats.get('wrong') == 0, "答錯數沒有被重置為0"
        
        print("✅ 普通用戶重置流程測試通過")
        
        # 清理測試數據
        supabase.table('user_stats').delete().eq('user_id', test_user_id).execute()
        return True
        
    except Exception as e:
        print(f"❌ 普通用戶重置流程測試失敗: {e}")
        return False

def test_admin_reset_other_user():
    """測試管理員重置其他用戶"""
    print("\n🧪 測試管理員重置其他用戶...")
    
    admin_id = "test_admin_12345"
    target_user_id = "test_target_user_12345"
    
    try:
        # 清理測試數據
        for user_id in [admin_id, target_user_id]:
            try:
                supabase.table('user_stats').delete().eq('user_id', user_id).execute()
            except:
                pass
        
        # 創建目標用戶數據
        target_data = {
            'user_id': target_user_id,
            'level': 5,
            'correct': 12,
            'wrong': 4,
            'correct_in_level': 1,
            'daily_quota': 1,
            'streak_days': 3,
            'last_updated': datetime.datetime.now().isoformat(),
            'correct_qids': [1, 2, 3, 4]
        }
        
        supabase.table('user_stats').upsert(target_data).execute()
        print(f"✅ 已創建目標用戶測試數據")
        
        # 模擬管理員發送重置他人指令
        with patch('app_supabase.send_message') as mock_send:
            with patch('app_supabase.is_admin_user', return_value=True):
                # 測試管理員重置他人指令
                mock_message = {'text': f'/admin reset {target_user_id}'}
                handle_text_message(admin_id, mock_message)
                
                # 檢查是否調用了發送訊息（應該發送給管理員和目標用戶）
                assert mock_send.call_count >= 1, "管理員重置他人指令沒有觸發訊息發送"
        
        # 驗證目標用戶數據是否被重置
        after_stats = get_user_stats(target_user_id)
        assert after_stats.get('level') == 1, "目標用戶等級沒有被重置為1"
        assert after_stats.get('correct') == 0, "目標用戶答對數沒有被重置為0"
        assert after_stats.get('wrong') == 0, "目標用戶答錯數沒有被重置為0"
        
        print("✅ 管理員重置其他用戶測試通過")
        
        # 清理測試數據
        for user_id in [admin_id, target_user_id]:
            try:
                supabase.table('user_stats').delete().eq('user_id', user_id).execute()
            except:
                pass
        
        return True
        
    except Exception as e:
        print(f"❌ 管理員重置其他用戶測試失敗: {e}")
        return False

def main():
    """主測試函數"""
    print("🚀 開始測試RESET功能的完整webhook流程...")
    print("=" * 60)
    
    # 檢查數據庫連接
    if not supabase:
        print("❌ 無法連接到數據庫")
        return False
    
    # 測試項目
    tests = [
        ("管理員重置流程測試", test_admin_reset_flow),
        ("普通用戶重置流程測試", test_normal_user_reset_flow),
        ("管理員重置其他用戶測試", test_admin_reset_other_user),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 執行: {test_name}")
        print("-" * 40)
        try:
            result = test_func()
            results.append((test_name, result))
            status = "✅ 通過" if result else "❌ 失敗"
            print(f"{status}: {test_name}")
        except Exception as e:
            print(f"❌ 測試異常: {test_name} - {e}")
            results.append((test_name, False))
    
    # 總結
    print("\n" + "=" * 60)
    print("📊 測試結果總結:")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    total = len(results)
    print(f"\n🏆 總計: {passed}/{total} 項測試通過")
    
    if passed == total:
        print("🎉 所有webhook流程測試都通過！RESET功能完全修復！")
    else:
        print("⚠️ 部分測試失敗，請檢查相關功能")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

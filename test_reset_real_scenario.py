#!/usr/bin/env python3
"""
測試RESET功能的真實場景模擬
模擬真實的LINE Bot webhook請求
"""

import sys
import os
import json
import datetime
from unittest.mock import patch, MagicMock

# 添加項目根目錄到Python路徑
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from app_supabase import app, supabase

def create_line_webhook_payload(user_id, message_text):
    """創建LINE webhook請求的模擬payload"""
    return {
        "events": [
            {
                "type": "message",
                "source": {
                    "userId": user_id,
                    "type": "user"
                },
                "message": {
                    "type": "text",
                    "text": message_text
                },
                "timestamp": int(datetime.datetime.now().timestamp() * 1000),
                "replyToken": "test_reply_token"
            }
        ]
    }

def test_line_webhook_reset():
    """測試通過LINE webhook的RESET功能"""
    print("🧪 測試LINE webhook RESET功能...")
    
    test_user_id = "U1234567890abcdef_line_test"
    
    try:
        # 清理測試數據
        try:
            supabase.table('user_stats').delete().eq('user_id', test_user_id).execute()
        except:
            pass
        
        # 創建測試用戶數據
        test_data = {
            'user_id': test_user_id,
            'level': 6,
            'correct': 18,
            'wrong': 7,
            'correct_in_level': 2,
            'daily_quota': 1,
            'streak_days': 4,
            'last_updated': datetime.datetime.now().isoformat(),
            'correct_qids': [1, 2, 3, 4, 5, 6, 7]
        }
        
        supabase.table('user_stats').upsert(test_data).execute()
        print(f"✅ 已創建測試用戶數據 (等級: {test_data['level']}, 答對: {test_data['correct']})")
        
        # 模擬LINE Bot發送訊息的函數
        sent_messages = []
        def mock_send_message(user_id, message):
            sent_messages.append((user_id, message))
            print(f"📤 模擬發送訊息給 {user_id}: {message.get('text', 'N/A')[:50]}...")
        
        with patch('app_supabase.send_message', side_effect=mock_send_message):
            with patch('app_supabase.is_admin_user', return_value=False):  # 測試普通用戶
                
                # 測試不同的重置指令
                reset_commands = ['reset', 'RESET', '重置', '重設', '重新開始']
                
                for i, cmd in enumerate(reset_commands):
                    print(f"\n📋 測試指令 {i+1}/5: '{cmd}'")
                    
                    # 創建webhook payload
                    payload = create_line_webhook_payload(test_user_id, cmd)
                    
                    # 直接調用webhook函數進行測試
                    from app_supabase import webhook
                    
                    # 模擬Flask request對象
                    with patch('app_supabase.request') as mock_request:
                        mock_request.get_json.return_value = payload
                        response_text, status_code = webhook()
                        
                        print(f"  HTTP響應狀態: {status_code}")
                        assert status_code == 200, f"Webhook請求失敗: {status_code}"
                    
                    # 檢查是否發送了重置成功的訊息
                    if sent_messages:
                        last_message = sent_messages[-1][1]['text']
                        assert '進度重置成功' in last_message, f"指令 '{cmd}' 沒有發送正確的重置訊息"
                        print(f"  ✅ 重置訊息已發送")
                    else:
                        print(f"  ❌ 沒有發送任何訊息")
                        return False
        
        # 驗證數據是否被重置
        after_stats = supabase.table('user_stats').select('*').eq('user_id', test_user_id).execute()
        if after_stats.data:
            stats = after_stats.data[0]
            assert stats.get('level') == 1, f"等級沒有被重置為1，當前為: {stats.get('level')}"
            assert stats.get('correct') == 0, f"答對數沒有被重置為0，當前為: {stats.get('correct')}"
            assert stats.get('wrong') == 0, f"答錯數沒有被重置為0，當前為: {stats.get('wrong')}"
            print(f"✅ 數據驗證成功 - 等級: {stats.get('level')}, 答對: {stats.get('correct')}, 答錯: {stats.get('wrong')}")
        else:
            print("❌ 無法獲取重置後的數據")
            return False
        
        # 清理測試數據
        supabase.table('user_stats').delete().eq('user_id', test_user_id).execute()
        print("🧹 已清理測試數據")
        
        return True
        
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        return False

def test_admin_webhook_reset():
    """測試管理員通過webhook的RESET功能"""
    print("\n🧪 測試管理員webhook RESET功能...")
    
    admin_user_id = "U_admin_test_12345"
    
    try:
        # 清理測試數據
        try:
            supabase.table('user_stats').delete().eq('user_id', admin_user_id).execute()
        except:
            pass
        
        # 創建管理員測試數據
        admin_data = {
            'user_id': admin_user_id,
            'level': 10,
            'correct': 35,
            'wrong': 12,
            'correct_in_level': 5,
            'daily_quota': 0,
            'streak_days': 8,
            'last_updated': datetime.datetime.now().isoformat(),
            'correct_qids': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        }
        
        supabase.table('user_stats').upsert(admin_data).execute()
        print(f"✅ 已創建管理員測試數據 (等級: {admin_data['level']}, 答對: {admin_data['correct']})")
        
        # 模擬發送訊息
        sent_messages = []
        def mock_send_message(user_id, message):
            sent_messages.append((user_id, message))
            print(f"📤 模擬發送訊息給 {user_id}: {message.get('text', 'N/A')[:50]}...")
        
        with patch('app_supabase.send_message', side_effect=mock_send_message):
            with patch('app_supabase.is_admin_user', return_value=True):  # 測試管理員
                
                # 測試管理員重置自己
                payload = create_line_webhook_payload(admin_user_id, '重置')
                
                # 直接調用webhook函數進行測試
                from app_supabase import webhook
                
                with patch('app_supabase.request') as mock_request:
                    mock_request.get_json.return_value = payload
                    response_text, status_code = webhook()
                    
                    print(f"HTTP響應狀態: {status_code}")
                    assert status_code == 200, f"Webhook請求失敗: {status_code}"
                
                # 檢查管理員重置訊息
                if sent_messages:
                    last_message = sent_messages[-1][1]['text']
                    assert '管理員模式 - 進度重置成功' in last_message, "沒有發送管理員重置訊息"
                    print("✅ 管理員重置訊息已發送")
                else:
                    print("❌ 沒有發送任何訊息")
                    return False
        
        # 驗證管理員數據是否被重置
        after_stats = supabase.table('user_stats').select('*').eq('user_id', admin_user_id).execute()
        if after_stats.data:
            stats = after_stats.data[0]
            assert stats.get('level') == 1, f"管理員等級沒有被重置為1，當前為: {stats.get('level')}"
            assert stats.get('correct') == 0, f"管理員答對數沒有被重置為0，當前為: {stats.get('correct')}"
            print(f"✅ 管理員數據驗證成功 - 等級: {stats.get('level')}, 答對: {stats.get('correct')}")
        else:
            print("❌ 無法獲取管理員重置後的數據")
            return False
        
        # 清理測試數據
        supabase.table('user_stats').delete().eq('user_id', admin_user_id).execute()
        print("🧹 已清理管理員測試數據")
        
        return True
        
    except Exception as e:
        print(f"❌ 管理員測試失敗: {e}")
        return False

def main():
    """主測試函數"""
    print("🚀 開始RESET功能真實場景測試...")
    print("=" * 60)
    
    # 檢查數據庫連接
    if not supabase:
        print("❌ 無法連接到數據庫")
        return False
    
    # 測試項目
    tests = [
        ("LINE webhook普通用戶重置測試", test_line_webhook_reset),
        ("LINE webhook管理員重置測試", test_admin_webhook_reset),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 執行: {test_name}")
        print("-" * 50)
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
    print("📊 真實場景測試結果總結:")
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
        print("🎉 所有真實場景測試都通過！RESET功能在實際環境中正常工作！")
        print("\n💡 用戶可以在LINE Bot中使用以下指令重置進度：")
        print("   • reset")
        print("   • RESET") 
        print("   • 重置")
        print("   • 重設")
        print("   • 重新開始")
    else:
        print("⚠️ 部分測試失敗，請檢查相關功能")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

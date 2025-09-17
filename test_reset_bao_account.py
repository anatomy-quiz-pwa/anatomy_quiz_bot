#!/usr/bin/env python3
"""
在保的帳號上測試 RESET 功能
"""

import sys
import os
import datetime
from unittest.mock import patch

# 添加項目根目錄到Python路徑
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_bao_account_reset():
    """測試保的帳號 RESET 功能"""
    print("🧪 測試保的帳號 RESET 功能...")
    
    # 這裡使用從生產日志中看到的真實用戶ID
    bao_user_id = "U977c24d1fec3a2bf07035504e1444911"
    
    try:
        from app_supabase import (
            handle_text_message,
            get_user_stats,
            reset_user_progress,
            supabase,
            is_admin_user
        )
        
        print(f"📋 測試用戶ID: {bao_user_id}")
        
        # 1. 檢查用戶當前狀態
        print("\n🔍 檢查用戶當前狀態...")
        current_stats = get_user_stats(bao_user_id)
        if current_stats:
            print(f"📊 當前狀態:")
            print(f"  • 等級: {current_stats.get('level', 'N/A')}")
            print(f"  • 答對: {current_stats.get('correct', 'N/A')}")
            print(f"  • 答錯: {current_stats.get('wrong', 'N/A')}")
            print(f"  • 連續天數: {current_stats.get('streak_days', 'N/A')}")
        else:
            print("⚠️ 用戶數據不存在，創建初始數據...")
            # 創建測試數據
            test_data = {
                'user_id': bao_user_id,
                'level': 4,
                'correct': 14,
                'wrong': 4,
                'correct_in_level': 2,
                'daily_quota': 0,
                'streak_days': 2,
                'last_updated': datetime.datetime.now().isoformat(),
                'correct_qids': [1, 2, 3, 7, 24, 45, 78]
            }
            supabase.table('user_stats').insert(test_data).execute()
            current_stats = get_user_stats(bao_user_id)
            print("✅ 初始數據創建完成")
        
        # 2. 檢查管理員權限
        is_admin = is_admin_user(bao_user_id)
        user_type = "管理員" if is_admin else "普通用戶"
        print(f"🔑 用戶類型: {user_type}")
        
        # 3. 測試 RESET 功能
        print(f"\n🔄 測試 RESET 功能...")
        
        # 記錄發送的訊息
        sent_messages = []
        def mock_send_message(user_id, message):
            sent_messages.append((user_id, message))
            print(f"📤 模擬發送訊息: {message.get('text', 'N/A')[:100]}...")
        
        def mock_handle_nickname_input(user_id, text):
            return False
        
        # 測試不同的 RESET 指令
        reset_commands = ['RESET', 'reset', '重置', '重設', '重新開始']
        
        for i, cmd in enumerate(reset_commands):
            print(f"\n📋 測試指令 {i+1}/5: '{cmd}'")
            
            # 清空之前的訊息
            sent_messages.clear()
            
            with patch('app_supabase.send_message', side_effect=mock_send_message):
                with patch('app_supabase.handle_nickname_input', side_effect=mock_handle_nickname_input):
                    
                    # 模擬用戶發送訊息
                    mock_message = {'text': cmd}
                    handle_text_message(bao_user_id, mock_message)
            
            # 檢查結果
            if sent_messages:
                last_message = sent_messages[-1][1]['text']
                if '進度重置成功' in last_message:
                    print(f"  ✅ 指令 '{cmd}' 處理成功")
                else:
                    print(f"  ❌ 指令 '{cmd}' 處理失敗")
                    print(f"      收到訊息: {last_message[:100]}...")
            else:
                print(f"  ❌ 指令 '{cmd}' 沒有發送任何訊息")
            
            # 只測試第一個指令的完整流程，其他只測試處理
            if i == 0:
                # 檢查數據是否被重置
                after_stats = get_user_stats(bao_user_id)
                if after_stats:
                    print(f"📊 重置後狀態:")
                    print(f"  • 等級: {after_stats.get('level', 'N/A')}")
                    print(f"  • 答對: {after_stats.get('correct', 'N/A')}")
                    print(f"  • 答錯: {after_stats.get('wrong', 'N/A')}")
                    print(f"  • 連續天數: {after_stats.get('streak_days', 'N/A')}")
                    
                    # 驗證重置是否成功
                    if (after_stats.get('level') == 1 and 
                        after_stats.get('correct') == 0 and 
                        after_stats.get('wrong') == 0):
                        print("  ✅ 數據重置成功")
                        reset_success = True
                    else:
                        print("  ❌ 數據重置失敗")
                        reset_success = False
                else:
                    print("  ❌ 無法獲取重置後數據")
                    reset_success = False
        
        return reset_success
        
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        return False

def test_direct_reset_function():
    """直接測試 reset_user_progress 函數"""
    print("\n🧪 直接測試 reset_user_progress 函數...")
    
    bao_user_id = "U977c24d1fec3a2bf07035504e1444911"
    
    try:
        from app_supabase import reset_user_progress, get_user_stats
        
        # 獲取重置前狀態
        before_stats = get_user_stats(bao_user_id)
        print(f"📊 重置前: 等級={before_stats.get('level') if before_stats else 'N/A'}, 答對={before_stats.get('correct') if before_stats else 'N/A'}")
        
        # 執行重置
        reset_result = reset_user_progress(bao_user_id)
        print(f"🔄 重置執行結果: {reset_result}")
        
        if reset_result:
            # 獲取重置後狀態
            after_stats = get_user_stats(bao_user_id)
            print(f"📊 重置後: 等級={after_stats.get('level') if after_stats else 'N/A'}, 答對={after_stats.get('correct') if after_stats else 'N/A'}")
            
            if (after_stats and 
                after_stats.get('level') == 1 and 
                after_stats.get('correct') == 0):
                print("✅ 直接重置功能正常")
                return True
            else:
                print("❌ 直接重置功能異常")
                return False
        else:
            print("❌ 重置函數執行失敗")
            return False
            
    except Exception as e:
        print(f"❌ 直接測試失敗: {e}")
        return False

def simulate_production_webhook():
    """模擬生產環境的 webhook 請求"""
    print("\n🧪 模擬生產環境 webhook 請求...")
    
    bao_user_id = "U977c24d1fec3a2bf07035504e1444911"
    
    try:
        from app_supabase import webhook
        import json
        
        # 創建模擬的 LINE webhook payload
        webhook_payload = {
            "events": [
                {
                    "type": "message",
                    "source": {
                        "userId": bao_user_id,
                        "type": "user"
                    },
                    "message": {
                        "type": "text",
                        "text": "RESET"
                    },
                    "timestamp": int(datetime.datetime.now().timestamp() * 1000),
                    "replyToken": "test_reply_token_for_bao"
                }
            ]
        }
        
        print(f"📋 模擬 webhook payload:")
        print(f"  • 用戶ID: {bao_user_id}")
        print(f"  • 訊息: RESET")
        
        # 記錄發送的訊息
        sent_messages = []
        def mock_send_message(user_id, message):
            sent_messages.append((user_id, message))
            print(f"📤 Webhook 發送訊息: {message.get('text', 'N/A')[:50]}...")
        
        # 模擬 webhook 處理
        with patch('app_supabase.request') as mock_request:
            with patch('app_supabase.send_message', side_effect=mock_send_message):
                with patch('app_supabase.handle_nickname_input', return_value=False):
                    
                    mock_request.get_json.return_value = webhook_payload
                    
                    # 調用 webhook 函數
                    response_text, status_code = webhook()
                    
                    print(f"📋 Webhook 響應: {status_code}")
                    
                    if status_code == 200:
                        print("✅ Webhook 處理成功")
                        
                        if sent_messages:
                            last_message = sent_messages[-1][1]['text']
                            if '進度重置成功' in last_message:
                                print("✅ RESET 功能通過 webhook 正常工作")
                                return True
                            else:
                                print("❌ RESET 功能通過 webhook 沒有正確處理")
                                print(f"收到訊息: {last_message[:100]}...")
                                return False
                        else:
                            print("❌ Webhook 沒有發送任何訊息")
                            return False
                    else:
                        print(f"❌ Webhook 處理失敗，狀態碼: {status_code}")
                        return False
        
    except Exception as e:
        print(f"❌ Webhook 模擬失敗: {e}")
        return False

def main():
    """主測試函數"""
    print("🚀 保的帳號 RESET 功能測試")
    print("=" * 50)
    
    # 執行測試
    tests = [
        ("直接重置功能測試", test_direct_reset_function),
        ("完整訊息處理測試", test_bao_account_reset),
        ("Webhook 模擬測試", simulate_production_webhook),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 執行: {test_name}")
        print("-" * 30)
        try:
            result = test_func()
            results.append((test_name, result))
            status = "✅ 通過" if result else "❌ 失敗"
            print(f"{status}: {test_name}")
        except Exception as e:
            print(f"❌ 測試異常: {test_name} - {e}")
            results.append((test_name, False))
    
    # 總結
    print("\n" + "=" * 50)
    print("📊 保的帳號 RESET 測試結果")
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
        print("""
🎉 保的帳號 RESET 功能測試全部通過！

✅ 測試結果：
• 直接重置功能正常
• 訊息處理流程正常
• Webhook 模擬正常

💡 這表示：
• RESET 功能已經修復
• 在實際環境中應該可以正常使用
• 用戶發送 RESET 指令會收到正確回應

🔧 如果生產環境仍有問題：
• 可能是部署還沒完成
• 或者需要清除緩存重新部署
""")
    else:
        print(f"""
⚠️ 發現 {total-passed} 個問題：
""")
        for test_name, result in results:
            if not result:
                print(f"  • {test_name}")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

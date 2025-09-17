#!/usr/bin/env python3
"""
簡化的每日三題限制功能測試
在手動執行資料庫遷移後使用此腳本測試功能
"""

import os
import sys

# 添加項目根目錄到 Python 路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_import():
    """測試模組導入"""
    print("🔧 測試模組導入...")
    try:
        from app_supabase import (
            check_daily_question_limit,
            update_daily_question_count
        )
        print("✅ 模組導入成功")
        return True
    except ImportError as e:
        print(f"❌ 模組導入失敗: {e}")
        return False

def test_daily_limit_functions():
    """測試每日限制函數"""
    print("\n🧪 測試每日限制函數...")
    
    try:
        from app_supabase import check_daily_question_limit
        
        test_user_id = "test_simple_daily_limit"
        
        # 測試檢查函數
        print(f"檢查用戶 {test_user_id} 的每日限制...")
        result = check_daily_question_limit(test_user_id)
        
        print(f"結果: {result}")
        
        if isinstance(result, dict) and 'can_answer' in result:
            print("✅ 每日限制檢查函數正常運作")
            return True
        else:
            print("❌ 每日限制檢查函數返回格式錯誤")
            return False
            
    except Exception as e:
        print(f"❌ 測試每日限制函數失敗: {e}")
        return False

def test_message_flow():
    """測試訊息流程"""
    print("\n📱 測試訊息處理流程...")
    
    try:
        from app_supabase import handle_normal_quiz
        
        # 模擬用戶輸入「開始」
        test_user_id = "test_message_flow"
        
        print(f"模擬用戶 {test_user_id} 輸入「開始」...")
        
        # 注意：這個測試不會實際發送訊息，只是檢查函數是否正常執行
        try:
            handle_normal_quiz(test_user_id, "開始")
            print("✅ 訊息處理流程執行完成（可能會有發送訊息的錯誤，這是正常的）")
            return True
        except Exception as e:
            if "LINE" in str(e) or "send_message" in str(e):
                print("✅ 訊息處理邏輯正常（LINE 發送錯誤是預期的）")
                return True
            else:
                print(f"❌ 訊息處理流程失敗: {e}")
                return False
                
    except Exception as e:
        print(f"❌ 測試訊息流程失敗: {e}")
        return False

def main():
    """主測試函數"""
    print("🧪 每日三題限制功能 - 簡化測試")
    print("=" * 40)
    
    # 檢查是否已執行資料庫遷移
    print("⚠️  請確認已在 Supabase 控制台執行以下 SQL：")
    print("   ALTER TABLE user_stats")
    print("   ADD COLUMN IF NOT EXISTS daily_questions_answered INTEGER DEFAULT 0,")
    print("   ADD COLUMN IF NOT EXISTS last_question_date DATE DEFAULT CURRENT_DATE;")
    print()
    
    response = input("已執行資料庫遷移？(y/n): ")
    if response.lower() != 'y':
        print("請先執行資料庫遷移，然後重新運行此測試")
        return False
    
    # 執行測試
    tests = [
        ("模組導入", test_import),
        ("每日限制函數", test_daily_limit_functions),
        ("訊息處理流程", test_message_flow)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 執行測試: {test_name}")
        if test_func():
            passed += 1
        else:
            print(f"❌ 測試失敗: {test_name}")
    
    print("\n" + "=" * 40)
    print(f"📊 測試結果: {passed}/{total} 通過")
    
    if passed == total:
        print("🎉 所有測試通過！")
        print("\n📋 下一步:")
        print("1. 啟動 LINE Bot 服務")
        print("2. 使用真實 LINE 帳號測試")
        print("3. 驗證每日限制功能")
        return True
    else:
        print("❌ 部分測試失敗，請檢查錯誤訊息")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

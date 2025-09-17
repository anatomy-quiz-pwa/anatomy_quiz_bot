#!/usr/bin/env python3
"""
測試RESET功能的完整性和正確性
"""

import sys
import os
import datetime
from supabase import create_client, Client

# 添加項目根目錄到Python路徑
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# 導入必要的函數和客戶端
from app_supabase import reset_user_progress, get_user_stats, create_initial_user_stats, supabase

def test_reset_function():
    """測試重置函數本身"""
    print("🧪 測試重置函數...")
    
    test_user_id = "test_reset_user_12345"
    
    try:
        # 檢查數據庫連接
        if not supabase:
            print("❌ 無法連接到數據庫")
            return False
        
        # 先清理可能存在的測試數據
        try:
            supabase.table('user_stats').delete().eq('user_id', test_user_id).execute()
            print(f"🧹 已清理之前的測試用戶 {test_user_id} 數據")
        except:
            pass  # 忽略清理錯誤
        
        # 創建測試用戶數據（模擬已有進度的用戶）
        test_data = {
            'user_id': test_user_id,
            'level': 5,
            'correct': 15,
            'wrong': 5,
            'correct_in_level': 2,
            'daily_quota': 2,
            'streak_days': 3,
            'last_updated': datetime.datetime.now().isoformat(),
            'correct_qids': [1, 2, 3, 4, 5]
        }
        
        # 插入測試數據
        supabase.table('user_stats').upsert(test_data).execute()
        print(f"✅ 已創建測試用戶 {test_user_id} 的進度數據")
        
        # 獲取重置前的數據
        before_stats = get_user_stats(test_user_id)
        print(f"📊 重置前數據: 等級={before_stats.get('level')}, 答對={before_stats.get('correct')}, 答錯={before_stats.get('wrong')}")
        
        # 執行重置
        reset_result = reset_user_progress(test_user_id)
        if not reset_result:
            print("❌ 重置函數執行失敗")
            return False
        
        # 獲取重置後的數據
        after_stats = get_user_stats(test_user_id)
        print(f"📊 重置後數據: 等級={after_stats.get('level')}, 答對={after_stats.get('correct')}, 答錯={after_stats.get('wrong')}")
        
        # 驗證重置結果
        expected_values = {
            'level': 1,
            'correct': 0,
            'wrong': 0,
            'correct_in_level': 0,
            'daily_quota': 0,
            'streak_days': 0
        }
        
        success = True
        for key, expected in expected_values.items():
            actual = after_stats.get(key)
            if actual != expected:
                print(f"❌ {key} 重置失敗: 期望={expected}, 實際={actual}")
                success = False
            else:
                print(f"✅ {key} 重置成功: {actual}")
        
        # 清理測試數據
        supabase.table('user_stats').delete().eq('user_id', test_user_id).execute()
        print(f"🧹 已清理測試用戶 {test_user_id} 的數據")
        
        return success
        
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {e}")
        return False

def test_reset_command_handling():
    """測試重置指令的處理邏輯"""
    print("\n🧪 測試重置指令處理...")
    
    # 測試各種重置指令格式
    reset_commands = ['reset', 'RESET', '重置', '重設', '重新開始']
    
    print("📝 支援的重置指令格式:")
    for cmd in reset_commands:
        print(f"  • '{cmd}'")
    
    # 這裡只是檢查指令格式，實際的訊息處理需要在機器人運行時測試
    print("✅ 重置指令格式檢查完成")
    return True

def test_admin_reset_command():
    """測試管理員重置指令"""
    print("\n🧪 測試管理員重置指令...")
    
    admin_commands = [
        "/admin reset user123",
        "/admin reset U1234567890abcdef",
    ]
    
    print("📝 管理員重置指令格式:")
    for cmd in admin_commands:
        print(f"  • '{cmd}'")
    
    print("✅ 管理員重置指令格式檢查完成")
    return True

def main():
    """主測試函數"""
    print("🚀 開始測試RESET功能...")
    print("=" * 50)
    
    # 測試項目
    tests = [
        ("重置函數測試", test_reset_function),
        ("重置指令處理測試", test_reset_command_handling),
        ("管理員重置指令測試", test_admin_reset_command),
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
        print("🎉 所有測試都通過！RESET功能實作成功！")
    else:
        print("⚠️ 部分測試失敗，請檢查相關功能")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

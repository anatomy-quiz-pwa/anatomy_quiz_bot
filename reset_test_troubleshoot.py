#!/usr/bin/env python3
"""
RESET測試問題診斷工具
"""

import sys
import os
import subprocess

# 添加項目根目錄到Python路徑
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def check_environment():
    """檢查環境設置"""
    print("🔍 檢查環境設置...")
    
    issues = []
    
    # 檢查 Python 版本
    python_version = sys.version_info
    print(f"Python 版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        issues.append("Python 版本過低，建議使用 Python 3.8+")
    
    # 檢查必要的模組
    required_modules = ['flask', 'supabase', 'requests']
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module} 模組已安裝")
        except ImportError:
            print(f"❌ {module} 模組未安裝")
            issues.append(f"缺少 {module} 模組")
    
    # 檢查環境變數
    env_vars = ['SUPABASE_URL', 'SUPABASE_ANON_KEY']
    for var in env_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var} 已設置")
        else:
            print(f"⚠️ {var} 未設置（使用預設值）")
    
    return issues

def check_files():
    """檢查測試文件是否存在"""
    print("\n📁 檢查測試文件...")
    
    test_files = [
        'test_reset_functionality.py',
        'test_reset_webhook_flow.py', 
        'test_reset_final.py',
        'app_supabase.py'
    ]
    
    missing_files = []
    
    for file in test_files:
        if os.path.exists(file):
            print(f"✅ {file} 存在")
        else:
            print(f"❌ {file} 不存在")
            missing_files.append(file)
    
    return missing_files

def test_import():
    """測試模組導入"""
    print("\n📦 測試模組導入...")
    
    try:
        from app_supabase import reset_user_progress, supabase, get_user_stats
        print("✅ 成功導入 app_supabase 模組")
        return True
    except ImportError as e:
        print(f"❌ 導入 app_supabase 失敗: {e}")
        return False
    except Exception as e:
        print(f"❌ 導入時發生錯誤: {e}")
        return False

def test_database_connection():
    """測試數據庫連接"""
    print("\n🔗 測試數據庫連接...")
    
    try:
        from app_supabase import supabase
        
        if not supabase:
            print("❌ Supabase 客戶端未初始化")
            return False
        
        # 嘗試簡單查詢
        result = supabase.table('user_stats').select('count').limit(1).execute()
        print("✅ 數據庫連接正常")
        return True
        
    except Exception as e:
        print(f"❌ 數據庫連接失敗: {e}")
        return False

def run_simple_test():
    """運行簡單的重置功能測試"""
    print("\n🧪 運行簡單測試...")
    
    try:
        from app_supabase import reset_user_progress, get_user_stats, supabase
        import datetime
        
        test_user_id = "diagnostic_test_user"
        
        # 清理可能存在的測試數據
        try:
            supabase.table('user_stats').delete().eq('user_id', test_user_id).execute()
        except:
            pass
        
        # 創建測試數據
        test_data = {
            'user_id': test_user_id,
            'level': 5,
            'correct': 10,
            'wrong': 3,
            'correct_in_level': 2,
            'daily_quota': 1,
            'streak_days': 2,
            'last_updated': datetime.datetime.now().isoformat(),
            'correct_qids': [1, 2, 3]
        }
        
        supabase.table('user_stats').insert(test_data).execute()
        print("✅ 創建測試數據成功")
        
        # 測試重置功能
        result = reset_user_progress(test_user_id)
        
        if result:
            print("✅ 重置功能執行成功")
            
            # 驗證重置結果
            after_stats = get_user_stats(test_user_id)
            if after_stats and after_stats.get('level') == 1 and after_stats.get('correct') == 0:
                print("✅ 重置結果驗證成功")
                success = True
            else:
                print("❌ 重置結果驗證失敗")
                success = False
        else:
            print("❌ 重置功能執行失敗")
            success = False
        
        # 清理測試數據
        supabase.table('user_stats').delete().eq('user_id', test_user_id).execute()
        print("✅ 清理測試數據完成")
        
        return success
        
    except Exception as e:
        print(f"❌ 簡單測試失敗: {e}")
        return False

def provide_solutions(issues, missing_files, import_ok, db_ok, test_ok):
    """提供解決方案"""
    print("\n" + "="*50)
    print("💡 問題診斷和解決方案")
    print("="*50)
    
    if issues:
        print("\n❌ 環境問題:")
        for issue in issues:
            print(f"  • {issue}")
        print("\n解決方案:")
        print("  • 升級 Python 到 3.8+")
        print("  • 安裝缺少的模組: pip install flask supabase requests")
    
    if missing_files:
        print("\n❌ 文件缺失:")
        for file in missing_files:
            print(f"  • {file}")
        print("\n解決方案:")
        print("  • 確認您在正確的項目目錄中")
        print("  • 檢查文件是否被意外刪除")
    
    if not import_ok:
        print("\n❌ 模組導入問題:")
        print("解決方案:")
        print("  • 檢查 app_supabase.py 文件是否存在語法錯誤")
        print("  • 確認所有依賴模組已正確安裝")
        print("  • 嘗試: python -c \"import app_supabase\" 查看詳細錯誤")
    
    if not db_ok:
        print("\n❌ 數據庫連接問題:")
        print("解決方案:")
        print("  • 檢查網路連接")
        print("  • 確認 SUPABASE_URL 和 SUPABASE_ANON_KEY 設置正確")
        print("  • 檢查 Supabase 服務是否正常")
    
    if not test_ok:
        print("\n❌ 功能測試失敗:")
        print("解決方案:")
        print("  • 檢查 reset_user_progress 函數實作")
        print("  • 確認數據庫表結構正確")
        print("  • 檢查權限設置")
    
    if not any([issues, missing_files]) and import_ok and db_ok and test_ok:
        print("\n✅ 所有檢查都通過！")
        print("RESET 測試功能應該可以正常使用。")
        print("\n如果仍然遇到問題，請提供具體的錯誤訊息。")

def main():
    """主函數"""
    print("🔧 RESET測試問題診斷工具")
    print("="*40)
    
    # 執行各項檢查
    issues = check_environment()
    missing_files = check_files()
    import_ok = test_import()
    db_ok = test_database_connection()
    test_ok = run_simple_test()
    
    # 提供解決方案
    provide_solutions(issues, missing_files, import_ok, db_ok, test_ok)
    
    # 總結
    print("\n" + "="*50)
    print("📊 診斷結果總結")
    print("="*50)
    
    checks = [
        ("環境設置", len(issues) == 0),
        ("文件完整性", len(missing_files) == 0),
        ("模組導入", import_ok),
        ("數據庫連接", db_ok),
        ("功能測試", test_ok)
    ]
    
    passed = 0
    for check_name, result in checks:
        status = "✅ 正常" if result else "❌ 異常"
        print(f"{status}: {check_name}")
        if result:
            passed += 1
    
    total = len(checks)
    print(f"\n🏆 總計: {passed}/{total} 項檢查通過")
    
    if passed == total:
        print("\n🎉 診斷完成！RESET測試功能應該可以正常使用。")
        print("\n可用的測試指令:")
        print("  • python test_reset_functionality.py")
        print("  • python test_reset_webhook_flow.py")
        print("  • python test_reset_final.py")
    else:
        print(f"\n⚠️ 發現 {total-passed} 個問題，請根據上述解決方案進行修復。")

if __name__ == "__main__":
    main()

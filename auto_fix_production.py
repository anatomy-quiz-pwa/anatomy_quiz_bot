#!/usr/bin/env python3
"""
自動修復生產環境排行榜問題
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

def main():
    """主函數"""
    print("🔧 自動修復生產環境排行榜問題...")
    
    # 1. 檢查文件是否存在
    if not os.path.exists('app_supabase_production_fixed.py'):
        print("❌ 找不到修復後的代碼文件")
        return False
    
    # 2. 備份原始生產環境代碼
    production_path = "/Users/baobaoc/Dev/anatomy_quiz_bot/app_supabase.py"
    backup_path = "/Users/baobaoc/Dev/anatomy_quiz_bot/app_supabase.py.backup"
    
    if os.path.exists(production_path):
        try:
            shutil.copy2(production_path, backup_path)
            print(f"✅ 已備份原始代碼到: {backup_path}")
        except Exception as e:
            print(f"❌ 備份失敗: {e}")
            return False
    else:
        print(f"⚠️ 找不到生產環境代碼: {production_path}")
        print("請確認生產環境代碼路徑是否正確")
        return False
    
    # 3. 複製修復後的代碼
    try:
        shutil.copy2('app_supabase_production_fixed.py', production_path)
        print("✅ 已複製修復後的代碼到生產環境")
    except Exception as e:
        print(f"❌ 複製失敗: {e}")
        return False
    
    # 4. 檢查修復是否成功
    try:
        with open(production_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 檢查關鍵函數是否存在
        required_functions = [
            'send_leaderboard_message',
            'get_leaderboard_data',
            'create_leaderboard_flex_message',
            '排行榜'
        ]
        
        missing_functions = []
        for func in required_functions:
            if func not in content:
                missing_functions.append(func)
        
        if missing_functions:
            print(f"❌ 缺少關鍵函數: {missing_functions}")
            return False
        
        print("✅ 修復後的代碼檢查通過")
        
    except Exception as e:
        print(f"❌ 檢查失敗: {e}")
        return False
    
    # 5. 提供重啟指令
    print("\n🚀 修復完成！請執行以下步驟重啟生產環境:")
    print("1. 停止現有的應用程式:")
    print("   pkill -f uvicorn")
    print("   pkill -f python")
    print()
    print("2. 重新啟動應用程式:")
    print("   cd /Users/baobaoc/Dev/anatomy_quiz_bot")
    print("   python app_supabase.py")
    print()
    print("3. 測試排行榜功能:")
    print("   在 LINE Bot 中輸入「排行榜」")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

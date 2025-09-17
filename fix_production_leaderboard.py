#!/usr/bin/env python3
"""
修復生產環境排行榜問題
這個腳本會檢查並修復生產環境的應用程式代碼
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

def check_production_app():
    """檢查生產環境應用程式"""
    production_path = "/Users/baobaoc/Dev/anatomy_quiz_bot/app_supabase.py"
    
    if not os.path.exists(production_path):
        print(f"❌ 找不到生產環境應用程式: {production_path}")
        return False
    
    print(f"✅ 找到生產環境應用程式: {production_path}")
    return True

def backup_production_app():
    """備份生產環境應用程式"""
    production_path = "/Users/baobaoc/Dev/anatomy_quiz_bot/app_supabase.py"
    backup_path = "/Users/baobaoc/Dev/anatomy_quiz_bot/app_supabase.py.backup"
    
    try:
        shutil.copy2(production_path, backup_path)
        print(f"✅ 已備份生產環境應用程式到: {backup_path}")
        return True
    except Exception as e:
        print(f"❌ 備份失敗: {e}")
        return False

def check_fixed_app():
    """檢查修復後的應用程式"""
    fixed_path = "app_supabase_fixed.py"
    
    if not os.path.exists(fixed_path):
        print(f"❌ 找不到修復後的應用程式: {fixed_path}")
        return False
    
    print(f"✅ 找到修復後的應用程式: {fixed_path}")
    return True

def copy_fixed_app():
    """複製修復後的應用程式到生產環境"""
    fixed_path = "app_supabase_fixed.py"
    production_path = "/Users/baobaoc/Dev/anatomy_quiz_bot/app_supabase.py"
    
    try:
        shutil.copy2(fixed_path, production_path)
        print(f"✅ 已複製修復後的應用程式到生產環境")
        return True
    except Exception as e:
        print(f"❌ 複製失敗: {e}")
        return False

def check_leaderboard_logic():
    """檢查排行榜邏輯是否存在"""
    production_path = "/Users/baobaoc/Dev/anatomy_quiz_bot/app_supabase.py"
    
    try:
        with open(production_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 檢查關鍵函數是否存在
        checks = [
            ("send_leaderboard_message", "send_leaderboard_message 函數"),
            ("create_leaderboard_flex_message", "create_leaderboard_flex_message 函數"),
            ("get_leaderboard_data", "get_leaderboard_data 函數"),
            ("排行榜", "排行榜關鍵字處理"),
            ("handle_normal_quiz", "handle_normal_quiz 函數")
        ]
        
        for check, name in checks:
            if check in content:
                print(f"✅ {name} 存在")
            else:
                print(f"❌ {name} 不存在")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ 檢查失敗: {e}")
        return False

def restart_production_app():
    """重啟生產環境應用程式"""
    try:
        # 停止現有的應用程式
        subprocess.run(["pkill", "-f", "uvicorn"], check=False)
        subprocess.run(["pkill", "-f", "python.*app_supabase"], check=False)
        print("✅ 已停止現有的應用程式")
        
        # 等待一下
        import time
        time.sleep(2)
        
        # 啟動新的應用程式
        production_dir = "/Users/baobaoc/Dev/anatomy_quiz_bot"
        result = subprocess.run(
            ["python", "app_supabase.py"],
            cwd=production_dir,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ 生產環境應用程式已重啟")
            return True
        else:
            print(f"❌ 重啟失敗: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 重啟失敗: {e}")
        return False

def main():
    """主函數"""
    print("🔧 開始修復生產環境排行榜問題...")
    
    # 1. 檢查生產環境應用程式
    if not check_production_app():
        return False
    
    # 2. 檢查修復後的應用程式
    if not check_fixed_app():
        return False
    
    # 3. 備份生產環境應用程式
    if not backup_production_app():
        return False
    
    # 4. 複製修復後的應用程式
    if not copy_fixed_app():
        return False
    
    # 5. 檢查排行榜邏輯
    if not check_leaderboard_logic():
        print("❌ 排行榜邏輯檢查失敗")
        return False
    
    # 6. 重啟生產環境應用程式
    if not restart_production_app():
        print("❌ 重啟失敗，請手動重啟")
        return False
    
    print("🎉 修復完成！")
    print("📋 請測試輸入「排行榜」是否正常顯示 Flex Message")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

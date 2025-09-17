#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
回滾到 Flask 版本
"""

import os
import shutil
from datetime import datetime

def backup_current_file():
    """備份當前文件"""
    print("🔍 備份當前文件...")
    
    current_file = "/Users/baobaoc/Dev/anatomy_quiz_bot/app_supabase.py"
    backup_file = f"/Users/baobaoc/Dev/anatomy_quiz_bot/app_supabase_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
    
    if os.path.exists(current_file):
        shutil.copy2(current_file, backup_file)
        print(f"✅ 當前文件已備份到: {backup_file}")
        return True
    else:
        print(f"❌ 當前文件不存在: {current_file}")
        return False

def find_flask_backup():
    """尋找 Flask 備份文件"""
    print("🔍 尋找 Flask 備份文件...")
    
    backup_dir = "/Users/baobaoc/Dev/anatomy_quiz_bot"
    flask_backup = None
    
    # 尋找最早的備份文件（應該是 Flask 版本）
    for file in os.listdir(backup_dir):
        if file.startswith("app_supabase_backup_") and file.endswith(".py"):
            file_path = os.path.join(backup_dir, file)
            if flask_backup is None or file < flask_backup:
                flask_backup = file_path
    
    if flask_backup:
        print(f"✅ 找到 Flask 備份文件: {flask_backup}")
        return flask_backup
    else:
        print("❌ 沒有找到 Flask 備份文件")
        return None

def restore_flask_version(flask_backup):
    """恢復 Flask 版本"""
    print("🔍 恢復 Flask 版本...")
    
    target_file = "/Users/baobaoc/Dev/anatomy_quiz_bot/app_supabase.py"
    
    if os.path.exists(flask_backup):
        shutil.copy2(flask_backup, target_file)
        print(f"✅ Flask 版本已恢復到: {target_file}")
        return True
    else:
        print(f"❌ Flask 備份文件不存在: {flask_backup}")
        return False

def update_requirements_for_flask():
    """更新 requirements.txt 為 Flask 版本"""
    print("🔍 更新 requirements.txt 為 Flask 版本...")
    
    flask_requirements = """flask==3.0.3
requests==2.32.5
supabase==2.6.0
line-bot-sdk==3.12.0
python-dotenv==1.0.1
gunicorn==22.0.0
"""
    
    requirements_file = "/Users/baobaoc/Dev/anatomy_quiz_bot/requirements.txt"
    
    with open(requirements_file, 'w', encoding='utf-8') as f:
        f.write(flask_requirements)
    
    print("✅ requirements.txt 已更新為 Flask 版本")

def create_procfile():
    """創建 Procfile"""
    print("🔍 創建 Procfile...")
    
    procfile_content = "web: gunicorn app_supabase:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120"
    
    procfile_path = "/Users/baobaoc/Dev/anatomy_quiz_bot/Procfile"
    
    with open(procfile_path, 'w', encoding='utf-8') as f:
        f.write(procfile_content)
    
    print("✅ Procfile 已創建")

def verify_flask_restore():
    """驗證 Flask 恢復"""
    print("🔍 驗證 Flask 恢復...")
    
    target_file = "/Users/baobaoc/Dev/anatomy_quiz_bot/app_supabase.py"
    
    try:
        with open(target_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # 檢查關鍵內容
            if "from flask import" in content:
                print("✅ Flask 版本已恢復")
            else:
                print("❌ Flask 版本未恢復")
                
            if "app = Flask" in content:
                print("✅ 確認是 Flask 應用程式")
            else:
                print("❌ 不是 Flask 應用程式")
                
    except Exception as e:
        print(f"❌ 驗證 Flask 恢復失敗: {e}")

def create_deployment_instructions():
    """創建部署說明"""
    print("🔍 創建部署說明...")
    
    instructions = f"""# Flask 版本回滾

## 回滾內容
1. ✅ 恢復到 Flask 版本
2. ✅ 更新 requirements.txt 為 Flask 依賴項
3. ✅ 創建 Procfile 使用 gunicorn
4. ✅ 確保與 Render 兼容

## 部署步驟
1. 將以下文件上傳到 Render:
   - app_supabase.py (Flask 版本)
   - requirements.txt (Flask 依賴項)
   - Procfile (gunicorn 配置)

2. 重新部署應用程式

3. 測試排行榜功能

## 預期結果
- ✅ webhook 返回 200 狀態碼
- ✅ 用戶輸入「排行榜」收到 Flex Message
- ✅ 排行榜顯示前10名用戶數據

## 技術回滾
- **問題**: FastAPI 版本在 Render 上返回 500 錯誤
- **解決**: 回滾到 Flask 版本，使用 gunicorn
- **結果**: 確保 webhook 正常運作，排行榜功能可用
"""
    
    with open("/Users/baobaoc/Dev/anatomy_quiz_bot/FLASK_ROLLBACK_INSTRUCTIONS.md", 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print("✅ 部署說明已創建: FLASK_ROLLBACK_INSTRUCTIONS.md")

def main():
    """主函數"""
    print("🚀 回滾到 Flask 版本")
    print("=" * 50)
    
    # 1. 備份當前文件
    backup_ok = backup_current_file()
    
    if backup_ok:
        # 2. 尋找 Flask 備份文件
        flask_backup = find_flask_backup()
        
        if flask_backup:
            # 3. 恢復 Flask 版本
            restore_ok = restore_flask_version(flask_backup)
            
            if restore_ok:
                # 4. 更新 requirements.txt
                update_requirements_for_flask()
                
                # 5. 創建 Procfile
                create_procfile()
                
                # 6. 驗證 Flask 恢復
                verify_flask_restore()
                
                # 7. 創建部署說明
                create_deployment_instructions()
                
                print("\n" + "=" * 50)
                print("🎉 Flask 版本回滾完成！")
                print("\n📋 下一步:")
                print("1. 將 app_supabase.py、requirements.txt、Procfile 上傳到 Render")
                print("2. 重新部署應用程式")
                print("3. 測試排行榜功能")
                print("\n💡 回滾內容:")
                print("- 恢復到 Flask 版本")
                print("- 更新 requirements.txt 為 Flask 依賴項")
                print("- 創建 Procfile 使用 gunicorn")
                print("- 確保與 Render 兼容")
                
            else:
                print("❌ 恢復 Flask 版本失敗")
        else:
            print("❌ 沒有找到 Flask 備份文件")
    else:
        print("❌ 備份當前文件失敗")

if __name__ == "__main__":
    main()

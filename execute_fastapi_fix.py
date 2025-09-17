#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
執行 FastAPI 修復
"""

import os
import shutil
from datetime import datetime

def backup_original_file():
    """備份原始文件"""
    print("🔍 備份原始文件...")
    
    original_file = "/Users/baobaoc/Dev/anatomy_quiz_bot/app_supabase.py"
    backup_file = f"/Users/baobaoc/Dev/anatomy_quiz_bot/app_supabase_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
    
    if os.path.exists(original_file):
        shutil.copy2(original_file, backup_file)
        print(f"✅ 原始文件已備份到: {backup_file}")
        return True
    else:
        print(f"❌ 原始文件不存在: {original_file}")
        return False

def replace_with_fastapi():
    """替換為 FastAPI 版本"""
    print("🔍 替換為 FastAPI 版本...")
    
    fastapi_file = "/Users/baobaoc/Dev/anatomy_quiz_bot/app_supabase_fastapi.py"
    target_file = "/Users/baobaoc/Dev/anatomy_quiz_bot/app_supabase.py"
    
    if os.path.exists(fastapi_file):
        shutil.copy2(fastapi_file, target_file)
        print(f"✅ FastAPI 版本已替換原始文件")
        return True
    else:
        print(f"❌ FastAPI 文件不存在: {fastapi_file}")
        return False

def update_requirements_for_fastapi():
    """更新 requirements.txt 為 FastAPI 版本"""
    print("🔍 更新 requirements.txt...")
    
    fastapi_requirements = """fastapi==0.115.14
uvicorn==0.30.1
requests==2.32.5
supabase==2.6.0
line-bot-sdk==3.12.0
python-dotenv==1.0.1
"""
    
    requirements_file = "/Users/baobaoc/Dev/anatomy_quiz_bot/requirements.txt"
    
    with open(requirements_file, 'w', encoding='utf-8') as f:
        f.write(fastapi_requirements)
    
    print("✅ requirements.txt 已更新為 FastAPI 版本")

def create_deployment_instructions():
    """創建部署說明"""
    print("🔍 創建部署說明...")
    
    instructions = f"""# FastAPI 修復完成

## 已執行的操作
1. ✅ 備份原始 Flask 文件
2. ✅ 替換為 FastAPI 版本
3. ✅ 更新 requirements.txt

## 部署步驟
1. 將以下文件上傳到 Render:
   - app_supabase.py (FastAPI 版本)
   - requirements.txt (FastAPI 依賴項)

2. 重新部署應用程式

3. 測試排行榜功能:
   ```bash
   curl -X POST https://anatomy-quiz-bot.onrender.com/webhook \\
     -H "Content-Type: application/json" \\
     -d '{{"events":[{{"type":"message","source":{{"userId":"test"}},"message":{{"type":"text","text":"排行榜"}}}}]}}'
   ```

## 預期結果
- ✅ webhook 返回 200 狀態碼
- ✅ 用戶輸入「排行榜」收到 Flex Message
- ✅ 排行榜顯示前10名用戶數據

## 技術變更
- **之前**: Flask (WSGI) + uvicorn (ASGI) = 不兼容
- **修復後**: FastAPI (ASGI) + uvicorn (ASGI) = 兼容 ✅

## 回滾方法
如果需要回滾到 Flask 版本:
1. 使用備份文件: app_supabase_backup_*.py
2. 恢復原始的 requirements.txt
3. 重新部署
"""
    
    with open("/Users/baobaoc/Dev/anatomy_quiz_bot/FASTAPI_FIX_INSTRUCTIONS.md", 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print("✅ 部署說明已創建: FASTAPI_FIX_INSTRUCTIONS.md")

def verify_files():
    """驗證文件"""
    print("🔍 驗證文件...")
    
    files_to_check = [
        "/Users/baobaoc/Dev/anatomy_quiz_bot/app_supabase.py",
        "/Users/baobaoc/Dev/anatomy_quiz_bot/requirements.txt"
    ]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"✅ {file_path} 存在")
        else:
            print(f"❌ {file_path} 不存在")
    
    # 檢查 FastAPI 導入
    try:
        with open("/Users/baobaoc/Dev/anatomy_quiz_bot/app_supabase.py", 'r', encoding='utf-8') as f:
            content = f.read()
            if 'from fastapi import' in content:
                print("✅ 文件已轉換為 FastAPI 版本")
            else:
                print("❌ 文件轉換失敗")
    except Exception as e:
        print(f"❌ 驗證文件時發生錯誤: {e}")

def main():
    """主函數"""
    print("🚀 執行 FastAPI 修復")
    print("=" * 50)
    
    # 1. 備份原始文件
    backup_ok = backup_original_file()
    
    if backup_ok:
        # 2. 替換為 FastAPI 版本
        replace_ok = replace_with_fastapi()
        
        if replace_ok:
            # 3. 更新 requirements.txt
            update_requirements_for_fastapi()
            
            # 4. 創建部署說明
            create_deployment_instructions()
            
            # 5. 驗證文件
            verify_files()
            
            print("\n" + "=" * 50)
            print("🎉 FastAPI 修復完成！")
            print("\n📋 下一步:")
            print("1. 將 app_supabase.py 和 requirements.txt 上傳到 Render")
            print("2. 重新部署應用程式")
            print("3. 測試排行榜功能")
            
        else:
            print("❌ 替換文件失敗")
    else:
        print("❌ 備份文件失敗")

if __name__ == "__main__":
    main()

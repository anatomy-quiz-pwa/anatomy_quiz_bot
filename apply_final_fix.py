#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
應用最終修復
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

def apply_fixed_version():
    """應用修復版本"""
    print("🔍 應用修復版本...")
    
    fixed_file = "/Users/baobaoc/Dev/anatomy_quiz_bot/app_supabase_fixed.py"
    target_file = "/Users/baobaoc/Dev/anatomy_quiz_bot/app_supabase.py"
    
    if os.path.exists(fixed_file):
        shutil.copy2(fixed_file, target_file)
        print(f"✅ 修復版本已應用到: {target_file}")
        return True
    else:
        print(f"❌ 修復文件不存在: {fixed_file}")
        return False

def verify_fix():
    """驗證修復"""
    print("🔍 驗證修復...")
    
    target_file = "/Users/baobaoc/Dev/anatomy_quiz_bot/app_supabase.py"
    
    try:
        with open(target_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # 檢查關鍵修復
            if "不查詢 nickname 欄位" in content:
                print("✅ 修復已應用：不查詢 nickname 欄位")
            else:
                print("❌ 修復未應用")
                
            if "from fastapi import" in content:
                print("✅ 確認是 FastAPI 版本")
            else:
                print("❌ 不是 FastAPI 版本")
                
    except Exception as e:
        print(f"❌ 驗證修復失敗: {e}")

def create_deployment_instructions():
    """創建部署說明"""
    print("🔍 創建部署說明...")
    
    instructions = f"""# 最終修復完成

## 修復內容
1. ✅ 修復了 Supabase nickname 欄位查詢錯誤
2. ✅ 使用 user_id 前8位作為顯示名稱
3. ✅ 保持 FastAPI 架構

## 部署步驟
1. 將 app_supabase.py 上傳到 Render
2. 重新部署應用程式
3. 測試排行榜功能

## 預期結果
- ✅ webhook 返回 200 狀態碼
- ✅ 用戶輸入「排行榜」收到 Flex Message
- ✅ 排行榜顯示前10名用戶數據

## 技術修復
- **問題**: Supabase 查詢 nickname 欄位失敗 (column users.nickname does not exist)
- **解決**: 直接使用 user_id 前8位作為顯示名稱
- **結果**: 避免數據庫查詢錯誤，確保排行榜功能正常運作
"""
    
    with open("/Users/baobaoc/Dev/anatomy_quiz_bot/FINAL_FIX_INSTRUCTIONS.md", 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print("✅ 部署說明已創建: FINAL_FIX_INSTRUCTIONS.md")

def main():
    """主函數"""
    print("🚀 應用最終修復")
    print("=" * 50)
    
    # 1. 備份當前文件
    backup_ok = backup_current_file()
    
    if backup_ok:
        # 2. 應用修復版本
        apply_ok = apply_fixed_version()
        
        if apply_ok:
            # 3. 驗證修復
            verify_fix()
            
            # 4. 創建部署說明
            create_deployment_instructions()
            
            print("\n" + "=" * 50)
            print("🎉 最終修復完成！")
            print("\n📋 下一步:")
            print("1. 將 app_supabase.py 上傳到 Render")
            print("2. 重新部署應用程式")
            print("3. 測試排行榜功能")
            print("\n💡 修復內容:")
            print("- 修復了 Supabase nickname 欄位查詢錯誤")
            print("- 使用 user_id 前8位作為顯示名稱")
            print("- 保持 FastAPI 架構")
            
        else:
            print("❌ 應用修復版本失敗")
    else:
        print("❌ 備份當前文件失敗")

if __name__ == "__main__":
    main()

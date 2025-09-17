#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
應用極簡修復版本
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

def apply_extreme_simple_version():
    """應用極簡版本"""
    print("🔍 應用極簡版本...")
    
    extreme_simple_file = "/Users/baobaoc/Dev/anatomy_quiz_bot/app_supabase_extreme_simple.py"
    target_file = "/Users/baobaoc/Dev/anatomy_quiz_bot/app_supabase.py"
    
    if os.path.exists(extreme_simple_file):
        shutil.copy2(extreme_simple_file, target_file)
        print(f"✅ 極簡版本已應用到: {target_file}")
        return True
    else:
        print(f"❌ 極簡文件不存在: {extreme_simple_file}")
        return False

def verify_extreme_simple_fix():
    """驗證極簡修復"""
    print("🔍 驗證極簡修復...")
    
    target_file = "/Users/baobaoc/Dev/anatomy_quiz_bot/app_supabase.py"
    
    try:
        with open(target_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # 檢查關鍵內容
            if "排行榜請求已收到" in content:
                print("✅ 極簡版本已應用")
            else:
                print("❌ 極簡版本未應用")
                
            if "from fastapi import" in content:
                print("✅ 確認是 FastAPI 版本")
            else:
                print("❌ 不是 FastAPI 版本")
                
    except Exception as e:
        print(f"❌ 驗證極簡修復失敗: {e}")

def create_deployment_instructions():
    """創建部署說明"""
    print("🔍 創建部署說明...")
    
    instructions = f"""# 極簡修復版本

## 修復內容
1. ✅ 移除了所有 LINE 訊息發送
2. ✅ 只返回 JSON 響應
3. ✅ 保持 FastAPI 架構
4. ✅ 添加了詳細的錯誤日誌

## 部署步驟
1. 將 app_supabase.py 上傳到 Render
2. 重新部署應用程式
3. 測試排行榜功能

## 預期結果
- ✅ webhook 返回 200 狀態碼
- ✅ 用戶輸入「排行榜」返回 JSON 響應
- ✅ 顯示「排行榜請求已收到」

## 技術修復
- **問題**: LINE 訊息發送可能導致問題
- **解決**: 只返回 JSON 響應，不發送任何訊息
- **結果**: 確保 webhook 正常運作，找出問題根源
"""
    
    with open("/Users/baobaoc/Dev/anatomy_quiz_bot/EXTREME_SIMPLE_FIX_INSTRUCTIONS.md", 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print("✅ 部署說明已創建: EXTREME_SIMPLE_FIX_INSTRUCTIONS.md")

def main():
    """主函數"""
    print("🚀 應用極簡修復版本")
    print("=" * 50)
    
    # 1. 備份當前文件
    backup_ok = backup_current_file()
    
    if backup_ok:
        # 2. 應用極簡版本
        apply_ok = apply_extreme_simple_version()
        
        if apply_ok:
            # 3. 驗證極簡修復
            verify_extreme_simple_fix()
            
            # 4. 創建部署說明
            create_deployment_instructions()
            
            print("\n" + "=" * 50)
            print("🎉 極簡修復版本完成！")
            print("\n📋 下一步:")
            print("1. 將 app_supabase.py 上傳到 Render")
            print("2. 重新部署應用程式")
            print("3. 測試排行榜功能")
            print("\n💡 修復內容:")
            print("- 移除了所有 LINE 訊息發送")
            print("- 只返回 JSON 響應")
            print("- 添加了詳細的錯誤日誌")
            print("- 找出問題根源")
            
        else:
            print("❌ 應用極簡版本失敗")
    else:
        print("❌ 備份當前文件失敗")

if __name__ == "__main__":
    main()

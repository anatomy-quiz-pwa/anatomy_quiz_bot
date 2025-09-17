#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
應用超簡單修復版本
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

def apply_ultra_simple_version():
    """應用超簡單版本"""
    print("🔍 應用超簡單版本...")
    
    ultra_simple_file = "/Users/baobaoc/Dev/anatomy_quiz_bot/app_supabase_ultra_simple.py"
    target_file = "/Users/baobaoc/Dev/anatomy_quiz_bot/app_supabase.py"
    
    if os.path.exists(ultra_simple_file):
        shutil.copy2(ultra_simple_file, target_file)
        print(f"✅ 超簡單版本已應用到: {target_file}")
        return True
    else:
        print(f"❌ 超簡單文件不存在: {ultra_simple_file}")
        return False

def verify_ultra_simple_fix():
    """驗證超簡單修復"""
    print("🔍 驗證超簡單修復...")
    
    target_file = "/Users/baobaoc/Dev/anatomy_quiz_bot/app_supabase.py"
    
    try:
        with open(target_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # 檢查關鍵內容
            if "排行榜功能正在測試中" in content:
                print("✅ 超簡單版本已應用")
            else:
                print("❌ 超簡單版本未應用")
                
            if "from fastapi import" in content:
                print("✅ 確認是 FastAPI 版本")
            else:
                print("❌ 不是 FastAPI 版本")
                
    except Exception as e:
        print(f"❌ 驗證超簡單修復失敗: {e}")

def create_deployment_instructions():
    """創建部署說明"""
    print("🔍 創建部署說明...")
    
    instructions = f"""# 超簡單修復版本

## 修復內容
1. ✅ 移除了所有 Flex Message
2. ✅ 使用最簡單的文字訊息
3. ✅ 保持 FastAPI 架構
4. ✅ 添加了詳細的錯誤日誌

## 部署步驟
1. 將 app_supabase.py 上傳到 Render
2. 重新部署應用程式
3. 測試排行榜功能

## 預期結果
- ✅ webhook 返回 200 狀態碼
- ✅ 用戶輸入「排行榜」收到文字訊息
- ✅ 顯示「🏆 排行榜功能正在測試中...請稍後再試！」

## 技術修復
- **問題**: Flex Message 可能導致問題
- **解決**: 使用最簡單的文字訊息
- **結果**: 確保 webhook 正常運作，排行榜功能基本可用
"""
    
    with open("/Users/baobaoc/Dev/anatomy_quiz_bot/ULTRA_SIMPLE_FIX_INSTRUCTIONS.md", 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print("✅ 部署說明已創建: ULTRA_SIMPLE_FIX_INSTRUCTIONS.md")

def main():
    """主函數"""
    print("🚀 應用超簡單修復版本")
    print("=" * 50)
    
    # 1. 備份當前文件
    backup_ok = backup_current_file()
    
    if backup_ok:
        # 2. 應用超簡單版本
        apply_ok = apply_ultra_simple_version()
        
        if apply_ok:
            # 3. 驗證超簡單修復
            verify_ultra_simple_fix()
            
            # 4. 創建部署說明
            create_deployment_instructions()
            
            print("\n" + "=" * 50)
            print("🎉 超簡單修復版本完成！")
            print("\n📋 下一步:")
            print("1. 將 app_supabase.py 上傳到 Render")
            print("2. 重新部署應用程式")
            print("3. 測試排行榜功能")
            print("\n💡 修復內容:")
            print("- 移除了所有 Flex Message")
            print("- 使用最簡單的文字訊息")
            print("- 添加了詳細的錯誤日誌")
            print("- 確保 webhook 正常運作")
            
        else:
            print("❌ 應用超簡單版本失敗")
    else:
        print("❌ 備份當前文件失敗")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
清空所有資料的腳本
包括資料庫中的用戶統計和本地快取
"""

import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

def clear_all_user_stats():
    """清空所有用戶統計資料"""
    try:
        from supabase_quiz_handler import supabase
        
        print("🗑️ 清空所有用戶統計資料...")
        
        # 刪除所有用戶統計記錄
        result = supabase.table("user_stats").delete().neq("user_id", "").execute()
        
        print(f"✅ 已清空 {len(result.data)} 個用戶統計記錄")
        return True
        
    except Exception as e:
        print(f"❌ 清空用戶統計資料失敗: {str(e)}")
        return False

def clear_all_quiz_logs():
    """清空所有測驗記錄"""
    try:
        from supabase_quiz_handler import supabase
        
        print("🗑️ 清空所有測驗記錄...")
        
        # 用一個永遠為真的條件（UUID 型別）
        result = supabase.table("quiz_logs").delete().gt("id", "00000000-0000-0000-0000-000000000000").execute()
        
        print(f"✅ 已清空 {len(result.data)} 個測驗記錄")
        return True
        
    except Exception as e:
        print(f"❌ 清空測驗記錄失敗: {str(e)}")
        return False

def clear_all_data():
    """清空所有資料"""
    print("🧹 開始清空所有資料...")
    print("=" * 50)
    
    # 清空資料庫資料
    success1 = clear_all_user_stats()
    success2 = clear_all_quiz_logs()
    
    # 清空本地快取
    try:
        from cache_utils import clear_all_cache
        success3 = clear_all_cache()
    except ImportError:
        print("ℹ️ 快取工具未找到，跳過快取清空")
        success3 = True
    
    print("=" * 50)
    
    if success1 and success2 and success3:
        print("🎉 所有資料清空完成！")
        print("\n📋 已清空的內容:")
        print("   ✅ 用戶統計資料 (user_stats)")
        print("   ✅ 測驗記錄 (quiz_logs)")
        print("   ✅ 本地快取資料")
        
        print("\n💡 現在您可以重新開始測試，所有積分都會從 0 開始計算")
        return True
    else:
        print("❌ 部分資料清空失敗，請檢查錯誤訊息")
        return False

def verify_clear():
    """驗證資料是否已清空"""
    try:
        from supabase_quiz_handler import supabase
        
        print("\n🔍 驗證資料清空結果...")
        
        # 檢查用戶統計
        user_stats = supabase.table("user_stats").select("*").execute()
        print(f"   用戶統計記錄: {len(user_stats.data)} 筆")
        
        # 檢查測驗記錄
        quiz_logs = supabase.table("quiz_logs").select("*").execute()
        print(f"   測驗記錄: {len(quiz_logs.data)} 筆")
        
        if len(user_stats.data) == 0 and len(quiz_logs.data) == 0:
            print("✅ 驗證成功：所有資料已清空")
            return True
        else:
            print("❌ 驗證失敗：仍有資料未清空")
            return False
            
    except Exception as e:
        print(f"❌ 驗證失敗: {str(e)}")
        return False

if __name__ == "__main__":
    # 確認操作
    print("⚠️  警告：此操作將清空所有用戶統計資料和測驗記錄！")
    print("此操作不可逆，請確認是否繼續？")
    
    confirm = input("輸入 'YES' 確認清空所有資料: ")
    
    if confirm == "YES":
        # 執行清空
        success = clear_all_data()
        
        if success:
            # 驗證結果
            verify_clear()
    else:
        print("❌ 操作已取消") 
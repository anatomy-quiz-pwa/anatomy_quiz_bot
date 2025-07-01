#!/usr/bin/env python3
"""
測試重置功能
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client

# 載入環境變數
load_dotenv()

# 初始化 Supabase 客戶端
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    raise ValueError("SUPABASE_URL 和 SUPABASE_ANON_KEY 必須在 .env 檔案中設定")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def test_reset_function():
    """測試重置功能"""
    test_user_id = "test_user_123"
    
    print("🧪 測試重置功能...")
    
    # 1. 檢查重置前的資料
    print(f"\n1️⃣ 檢查重置前的資料...")
    try:
        response = supabase.table("user_stats").select("*").eq("user_id", test_user_id).execute()
        if hasattr(response, 'data'):
            user_stats = response.data
        else:
            user_stats = response
            
        if user_stats:
            print(f"   找到用戶資料: {user_stats[0]}")
        else:
            print(f"   用戶 {test_user_id} 沒有資料")
    except Exception as e:
        print(f"   檢查資料失敗: {e}")
        return False
    
    # 2. 執行重置
    print(f"\n2️⃣ 執行重置...")
    try:
        from supabase_user_stats_handler import reset_user_stats
        success = reset_user_stats(test_user_id)
        print(f"   重置結果: {'成功' if success else '失敗'}")
    except Exception as e:
        print(f"   重置失敗: {e}")
        return False
    
    # 3. 檢查重置後的資料
    print(f"\n3️⃣ 檢查重置後的資料...")
    try:
        response = supabase.table("user_stats").select("*").eq("user_id", test_user_id).execute()
        if hasattr(response, 'data'):
            user_stats = response.data
        else:
            user_stats = response
            
        if user_stats:
            print(f"   ❌ 重置失敗：用戶資料仍然存在: {user_stats[0]}")
            return False
        else:
            print(f"   ✅ 重置成功：用戶 {test_user_id} 的資料已被完全刪除")
    except Exception as e:
        print(f"   檢查資料失敗: {e}")
        return False
    
    print(f"\n🎉 重置功能測試完成！")
    return True

if __name__ == "__main__":
    test_reset_function() 
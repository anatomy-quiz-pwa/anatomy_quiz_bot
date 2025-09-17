#!/usr/bin/env python3
"""
檢查 Supabase 中的表格結構
"""

from supabase import create_client, Client

# Supabase 配置
SUPABASE_URL = "https://ciqlfqfgzqqgdrogedxg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA"

def check_all_tables():
    """檢查所有表格"""
    print("🔍 檢查 Supabase 中的所有表格...")
    
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # 嘗試獲取所有表格信息
        tables_to_check = ['user', 'users', 'user_stats', 'game_users', 'player', 'players']
        
        for table_name in tables_to_check:
            try:
                response = supabase.table(table_name).select('*').limit(1).execute()
                if response.data is not None:
                    print(f"✅ 表格 '{table_name}' 存在")
                    print(f"   📋 字段：{list(response.data[0].keys()) if response.data else '空表格'}")
                    
                    # 檢查是否包含暱稱相關欄位
                    if response.data:
                        fields = list(response.data[0].keys())
                        nickname_fields = [field for field in fields if 'nickname' in field.lower() or 'name' in field.lower()]
                        if nickname_fields:
                            print(f"   🎯 暱稱相關欄位：{nickname_fields}")
                else:
                    print(f"❌ 表格 '{table_name}' 不存在或無法訪問")
            except Exception as e:
                print(f"❌ 表格 '{table_name}' 不存在或無法訪問: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ 檢查失敗：{e}")
        return False

def check_user_stats_table():
    """檢查 user_stats 表格"""
    print("\n📊 檢查 user_stats 表格...")
    
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        response = supabase.table('user_stats').select('*').limit(3).execute()
        
        if response.data:
            print(f"✅ user_stats 表格存在，有 {len(response.data)} 條記錄")
            print(f"📋 字段：{list(response.data[0].keys())}")
            
            # 顯示樣本數據
            print("\n📋 樣本數據：")
            for i, record in enumerate(response.data, 1):
                print(f"  記錄 {i}: {record}")
            
            return True
        else:
            print("❌ user_stats 表格為空或無法訪問")
            return False
            
    except Exception as e:
        print(f"❌ 檢查失敗：{e}")
        return False

if __name__ == "__main__":
    print("🚀 檢查 Supabase 表格結構")
    print("=" * 50)
    
    # 檢查所有表格
    check_all_tables()
    
    # 檢查 user_stats 表格
    check_user_stats_table()
    
    print("\n📝 建議：")
    print("1. 確認暱稱欄位在哪個表格中")
    print("2. 確認欄位的確切名稱")
    print("3. 更新應用程序代碼以使用正確的表格和欄位")


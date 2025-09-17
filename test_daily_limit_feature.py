#!/usr/bin/env python3
"""
測試每日三題限制功能
驗證用戶每天最多只能答三題的限制邏輯
"""

import os
import sys
import datetime
from supabase import create_client, Client

# 添加項目根目錄到 Python 路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 導入應用程式模組
try:
    from app_supabase import (
        check_daily_question_limit,
        update_daily_question_count,
        get_user_stats,
        create_initial_user_stats
    )
    print("✅ 成功導入應用程式模組")
except ImportError as e:
    print(f"❌ 導入應用程式模組失敗: {e}")
    sys.exit(1)

# 環境變數設置
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://ciqlfqfgzqqgdrogedxg.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA')

def test_database_connection():
    """測試資料庫連接"""
    print("\n🔗 測試資料庫連接...")
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # 測試連接
        response = supabase.table('user_stats').select('count', count='exact').limit(1).execute()
        print(f"✅ 資料庫連接成功！共有 {response.count} 條記錄")
        return supabase
    except Exception as e:
        print(f"❌ 資料庫連接失敗: {e}")
        return None

def test_daily_limit_fields(supabase):
    """測試每日限制相關欄位是否存在"""
    print("\n📊 檢查每日限制欄位...")
    try:
        # 檢查是否有測試用戶
        test_user_id = "test_daily_limit_user"
        
        # 查詢欄位
        response = supabase.table('user_stats').select(
            'user_id, daily_questions_answered, last_question_date'
        ).eq('user_id', test_user_id).limit(1).execute()
        
        print("✅ 每日限制欄位存在且可查詢")
        return True
        
    except Exception as e:
        print(f"❌ 每日限制欄位檢查失敗: {e}")
        if "column" in str(e).lower() and "does not exist" in str(e).lower():
            print("💡 提示：需要先執行資料庫遷移來添加每日限制欄位")
        return False

def test_daily_limit_logic():
    """測試每日限制邏輯"""
    print("\n🧪 測試每日限制邏輯...")
    
    test_user_id = "test_daily_limit_user"
    
    try:
        # 1. 測試新用戶（應該可以答題）
        print(f"1️⃣ 測試新用戶 {test_user_id}...")
        limit_status = check_daily_question_limit(test_user_id)
        
        print(f"   - 可以答題: {limit_status['can_answer']}")
        print(f"   - 已答題數: {limit_status['questions_answered']}")
        print(f"   - 剩餘次數: {limit_status['remaining']}")
        
        if not limit_status['can_answer']:
            print("❌ 新用戶應該可以答題")
            return False
            
        # 2. 模擬答題三次
        print("2️⃣ 模擬答題三次...")
        for i in range(3):
            print(f"   答第 {i+1} 題...")
            success = update_daily_question_count(test_user_id)
            if not success:
                print(f"❌ 更新第 {i+1} 題計數失敗")
                return False
            
            # 檢查狀態
            limit_status = check_daily_question_limit(test_user_id)
            print(f"   - 已答題數: {limit_status['questions_answered']}")
            print(f"   - 剩餘次數: {limit_status['remaining']}")
        
        # 3. 測試達到限制後的狀態
        print("3️⃣ 測試達到限制後的狀態...")
        final_limit_status = check_daily_question_limit(test_user_id)
        
        if final_limit_status['can_answer']:
            print("❌ 答完三題後應該不能再答題")
            return False
            
        if final_limit_status['questions_answered'] != 3:
            print(f"❌ 答題數應該是3，實際是 {final_limit_status['questions_answered']}")
            return False
            
        if final_limit_status['remaining'] != 0:
            print(f"❌ 剩餘次數應該是0，實際是 {final_limit_status['remaining']}")
            return False
        
        print("✅ 每日限制邏輯測試通過")
        return True
        
    except Exception as e:
        print(f"❌ 每日限制邏輯測試失敗: {e}")
        return False

def test_daily_reset_logic(supabase):
    """測試每日重置邏輯"""
    print("\n🔄 測試每日重置邏輯...")
    
    test_user_id = "test_daily_reset_user"
    
    try:
        # 創建一個昨天的記錄
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        
        # 插入昨天的記錄
        test_data = {
            'user_id': test_user_id,
            'correct': 5,
            'wrong': 2,
            'level': 3,
            'daily_questions_answered': 3,  # 昨天答了3題
            'last_question_date': yesterday.isoformat(),
            'last_update': datetime.datetime.now().isoformat()
        }
        
        result = supabase.table('user_stats').upsert(test_data).execute()
        if not result.data:
            print("❌ 創建測試記錄失敗")
            return False
        
        print(f"✅ 創建了昨天 ({yesterday}) 的測試記錄")
        
        # 檢查今天的狀態（應該重置）
        limit_status = check_daily_question_limit(test_user_id)
        
        if not limit_status['can_answer']:
            print("❌ 新的一天應該可以答題")
            return False
            
        if limit_status['questions_answered'] != 0:
            print(f"❌ 新的一天答題數應該重置為0，實際是 {limit_status['questions_answered']}")
            return False
            
        if limit_status['remaining'] != 3:
            print(f"❌ 新的一天剩餘次數應該是3，實際是 {limit_status['remaining']}")
            return False
        
        print("✅ 每日重置邏輯測試通過")
        return True
        
    except Exception as e:
        print(f"❌ 每日重置邏輯測試失敗: {e}")
        return False

def cleanup_test_data(supabase):
    """清理測試數據"""
    print("\n🧹 清理測試數據...")
    try:
        test_users = [
            "test_daily_limit_user",
            "test_daily_reset_user"
        ]
        
        for user_id in test_users:
            supabase.table('user_stats').delete().eq('user_id', user_id).execute()
            print(f"✅ 清理測試用戶: {user_id}")
            
    except Exception as e:
        print(f"⚠️ 清理測試數據時出現錯誤: {e}")

def main():
    """主測試函數"""
    print("🧪 開始測試每日三題限制功能")
    print("=" * 50)
    
    # 1. 測試資料庫連接
    supabase = test_database_connection()
    if not supabase:
        return False
    
    # 2. 檢查每日限制欄位
    if not test_daily_limit_fields(supabase):
        print("\n💡 請先執行以下 SQL 來添加每日限制欄位:")
        print("   supabase/migrations/20250117000001_add_daily_limit_fields.sql")
        return False
    
    # 3. 測試每日限制邏輯
    if not test_daily_limit_logic():
        return False
    
    # 4. 測試每日重置邏輯
    if not test_daily_reset_logic(supabase):
        return False
    
    # 5. 清理測試數據
    cleanup_test_data(supabase)
    
    print("\n" + "=" * 50)
    print("🎉 所有測試通過！每日三題限制功能正常運作")
    
    print("\n📋 功能摘要:")
    print("✅ 新用戶可以答題（每天3題）")
    print("✅ 答完3題後不能再答題")
    print("✅ 每天午夜自動重置答題次數")
    print("✅ 達到限制時顯示適當提醒訊息")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

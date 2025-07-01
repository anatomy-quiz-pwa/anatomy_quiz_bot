#!/usr/bin/env python3
"""
詳細測試重置功能
"""

def test_reset_detailed():
    """詳細測試重置功能"""
    test_user_id = "test_user_123"
    
    print("🧪 詳細測試重置功能...")
    
    # 1. 檢查重置前狀態
    print(f"\n1️⃣ 檢查重置前狀態...")
    try:
        from supabase_user_stats_handler import get_user_stats
        stats = get_user_stats(test_user_id)
        print(f"   重置前統計: {stats}")
    except Exception as e:
        print(f"   檢查失敗: {e}")
    
    # 2. 直接調用重置函數
    print(f"\n2️⃣ 直接調用重置函數...")
    try:
        from supabase_user_stats_handler import reset_user_stats
        reset_success = reset_user_stats(test_user_id)
        print(f"   重置結果: {reset_success}")
    except Exception as e:
        print(f"   重置失敗: {e}")
    
    # 3. 檢查重置後狀態
    print(f"\n3️⃣ 檢查重置後狀態...")
    try:
        from supabase_user_stats_handler import get_user_stats
        stats = get_user_stats(test_user_id)
        print(f"   重置後統計: {stats}")
    except Exception as e:
        print(f"   檢查失敗: {e}")
    
    # 4. 檢查是否真的被刪除
    print(f"\n4️⃣ 檢查是否真的被刪除...")
    try:
        from supabase_user_stats_handler import get_all_user_stats
        all_stats = get_all_user_stats()
        print(f"   所有用戶統計數量: {len(all_stats)}")
        for stat in all_stats:
            print(f"   用戶 {stat['user_id']}: 正確={stat['correct']}, 錯誤={stat['wrong']}, correct_qids={stat['correct_qids']}")
    except Exception as e:
        print(f"   檢查失敗: {e}")
    
    print(f"\n🎉 詳細測試完成！")

if __name__ == "__main__":
    test_reset_detailed() 
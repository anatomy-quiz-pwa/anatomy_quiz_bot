#!/usr/bin/env python3
"""
測試管理員權限功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app_supabase_fixed import (
    get_user_admin_permissions, 
    check_admin_access, 
    is_admin_user,
    get_user_nickname
)

def test_admin_permissions():
    """測試管理員權限功能"""
    print("🧪 開始測試管理員權限功能...")
    print("=" * 50)
    
    # 測試用戶ID
    test_user_id = "U9a9df49945755ef651d067743f3c7ea7"
    
    print(f"📋 測試用戶ID: {test_user_id}")
    print()
    
    # 1. 測試獲取用戶暱稱
    print("1️⃣ 測試獲取用戶暱稱...")
    try:
        nickname = get_user_nickname(test_user_id)
        print(f"   ✅ 用戶暱稱: {nickname}")
    except Exception as e:
        print(f"   ❌ 獲取暱稱失敗: {e}")
    print()
    
    # 2. 測試獲取管理員權限
    print("2️⃣ 測試獲取管理員權限...")
    try:
        admin_info = get_user_admin_permissions(test_user_id)
        if admin_info:
            print(f"   ✅ 管理員權限信息:")
            print(f"      - is_admin: {admin_info.get('is_admin', False)}")
            print(f"      - test_mode: {admin_info.get('test_mode', False)}")
            print(f"      - admin_levels: {admin_info.get('admin_levels', [])}")
            print(f"      - admin_permissions: {admin_info.get('admin_permissions', {})}")
        else:
            print("   ⚠️ 未找到管理員權限信息")
    except Exception as e:
        print(f"   ❌ 獲取管理員權限失敗: {e}")
    print()
    
    # 3. 測試檢查是否為管理員
    print("3️⃣ 測試檢查是否為管理員...")
    try:
        is_admin = is_admin_user(test_user_id)
        print(f"   ✅ 是否為管理員: {is_admin}")
    except Exception as e:
        print(f"   ❌ 檢查管理員狀態失敗: {e}")
    print()
    
    # 4. 測試檢查管理員訪問權限
    print("4️⃣ 測試檢查管理員訪問權限...")
    try:
        # 測試不同等級的訪問權限
        for level in [1, 5, 10, 15, 20]:
            has_access = check_admin_access(test_user_id, level)
            print(f"   - 等級 {level}: {'✅ 有權限' if has_access else '❌ 無權限'}")
    except Exception as e:
        print(f"   ❌ 檢查訪問權限失敗: {e}")
    print()
    
    # 5. 測試無指定等級的訪問權限
    print("5️⃣ 測試無指定等級的訪問權限...")
    try:
        has_access = check_admin_access(test_user_id)
        print(f"   ✅ 無指定等級訪問權限: {has_access}")
    except Exception as e:
        print(f"   ❌ 檢查無指定等級訪問權限失敗: {e}")
    print()
    
    print("=" * 50)
    print("🎉 管理員權限功能測試完成！")
    
    # 總結
    print("\n📊 測試總結:")
    print("✅ 已實現的功能:")
    print("   - 獲取用戶管理員權限信息")
    print("   - 檢查用戶是否為管理員")
    print("   - 檢查用戶對特定等級的訪問權限")
    print("   - 支持管理員測試模式")
    print()
    print("🔧 管理員命令:")
    print("   - /admin status - 查看管理員狀態")
    print("   - /admin users - 查看用戶列表")
    print("   - /admin stats - 查看統計數據")
    print("   - /test level <等級> - 測試指定等級權限")
    print("   - /test all - 測試所有等級權限")
    print("   - /level set <等級> - 設置用戶等級")
    print("   - /level check - 檢查當前等級")

if __name__ == "__main__":
    test_admin_permissions()

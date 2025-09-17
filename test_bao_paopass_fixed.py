#!/usr/bin/env python3
"""
測試保帳號 PAOPASS 管理員功能修復
驗證修復後的管理員權限是否正常工作
"""

import os
from supabase import create_client, Client
import logging

# 設置日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Supabase 配置
SUPABASE_URL = 'https://ciqlfqfgzqqgdrogedxg.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA'

# 創建 Supabase 客戶端
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 保帳號的用戶ID
BAO_USER_ID = 'U977c24d1fec3a2bf07035504e1444911'

def get_user_admin_permissions(user_id):
    """獲取用戶管理員權限"""
    try:
        response = supabase.table('users').select(
            'is_admin', 'admin_levels', 'test_mode', 'admin_permissions'
        ).eq('line_user_id', user_id).execute()
        
        if response.data and len(response.data) > 0:
            user_data = response.data[0]
            admin_info = {
                'is_admin': user_data.get('is_admin', False),
                'admin_levels': user_data.get('admin_levels', []),
                'test_mode': user_data.get('test_mode', False),
                'admin_permissions': user_data.get('admin_permissions', {})
            }
            return admin_info
        else:
            return None
            
    except Exception as e:
        logger.error(f"❌ 獲取用戶 {user_id} 管理員權限失敗: {e}")
        return None

def is_admin_user(user_id):
    """檢查用戶是否為管理員"""
    try:
        admin_info = get_user_admin_permissions(user_id)
        if not admin_info:
            return False
        
        return admin_info.get('is_admin', False) and admin_info.get('test_mode', False)
        
    except Exception as e:
        logger.error(f"❌ 檢查用戶 {user_id} 是否為管理員失敗: {e}")
        return False

def check_admin_access(user_id, required_level=None):
    """檢查用戶是否有管理員權限訪問指定level"""
    try:
        admin_info = get_user_admin_permissions(user_id)
        if not admin_info:
            return False
        
        # 檢查是否為管理員
        if not admin_info.get('is_admin', False):
            return False
        
        # 檢查測試模式
        if not admin_info.get('test_mode', False):
            return False
        
        # 檢查權限配置
        permissions = admin_info.get('admin_permissions', {})
        if not permissions.get('can_access_all_levels', False):
            return False
        
        # 如果指定了level，檢查是否在允許的level列表中
        if required_level is not None:
            admin_levels = admin_info.get('admin_levels', [])
            if required_level not in admin_levels:
                return False
        
        return True
        
    except Exception as e:
        logger.error(f"❌ 檢查用戶 {user_id} 管理員權限失敗: {e}")
        return False

def test_bao_paopass_function():
    """測試保帳號的 PAOPASS 管理員功能"""
    print("=" * 60)
    print("🧪 測試保帳號 PAOPASS 管理員功能修復")
    print("=" * 60)
    
    print(f"\n📋 測試用戶ID: {BAO_USER_ID}")
    
    # 測試1: 檢查基本管理員權限
    print("\n🔍 測試1: 檢查基本管理員權限")
    admin_info = get_user_admin_permissions(BAO_USER_ID)
    if admin_info:
        print("✅ 獲取管理員權限成功")
        print(f"   is_admin: {admin_info['is_admin']}")
        print(f"   test_mode: {admin_info['test_mode']}")
        print(f"   admin_levels: {len(admin_info['admin_levels'])} 個等級 {admin_info['admin_levels'][:5]}{'...' if len(admin_info['admin_levels']) > 5 else ''}")
        print(f"   admin_permissions: {list(admin_info['admin_permissions'].keys())}")
    else:
        print("❌ 無法獲取管理員權限")
        return False
    
    # 測試2: 檢查 is_admin_user 函數
    print("\n🔍 測試2: 檢查 is_admin_user 函數")
    is_admin = is_admin_user(BAO_USER_ID)
    print(f"   is_admin_user 結果: {is_admin}")
    if is_admin:
        print("✅ 保帳號被正確識別為管理員")
    else:
        print("❌ 保帳號未被識別為管理員")
        return False
    
    # 測試3: 檢查等級訪問權限
    print("\n🔍 測試3: 檢查等級訪問權限")
    test_levels = [1, 5, 10, 15, 20]
    for level in test_levels:
        has_access = check_admin_access(BAO_USER_ID, level)
        status = "✅" if has_access else "❌"
        print(f"   等級 {level}: {status} {'有權限' if has_access else '無權限'}")
    
    # 測試4: 檢查特殊管理員權限
    print("\n🔍 測試4: 檢查特殊管理員權限")
    permissions = admin_info['admin_permissions']
    required_permissions = [
        'can_access_all_levels',
        'can_test_all_questions',
        'can_bypass_restrictions',
        'test_mode_enabled'
    ]
    
    all_permissions_ok = True
    for perm in required_permissions:
        has_perm = permissions.get(perm, False)
        status = "✅" if has_perm else "❌"
        print(f"   {perm}: {status} {'啟用' if has_perm else '停用'}")
        if not has_perm:
            all_permissions_ok = False
    
    # 總結
    print("\n" + "=" * 60)
    if is_admin and all_permissions_ok:
        print("🎉 保帳號 PAOPASS 管理員功能修復成功！")
        print("\n✅ 可用功能:")
        print("   • 輸入 'PAOPASS' 切換管理員模式")
        print("   • 輸入 '/admin status' 查看管理員狀態")
        print("   • 輸入 '/test level <等級>' 測試特定等級")
        print("   • 不受每日答題限制")
        print("   • 可以訪問所有等級 (1-20) 的題目")
        print("   • 可以繞過所有限制")
        return True
    else:
        print("❌ 保帳號 PAOPASS 管理員功能仍有問題")
        return False

if __name__ == "__main__":
    try:
        success = test_bao_paopass_function()
        if success:
            print("\n🎊 測試完成 - 修復成功！")
        else:
            print("\n⚠️ 測試完成 - 仍需修復")
    except Exception as e:
        logger.error(f"❌ 測試過程中發生錯誤: {e}")
        print(f"\n💥 測試失敗: {e}")

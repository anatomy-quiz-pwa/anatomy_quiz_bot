#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理數據庫中的測試用戶腳本
只保留真實的LINE用戶，讓排行榜更美觀
"""

import os
import json
from datetime import datetime
from supabase import create_client, Client

# Supabase 配置
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://ciqlfqfgzqqgdrogedxg.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA')

# 創建 Supabase 客戶端
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def is_real_line_user(user_id: str) -> bool:
    """判斷是否為真實的LINE用戶"""
    # LINE用戶ID通常以U開頭且長度大於30
    return user_id.startswith('U') and len(user_id) > 30

def backup_data():
    """備份即將刪除的數據"""
    print("🔄 正在備份測試用戶數據...")
    
    try:
        # 獲取所有用戶統計數據
        stats_response = supabase.table('user_stats').select('*').execute()
        
        # 獲取所有用戶資料
        users_response = supabase.table('users').select('*').execute()
        
        # 分類數據
        test_user_stats = []
        test_user_data = []
        real_user_stats = []
        real_user_data = []
        
        # 分類 user_stats
        for user in stats_response.data:
            if is_real_line_user(user['user_id']):
                real_user_stats.append(user)
            else:
                test_user_stats.append(user)
        
        # 分類 users
        for user in users_response.data:
            if is_real_line_user(user['line_user_id']):
                real_user_data.append(user)
            else:
                test_user_data.append(user)
        
        # 創建備份文件
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_data = {
            'timestamp': timestamp,
            'test_user_stats': test_user_stats,
            'test_user_data': test_user_data,
            'real_user_stats': real_user_stats,
            'real_user_data': real_user_data,
            'summary': {
                'total_test_users_stats': len(test_user_stats),
                'total_test_users_data': len(test_user_data),
                'total_real_users_stats': len(real_user_stats),
                'total_real_users_data': len(real_user_data)
            }
        }
        
        backup_filename = f'test_users_backup_{timestamp}.json'
        with open(backup_filename, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 備份完成: {backup_filename}")
        print(f"📊 將刪除 {len(test_user_stats)} 個測試用戶統計記錄")
        print(f"📊 將刪除 {len(test_user_data)} 個測試用戶資料記錄")
        print(f"🔒 將保留 {len(real_user_stats)} 個真實LINE用戶統計記錄")
        print(f"🔒 將保留 {len(real_user_data)} 個真實LINE用戶資料記錄")
        
        return backup_data
        
    except Exception as e:
        print(f"❌ 備份失敗: {e}")
        return None

def cleanup_test_users(dry_run=True):
    """清理測試用戶數據"""
    print(f"{'🔍 模擬運行' if dry_run else '🗑️ 正在清理'} 測試用戶數據...")
    
    try:
        # 獲取所有用戶統計數據
        stats_response = supabase.table('user_stats').select('*').execute()
        test_user_ids = []
        
        for user in stats_response.data:
            if not is_real_line_user(user['user_id']):
                test_user_ids.append(user['user_id'])
        
        print(f"📋 找到 {len(test_user_ids)} 個測試用戶需要清理:")
        for user_id in test_user_ids[:10]:  # 顯示前10個
            print(f"  - {user_id}")
        if len(test_user_ids) > 10:
            print(f"  ... 還有 {len(test_user_ids) - 10} 個")
        
        if not dry_run:
            # 實際刪除操作
            deleted_stats = 0
            deleted_users = 0
            
            # 刪除 user_stats 中的測試用戶
            for user_id in test_user_ids:
                try:
                    supabase.table('user_stats').delete().eq('user_id', user_id).execute()
                    deleted_stats += 1
                except Exception as e:
                    print(f"⚠️ 刪除 user_stats 記錄失敗 ({user_id}): {e}")
            
            # 刪除 users 中的測試用戶
            for user_id in test_user_ids:
                try:
                    supabase.table('users').delete().eq('line_user_id', user_id).execute()
                    deleted_users += 1
                except Exception as e:
                    # 如果記錄不存在，這是正常的
                    pass
            
            print(f"✅ 清理完成:")
            print(f"  - 刪除了 {deleted_stats} 個 user_stats 記錄")
            print(f"  - 刪除了 {deleted_users} 個 users 記錄")
        
        return test_user_ids
        
    except Exception as e:
        print(f"❌ 清理失敗: {e}")
        return None

def verify_cleanup():
    """驗證清理結果"""
    print("🔍 驗證清理結果...")
    
    try:
        # 檢查剩餘的用戶
        stats_response = supabase.table('user_stats').select('user_id, correct, level').execute()
        
        real_users = []
        remaining_test_users = []
        
        for user in stats_response.data:
            if is_real_line_user(user['user_id']):
                real_users.append(user)
            else:
                remaining_test_users.append(user)
        
        print(f"✅ 驗證結果:")
        print(f"🧑‍💼 真實LINE用戶: {len(real_users)} 個")
        for user in real_users:
            print(f"  - {user['user_id'][:20]}... (答對{user['correct']}題, 等級{user['level']})")
        
        if remaining_test_users:
            print(f"⚠️ 仍有 {len(remaining_test_users)} 個測試用戶:")
            for user in remaining_test_users:
                print(f"  - {user['user_id']}")
        else:
            print("🎉 所有測試用戶已成功清理!")
        
        return len(real_users), len(remaining_test_users)
        
    except Exception as e:
        print(f"❌ 驗證失敗: {e}")
        return None, None

def main():
    """主函數"""
    print("🧹 測試用戶清理工具")
    print("=" * 50)
    
    # 1. 備份數據
    backup_result = backup_data()
    if not backup_result:
        print("❌ 備份失敗，停止清理操作")
        return
    
    print("\n" + "=" * 50)
    
    # 2. 模擬運行
    print("📋 模擬運行 - 查看將要刪除的數據:")
    test_users = cleanup_test_users(dry_run=True)
    
    if not test_users:
        print("❌ 無法獲取測試用戶列表")
        return
    
    print("\n" + "=" * 50)
    
    # 3. 確認是否執行
    print("⚠️ 注意: 此操作將永久刪除測試用戶數據!")
    print("✅ 數據已備份，可以安全恢復")
    
    # 在腳本中我們先不自動執行，讓用戶手動確認
    print("\n如要執行清理，請運行:")
    print("python3 cleanup_test_users.py --execute")

if __name__ == "__main__":
    import sys
    
    if "--execute" in sys.argv:
        print("🧹 測試用戶清理工具 - 執行模式")
        print("=" * 50)
        
        # 備份
        backup_result = backup_data()
        if not backup_result:
            print("❌ 備份失敗，停止清理操作")
            exit(1)
        
        # 執行清理
        print("\n" + "=" * 50)
        test_users = cleanup_test_users(dry_run=False)
        
        # 驗證結果
        print("\n" + "=" * 50)
        real_count, test_count = verify_cleanup()
        
        if test_count == 0:
            print("\n🎉 清理完成！排行榜現在只顯示真實LINE用戶")
        else:
            print(f"\n⚠️ 清理不完整，仍有 {test_count} 個測試用戶")
    
    else:
        main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
刪除管理員測試資料並重置排行榜統計腳本
- 刪除非真實LINE用戶的測試資料
- 重置排行榜統計，從今天開始重新計算
- 保留真實LINE用戶的資料但重置統計
"""

import os
import json
from datetime import datetime, timezone
from supabase import create_client, Client

# Supabase 配置
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://ciqlfqfgzqqgdrogedxg.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA')

# 創建 Supabase 客戶端
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 已知的真實LINE用戶ID [[memory:9037129]]
REAL_LINE_USERS = [
    'U9a9df49945755ef651d067743f3c7ea7',  # 蘇的測試帳號
    'U977c24d1fec3a2bf07035504e1444911'   # 寶的測試帳號 [[memory:9037033]]
]

def is_real_line_user(user_id: str) -> bool:
    """判斷是否為真實的LINE用戶"""
    # LINE用戶ID通常以U開頭且長度大於30，或在已知真實用戶列表中
    return (user_id.startswith('U') and len(user_id) > 30) or user_id in REAL_LINE_USERS

def backup_all_data():
    """備份所有數據"""
    print("🔄 正在備份所有數據...")
    
    try:
        # 獲取所有表的數據
        user_stats_response = supabase.table('user_stats').select('*').execute()
        users_response = supabase.table('users').select('*').execute()
        
        # 分類數據
        admin_test_stats = []
        admin_test_users = []
        real_user_stats = []
        real_user_data = []
        
        # 分類 user_stats
        for user in user_stats_response.data:
            if is_real_line_user(user['user_id']):
                real_user_stats.append(user)
            else:
                admin_test_stats.append(user)
        
        # 分類 users
        for user in users_response.data:
            if is_real_line_user(user['line_user_id']):
                real_user_data.append(user)
            else:
                admin_test_users.append(user)
        
        # 創建備份文件
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_data = {
            'timestamp': timestamp,
            'operation': 'reset_admin_data_and_leaderboard',
            'admin_test_stats': admin_test_stats,
            'admin_test_users': admin_test_users,
            'real_user_stats_before_reset': real_user_stats,
            'real_user_data_before_reset': real_user_data,
            'summary': {
                'total_admin_test_stats': len(admin_test_stats),
                'total_admin_test_users': len(admin_test_users),
                'total_real_users_stats': len(real_user_stats),
                'total_real_users_data': len(real_user_data)
            }
        }
        
        backup_filename = f'admin_data_reset_backup_{timestamp}.json'
        with open(backup_filename, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 備份完成: {backup_filename}")
        print(f"📊 將刪除 {len(admin_test_stats)} 個管理員測試統計記錄")
        print(f"📊 將刪除 {len(admin_test_users)} 個管理員測試用戶記錄")
        print(f"🔄 將重置 {len(real_user_stats)} 個真實用戶的統計")
        print(f"🔒 將保留 {len(real_user_data)} 個真實用戶的基本資料")
        
        return backup_data
        
    except Exception as e:
        print(f"❌ 備份失敗: {e}")
        return None

def delete_admin_test_data(dry_run=True):
    """刪除管理員測試資料"""
    print(f"{'🔍 模擬運行' if dry_run else '🗑️ 正在刪除'} 管理員測試資料...")
    
    try:
        # 獲取所有用戶統計數據
        stats_response = supabase.table('user_stats').select('*').execute()
        users_response = supabase.table('users').select('*').execute()
        
        admin_test_user_ids = []
        admin_test_line_user_ids = []
        
        # 找出管理員測試用戶
        for user in stats_response.data:
            if not is_real_line_user(user['user_id']):
                admin_test_user_ids.append(user['user_id'])
        
        for user in users_response.data:
            if not is_real_line_user(user['line_user_id']):
                admin_test_line_user_ids.append(user['line_user_id'])
        
        print(f"📋 找到 {len(admin_test_user_ids)} 個管理員測試統計記錄需要刪除")
        print(f"📋 找到 {len(admin_test_line_user_ids)} 個管理員測試用戶記錄需要刪除")
        
        # 顯示前10個
        if admin_test_user_ids:
            print("管理員測試統計記錄:")
            for user_id in admin_test_user_ids[:10]:
                print(f"  - {user_id}")
            if len(admin_test_user_ids) > 10:
                print(f"  ... 還有 {len(admin_test_user_ids) - 10} 個")
        
        if admin_test_line_user_ids:
            print("管理員測試用戶記錄:")
            for user_id in admin_test_line_user_ids[:10]:
                print(f"  - {user_id}")
            if len(admin_test_line_user_ids) > 10:
                print(f"  ... 還有 {len(admin_test_line_user_ids) - 10} 個")
        
        if not dry_run:
            # 實際刪除操作
            deleted_stats = 0
            deleted_users = 0
            
            # 刪除 user_stats 中的管理員測試用戶
            for user_id in admin_test_user_ids:
                try:
                    supabase.table('user_stats').delete().eq('user_id', user_id).execute()
                    deleted_stats += 1
                    print(f"🗑️ 已刪除統計記錄: {user_id}")
                except Exception as e:
                    print(f"⚠️ 刪除統計記錄失敗 ({user_id}): {e}")
            
            # 刪除 users 中的管理員測試用戶
            for user_id in admin_test_line_user_ids:
                try:
                    supabase.table('users').delete().eq('line_user_id', user_id).execute()
                    deleted_users += 1
                    print(f"🗑️ 已刪除用戶記錄: {user_id}")
                except Exception as e:
                    print(f"⚠️ 刪除用戶記錄失敗 ({user_id}): {e}")
            
            print(f"✅ 管理員測試資料刪除完成:")
            print(f"  - 刪除了 {deleted_stats} 個統計記錄")
            print(f"  - 刪除了 {deleted_users} 個用戶記錄")
        
        return admin_test_user_ids, admin_test_line_user_ids
        
    except Exception as e:
        print(f"❌ 刪除管理員測試資料失敗: {e}")
        return None, None

def reset_leaderboard_stats(dry_run=True):
    """重置排行榜統計，從今天開始重新計算"""
    print(f"{'🔍 模擬運行' if dry_run else '🔄 正在重置'} 排行榜統計...")
    
    try:
        # 獲取所有真實用戶的統計數據
        stats_response = supabase.table('user_stats').select('*').execute()
        real_users = []
        
        for user in stats_response.data:
            if is_real_line_user(user['user_id']):
                real_users.append(user)
        
        print(f"📋 找到 {len(real_users)} 個真實用戶需要重置統計")
        
        current_time = datetime.now(timezone.utc).isoformat()
        
        if not dry_run:
            reset_count = 0
            
            for user in real_users:
                try:
                    # 重置統計但保留基本資料，使用實際的欄位名稱
                    reset_data = {
                        'user_id': user['user_id'],
                        'correct': 0,
                        'wrong': 0,
                        'level': 1,
                        'correct_in_level': 0,
                        'daily_quota': 3,
                        'streak_days': 0,
                        'correct_qids': '[]',
                        'last_update': current_time,
                        'last_updated': current_time,
                        'created_at': current_time
                    }
                    
                    supabase.table('user_stats').upsert(reset_data).execute()
                    reset_count += 1
                    print(f"🔄 已重置用戶統計: {user['user_id'][:20]}... (暱稱: {user.get('nickname', '無')})")
                    
                except Exception as e:
                    print(f"⚠️ 重置用戶統計失敗 ({user['user_id']}): {e}")
            
            print(f"✅ 排行榜統計重置完成:")
            print(f"  - 重置了 {reset_count} 個用戶的統計")
            print(f"  - 所有統計從今天 ({datetime.now().strftime('%Y-%m-%d')}) 開始重新計算")
        
        return real_users
        
    except Exception as e:
        print(f"❌ 重置排行榜統計失敗: {e}")
        return None

def verify_reset_results():
    """驗證重置結果"""
    print("🔍 驗證重置結果...")
    
    try:
        # 檢查剩餘的用戶
        stats_response = supabase.table('user_stats').select('*').execute()
        users_response = supabase.table('users').select('*').execute()
        
        real_stats = []
        remaining_admin_stats = []
        real_users = []
        remaining_admin_users = []
        
        # 分類統計記錄
        for user in stats_response.data:
            if is_real_line_user(user['user_id']):
                real_stats.append(user)
            else:
                remaining_admin_stats.append(user)
        
        # 分類用戶記錄
        for user in users_response.data:
            if is_real_line_user(user['line_user_id']):
                real_users.append(user)
            else:
                remaining_admin_users.append(user)
        
        print(f"✅ 驗證結果:")
        print(f"🧑‍💼 真實LINE用戶統計: {len(real_stats)} 個")
        for user in real_stats:
            print(f"  - {user['user_id'][:20]}... (答對{user.get('correct', 0)}題, 等級{user.get('level', 1)}, 暱稱: {user.get('nickname', '無')})")
        
        print(f"🧑‍💼 真實LINE用戶資料: {len(real_users)} 個")
        
        if remaining_admin_stats:
            print(f"⚠️ 仍有 {len(remaining_admin_stats)} 個管理員測試統計記錄:")
            for user in remaining_admin_stats[:5]:
                print(f"  - {user['user_id']}")
        else:
            print("🎉 所有管理員測試統計記錄已成功清理!")
        
        if remaining_admin_users:
            print(f"⚠️ 仍有 {len(remaining_admin_users)} 個管理員測試用戶記錄:")
            for user in remaining_admin_users[:5]:
                print(f"  - {user['line_user_id']}")
        else:
            print("🎉 所有管理員測試用戶記錄已成功清理!")
        
        return len(real_stats), len(remaining_admin_stats), len(real_users), len(remaining_admin_users)
        
    except Exception as e:
        print(f"❌ 驗證失敗: {e}")
        return None, None, None, None

def main():
    """主函數"""
    print("🔄 管理員測試資料清理與排行榜重置工具")
    print("=" * 60)
    
    # 1. 備份數據
    backup_result = backup_all_data()
    if not backup_result:
        print("❌ 備份失敗，停止操作")
        return
    
    print("\n" + "=" * 60)
    
    # 2. 模擬運行 - 刪除管理員測試資料
    print("📋 模擬運行 - 查看將要刪除的管理員測試資料:")
    admin_stats, admin_users = delete_admin_test_data(dry_run=True)
    
    if admin_stats is None:
        print("❌ 無法獲取管理員測試資料列表")
        return
    
    print("\n" + "=" * 60)
    
    # 3. 模擬運行 - 重置排行榜統計
    print("📋 模擬運行 - 查看將要重置的真實用戶統計:")
    real_users = reset_leaderboard_stats(dry_run=True)
    
    if real_users is None:
        print("❌ 無法獲取真實用戶列表")
        return
    
    print("\n" + "=" * 60)
    
    # 4. 確認信息
    print("⚠️ 注意: 此操作將:")
    print("  1. 永久刪除所有管理員測試資料")
    print("  2. 重置所有真實用戶的統計（但保留暱稱）")
    print("  3. 讓排行榜從今天開始重新計算")
    print("✅ 所有數據已備份，可以安全恢復")
    
    print("\n如要執行操作，請運行:")
    print("python3 reset_admin_data_and_leaderboard.py --execute")

if __name__ == "__main__":
    import sys
    
    if "--execute" in sys.argv:
        print("🔄 管理員測試資料清理與排行榜重置工具 - 執行模式")
        print("=" * 60)
        
        # 備份
        backup_result = backup_all_data()
        if not backup_result:
            print("❌ 備份失敗，停止操作")
            exit(1)
        
        print("\n" + "=" * 60)
        
        # 執行刪除管理員測試資料
        print("🗑️ 正在刪除管理員測試資料...")
        admin_stats, admin_users = delete_admin_test_data(dry_run=False)
        
        print("\n" + "=" * 60)
        
        # 執行重置排行榜統計
        print("🔄 正在重置排行榜統計...")
        real_users = reset_leaderboard_stats(dry_run=False)
        
        print("\n" + "=" * 60)
        
        # 驗證結果
        print("🔍 正在驗證結果...")
        real_stats_count, admin_stats_count, real_users_count, admin_users_count = verify_reset_results()
        
        print("\n" + "=" * 60)
        
        if admin_stats_count == 0 and admin_users_count == 0:
            print("🎉 操作完成！")
            print(f"✅ 已清理所有管理員測試資料")
            print(f"✅ 已重置 {real_stats_count} 個真實用戶的統計")
            print(f"📊 排行榜現在從今天 ({datetime.now().strftime('%Y-%m-%d')}) 開始重新計算")
        else:
            print(f"⚠️ 操作不完整:")
            if admin_stats_count > 0:
                print(f"  - 仍有 {admin_stats_count} 個管理員測試統計記錄")
            if admin_users_count > 0:
                print(f"  - 仍有 {admin_users_count} 個管理員測試用戶記錄")
    
    else:
        main()

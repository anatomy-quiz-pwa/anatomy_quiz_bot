#!/usr/bin/env python3
"""
檢查數據庫中的真實用戶ID，找到寶的帳號
"""

import sys
import os
from datetime import datetime

# 添加當前目錄到路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_real_user_ids():
    """檢查數據庫中的真實用戶ID"""
    print("=" * 60)
    print("🔍 檢查數據庫中的真實用戶ID")
    print("=" * 60)
    
    try:
        from app_supabase import supabase
        
        if not supabase:
            print("❌ Supabase連接失敗")
            return False
        
        # 查詢user_stats表中的用戶
        print("📊 查詢user_stats表...")
        stats_response = supabase.table('user_stats').select('user_id, level, correct, wrong').limit(10).execute()
        
        if stats_response.data:
            print(f"✅ 找到 {len(stats_response.data)} 個用戶記錄:")
            for i, user in enumerate(stats_response.data, 1):
                user_id = user.get('user_id', 'Unknown')
                level = user.get('level', 0)
                correct = user.get('correct', 0)
                wrong = user.get('wrong', 0)
                print(f"   {i}. ID: {user_id}")
                print(f"      等級: {level}, 正確: {correct}, 錯誤: {wrong}")
                print()
        
        # 查詢users表中的用戶（如果存在）
        print("👥 查詢users表...")
        try:
            users_response = supabase.table('users').select('line_user_id, game_nickname, is_admin').limit(10).execute()
            
            if users_response.data:
                print(f"✅ 找到 {len(users_response.data)} 個用戶記錄:")
                for i, user in enumerate(users_response.data, 1):
                    line_id = user.get('line_user_id', 'Unknown')
                    nickname = user.get('game_nickname', 'No nickname')
                    is_admin = user.get('is_admin', False)
                    admin_flag = " (管理員)" if is_admin else ""
                    print(f"   {i}. LINE ID: {line_id}")
                    print(f"      暱稱: {nickname}{admin_flag}")
                    print()
            else:
                print("⚠️  users表中沒有找到用戶記錄")
        except Exception as e:
            print(f"⚠️  查詢users表時出錯: {e}")
        
        # 尋找可能是寶的帳號
        print("🕵️ 尋找可能是寶的帳號...")
        
        # 檢查是否有包含"bao"、"寶"或高等級的用戶
        potential_bao_accounts = []
        
        for user in stats_response.data:
            user_id = user.get('user_id', '')
            level = user.get('level', 0)
            
            # 檢查用戶ID是否包含相關關鍵字或是高等級用戶
            if any(keyword in user_id.lower() for keyword in ['bao', '寶']) or level >= 5:
                potential_bao_accounts.append(user)
        
        if potential_bao_accounts:
            print(f"🎯 找到 {len(potential_bao_accounts)} 個可能的帳號:")
            for i, user in enumerate(potential_bao_accounts, 1):
                user_id = user.get('user_id', 'Unknown')
                level = user.get('level', 0)
                correct = user.get('correct', 0)
                print(f"   候選 {i}: {user_id} (等級: {level}, 正確: {correct})")
        else:
            print("⚠️  沒有找到明顯的候選帳號")
        
        return True
        
    except Exception as e:
        print(f"❌ 檢查過程中發生錯誤: {e}")
        return False

def create_test_message_with_real_id():
    """使用真實ID創建測試訊息"""
    print("\n" + "=" * 60)
    print("📱 使用真實ID創建升級測試訊息")
    print("=" * 60)
    
    try:
        from app_supabase import supabase, create_level_up_flex_message, send_message
        
        # 獲取第一個真實用戶ID
        stats_response = supabase.table('user_stats').select('user_id').limit(1).execute()
        
        if not stats_response.data:
            print("❌ 沒有找到用戶記錄")
            return False
        
        real_user_id = stats_response.data[0]['user_id']
        print(f"🎯 使用真實用戶ID: {real_user_id}")
        
        # 創建升級Flex Message
        upgrade_flex = create_level_up_flex_message(3, 4)
        
        if upgrade_flex:
            print("✅ Flex Message創建成功")
            
            # 保存到檔案而不是實際發送（避免發送到錯誤的用戶）
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"upgrade_flex_message_{timestamp}.json"
            
            import json
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    'target_user_id': real_user_id,
                    'message': upgrade_flex,
                    'created_at': timestamp
                }, f, ensure_ascii=False, indent=2)
            
            print(f"💾 Flex Message已保存到: {filename}")
            print("📝 您可以檢視此檔案來確認訊息格式")
            
            # 顯示訊息摘要
            print(f"\n📱 訊息摘要:")
            print(f"   Alt Text: {upgrade_flex['altText']}")
            print(f"   Hero圖片: {upgrade_flex['contents']['hero']['url']}")
            print(f"   訊息類型: {upgrade_flex['type']}")
            
            return True
        else:
            print("❌ Flex Message創建失敗")
            return False
            
    except Exception as e:
        print(f"❌ 創建測試訊息失敗: {e}")
        return False

def main():
    """主函數"""
    print(f"🕐 開始時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 檢查真實用戶ID
    if check_real_user_ids():
        print("✅ 用戶ID檢查完成")
    else:
        print("❌ 用戶ID檢查失敗")
        return 1
    
    # 創建測試訊息
    if create_test_message_with_real_id():
        print("✅ 測試訊息創建完成")
    else:
        print("❌ 測試訊息創建失敗")
        return 1
    
    print("\n" + "="*60)
    print("📋 總結")
    print("="*60)
    print("✅ 已檢查數據庫中的真實用戶ID")
    print("✅ 已創建升級Flex Message範例")
    print("💡 建議:")
    print("   1. 確認寶的真實LINE用戶ID")
    print("   2. 檢查LINE Channel設定是否正確")
    print("   3. 使用正確的用戶ID進行測試")
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

#!/usr/bin/env python3
"""
檢查所有用戶的統計資料同步問題
"""
import os
from supabase import create_client, Client
import json

# Supabase 配置
SUPABASE_URL = "https://ciqlfqfgzqqgdrogedxg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA"

def main():
    print("🔍 檢查所有用戶的統計資料同步問題...")
    
    try:
        # 創建 Supabase 客戶端
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Supabase 連接成功")
        
        # 1. 獲取所有用戶統計資料
        print(f"\n📊 步驟1: 獲取所有用戶統計資料...")
        stats_response = supabase.table('user_stats').select('*').execute()
        
        if not stats_response.data:
            print("❌ 沒有找到任何用戶統計資料")
            return
        
        print(f"✅ 找到 {len(stats_response.data)} 個用戶統計記錄")
        
        # 2. 檢查同步問題
        print(f"\n🔍 步驟2: 檢查統計資料同步問題...")
        
        sync_issues = []
        correct_users = []
        
        for stats in stats_response.data:
            user_id = stats.get('user_id')
            correct_count = stats.get('correct', 0)
            wrong_count = stats.get('wrong', 0)
            correct_qids = stats.get('correct_qids', [])
            level = stats.get('level', 1)
            correct_in_level = stats.get('correct_in_level', 0)
            
            # 檢查 correct 計數與 correct_qids 長度是否一致
            actual_correct = len(correct_qids) if correct_qids else 0
            
            if actual_correct != correct_count:
                # 獲取用戶暱稱
                user_response = supabase.table('users').select('game_nickname').eq('line_user_id', user_id).execute()
                nickname = user_response.data[0].get('game_nickname') if user_response.data else '無暱稱'
                
                sync_issues.append({
                    'user_id': user_id,
                    'nickname': nickname,
                    'stats_correct': correct_count,
                    'actual_correct': actual_correct,
                    'correct_qids': correct_qids,
                    'level': level,
                    'correct_in_level': correct_in_level
                })
            else:
                correct_users.append({
                    'user_id': user_id,
                    'correct_count': correct_count,
                    'actual_correct': actual_correct
                })
        
        # 3. 報告結果
        print(f"\n📋 步驟3: 同步檢查結果...")
        print(f"✅ 統計正確的用戶: {len(correct_users)} 個")
        print(f"❌ 發現同步問題的用戶: {len(sync_issues)} 個")
        
        if sync_issues:
            print(f"\n🚨 發現統計資料同步問題的用戶:")
            for i, issue in enumerate(sync_issues, 1):
                user_id = issue['user_id']
                nickname = issue['nickname']
                stats_correct = issue['stats_correct']
                actual_correct = issue['actual_correct']
                correct_qids = issue['correct_qids']
                level = issue['level']
                
                print(f"\n{i}. {user_id} ({nickname})")
                print(f"   📊 統計顯示答對: {stats_correct} 題")
                print(f"   📝 實際答對記錄: {actual_correct} 題")
                print(f"   🏆 當前等級: {level}")
                print(f"   📋 答對題目ID: {correct_qids}")
                
                # 計算應該的等級
                expected_level = min(14, (actual_correct // 3) + 1)
                expected_correct_in_level = actual_correct % 3
                
                print(f"   🔧 建議修復:")
                print(f"      - correct: {stats_correct} → {actual_correct}")
                print(f"      - level: {level} → {expected_level}")
                print(f"      - correct_in_level: {issue['correct_in_level']} → {expected_correct_in_level}")
        
        # 4. 提供批量修復選項
        if sync_issues:
            print(f"\n💡 批量修復選項:")
            print(f"   發現 {len(sync_issues)} 個用戶需要修復統計資料")
            
            confirmation = input("\n❓ 是否要批量修復所有用戶的統計資料？(y/N): ")
            
            if confirmation.lower() == 'y':
                print(f"\n🔧 開始批量修復...")
                
                success_count = 0
                fail_count = 0
                
                for issue in sync_issues:
                    try:
                        user_id = issue['user_id']
                        actual_correct = issue['actual_correct']
                        correct_qids = issue['correct_qids']
                        wrong_count = 0  # 保持原有錯誤計數，這裡簡化處理
                        
                        # 計算正確的等級和本級答對數
                        new_level = min(14, (actual_correct // 3) + 1)
                        new_correct_in_level = actual_correct % 3
                        
                        update_data = {
                            'user_id': user_id,
                            'correct': actual_correct,
                            'level': new_level,
                            'correct_in_level': new_correct_in_level,
                            'correct_qids': correct_qids,
                            'last_update': '2025-09-17'
                        }
                        
                        result = supabase.table('user_stats').upsert(update_data, on_conflict='user_id').execute()
                        
                        if result.data:
                            print(f"   ✅ {user_id} ({issue['nickname']}) 修復成功")
                            success_count += 1
                        else:
                            print(f"   ❌ {user_id} ({issue['nickname']}) 修復失敗")
                            fail_count += 1
                            
                    except Exception as e:
                        print(f"   ❌ {user_id} ({issue['nickname']}) 修復出錯: {e}")
                        fail_count += 1
                
                print(f"\n📊 批量修復結果:")
                print(f"   ✅ 成功修復: {success_count} 個用戶")
                print(f"   ❌ 修復失敗: {fail_count} 個用戶")
            else:
                print("❌ 取消批量修復操作")
        else:
            print(f"\n🎉 太好了！所有用戶的統計資料都是同步的。")
        
    except Exception as e:
        print(f"❌ 檢查過程中發生錯誤: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

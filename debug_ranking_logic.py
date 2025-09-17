#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
調試排名計算邏輯
找出為什麼同一個用戶會有不同的排名結果
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app_supabase import (
    supabase,
    get_user_rank_info,
    get_leaderboard_data,
    logger
)

def debug_ranking_calculation():
    """調試排名計算"""
    print("🔍 調試排名計算邏輯")
    print("=" * 50)
    
    test_user_id = "U977c24d1fec3a2bf07035504e1444911"
    
    try:
        # 1. 查詢用戶統計
        print("1️⃣ 查詢用戶統計數據...")
        user_response = supabase.table('user_stats').select('*').eq('user_id', test_user_id).execute()
        
        if user_response.data:
            user_stats = user_response.data[0]
            user_correct = user_stats.get('correct', 0)
            print(f"   用戶正確答案數: {user_correct}")
        else:
            print("   ❌ 找不到用戶統計數據")
            return
        
        # 2. 使用 get_user_rank_info 計算排名
        print("\n2️⃣ 使用 get_user_rank_info 函數計算排名...")
        user_rank_info = get_user_rank_info(test_user_id)
        if user_rank_info:
            print(f"   函數計算排名: 第{user_rank_info['rank']}名")
        
        # 3. 手動計算排名
        print("\n3️⃣ 手動計算排名...")
        higher_scores_response = supabase.table('user_stats').select('user_id').gt('correct', user_correct).execute()
        manual_rank = len(higher_scores_response.data) + 1
        print(f"   手動計算排名: 第{manual_rank}名")
        print(f"   比用戶分數高的用戶數: {len(higher_scores_response.data)}")
        
        # 4. 獲取排行榜數據並查找用戶位置
        print("\n4️⃣ 在排行榜數據中查找用戶位置...")
        leaderboard_data = get_leaderboard_data()
        
        if leaderboard_data:
            user_position = None
            for i, student in enumerate(leaderboard_data, 1):
                if student['user_id'] == test_user_id:
                    user_position = i
                    break
            
            if user_position:
                print(f"   在排行榜數據中的位置: 第{user_position}名")
            else:
                print("   ❌ 在排行榜數據中找不到用戶")
                
                # 查看用戶是否在50名之外
                print("   🔍 檢查用戶是否在前50名之外...")
                all_users_response = supabase.table('user_stats').select('user_id, correct').order('correct', desc=True).execute()
                
                if all_users_response.data:
                    print(f"   資料庫總用戶數: {len(all_users_response.data)}")
                    for i, user in enumerate(all_users_response.data, 1):
                        if user['user_id'] == test_user_id:
                            print(f"   用戶在完整排序中的位置: 第{i}名")
                            break
        
        # 5. 分析 0 分用戶的排名問題
        print("\n5️⃣ 分析 0 分用戶的排名問題...")
        zero_score_response = supabase.table('user_stats').select('user_id').eq('correct', 0).execute()
        zero_score_users = len(zero_score_response.data)
        print(f"   0 分用戶總數: {zero_score_users}")
        
        if zero_score_users > 1:
            print("   ⚠️ 多個用戶都是 0 分，排名可能不穩定")
            print("   建議使用次要排序條件（如 user_id 或 created_at）")
        
        # 6. 檢查排序邏輯
        print("\n6️⃣ 檢查排序邏輯...")
        print("   當前排序: ORDER BY correct DESC")
        print("   對於相同分數的用戶，排名可能會不穩定")
        
        # 7. 建議的修復方案
        print("\n7️⃣ 建議的修復方案:")
        print("   1. 使用穩定的排序條件（如添加 user_id 作為次要排序）")
        print("   2. 對於相同分數的用戶，使用一致的排名邏輯")
        print("   3. 考慮使用 ROW_NUMBER() 或 RANK() 函數")
        
    except Exception as e:
        print(f"❌ 調試失敗: {e}")

def test_consistent_ranking():
    """測試一致性排名"""
    print("\n🧪 測試一致性排名")
    print("=" * 50)
    
    test_user_id = "U977c24d1fec3a2bf07035504e1444911"
    
    try:
        # 多次計算排名，看是否一致
        ranks = []
        for i in range(5):
            user_rank_info = get_user_rank_info(test_user_id)
            if user_rank_info:
                ranks.append(user_rank_info['rank'])
                print(f"   第{i+1}次計算: 第{user_rank_info['rank']}名")
        
        if len(set(ranks)) == 1:
            print("✅ 排名計算一致")
        else:
            print("❌ 排名計算不一致")
            print(f"   不同的排名結果: {set(ranks)}")
            
    except Exception as e:
        print(f"❌ 測試失敗: {e}")

def main():
    """主函數"""
    print("🧪 開始調試排名計算邏輯")
    print("=" * 60)
    
    debug_ranking_calculation()
    test_consistent_ranking()
    
    print("\n" + "=" * 60)
    print("🏁 調試完成")

if __name__ == "__main__":
    main()

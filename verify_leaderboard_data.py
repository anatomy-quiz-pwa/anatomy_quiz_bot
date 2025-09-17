#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
驗證排行榜數據是否與 Supabase 資料庫一致
檢查數據是否即時調取
"""

import sys
import os
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app_supabase import (
    supabase,
    get_leaderboard_data, 
    get_user_rank_info,
    logger
)

def check_raw_database_data():
    """直接查詢 Supabase 資料庫的原始數據"""
    print("🔍 直接查詢 Supabase user_stats 表的原始數據...")
    
    try:
        # 直接查詢所有用戶統計，按正確答案數排序
        response = supabase.table('user_stats').select('*').order('correct', desc=True).execute()
        
        if response.data:
            print(f"✅ 資料庫中共有 {len(response.data)} 條用戶統計記錄")
            print("\n📊 前10名用戶的原始數據：")
            print("排名 | 用戶ID | 正確答案 | 錯誤答案 | 等級 | 更新時間")
            print("-" * 80)
            
            for i, record in enumerate(response.data[:10], 1):
                user_id = record.get('user_id', 'N/A')[:20] + "..." if len(record.get('user_id', '')) > 20 else record.get('user_id', 'N/A')
                correct = record.get('correct', 0)
                wrong = record.get('wrong', 0)
                level = record.get('level', 1)
                updated_at = record.get('updated_at', 'N/A')
                
                print(f"{i:2d}   | {user_id:23s} | {correct:8d} | {wrong:8d} | {level:4d} | {updated_at}")
            
            return response.data
        else:
            print("❌ 資料庫中沒有用戶統計數據")
            return []
            
    except Exception as e:
        print(f"❌ 查詢資料庫失敗: {e}")
        return []

def check_processed_leaderboard_data():
    """檢查經過處理的排行榜數據"""
    print("\n🔍 檢查經過處理的排行榜數據...")
    
    try:
        leaderboard_data = get_leaderboard_data()
        
        if leaderboard_data:
            print(f"✅ 排行榜函數返回 {len(leaderboard_data)} 條記錄")
            print("\n📊 前10名用戶的處理後數據：")
            print("排名 | 暱稱 | 用戶ID | 正確答案 | 錯誤答案 | 等級 | 準確率")
            print("-" * 85)
            
            for i, record in enumerate(leaderboard_data[:10], 1):
                nickname = record.get('nickname', 'N/A')[:15]
                user_id = record.get('user_id', 'N/A')[:15] + "..." if len(record.get('user_id', '')) > 15 else record.get('user_id', 'N/A')
                correct = record.get('correct', 0)
                wrong = record.get('wrong', 0)
                level = record.get('level', 1)
                accuracy = record.get('accuracy', 0)
                
                print(f"{i:2d}   | {nickname:15s} | {user_id:18s} | {correct:8d} | {wrong:8d} | {level:4d} | {accuracy:6.1f}%")
            
            return leaderboard_data
        else:
            print("❌ 排行榜函數沒有返回數據")
            return []
            
    except Exception as e:
        print(f"❌ 獲取排行榜數據失敗: {e}")
        return []

def compare_data_consistency(raw_data, processed_data):
    """比較原始數據和處理後數據的一致性"""
    print("\n🔍 比較數據一致性...")
    
    if not raw_data or not processed_data:
        print("❌ 無法比較 - 缺少數據")
        return
    
    print("檢查前10名的數據是否一致：")
    
    inconsistencies = []
    for i in range(min(10, len(raw_data), len(processed_data))):
        raw_record = raw_data[i]
        processed_record = processed_data[i]
        
        raw_user_id = raw_record.get('user_id')
        processed_user_id = processed_record.get('user_id')
        raw_correct = raw_record.get('correct', 0)
        processed_correct = processed_record.get('correct', 0)
        
        if raw_user_id != processed_user_id or raw_correct != processed_correct:
            inconsistencies.append({
                'rank': i + 1,
                'raw_user_id': raw_user_id,
                'processed_user_id': processed_user_id,
                'raw_correct': raw_correct,
                'processed_correct': processed_correct
            })
    
    if inconsistencies:
        print("❌ 發現數據不一致：")
        for inc in inconsistencies:
            print(f"  排名 {inc['rank']}: 原始({inc['raw_user_id'][:20]}, {inc['raw_correct']}) vs 處理後({inc['processed_user_id'][:20]}, {inc['processed_correct']})")
    else:
        print("✅ 前10名數據完全一致")

def check_specific_user_rank(user_id):
    """檢查特定用戶的排名計算是否正確"""
    print(f"\n🔍 檢查用戶 {user_id} 的排名計算...")
    
    try:
        # 方法1: 使用我們的排名函數
        user_rank_info = get_user_rank_info(user_id)
        
        # 方法2: 直接查詢資料庫計算排名
        user_stats_response = supabase.table('user_stats').select('*').eq('user_id', user_id).execute()
        
        if not user_stats_response.data:
            print(f"❌ 資料庫中找不到用戶 {user_id}")
            return
        
        user_stats = user_stats_response.data[0]
        user_correct = user_stats.get('correct', 0)
        
        # 查詢有多少用戶比這個用戶分數高
        higher_scores_response = supabase.table('user_stats').select('user_id').gt('correct', user_correct).execute()
        calculated_rank = len(higher_scores_response.data) + 1
        
        print(f"用戶統計: 正確答案 {user_correct} 題")
        print(f"函數計算排名: {user_rank_info['rank'] if user_rank_info else 'N/A'}")
        print(f"直接計算排名: {calculated_rank}")
        
        if user_rank_info and user_rank_info['rank'] == calculated_rank:
            print("✅ 排名計算一致")
        else:
            print("❌ 排名計算不一致")
        
        return user_rank_info, calculated_rank
        
    except Exception as e:
        print(f"❌ 檢查用戶排名失敗: {e}")
        return None, None

def check_data_freshness():
    """檢查數據的新鮮度"""
    print("\n🔍 檢查數據新鮮度...")
    
    try:
        # 查詢最近更新的記錄
        response = supabase.table('user_stats').select('user_id, correct, updated_at').order('updated_at', desc=True).limit(5).execute()
        
        if response.data:
            print("📅 最近更新的5條記錄：")
            for record in response.data:
                user_id = record.get('user_id', 'N/A')[:25]
                correct = record.get('correct', 0)
                updated_at = record.get('updated_at', 'N/A')
                print(f"  {user_id:25s} | {correct:3d} 題 | {updated_at}")
        else:
            print("❌ 沒有找到更新時間記錄")
            
    except Exception as e:
        print(f"❌ 檢查數據新鮮度失敗: {e}")

def main():
    """主檢查函數"""
    print("🧪 開始驗證排行榜數據一致性")
    print("=" * 70)
    
    # 1. 檢查原始資料庫數據
    raw_data = check_raw_database_data()
    
    # 2. 檢查處理後的排行榜數據
    processed_data = check_processed_leaderboard_data()
    
    # 3. 比較數據一致性
    compare_data_consistency(raw_data, processed_data)
    
    # 4. 檢查特定用戶排名（保的帳號）
    test_user_id = "U977c24d1fec3a2bf07035504e1444911"
    check_specific_user_rank(test_user_id)
    
    # 5. 檢查數據新鮮度
    check_data_freshness()
    
    print("\n" + "=" * 70)
    print("🏁 驗證完成")
    
    # 總結
    print("\n📋 總結:")
    if raw_data and processed_data:
        print(f"   原始數據: {len(raw_data)} 條記錄")
        print(f"   處理後數據: {len(processed_data)} 條記錄")
        if len(raw_data) == len(processed_data):
            print("   數據量一致 ✅")
        else:
            print("   數據量不一致 ❌")
    
    print("\n💡 建議:")
    print("   1. 檢查是否有緩存機制影響數據即時性")
    print("   2. 確認排行榜顯示的數據來源")
    print("   3. 檢查數據庫連接和查詢邏輯")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
分析用戶連續登入情況
"""

import os
import json
import datetime
from supabase import create_client, Client
from typing import List, Dict, Any, Set
from collections import defaultdict

# 設定 Supabase 連接
SUPABASE_URL = os.getenv('SUPABASE_URL') or "https://ciqlfqfgzqqgdrogedxg.supabase.co"
SUPABASE_KEY = os.getenv('SUPABASE_KEY') or "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_user_nickname(user_id):
    """獲取用戶暱稱"""
    try:
        response = supabase.table('users').select('game_nickname').eq('line_user_id', user_id).execute()
        if response.data and len(response.data) > 0:
            return response.data[0].get('game_nickname', '未設置')
        return '未設置'
    except:
        return '未設置'

def get_user_activity_by_date(start_date: str, end_date: str):
    """獲取指定日期範圍內用戶活動數據"""
    try:
        # 獲取用戶統計數據
        stats_response = supabase.table('user_stats').select('*').gte(
            'last_updated', start_date
        ).lte('last_updated', end_date).execute()
        
        # 獲取新註冊用戶數據
        users_response = supabase.table('users').select('*').gte(
            'created_at', start_date
        ).lte('created_at', end_date).execute()
        
        return {
            'user_stats': stats_response.data,
            'new_users': users_response.data
        }
    except Exception as e:
        print(f"❌ 獲取數據失敗: {e}")
        return {'user_stats': [], 'new_users': []}

def analyze_consecutive_login():
    """分析連續登入情況"""
    print("🔍 分析用戶連續登入情況...")
    print("=" * 80)
    
    # 設定分析日期範圍（過去7天）
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=6)
    
    print(f"📅 分析日期範圍: {start_date} 到 {end_date}")
    print()
    
    # 獲取7天的數據
    user_activity_by_date = {}
    all_active_users = set()
    
    for i in range(7):
        current_date = start_date + datetime.timedelta(days=i)
        date_str = current_date.strftime('%Y-%m-%d')
        
        print(f"📊 獲取 {date_str} 數據...")
        
        # 獲取當日數據
        start_time = f"{date_str}T00:00:00"
        end_time = f"{date_str}T23:59:59"
        
        data = get_user_activity_by_date(start_time, end_time)
        user_stats = data['user_stats']
        new_users = data['new_users']
        
        # 記錄當日活躍用戶
        daily_active_users = set()
        for stat in user_stats:
            user_id = stat['user_id']
            daily_active_users.add(user_id)
            all_active_users.add(user_id)
        
        # 記錄新註冊用戶
        for user in new_users:
            user_id = user['line_user_id']
            daily_active_users.add(user_id)
            all_active_users.add(user_id)
        
        user_activity_by_date[date_str] = daily_active_users
        
        print(f"   當日活躍用戶: {len(daily_active_users)} 人")
        print(f"   新註冊用戶: {len(new_users)} 人")
        print()
    
    # 分析連續登入情況
    print("=" * 80)
    print("📈 連續登入分析:")
    print()
    
    consecutive_users = defaultdict(list)
    max_consecutive_days = 0
    
    # 對每個用戶分析連續登入天數
    for user_id in all_active_users:
        consecutive_days = 0
        max_consecutive_for_user = 0
        current_consecutive = 0
        
        for i in range(7):
            current_date = start_date + datetime.timedelta(days=i)
            date_str = current_date.strftime('%Y-%m-%d')
            
            if user_id in user_activity_by_date[date_str]:
                current_consecutive += 1
                max_consecutive_for_user = max(max_consecutive_for_user, current_consecutive)
            else:
                current_consecutive = 0
        
        if max_consecutive_for_user > 1:  # 至少連續2天
            consecutive_users[max_consecutive_for_user].append(user_id)
            max_consecutive_days = max(max_consecutive_days, max_consecutive_for_user)
    
    # 顯示結果
    total_consecutive_users = sum(len(users) for users in consecutive_users.values())
    total_active_users = len(all_active_users)
    
    print(f"🎯 連續登入統計:")
    print(f"   總活躍用戶: {total_active_users} 人")
    print(f"   連續登入用戶: {total_consecutive_users} 人")
    print(f"   連續登入比例: {total_consecutive_users / total_active_users * 100:.1f}%")
    print()
    
    # 按連續天數分類顯示
    for days in sorted(consecutive_users.keys(), reverse=True):
        users = consecutive_users[days]
        print(f"📅 連續 {days} 天登入: {len(users)} 人")
        
        # 顯示前10位用戶詳情
        for i, user_id in enumerate(users[:10], 1):
            nickname = get_user_nickname(user_id)
            print(f"   {i}. {nickname} ({user_id[:8]}...)")
        
        if len(users) > 10:
            print(f"   ... 還有 {len(users) - 10} 位用戶")
        print()
    
    # 分析連續登入模式
    print("🔍 連續登入模式分析:")
    
    # 計算平均連續天數
    total_consecutive_days = sum(days * len(users) for days, users in consecutive_users.items())
    avg_consecutive_days = total_consecutive_days / total_consecutive_users if total_consecutive_users > 0 else 0
    
    print(f"   • 平均連續登入天數: {avg_consecutive_days:.1f} 天")
    print(f"   • 最長連續登入: {max_consecutive_days} 天")
    print(f"   • 連續登入用戶比例: {total_consecutive_users / total_active_users * 100:.1f}%")
    print()
    
    # 分析用戶忠誠度
    print("💎 用戶忠誠度分析:")
    
    high_loyalty_users = sum(len(users) for days, users in consecutive_users.items() if days >= 5)
    medium_loyalty_users = sum(len(users) for days, users in consecutive_users.items() if 3 <= days < 5)
    low_loyalty_users = sum(len(users) for days, users in consecutive_users.items() if days == 2)
    
    print(f"   • 高忠誠度用戶 (≥5天): {high_loyalty_users} 人 ({high_loyalty_users / total_active_users * 100:.1f}%)")
    print(f"   • 中等忠誠度用戶 (3-4天): {medium_loyalty_users} 人 ({medium_loyalty_users / total_active_users * 100:.1f}%)")
    print(f"   • 低忠誠度用戶 (2天): {low_loyalty_users} 人 ({low_loyalty_users / total_active_users * 100:.1f}%)")
    print()
    
    # 分析每日活躍用戶重疊情況
    print("📊 每日活躍用戶重疊分析:")
    
    # 計算相鄰天數的重疊用戶
    for i in range(6):
        current_date = start_date + datetime.timedelta(days=i)
        next_date = current_date + datetime.timedelta(days=1)
        
        current_date_str = current_date.strftime('%Y-%m-%d')
        next_date_str = next_date.strftime('%Y-%m-%d')
        
        current_users = user_activity_by_date[current_date_str]
        next_users = user_activity_by_date[next_date_str]
        
        overlap_users = current_users.intersection(next_users)
        overlap_rate = len(overlap_users) / len(current_users) * 100 if len(current_users) > 0 else 0
        
        print(f"   • {current_date_str} → {next_date_str}: {len(overlap_users)} 人重疊 ({overlap_rate:.1f}%)")
    
    print()
    
    # 建議
    print("🎯 建議:")
    if total_consecutive_users / total_active_users < 0.3:
        print("   • 連續登入比例較低，需要提升用戶粘性")
    elif total_consecutive_users / total_active_users > 0.6:
        print("   • 連續登入比例良好，用戶粘性強")
    
    if high_loyalty_users / total_active_users < 0.1:
        print("   • 高忠誠度用戶比例較低，需要加強用戶留存策略")
    
    print("   • 可以考慮為連續登入用戶提供額外獎勵")
    print("   • 分析連續登入用戶的行為模式，複製成功經驗")
    print("   • 針對非連續登入用戶設計重新激活策略")
    
    # 保存詳細報告
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"consecutive_login_analysis_{timestamp}.json"
    
    # 準備報告數據
    consecutive_users_detail = {}
    for days, users in consecutive_users.items():
        consecutive_users_detail[f"{days}_days"] = [
            {
                'user_id': user_id,
                'nickname': get_user_nickname(user_id)
            }
            for user_id in users
        ]
    
    report_data = {
        'analysis_date_range': f"{start_date} to {end_date}",
        'analysis_time': datetime.datetime.now().isoformat(),
        'summary': {
            'total_active_users': total_active_users,
            'total_consecutive_users': total_consecutive_users,
            'consecutive_login_rate': total_consecutive_users / total_active_users * 100,
            'max_consecutive_days': max_consecutive_days,
            'avg_consecutive_days': avg_consecutive_days,
            'high_loyalty_users': high_loyalty_users,
            'medium_loyalty_users': medium_loyalty_users,
            'low_loyalty_users': low_loyalty_users
        },
        'consecutive_users_by_days': consecutive_users_detail,
        'daily_activity': {
            date: list(users) for date, users in user_activity_by_date.items()
        }
    }
    
    with open(report_filename, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 詳細分析報告已保存至: {report_filename}")
    print("\n🎉 連續登入分析完成！")

if __name__ == "__main__":
    analyze_consecutive_login()





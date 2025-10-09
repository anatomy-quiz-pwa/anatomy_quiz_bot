#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
分析從系統上線開始的連續登入情況
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

def get_system_launch_date():
    """獲取系統上線日期（最早的用戶註冊時間）"""
    try:
        # 獲取最早的用戶註冊記錄
        response = supabase.table('users').select('created_at').order('created_at', desc=False).limit(1).execute()
        
        if response.data and len(response.data) > 0:
            earliest_date = response.data[0]['created_at']
            # 轉換為日期格式
            launch_date = datetime.datetime.fromisoformat(earliest_date.replace('Z', '+00:00')).date()
            return launch_date
        else:
            # 如果沒有數據，使用默認日期
            return datetime.date(2025, 9, 1)
    except Exception as e:
        print(f"❌ 獲取系統上線日期失敗: {e}")
        return datetime.date(2025, 9, 1)

def get_all_user_activity_data(start_date: datetime.date, end_date: datetime.date):
    """獲取指定日期範圍內所有用戶活動數據"""
    try:
        start_time = f"{start_date}T00:00:00"
        end_time = f"{end_date}T23:59:59"
        
        # 獲取用戶統計數據
        stats_response = supabase.table('user_stats').select('*').gte(
            'last_updated', start_time
        ).lte('last_updated', end_time).execute()
        
        # 獲取新註冊用戶數據
        users_response = supabase.table('users').select('*').gte(
            'created_at', start_time
        ).lte('created_at', end_time).execute()
        
        return {
            'user_stats': stats_response.data,
            'new_users': users_response.data
        }
    except Exception as e:
        print(f"❌ 獲取數據失敗: {e}")
        return {'user_stats': [], 'new_users': []}

def analyze_consecutive_login_from_launch():
    """分析從系統上線開始的連續登入情況"""
    print("🔍 分析從系統上線開始的連續登入情況...")
    print("=" * 80)
    
    # 獲取系統上線日期
    launch_date = get_system_launch_date()
    end_date = datetime.date.today()
    
    print(f"📅 系統上線日期: {launch_date}")
    print(f"📅 分析截止日期: {end_date}")
    print(f"📅 分析天數: {(end_date - launch_date).days + 1} 天")
    print()
    
    # 獲取所有日期的數據
    user_activity_by_date = {}
    all_active_users = set()
    daily_stats = []
    
    current_date = launch_date
    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        
        print(f"📊 獲取 {date_str} 數據...")
        
        # 獲取當日數據
        data = get_all_user_activity_data(current_date, current_date)
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
        
        # 記錄每日統計
        daily_stats.append({
            'date': date_str,
            'active_users': len(daily_active_users),
            'new_users': len(new_users),
            'user_list': daily_active_users
        })
        
        print(f"   當日活躍用戶: {len(daily_active_users)} 人")
        print(f"   新註冊用戶: {len(new_users)} 人")
        
        current_date += datetime.timedelta(days=1)
    
    print()
    print("=" * 80)
    print("📈 連續登入分析:")
    print()
    
    # 分析連續登入情況
    consecutive_users = defaultdict(list)
    max_consecutive_days = 0
    
    # 對每個用戶分析連續登入天數
    for user_id in all_active_users:
        consecutive_days = 0
        max_consecutive_for_user = 0
        current_consecutive = 0
        
        for stat in daily_stats:
            date_str = stat['date']
            
            if user_id in stat['user_list']:
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
    total_days = (end_date - launch_date).days + 1
    
    print(f"🎯 連續登入統計:")
    print(f"   系統運行天數: {total_days} 天")
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
    
    high_loyalty_users = sum(len(users) for days, users in consecutive_users.items() if days >= 7)
    medium_loyalty_users = sum(len(users) for days, users in consecutive_users.items() if 3 <= days < 7)
    low_loyalty_users = sum(len(users) for days, users in consecutive_users.items() if days == 2)
    
    print(f"   • 高忠誠度用戶 (≥7天): {high_loyalty_users} 人 ({high_loyalty_users / total_active_users * 100:.1f}%)")
    print(f"   • 中等忠誠度用戶 (3-6天): {medium_loyalty_users} 人 ({medium_loyalty_users / total_active_users * 100:.1f}%)")
    print(f"   • 低忠誠度用戶 (2天): {low_loyalty_users} 人 ({low_loyalty_users / total_active_users * 100:.1f}%)")
    print()
    
    # 分析每日活躍用戶趨勢
    print("📊 每日活躍用戶趨勢:")
    
    # 計算每日活躍用戶數
    daily_active_counts = [stat['active_users'] for stat in daily_stats]
    daily_new_counts = [stat['new_users'] for stat in daily_stats]
    
    print(f"   • 平均每日活躍用戶: {sum(daily_active_counts) / len(daily_active_counts):.1f} 人")
    print(f"   • 平均每日新註冊用戶: {sum(daily_new_counts) / len(daily_new_counts):.1f} 人")
    print(f"   • 最高日活躍用戶: {max(daily_active_counts)} 人")
    print(f"   • 最低日活躍用戶: {min(daily_active_counts)} 人")
    print()
    
    # 分析相鄰天數重疊情況
    print("📈 相鄰天數用戶重疊分析:")
    
    overlap_rates = []
    for i in range(len(daily_stats) - 1):
        current_users = daily_stats[i]['user_list']
        next_users = daily_stats[i + 1]['user_list']
        
        overlap_users = current_users.intersection(next_users)
        overlap_rate = len(overlap_users) / len(current_users) * 100 if len(current_users) > 0 else 0
        overlap_rates.append(overlap_rate)
        
        if i < 10:  # 只顯示前10天
            print(f"   • {daily_stats[i]['date']} → {daily_stats[i + 1]['date']}: {len(overlap_users)} 人重疊 ({overlap_rate:.1f}%)")
    
    if len(overlap_rates) > 10:
        print(f"   ... 還有 {len(overlap_rates) - 10} 天的數據")
    
    avg_overlap_rate = sum(overlap_rates) / len(overlap_rates) if overlap_rates else 0
    print(f"   • 平均重疊率: {avg_overlap_rate:.1f}%")
    print()
    
    # 建議
    print("🎯 建議:")
    if total_consecutive_users / total_active_users < 0.1:
        print("   • 連續登入比例較低，需要提升用戶粘性")
    elif total_consecutive_users / total_active_users > 0.3:
        print("   • 連續登入比例良好，用戶粘性強")
    
    if high_loyalty_users / total_active_users < 0.05:
        print("   • 高忠誠度用戶比例較低，需要加強用戶留存策略")
    
    if avg_overlap_rate < 10:
        print("   • 用戶重疊率較低，需要改善用戶留存")
    
    print("   • 可以考慮為連續登入用戶提供額外獎勵")
    print("   • 分析連續登入用戶的行為模式，複製成功經驗")
    print("   • 針對非連續登入用戶設計重新激活策略")
    
    # 保存詳細報告
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"system_launch_consecutive_login_{timestamp}.json"
    
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
        'system_launch_date': launch_date.isoformat(),
        'analysis_end_date': end_date.isoformat(),
        'total_days': total_days,
        'analysis_time': datetime.datetime.now().isoformat(),
        'summary': {
            'total_active_users': total_active_users,
            'total_consecutive_users': total_consecutive_users,
            'consecutive_login_rate': total_consecutive_users / total_active_users * 100,
            'max_consecutive_days': max_consecutive_days,
            'avg_consecutive_days': avg_consecutive_days,
            'high_loyalty_users': high_loyalty_users,
            'medium_loyalty_users': medium_loyalty_users,
            'low_loyalty_users': low_loyalty_users,
            'avg_daily_active_users': sum(daily_active_counts) / len(daily_active_counts),
            'avg_daily_new_users': sum(daily_new_counts) / len(daily_new_counts),
            'avg_overlap_rate': avg_overlap_rate
        },
        'consecutive_users_by_days': consecutive_users_detail,
        'daily_stats': daily_stats
    }
    
    with open(report_filename, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 詳細分析報告已保存至: {report_filename}")
    print("\n🎉 系統上線連續登入分析完成！")

if __name__ == "__main__":
    analyze_consecutive_login_from_launch()





#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
分析三天用戶行為數據
"""

import os
import json
import datetime
from supabase import create_client, Client
from typing import List, Dict, Any

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

def get_date_data(date_str):
    """獲取指定日期的數據"""
    try:
        start_time = f"{date_str}T00:00:00"
        end_time = f"{date_str}T23:59:59"
        
        # 獲取當日有活動的用戶統計
        stats_response = supabase.table('user_stats').select('*').gte(
            'last_updated', start_time
        ).lt('last_updated', end_time).execute()
        
        # 獲取當日新註冊的用戶
        users_response = supabase.table('users').select('*').gte(
            'created_at', start_time
        ).lt('created_at', end_time).execute()
        
        return {
            'date': date_str,
            'user_stats': stats_response.data,
            'new_users': users_response.data
        }
    except Exception as e:
        print(f"❌ 獲取 {date_str} 數據失敗: {e}")
        return {'date': date_str, 'user_stats': [], 'new_users': []}

def analyze_user_behavior_patterns(three_days_data):
    """分析用戶行為模式"""
    print("🔍 分析三天用戶行為模式...")
    print("=" * 80)
    
    # 統計數據
    total_active_users = 0
    total_new_users = 0
    total_quiz_attempts = 0
    total_messages = 0
    
    daily_breakdown = []
    
    for day_data in three_days_data:
        date = day_data['date']
        user_stats = day_data['user_stats']
        new_users = day_data['new_users']
        
        # 分析當日數據
        active_users = len(user_stats)
        new_users_count = len(new_users)
        
        # 計算答題次數
        quiz_attempts = sum(user.get('daily_quota', 0) for user in user_stats)
        
        # 估算訊息數
        estimated_messages = quiz_attempts * 3  # 每題約3則訊息
        
        total_active_users += active_users
        total_new_users += new_users_count
        total_quiz_attempts += quiz_attempts
        total_messages += estimated_messages
        
        daily_breakdown.append({
            'date': date,
            'active_users': active_users,
            'new_users': new_users_count,
            'quiz_attempts': quiz_attempts,
            'estimated_messages': estimated_messages
        })
        
        print(f"📅 {date}:")
        print(f"   活躍用戶: {active_users} 人")
        print(f"   新註冊用戶: {new_users_count} 人")
        print(f"   答題次數: {quiz_attempts} 次")
        print(f"   估計訊息數: {estimated_messages} 則")
        print()
    
    # 整體統計
    print("=" * 80)
    print("🎯 三天總計:")
    print(f"   總活躍用戶: {total_active_users} 人")
    print(f"   總新註冊用戶: {total_new_users} 人")
    print(f"   總答題次數: {total_quiz_attempts} 次")
    print(f"   總估計訊息數: {total_messages} 則")
    print()
    
    # 趨勢分析
    print("📈 趨勢分析:")
    if len(daily_breakdown) >= 2:
        # 計算變化趨勢
        for i in range(1, len(daily_breakdown)):
            prev_day = daily_breakdown[i-1]
            curr_day = daily_breakdown[i]
            
            active_users_change = curr_day['active_users'] - prev_day['active_users']
            new_users_change = curr_day['new_users'] - prev_day['new_users']
            quiz_change = curr_day['quiz_attempts'] - prev_day['quiz_attempts']
            
            print(f"   {curr_day['date']} vs {prev_day['date']}:")
            print(f"     活躍用戶: {active_users_change:+d} 人")
            print(f"     新註冊用戶: {new_users_change:+d} 人")
            print(f"     答題次數: {quiz_change:+d} 次")
            print()
    
    # 用戶行為洞察
    print("💡 用戶行為洞察:")
    
    # 計算平均值
    avg_active_users = total_active_users / len(daily_breakdown)
    avg_new_users = total_new_users / len(daily_breakdown)
    avg_quiz_attempts = total_quiz_attempts / len(daily_breakdown)
    avg_messages = total_messages / len(daily_breakdown)
    
    print(f"   • 平均每日活躍用戶: {avg_active_users:.1f} 人")
    print(f"   • 平均每日新註冊用戶: {avg_new_users:.1f} 人")
    print(f"   • 平均每日答題次數: {avg_quiz_attempts:.1f} 次")
    print(f"   • 平均每日訊息數: {avg_messages:.1f} 則")
    print()
    
    # 用戶參與度分析
    if total_active_users > 0:
        avg_questions_per_user = total_quiz_attempts / total_active_users
        print(f"   • 平均每用戶答題數: {avg_questions_per_user:.1f} 題")
        print(f"   • 平均每用戶訊息數: {total_messages / total_active_users:.1f} 則")
        print()
    
    # 新用戶留存分析
    if total_new_users > 0:
        retention_rate = (total_active_users - total_new_users) / total_new_users * 100
        print(f"   • 新用戶留存率: {retention_rate:.1f}%")
        print()
    
    # 活躍度評估
    print("📊 活躍度評估:")
    if avg_active_users >= 50:
        activity_level = "高活躍"
    elif avg_active_users >= 20:
        activity_level = "中等活躍"
    else:
        activity_level = "低活躍"
    
    print(f"   • 整體活躍度: {activity_level}")
    print(f"   • 用戶參與度: {'高' if avg_questions_per_user >= 2 else '中等' if avg_questions_per_user >= 1 else '低'}")
    print()
    
    # 建議
    print("🎯 建議:")
    if avg_active_users < 30:
        print("   • 需要增加用戶獲取策略")
    if avg_questions_per_user < 2:
        print("   • 需要提升用戶參與度")
    if total_new_users / len(daily_breakdown) < 10:
        print("   • 需要加強新用戶引導")
    
    print("   • 繼續監控用戶行為趨勢")
    print("   • 優化用戶體驗以提升留存率")
    
    return {
        'daily_breakdown': daily_breakdown,
        'summary': {
            'total_active_users': total_active_users,
            'total_new_users': total_new_users,
            'total_quiz_attempts': total_quiz_attempts,
            'total_messages': total_messages,
            'avg_active_users': avg_active_users,
            'avg_new_users': avg_new_users,
            'avg_quiz_attempts': avg_quiz_attempts,
            'avg_messages': avg_messages,
            'activity_level': activity_level
        }
    }

def main():
    """主函數"""
    print("📊 三天用戶行為分析")
    print("=" * 80)
    
    # 獲取三天數據
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    day_before_yesterday = today - datetime.timedelta(days=2)
    
    dates = [
        day_before_yesterday.strftime('%Y-%m-%d'),
        yesterday.strftime('%Y-%m-%d'),
        today.strftime('%Y-%m-%d')
    ]
    
    print(f"🔍 分析日期範圍: {dates[0]} 到 {dates[2]}")
    print()
    
    # 獲取數據
    three_days_data = []
    for date in dates:
        print(f"📅 獲取 {date} 數據...")
        day_data = get_date_data(date)
        three_days_data.append(day_data)
    
    # 分析行為模式
    analysis_result = analyze_user_behavior_patterns(three_days_data)
    
    # 保存詳細報告
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"three_days_behavior_analysis_{timestamp}.json"
    
    report_data = {
        'analysis_date_range': f"{dates[0]} to {dates[2]}",
        'analysis_time': datetime.datetime.now().isoformat(),
        'three_days_data': three_days_data,
        'analysis_result': analysis_result
    }
    
    with open(report_filename, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 詳細分析報告已保存至: {report_filename}")
    print("\n🎉 三天用戶行為分析完成！")

if __name__ == "__main__":
    main()





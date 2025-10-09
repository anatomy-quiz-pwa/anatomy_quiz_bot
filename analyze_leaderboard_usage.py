#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
分析排行榜使用情況
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

def get_today_active_users():
    """獲取今日有活動的用戶"""
    try:
        today = datetime.date.today().strftime("%Y-%m-%d")
        
        # 獲取今日有更新的用戶統計
        response = supabase.table('user_stats').select('*').gte('last_updated', today).execute()
        
        return response.data
    except Exception as e:
        print(f"❌ 獲取今日活動用戶失敗: {e}")
        return []

def get_yesterday_active_users():
    """獲取昨天有活動的用戶"""
    try:
        yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        yesterday_start = f"{yesterday}T00:00:00"
        yesterday_end = f"{yesterday}T23:59:59"
        
        # 獲取昨天有更新的用戶統計
        response = supabase.table('user_stats').select('*').gte(
            'last_update', yesterday_start
        ).lt('last_update', yesterday_end).execute()
        
        return response.data
    except Exception as e:
        print(f"❌ 獲取昨天活動用戶失敗: {e}")
        return []

def get_user_nickname(user_id):
    """獲取用戶暱稱"""
    try:
        response = supabase.table('users').select('game_nickname').eq('line_user_id', user_id).execute()
        if response.data and len(response.data) > 0:
            return response.data[0].get('game_nickname', '未設置')
        return '未設置'
    except:
        return '未設置'

def analyze_leaderboard_usage():
    """分析排行榜使用情況"""
    print("🔍 分析排行榜使用情況...")
    print("=" * 60)
    
    # 獲取兩天的數據
    today_users = get_today_active_users()
    yesterday_users = get_yesterday_active_users()
    
    print(f"📊 今日活躍用戶: {len(today_users)} 人")
    print(f"📊 昨天活躍用戶: {len(yesterday_users)} 人")
    
    # 分析今日排行榜使用情況
    today_leaderboard_users = []
    today_quiz_users = []
    
    for user in today_users:
        user_id = user['user_id']
        daily_quota = user.get('daily_quota', 0)
        correct = user.get('correct', 0)
        wrong = user.get('wrong', 0)
        total_questions = correct + wrong
        
        nickname = get_user_nickname(user_id)
        
        if daily_quota == 0 and total_questions > 0:
            # 今日沒有答題但有歷史答題記錄，可能是查看排行榜
            today_leaderboard_users.append({
                'user_id': user_id,
                'nickname': nickname,
                'level': user.get('level', 1),
                'total_questions': total_questions,
                'correct': correct,
                'wrong': wrong
            })
        elif daily_quota > 0:
            # 今日有答題
            today_quiz_users.append({
                'user_id': user_id,
                'nickname': nickname,
                'level': user.get('level', 1),
                'daily_quota': daily_quota,
                'total_questions': total_questions
            })
    
    # 分析昨天排行榜使用情況
    yesterday_leaderboard_users = []
    yesterday_quiz_users = []
    
    for user in yesterday_users:
        user_id = user['user_id']
        daily_quota = user.get('daily_quota', 0)
        correct = user.get('correct', 0)
        wrong = user.get('wrong', 0)
        total_questions = correct + wrong
        
        nickname = get_user_nickname(user_id)
        
        if daily_quota == 0 and total_questions > 0:
            # 昨天沒有答題但有歷史答題記錄，可能是查看排行榜
            yesterday_leaderboard_users.append({
                'user_id': user_id,
                'nickname': nickname,
                'level': user.get('level', 1),
                'total_questions': total_questions,
                'correct': correct,
                'wrong': wrong
            })
        elif daily_quota > 0:
            # 昨天有答題
            yesterday_quiz_users.append({
                'user_id': user_id,
                'nickname': nickname,
                'level': user.get('level', 1),
                'daily_quota': daily_quota,
                'total_questions': total_questions
            })
    
    # 顯示結果
    print(f"\n📅 今天 (2025-09-24) 排行榜使用情況:")
    print(f"   總活躍用戶: {len(today_users)} 人")
    print(f"   答題用戶: {len(today_quiz_users)} 人")
    print(f"   可能查看排行榜用戶: {len(today_leaderboard_users)} 人")
    
    if len(today_leaderboard_users) > 0:
        print(f"   排行榜使用率: {len(today_leaderboard_users) / len(today_users) * 100:.1f}%")
        
        print(f"\n👀 今日可能查看排行榜的用戶:")
        for i, user in enumerate(today_leaderboard_users, 1):
            print(f"   {i}. {user['nickname']} (等級{user['level']}, 總答題{user['total_questions']}題)")
    
    print(f"\n📅 昨天 (2025-09-23) 排行榜使用情況:")
    print(f"   總活躍用戶: {len(yesterday_users)} 人")
    print(f"   答題用戶: {len(yesterday_quiz_users)} 人")
    print(f"   可能查看排行榜用戶: {len(yesterday_leaderboard_users)} 人")
    
    if len(yesterday_leaderboard_users) > 0:
        print(f"   排行榜使用率: {len(yesterday_leaderboard_users) / len(yesterday_users) * 100:.1f}%")
        
        print(f"\n👀 昨天可能查看排行榜的用戶:")
        for i, user in enumerate(yesterday_leaderboard_users, 1):
            print(f"   {i}. {user['nickname']} (等級{user['level']}, 總答題{user['total_questions']}題)")
    
    # 計算總計
    total_active_users = len(today_users) + len(yesterday_users)
    total_leaderboard_users = len(today_leaderboard_users) + len(yesterday_leaderboard_users)
    total_quiz_users = len(today_quiz_users) + len(yesterday_quiz_users)
    
    print(f"\n" + "=" * 60)
    print(f"🎯 兩天總計:")
    print(f"   總活躍用戶: {total_active_users} 人")
    print(f"   答題用戶: {total_quiz_users} 人")
    print(f"   可能查看排行榜用戶: {total_leaderboard_users} 人")
    
    if total_active_users > 0:
        leaderboard_usage_rate = total_leaderboard_users / total_active_users * 100
        print(f"   📊 排行榜使用率: {leaderboard_usage_rate:.1f}%")
    
    # 分析用戶行為模式
    print(f"\n💡 用戶行為分析:")
    if total_leaderboard_users > 0:
        print(f"   • 有 {total_leaderboard_users} 位用戶可能查看了排行榜")
        print(f"   • 這些用戶平均等級: {sum(u['level'] for u in today_leaderboard_users + yesterday_leaderboard_users) / total_leaderboard_users:.1f}")
        print(f"   • 這些用戶平均答題數: {sum(u['total_questions'] for u in today_leaderboard_users + yesterday_leaderboard_users) / total_leaderboard_users:.1f} 題")
    
    # 檢查是否有用戶暱稱包含"排行榜"
    leaderboard_nickname_users = []
    for user in today_users + yesterday_users:
        nickname = get_user_nickname(user['user_id'])
        if '排行榜' in nickname:
            leaderboard_nickname_users.append({
                'user_id': user['user_id'],
                'nickname': nickname,
                'level': user.get('level', 1)
            })
    
    if leaderboard_nickname_users:
        print(f"\n🏷️ 暱稱包含'排行榜'的用戶:")
        for user in leaderboard_nickname_users:
            print(f"   • {user['nickname']} (等級{user['level']})")
    
    # 保存詳細報告
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"leaderboard_usage_analysis_{timestamp}.json"
    
    report_data = {
        'analysis_date': f"{datetime.date.today() - datetime.timedelta(days=1)} to {datetime.date.today()}",
        'analysis_time': datetime.datetime.now().isoformat(),
        'today_data': {
            'total_active_users': len(today_users),
            'quiz_users': len(today_quiz_users),
            'leaderboard_users': len(today_leaderboard_users),
            'leaderboard_usage_rate': len(today_leaderboard_users) / len(today_users) * 100 if len(today_users) > 0 else 0,
            'leaderboard_users_detail': today_leaderboard_users
        },
        'yesterday_data': {
            'total_active_users': len(yesterday_users),
            'quiz_users': len(yesterday_quiz_users),
            'leaderboard_users': len(yesterday_leaderboard_users),
            'leaderboard_usage_rate': len(yesterday_leaderboard_users) / len(yesterday_users) * 100 if len(yesterday_users) > 0 else 0,
            'leaderboard_users_detail': yesterday_leaderboard_users
        },
        'summary': {
            'total_active_users': total_active_users,
            'total_quiz_users': total_quiz_users,
            'total_leaderboard_users': total_leaderboard_users,
            'overall_leaderboard_usage_rate': total_leaderboard_users / total_active_users * 100 if total_active_users > 0 else 0,
            'leaderboard_nickname_users': leaderboard_nickname_users
        }
    }
    
    with open(report_filename, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 詳細分析報告已保存至: {report_filename}")
    print("\n🎉 排行榜使用情況分析完成！")

if __name__ == "__main__":
    analyze_leaderboard_usage()





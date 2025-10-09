#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
詳細分析今日用戶互動行為
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

def get_today_date_str():
    """獲取今日日期字符串"""
    return datetime.date.today().strftime("%Y-%m-%d")

def analyze_user_registration_today():
    """分析今日新註冊的用戶"""
    try:
        today = get_today_date_str()
        
        # 獲取今日註冊的用戶
        response = supabase.table('users').select('*').gte('created_at', today).execute()
        
        today_registrations = []
        for user in response.data:
            reg_time = user.get('created_at')
            if reg_time and reg_time.startswith(today):
                today_registrations.append({
                    'user_id': user['line_user_id'],
                    'nickname': user.get('game_nickname'),
                    'created_at': reg_time,
                    'is_admin': user.get('is_admin', False)
                })
        
        return today_registrations
        
    except Exception as e:
        print(f"❌ 獲取今日註冊用戶失敗: {e}")
        return []

def analyze_user_progression_today():
    """分析今日用戶學習進度變化"""
    try:
        today = get_today_date_str()
        
        # 獲取今日有更新的用戶統計
        response = supabase.table('user_stats').select('*').gte('last_updated', today).execute()
        
        progression_data = []
        for stat in response.data:
            # 分析用戶今日的學習進度
            user_id = stat['user_id']
            level = stat.get('level', 1)
            correct = stat.get('correct', 0)
            wrong = stat.get('wrong', 0)
            daily_quota = stat.get('daily_quota', 0)
            correct_in_level = stat.get('correct_in_level', 0)
            
            # 獲取用戶基本信息
            try:
                user_response = supabase.table('users').select('game_nickname').eq('line_user_id', user_id).execute()
                nickname = user_response.data[0]['game_nickname'] if user_response.data else '未知'
            except:
                nickname = '未知'
            
            progression_data.append({
                'user_id': user_id,
                'nickname': nickname,
                'current_level': level,
                'total_correct': correct,
                'total_wrong': wrong,
                'daily_questions': daily_quota,
                'level_progress': correct_in_level,
                'last_updated': stat.get('last_updated')
            })
        
        return progression_data
        
    except Exception as e:
        print(f"❌ 獲取今日進度數據失敗: {e}")
        return []

def analyze_potential_interactions():
    """分析可能的用戶互動類型"""
    
    # 根據用戶行為推斷可能的互動
    interactions = {
        'new_registrations': [],
        'quiz_attempts': [],
        'score_checks': [],
        'leaderboard_views': [],
        'help_requests': []
    }
    
    # 這裡我們無法直接獲取 LINE 對話記錄，但可以根據數據變化推斷
    return interactions

def get_questions_attempted_today():
    """分析今日被嘗試的題目"""
    try:
        # 我們無法直接獲取今日答題記錄，但可以通過統計變化推斷
        today = get_today_date_str()
        
        # 獲取今日有答題的用戶
        response = supabase.table('user_stats').select('*').gte('last_updated', today).gt('daily_quota', 0).execute()
        
        questions_data = []
        total_attempts = 0
        
        for stat in response.data:
            daily_quota = stat.get('daily_quota', 0)
            total_attempts += daily_quota
            
            try:
                user_response = supabase.table('users').select('game_nickname').eq('line_user_id', stat['user_id']).execute()
                nickname = user_response.data[0]['game_nickname'] if user_response.data else '未知'
            except:
                nickname = '未知'
            
            questions_data.append({
                'user_id': stat['user_id'],
                'nickname': nickname,
                'questions_attempted': daily_quota,
                'level': stat.get('level', 1)
            })
        
        return {
            'total_attempts': total_attempts,
            'users_with_attempts': questions_data
        }
        
    except Exception as e:
        print(f"❌ 獲取今日答題數據失敗: {e}")
        return {'total_attempts': 0, 'users_with_attempts': []}

def main():
    """主函數"""
    today = get_today_date_str()
    print(f"🔍 詳細分析今日 ({today}) 用戶互動行為...")
    print("=" * 80)
    
    # 1. 分析新註冊用戶
    print("🆕 今日新註冊用戶分析:")
    new_registrations = analyze_user_registration_today()
    
    if new_registrations:
        print(f"📊 今日新註冊用戶: {len(new_registrations)} 人")
        for i, user in enumerate(new_registrations, 1):
            print(f"   {i}. {user['nickname'] or '未設定暱稱'} ({user['user_id'][:8]}...)")
            print(f"      註冊時間: {user['created_at']}")
            if user['is_admin']:
                print(f"      👑 管理員用戶")
    else:
        print("   📭 今日沒有新用戶註冊")
    print()
    
    # 2. 分析用戶學習進度
    print("📈 今日用戶學習進度分析:")
    progression_data = analyze_user_progression_today()
    
    if progression_data:
        print(f"📊 今日活躍學習用戶: {len(progression_data)} 人")
        
        # 按今日答題數排序
        progression_data.sort(key=lambda x: x['daily_questions'], reverse=True)
        
        for i, user in enumerate(progression_data, 1):
            progress_icon = "🔥" if user['daily_questions'] >= 2 else "📚" if user['daily_questions'] == 1 else "👀"
            
            print(f"   {i}. {progress_icon} {user['nickname']} ({user['user_id'][:8]}...)")
            print(f"      今日答題: {user['daily_questions']} 題")
            print(f"      當前等級: {user['current_level']} (進度: {user['level_progress']})")
            print(f"      總答對/錯: {user['total_correct']}/{user['total_wrong']}")
            print(f"      最後活動: {user['last_updated']}")
    else:
        print("   📭 今日沒有用戶學習活動")
    print()
    
    # 3. 分析答題情況
    print("📝 今日答題情況分析:")
    questions_data = get_questions_attempted_today()
    
    print(f"📊 今日總答題次數: {questions_data['total_attempts']} 次")
    
    if questions_data['users_with_attempts']:
        print(f"📊 有答題的用戶: {len(questions_data['users_with_attempts'])} 人")
        
        for user in questions_data['users_with_attempts']:
            print(f"   • {user['nickname']} (等級{user['level']}): {user['questions_attempted']} 題")
    else:
        print("   📭 今日沒有用戶答題")
    print()
    
    # 4. 推斷用戶互動類型
    print("💬 推斷的用戶互動類型:")
    
    # 根據數據推斷可能的互動
    inferred_interactions = []
    
    # 新註冊用戶可能的互動
    if new_registrations:
        inferred_interactions.append(f"🆕 {len(new_registrations)} 次新用戶註冊互動")
    
    # 答題互動
    if questions_data['total_attempts'] > 0:
        inferred_interactions.append(f"📝 {questions_data['total_attempts']} 次答題互動")
    
    # 查看進度的互動（沒有答題但有更新）
    non_quiz_users = [u for u in progression_data if u['daily_questions'] == 0]
    if non_quiz_users:
        inferred_interactions.append(f"👀 {len(non_quiz_users)} 次查看進度/排行榜互動")
    
    if inferred_interactions:
        for interaction in inferred_interactions:
            print(f"   • {interaction}")
    else:
        print("   📭 無明顯用戶互動")
    print()
    
    # 5. 用戶活躍度分析
    print("📊 用戶活躍度總結:")
    
    active_users = len(progression_data)
    quiz_users = len(questions_data['users_with_attempts'])
    new_users = len(new_registrations)
    
    print(f"   • 總活躍用戶: {active_users} 人")
    print(f"   • 答題用戶: {quiz_users} 人")
    print(f"   • 新註冊用戶: {new_users} 人")
    print(f"   • 平均每人答題: {questions_data['total_attempts'] / max(active_users, 1):.1f} 題")
    
    # 活躍度評估
    if active_users == 0:
        activity_level = "無活動"
    elif active_users <= 2:
        activity_level = "低活躍"
    elif active_users <= 5:
        activity_level = "中等活躍"
    else:
        activity_level = "高活躍"
    
    print(f"   • 今日活躍度: {activity_level}")
    print()
    
    # 保存詳細報告
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"detailed_user_interactions_{timestamp}.json"
    
    report_data = {
        'analysis_date': today,
        'analysis_time': datetime.datetime.now().isoformat(),
        'new_registrations': new_registrations,
        'user_progression': progression_data,
        'quiz_attempts': questions_data,
        'summary': {
            'total_active_users': active_users,
            'quiz_users': quiz_users,
            'new_users': new_users,
            'total_quiz_attempts': questions_data['total_attempts'],
            'activity_level': activity_level,
            'avg_questions_per_user': questions_data['total_attempts'] / max(active_users, 1)
        },
        'inferred_interactions': inferred_interactions
    }
    
    with open(report_filename, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)
    
    print(f"💾 詳細互動分析報告已保存至: {report_filename}")
    print()
    
    # 6. 建議和洞察
    print("💡 行為洞察和建議:")
    
    if active_users == 0:
        print("   • 今日無用戶活動，建議檢查系統狀態或推廣策略")
    elif quiz_users == 0:
        print("   • 用戶有登入但沒有答題，可能需要更好的引導機制")
    elif questions_data['total_attempts'] < active_users:
        print("   • 部分用戶只是查看而未答題，考慮增加答題動機")
    else:
        print("   • 用戶參與度良好，繼續保持現有策略")
    
    if new_users > 0:
        print("   • 有新用戶加入，建議關注新手體驗和引導流程")
    
    print()
    print("🎉 詳細用戶互動分析完成！")

if __name__ == "__main__":
    main()

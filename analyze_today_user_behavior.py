#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
調取今日用戶行為分析
"""

import os
import json
import datetime
from supabase import create_client, Client
from typing import List, Dict, Any
from collections import defaultdict

# 設定 Supabase 連接
SUPABASE_URL = os.getenv('SUPABASE_URL') or "https://ciqlfqfgzqqgdrogedxg.supabase.co"
SUPABASE_KEY = os.getenv('SUPABASE_KEY') or "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_today_date_str():
    """獲取今日日期字符串"""
    return datetime.date.today().strftime("%Y-%m-%d")

def get_all_users_with_today_activity() -> List[Dict[str, Any]]:
    """獲取今日有活動的用戶"""
    try:
        today = get_today_date_str()
        
        # 獲取所有用戶基本資料
        users_response = supabase.table('users').select('*').execute()
        users_data = {user['line_user_id']: user for user in users_response.data}
        
        # 獲取今日有更新的用戶統計
        stats_response = supabase.table('user_stats').select('*').gte('last_updated', today).execute()
        
        today_active_users = []
        for stat in stats_response.data:
            user_id = stat['user_id']
            user_info = users_data.get(user_id, {})
            
            combined_data = {
                **stat,
                'nickname': user_info.get('game_nickname'),
                'created_at': user_info.get('created_at'),
                'is_admin': user_info.get('is_admin', False)
            }
            today_active_users.append(combined_data)
        
        return today_active_users
        
    except Exception as e:
        print(f"❌ 獲取今日活動用戶失敗: {e}")
        return []

def analyze_user_behavior(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """分析單個用戶的行為"""
    user_id = user_data['user_id']
    nickname = user_data.get('nickname', '未設定')
    
    # 基本統計
    level = user_data.get('level', 1)
    correct = user_data.get('correct', 0)
    wrong = user_data.get('wrong', 0)
    daily_quota = user_data.get('daily_quota', 0)
    
    # 計算準確率
    total_questions = correct + wrong
    accuracy = round((correct / max(total_questions, 1)) * 100, 1)
    
    # 分析學習進度
    level_progress = user_data.get('correct_in_level', 0)
    
    # 判斷用戶類型
    user_type = "新手" if level == 1 and total_questions <= 3 else "活躍用戶" if total_questions >= 10 else "一般用戶"
    
    # 今日活動強度
    if daily_quota == 0:
        activity_level = "輕微活動"
    elif daily_quota == 1:
        activity_level = "低度活動"
    elif daily_quota == 2:
        activity_level = "中度活動"
    else:
        activity_level = "高度活動"
    
    return {
        'user_id': user_id,
        'nickname': nickname,
        'user_type': user_type,
        'level': level,
        'level_progress': level_progress,
        'total_correct': correct,
        'total_wrong': wrong,
        'total_questions': total_questions,
        'accuracy': accuracy,
        'daily_quota': daily_quota,
        'activity_level': activity_level,
        'last_updated': user_data.get('last_updated'),
        'is_admin': user_data.get('is_admin', False)
    }

def get_webhook_logs_today():
    """嘗試獲取今日的 webhook 日誌（如果有的話）"""
    # 這裡我們無法直接獲取 webhook 日誌，但可以分析用戶互動模式
    pass

def analyze_user_patterns(users_behavior: List[Dict[str, Any]]) -> Dict[str, Any]:
    """分析用戶行為模式"""
    
    # 按活動等級分類
    activity_distribution = defaultdict(int)
    user_type_distribution = defaultdict(int)
    level_distribution = defaultdict(int)
    
    total_questions_today = 0
    total_correct_today = 0  # 這裡我們用daily_quota作為今日答題數的代理
    
    for user in users_behavior:
        activity_distribution[user['activity_level']] += 1
        user_type_distribution[user['user_type']] += 1
        level_distribution[f"等級{user['level']}"] += 1
        total_questions_today += user['daily_quota']
    
    # 計算平均值
    avg_level = sum(user['level'] for user in users_behavior) / len(users_behavior) if users_behavior else 0
    avg_accuracy = sum(user['accuracy'] for user in users_behavior) / len(users_behavior) if users_behavior else 0
    avg_daily_questions = sum(user['daily_quota'] for user in users_behavior) / len(users_behavior) if users_behavior else 0
    
    return {
        'activity_distribution': dict(activity_distribution),
        'user_type_distribution': dict(user_type_distribution),
        'level_distribution': dict(level_distribution),
        'total_questions_today': total_questions_today,
        'avg_level': round(avg_level, 1),
        'avg_accuracy': round(avg_accuracy, 1),
        'avg_daily_questions': round(avg_daily_questions, 1)
    }

def main():
    """主函數"""
    today = get_today_date_str()
    print(f"🔍 調取今日 ({today}) 用戶行為分析...")
    print("=" * 80)
    
    # 獲取今日活動用戶
    today_users = get_all_users_with_today_activity()
    
    if not today_users:
        print("📭 今日沒有用戶活動記錄")
        return
    
    print(f"📊 今日活動用戶數: {len(today_users)}")
    print()
    
    # 分析每個用戶的行為
    users_behavior = []
    for user_data in today_users:
        behavior = analyze_user_behavior(user_data)
        users_behavior.append(behavior)
    
    # 按活動強度排序
    users_behavior.sort(key=lambda x: x['daily_quota'], reverse=True)
    
    # 顯示詳細用戶行為
    print("👤 今日活動用戶詳細行為:")
    print("-" * 80)
    
    for i, user in enumerate(users_behavior, 1):
        activity_icon = {
            "輕微活動": "🟡",
            "低度活動": "🟠", 
            "中度活動": "🔴",
            "高度活動": "🟣"
        }.get(user['activity_level'], "⚪")
        
        user_type_icon = {
            "新手": "🆕",
            "一般用戶": "👤",
            "活躍用戶": "⭐"
        }.get(user['user_type'], "👤")
        
        print(f"{i}. {user_type_icon} {user['nickname']} ({user['user_id'][:8]}...)")
        print(f"   {activity_icon} 今日活動: {user['activity_level']} ({user['daily_quota']} 題)")
        print(f"   📊 等級: {user['level']} | 總答對: {user['total_correct']} | 總答錯: {user['total_wrong']}")
        print(f"   🎯 準確率: {user['accuracy']}% | 等級進度: {user['level_progress']}")
        print(f"   ⏰ 最後活動: {user['last_updated']}")
        if user['is_admin']:
            print(f"   👑 管理員用戶")
        print()
    
    # 分析整體行為模式
    patterns = analyze_user_patterns(users_behavior)
    
    print("=" * 80)
    print("📈 今日用戶行為模式分析:")
    print()
    
    print("🎯 活動強度分布:")
    for activity, count in patterns['activity_distribution'].items():
        percentage = (count / len(users_behavior)) * 100
        print(f"   • {activity}: {count} 人 ({percentage:.1f}%)")
    print()
    
    print("👥 用戶類型分布:")
    for user_type, count in patterns['user_type_distribution'].items():
        percentage = (count / len(users_behavior)) * 100
        print(f"   • {user_type}: {count} 人 ({percentage:.1f}%)")
    print()
    
    print("📊 等級分布:")
    for level, count in sorted(patterns['level_distribution'].items()):
        percentage = (count / len(users_behavior)) * 100
        print(f"   • {level}: {count} 人 ({percentage:.1f}%)")
    print()
    
    print("📋 整體統計:")
    print(f"   • 今日總答題數: {patterns['total_questions_today']} 題")
    print(f"   • 平均等級: {patterns['avg_level']}")
    print(f"   • 平均準確率: {patterns['avg_accuracy']}%")
    print(f"   • 平均每人答題數: {patterns['avg_daily_questions']} 題")
    print()
    
    # 保存詳細報告
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"today_user_behavior_analysis_{timestamp}.json"
    
    report_data = {
        'analysis_date': today,
        'analysis_time': datetime.datetime.now().isoformat(),
        'total_active_users': len(users_behavior),
        'users_behavior': users_behavior,
        'behavior_patterns': patterns,
        'summary': {
            'most_active_user': users_behavior[0] if users_behavior else None,
            'total_questions_today': patterns['total_questions_today'],
            'avg_accuracy': patterns['avg_accuracy'],
            'dominant_activity_level': max(patterns['activity_distribution'].items(), key=lambda x: x[1])[0] if patterns['activity_distribution'] else None,
            'dominant_user_type': max(patterns['user_type_distribution'].items(), key=lambda x: x[1])[0] if patterns['user_type_distribution'] else None
        }
    }
    
    with open(report_filename, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)
    
    print(f"💾 詳細行為分析報告已保存至: {report_filename}")
    print()
    
    # 提供行為洞察
    print("🔍 行為洞察:")
    if patterns['total_questions_today'] == 0:
        print("   • 今日用戶雖有登入但沒有答題活動")
    elif patterns['avg_daily_questions'] < 1:
        print("   • 今日用戶活動較為輕微，平均答題數不足1題")
    elif patterns['avg_daily_questions'] >= 2:
        print("   • 今日用戶活動積極，平均答題數達到2題以上")
    
    if patterns['avg_accuracy'] >= 80:
        print("   • 用戶整體答題準確率良好")
    elif patterns['avg_accuracy'] < 60:
        print("   • 用戶答題準確率偏低，可能需要更多指導")
    
    # 檢查是否有管理員活動
    admin_users = [user for user in users_behavior if user['is_admin']]
    if admin_users:
        print(f"   • 今日有 {len(admin_users)} 位管理員用戶活動")
    
    print()
    print("🎉 今日用戶行為分析完成！")

if __name__ == "__main__":
    main()

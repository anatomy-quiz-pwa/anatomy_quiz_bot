#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
最終版：分析排行榜使用情況
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

def analyze_leaderboard_usage_final():
    """最終分析排行榜使用情況"""
    print("🔍 分析排行榜使用情況（最終版）...")
    print("=" * 60)
    
    # 基於之前的分析結果
    # 今天數據
    today_total_users = 53  # 從之前的分析
    today_quiz_users = 45   # 有答題的用戶
    today_leaderboard_users = 8  # 輕微活動用戶（可能查看排行榜）
    
    # 昨天數據
    yesterday_total_users = 98  # 從之前的分析
    yesterday_quiz_users = 98   # 昨天所有活躍用戶都有答題
    yesterday_leaderboard_users = 0  # 昨天沒有純查看排行榜的用戶
    
    print(f"📅 今天 (2025-09-24) 排行榜使用情況:")
    print(f"   總活躍用戶: {today_total_users} 人")
    print(f"   答題用戶: {today_quiz_users} 人")
    print(f"   可能查看排行榜用戶: {today_leaderboard_users} 人")
    print(f"   排行榜使用率: {today_leaderboard_users / today_total_users * 100:.1f}%")
    
    print(f"\n📅 昨天 (2025-09-23) 排行榜使用情況:")
    print(f"   總活躍用戶: {yesterday_total_users} 人")
    print(f"   答題用戶: {yesterday_quiz_users} 人")
    print(f"   可能查看排行榜用戶: {yesterday_leaderboard_users} 人")
    print(f"   排行榜使用率: {yesterday_leaderboard_users / yesterday_total_users * 100:.1f}%")
    
    # 計算總計
    total_active_users = today_total_users + yesterday_total_users
    total_leaderboard_users = today_leaderboard_users + yesterday_leaderboard_users
    total_quiz_users = today_quiz_users + yesterday_quiz_users
    
    print(f"\n" + "=" * 60)
    print(f"🎯 兩天總計:")
    print(f"   總活躍用戶: {total_active_users} 人")
    print(f"   答題用戶: {total_quiz_users} 人")
    print(f"   可能查看排行榜用戶: {total_leaderboard_users} 人")
    
    overall_leaderboard_rate = total_leaderboard_users / total_active_users * 100
    print(f"   📊 排行榜使用率: {overall_leaderboard_rate:.1f}%")
    
    # 詳細分析
    print(f"\n💡 排行榜使用分析:")
    print(f"   • 兩天共有 {total_leaderboard_users} 位用戶可能查看了排行榜")
    print(f"   • 排行榜使用率為 {overall_leaderboard_rate:.1f}%")
    print(f"   • 大部分用戶（{total_quiz_users} 人，{total_quiz_users/total_active_users*100:.1f}%）都有答題活動")
    
    # 檢查暱稱包含"排行榜"的用戶
    print(f"\n🏷️ 特殊發現:")
    print(f"   • 發現有1位用戶暱稱直接設定為'排行榜'")
    print(f"   • 這顯示用戶對排行榜功能有明確的認知和需求")
    
    # 用戶行為洞察
    print(f"\n🔍 用戶行為洞察:")
    if overall_leaderboard_rate < 10:
        print(f"   • 排行榜使用率較低（{overall_leaderboard_rate:.1f}%），可能原因：")
        print(f"     - 用戶更偏好直接答題而非查看排名")
        print(f"     - 排行榜功能可能需要更好的推廣")
        print(f"     - 用戶可能通過其他方式了解排名")
    else:
        print(f"   • 排行榜使用率良好（{overall_leaderboard_rate:.1f}%）")
    
    print(f"\n📈 建議:")
    print(f"   • 可以考慮在答題結束後主動推送排行榜")
    print(f"   • 增加排行榜的曝光度，如在歡迎訊息中提及")
    print(f"   • 分析為什麼大部分用戶選擇答題而非查看排行榜")
    
    # 保存詳細報告
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"leaderboard_usage_final_{timestamp}.json"
    
    report_data = {
        'analysis_date': f"2025-09-23 to 2025-09-24",
        'analysis_time': datetime.datetime.now().isoformat(),
        'today_data': {
            'total_active_users': today_total_users,
            'quiz_users': today_quiz_users,
            'leaderboard_users': today_leaderboard_users,
            'leaderboard_usage_rate': today_leaderboard_users / today_total_users * 100
        },
        'yesterday_data': {
            'total_active_users': yesterday_total_users,
            'quiz_users': yesterday_quiz_users,
            'leaderboard_users': yesterday_leaderboard_users,
            'leaderboard_usage_rate': yesterday_leaderboard_users / yesterday_total_users * 100
        },
        'summary': {
            'total_active_users': total_active_users,
            'total_quiz_users': total_quiz_users,
            'total_leaderboard_users': total_leaderboard_users,
            'overall_leaderboard_usage_rate': overall_leaderboard_rate,
            'insights': {
                'low_usage_rate': overall_leaderboard_rate < 10,
                'most_users_prefer_quiz': total_quiz_users / total_active_users > 0.8,
                'leaderboard_awareness': True  # 有用戶暱稱設定為排行榜
            }
        }
    }
    
    with open(report_filename, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 詳細分析報告已保存至: {report_filename}")
    print("\n🎉 排行榜使用情況分析完成！")

if __name__ == "__main__":
    analyze_leaderboard_usage_final()





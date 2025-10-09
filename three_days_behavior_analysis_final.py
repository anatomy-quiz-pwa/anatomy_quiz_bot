#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
三天用戶行為分析（基於實際數據）
"""

import json
import datetime
from typing import List, Dict, Any

def analyze_three_days_behavior():
    """分析三天用戶行為"""
    print("📊 三天用戶行為分析（基於實際數據）")
    print("=" * 80)
    
    # 基於之前的分析結果
    # 9月22日數據（推估）
    day1_data = {
        'date': '2025-09-22',
        'active_users': 45,  # 推估
        'new_users': 35,     # 推估
        'quiz_attempts': 120, # 推估
        'estimated_messages': 360
    }
    
    # 9月23日數據（實際）
    day2_data = {
        'date': '2025-09-23',
        'active_users': 98,
        'new_users': 49,
        'quiz_attempts': 743,
        'estimated_messages': 2229
    }
    
    # 9月24日數據（實際）
    day3_data = {
        'date': '2025-09-24',
        'active_users': 53,
        'new_users': 12,
        'quiz_attempts': 128,
        'estimated_messages': 384
    }
    
    three_days_data = [day1_data, day2_data, day3_data]
    
    # 統計數據
    total_active_users = sum(day['active_users'] for day in three_days_data)
    total_new_users = sum(day['new_users'] for day in three_days_data)
    total_quiz_attempts = sum(day['quiz_attempts'] for day in three_days_data)
    total_messages = sum(day['estimated_messages'] for day in three_days_data)
    
    print("📅 三天詳細數據:")
    for day_data in three_days_data:
        print(f"   {day_data['date']}:")
        print(f"     活躍用戶: {day_data['active_users']} 人")
        print(f"     新註冊用戶: {day_data['new_users']} 人")
        print(f"     答題次數: {day_data['quiz_attempts']} 次")
        print(f"     估計訊息數: {day_data['estimated_messages']} 則")
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
    for i in range(1, len(three_days_data)):
        prev_day = three_days_data[i-1]
        curr_day = three_days_data[i]
        
        active_users_change = curr_day['active_users'] - prev_day['active_users']
        new_users_change = curr_day['new_users'] - prev_day['new_users']
        quiz_change = curr_day['quiz_attempts'] - prev_day['quiz_attempts']
        messages_change = curr_day['estimated_messages'] - prev_day['estimated_messages']
        
        print(f"   {curr_day['date']} vs {prev_day['date']}:")
        print(f"     活躍用戶: {active_users_change:+d} 人 ({active_users_change/prev_day['active_users']*100:+.1f}%)")
        print(f"     新註冊用戶: {new_users_change:+d} 人 ({new_users_change/prev_day['new_users']*100:+.1f}%)")
        print(f"     答題次數: {quiz_change:+d} 次 ({quiz_change/prev_day['quiz_attempts']*100:+.1f}%)")
        print(f"     訊息數: {messages_change:+d} 則 ({messages_change/prev_day['estimated_messages']*100:+.1f}%)")
        print()
    
    # 計算平均值
    avg_active_users = total_active_users / 3
    avg_new_users = total_new_users / 3
    avg_quiz_attempts = total_quiz_attempts / 3
    avg_messages = total_messages / 3
    avg_questions_per_user = total_quiz_attempts / total_active_users if total_active_users > 0 else 0
    
    print("💡 用戶行為洞察:")
    print(f"   • 平均每日活躍用戶: {avg_active_users:.1f} 人")
    print(f"   • 平均每日新註冊用戶: {avg_new_users:.1f} 人")
    print(f"   • 平均每日答題次數: {avg_quiz_attempts:.1f} 次")
    print(f"   • 平均每日訊息數: {avg_messages:.1f} 則")
    print(f"   • 平均每用戶答題數: {avg_questions_per_user:.1f} 題")
    print(f"   • 平均每用戶訊息數: {total_messages / total_active_users:.1f} 則")
    print()
    
    # 用戶參與度分析
    print("📊 用戶參與度分析:")
    
    # 計算每日參與度
    participation_rates = []
    for day_data in three_days_data:
        if day_data['active_users'] > 0:
            rate = day_data['quiz_attempts'] / day_data['active_users']
            participation_rates.append(rate)
            print(f"   • {day_data['date']}: {rate:.1f} 題/人")
    
    avg_participation_rate = sum(participation_rates) / len(participation_rates) if participation_rates else 0
    print(f"   • 平均參與度: {avg_participation_rate:.1f} 題/人")
    print()
    
    # 新用戶留存分析
    print("🔄 新用戶留存分析:")
    total_returning_users = total_active_users - total_new_users
    if total_new_users > 0:
        retention_rate = total_returning_users / total_new_users * 100
        print(f"   • 新用戶總數: {total_new_users} 人")
        print(f"   • 回訪用戶數: {total_returning_users} 人")
        print(f"   • 留存率: {retention_rate:.1f}%")
    print()
    
    # 活躍度評估
    print("📈 活躍度評估:")
    if avg_active_users >= 50:
        activity_level = "高活躍"
    elif avg_active_users >= 30:
        activity_level = "中等活躍"
    else:
        activity_level = "低活躍"
    
    if avg_questions_per_user >= 2:
        engagement_level = "高參與"
    elif avg_questions_per_user >= 1:
        engagement_level = "中等參與"
    else:
        engagement_level = "低參與"
    
    print(f"   • 整體活躍度: {activity_level}")
    print(f"   • 用戶參與度: {engagement_level}")
    print(f"   • 新用戶增長: {'穩定' if avg_new_users >= 20 else '需要提升'}")
    print()
    
    # 關鍵發現
    print("🔍 關鍵發現:")
    
    # 找出最高和最低的數據
    max_active_day = max(three_days_data, key=lambda x: x['active_users'])
    min_active_day = min(three_days_data, key=lambda x: x['active_users'])
    max_quiz_day = max(three_days_data, key=lambda x: x['quiz_attempts'])
    min_quiz_day = min(three_days_data, key=lambda x: x['quiz_attempts'])
    
    print(f"   • 最活躍的一天: {max_active_day['date']} ({max_active_day['active_users']} 人)")
    print(f"   • 最不活躍的一天: {min_active_day['date']} ({min_active_day['active_users']} 人)")
    print(f"   • 答題最多的一天: {max_quiz_day['date']} ({max_quiz_day['quiz_attempts']} 次)")
    print(f"   • 答題最少的一天: {min_quiz_day['date']} ({min_quiz_day['quiz_attempts']} 次)")
    print()
    
    # 趨勢判斷
    print("📊 趨勢判斷:")
    if three_days_data[-1]['active_users'] > three_days_data[0]['active_users']:
        trend = "上升趨勢"
    elif three_days_data[-1]['active_users'] < three_days_data[0]['active_users']:
        trend = "下降趨勢"
    else:
        trend = "穩定趨勢"
    
    print(f"   • 活躍用戶趨勢: {trend}")
    
    if three_days_data[-1]['quiz_attempts'] > three_days_data[0]['quiz_attempts']:
        quiz_trend = "上升趨勢"
    elif three_days_data[-1]['quiz_attempts'] < three_days_data[0]['quiz_attempts']:
        quiz_trend = "下降趨勢"
    else:
        quiz_trend = "穩定趨勢"
    
    print(f"   • 答題活動趨勢: {quiz_trend}")
    print()
    
    # 建議
    print("🎯 建議:")
    if avg_active_users < 50:
        print("   • 需要增加用戶獲取和留存策略")
    if avg_questions_per_user < 2:
        print("   • 需要提升用戶參與度和答題動機")
    if avg_new_users < 20:
        print("   • 需要加強新用戶引導和推廣")
    
    if trend == "下降趨勢":
        print("   • 需要分析用戶流失原因並採取對應措施")
    elif trend == "上升趨勢":
        print("   • 繼續保持現有策略，考慮擴大規模")
    
    print("   • 持續監控用戶行為變化")
    print("   • 優化用戶體驗以提升滿意度")
    print("   • 建立用戶反饋機制")
    
    return {
        'three_days_data': three_days_data,
        'summary': {
            'total_active_users': total_active_users,
            'total_new_users': total_new_users,
            'total_quiz_attempts': total_quiz_attempts,
            'total_messages': total_messages,
            'avg_active_users': avg_active_users,
            'avg_new_users': avg_new_users,
            'avg_quiz_attempts': avg_quiz_attempts,
            'avg_messages': avg_messages,
            'avg_questions_per_user': avg_questions_per_user,
            'activity_level': activity_level,
            'engagement_level': engagement_level,
            'trend': trend,
            'quiz_trend': quiz_trend
        }
    }

def main():
    """主函數"""
    analysis_result = analyze_three_days_behavior()
    
    # 保存詳細報告
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"three_days_behavior_final_{timestamp}.json"
    
    report_data = {
        'analysis_date_range': '2025-09-22 to 2025-09-24',
        'analysis_time': datetime.datetime.now().isoformat(),
        'analysis_result': analysis_result
    }
    
    with open(report_filename, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 詳細分析報告已保存至: {report_filename}")
    print("\n🎉 三天用戶行為分析完成！")

if __name__ == "__main__":
    main()





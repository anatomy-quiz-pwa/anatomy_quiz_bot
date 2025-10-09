#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析等級1且低活動量（<5則訊息）用戶的行為模式
"""

import os
from datetime import datetime, timedelta
from supabase import create_client, Client
import logging
import json

# 設置日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Supabase 設定
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://ciqlfqfgzqqgdrogedxg.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA')

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    logger.info("✅ Supabase 連接成功")
except Exception as e:
    logger.error(f"❌ Supabase 連接失敗: {e}")
    exit(1)

def get_level1_low_activity_users():
    """獲取等級1且低活動量的用戶"""
    try:
        # 查詢等級1的用戶統計
        stats_response = supabase.table('user_stats').select('*').eq('level', 1).order('last_update', desc=True).execute()
        
        # 篩選出低活動量用戶（總答題數 < 5）
        low_activity_users = []
        for user in stats_response.data:
            total_answers = user.get('correct', 0) + user.get('wrong', 0)
            if total_answers < 5:
                user['total_answers'] = total_answers
                low_activity_users.append(user)
        
        logger.info(f"📊 找到 {len(low_activity_users)} 個等級1低活動量用戶")
        return low_activity_users
        
    except Exception as e:
        logger.error(f"❌ 獲取等級1低活動量用戶失敗: {e}")
        return []

def get_user_details(user_id):
    """獲取用戶詳細信息"""
    try:
        response = supabase.table('users').select('*').eq('line_user_id', user_id).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]
        return None
    except:
        return None

def categorize_user_behavior(user_stats, user_details):
    """分析用戶行為模式"""
    correct = user_stats.get('correct', 0)
    wrong = user_stats.get('wrong', 0)
    total_answers = correct + wrong
    level = user_stats.get('level', 1)
    correct_in_level = user_stats.get('correct_in_level', 0)
    last_update = user_stats.get('last_update', '')
    
    # 註冊時間
    created_at = user_details.get('created_at', '') if user_details else ''
    nickname = user_details.get('game_nickname', '未設置') if user_details else '未設置'
    
    # 行為分類
    behavior_type = "未知"
    behavior_description = ""
    
    if total_answers == 0:
        behavior_type = "純註冊用戶"
        behavior_description = "只註冊但未答題"
    elif total_answers == 1:
        if correct == 1:
            behavior_type = "一題即走(成功)"
            behavior_description = "答對1題後離開"
        else:
            behavior_type = "一題即走(失敗)"
            behavior_description = "答錯1題後離開"
    elif total_answers == 2:
        if correct >= 1:
            behavior_type = "淺嘗試用戶"
            behavior_description = f"答了2題，{correct}對{wrong}錯"
        else:
            behavior_type = "受挫用戶"
            behavior_description = "連答2題都錯，可能受挫離開"
    elif total_answers <= 4:
        accuracy = (correct / total_answers) * 100 if total_answers > 0 else 0
        if accuracy >= 75:
            behavior_type = "謹慎探索用戶"
            behavior_description = f"少量答題但準確率高({accuracy:.1f}%)"
        elif accuracy >= 50:
            behavior_type = "普通探索用戶"  
            behavior_description = f"少量答題，準確率一般({accuracy:.1f}%)"
        else:
            behavior_type = "困難用戶"
            behavior_description = f"少量答題但準確率低({accuracy:.1f}%)，可能覺得太難"
    
    # 時間分析
    time_analysis = ""
    if created_at and last_update:
        try:
            created = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            updated = datetime.fromisoformat(last_update.replace('Z', '+00:00'))
            time_diff = updated - created
            
            if time_diff.days == 0:
                if time_diff.seconds < 300:  # 5分鐘內
                    time_analysis = "快速離開(5分鐘內)"
                elif time_diff.seconds < 1800:  # 30分鐘內
                    time_analysis = "短暫體驗(30分鐘內)"
                else:
                    time_analysis = "當日體驗"
            elif time_diff.days == 1:
                time_analysis = "隔日再訪"
            else:
                time_analysis = f"多日使用({time_diff.days}天)"
        except:
            time_analysis = "時間分析失敗"
    
    return {
        'behavior_type': behavior_type,
        'behavior_description': behavior_description,
        'time_analysis': time_analysis,
        'accuracy': (correct / total_answers) * 100 if total_answers > 0 else 0
    }

def analyze_level1_low_activity():
    """分析等級1低活動量用戶"""
    print("🔍 等級1低活動量用戶行為分析")
    print("=" * 80)
    
    # 獲取用戶數據
    low_activity_users = get_level1_low_activity_users()
    
    if not low_activity_users:
        print("❌ 沒有找到符合條件的用戶")
        return
    
    print(f"\n📊 找到 {len(low_activity_users)} 個等級1低活動量用戶 (答題數 < 5)")
    
    # 行為統計
    behavior_stats = {}
    time_stats = {}
    detailed_analysis = []
    
    print(f"\n📋 詳細用戶行為分析:")
    print(f"{'序號':<4} {'用戶ID':<20} {'暱稱':<15} {'答對':<4} {'答錯':<4} {'行為類型':<15} {'時間模式':<15}")
    print("-" * 100)
    
    for i, user_stats in enumerate(low_activity_users, 1):
        user_id = user_stats.get('user_id', 'Unknown')
        correct = user_stats.get('correct', 0)
        wrong = user_stats.get('wrong', 0)
        
        # 獲取用戶詳細信息
        user_details = get_user_details(user_id)
        nickname = user_details.get('game_nickname', '未設置') if user_details else '未設置'
        if not nickname or nickname == '未設置':
            nickname = f"用戶{i}"
        
        # 分析行為
        behavior = categorize_user_behavior(user_stats, user_details)
        
        # 統計
        behavior_type = behavior['behavior_type']
        time_analysis = behavior['time_analysis']
        
        behavior_stats[behavior_type] = behavior_stats.get(behavior_type, 0) + 1
        time_stats[time_analysis] = time_stats.get(time_analysis, 0) + 1
        
        # 隱藏部分用戶ID
        masked_id = user_id[:8] + "..." + user_id[-4:] if len(user_id) > 12 else user_id
        
        print(f"{i:<4} {masked_id:<20} {nickname:<15} {correct:<4} {wrong:<4} {behavior_type:<15} {time_analysis:<15}")
        
        # 保存詳細分析
        detailed_analysis.append({
            'user_id': user_id,
            'nickname': nickname,
            'correct': correct,
            'wrong': wrong,
            'total_answers': correct + wrong,
            'accuracy': behavior['accuracy'],
            'behavior_type': behavior_type,
            'behavior_description': behavior['behavior_description'],
            'time_analysis': time_analysis,
            'created_at': user_details.get('created_at', '') if user_details else '',
            'last_update': user_stats.get('last_update', '')
        })
    
    # 行為模式統計
    print(f"\n📈 行為模式統計:")
    print("-" * 50)
    for behavior_type, count in sorted(behavior_stats.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / len(low_activity_users)) * 100
        print(f"   {behavior_type:<20}: {count:>3} 人 ({percentage:>5.1f}%)")
    
    # 時間模式統計
    print(f"\n⏰ 時間模式統計:")
    print("-" * 50)
    for time_pattern, count in sorted(time_stats.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / len(low_activity_users)) * 100
        print(f"   {time_pattern:<20}: {count:>3} 人 ({percentage:>5.1f}%)")
    
    # 深度分析
    print(f"\n🔍 深度行為分析:")
    print("-" * 50)
    
    # 0題用戶分析
    zero_answer_users = [u for u in detailed_analysis if u['total_answers'] == 0]
    print(f"📌 純註冊用戶 ({len(zero_answer_users)} 人):")
    print(f"   - 可能原因: 介面不清楚、不知道如何開始、或只是好奇註冊")
    
    # 1題用戶分析
    one_answer_users = [u for u in detailed_analysis if u['total_answers'] == 1]
    one_correct = len([u for u in one_answer_users if u['correct'] == 1])
    one_wrong = len([u for u in one_answer_users if u['wrong'] == 1])
    print(f"📌 一題即走用戶 ({len(one_answer_users)} 人):")
    print(f"   - 答對後離開: {one_correct} 人 (可能覺得太簡單或滿足了)")
    print(f"   - 答錯後離開: {one_wrong} 人 (可能覺得太難或受挫)")
    
    # 2-4題用戶分析
    multi_answer_users = [u for u in detailed_analysis if 2 <= u['total_answers'] <= 4]
    high_accuracy = len([u for u in multi_answer_users if u['accuracy'] >= 75])
    medium_accuracy = len([u for u in multi_answer_users if 50 <= u['accuracy'] < 75])
    low_accuracy = len([u for u in multi_answer_users if u['accuracy'] < 50])
    
    print(f"📌 多題探索用戶 ({len(multi_answer_users)} 人):")
    print(f"   - 高準確率 (≥75%): {high_accuracy} 人 (可能在觀望或時間不夠)")
    print(f"   - 中準確率 (50-74%): {medium_accuracy} 人 (正常學習曲線)")
    print(f"   - 低準確率 (<50%): {low_accuracy} 人 (可能覺得太困難)")
    
    # 時間行為分析
    quick_exit = len([u for u in detailed_analysis if u['time_analysis'] == '快速離開(5分鐘內)'])
    short_experience = len([u for u in detailed_analysis if u['time_analysis'] == '短暫體驗(30分鐘內)'])
    
    print(f"\n⚡ 用戶留存分析:")
    print(f"   - 快速離開 (5分鐘內): {quick_exit} 人 - 需要改善首次體驗")
    print(f"   - 短暫體驗 (30分鐘內): {short_experience} 人 - 需要增加黏性")
    
    # 改善建議
    print(f"\n💡 改善建議:")
    print("-" * 50)
    print("1. 針對純註冊用戶:")
    print("   - 加強歡迎引導流程")
    print("   - 提供清晰的開始按鈕和說明")
    print("   - 考慮發送引導訊息")
    
    print("2. 針對一題即走用戶:")
    print("   - 答對用戶: 提供鼓勵和進階挑戰")
    print("   - 答錯用戶: 提供解釋和鼓勵再試")
    print("   - 加入解題提示功能")
    
    print("3. 針對多題探索用戶:")
    print("   - 提供進度追蹤和成就系統")
    print("   - 增加社交元素 (排行榜、好友)")
    print("   - 優化題目難度曲線")
    
    print("4. 針對快速離開用戶:")
    print("   - 簡化初始操作流程")
    print("   - 提供更好的視覺引導")
    print("   - 考慮推送提醒功能")
    
    # 保存分析結果
    analysis_result = {
        'analysis_date': datetime.now().isoformat(),
        'total_low_activity_users': len(low_activity_users),
        'behavior_statistics': behavior_stats,
        'time_pattern_statistics': time_stats,
        'detailed_user_analysis': detailed_analysis
    }
    
    filename = f'level1_low_activity_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(analysis_result, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 詳細分析結果已保存到: {filename}")
    print("=" * 80)

if __name__ == "__main__":
    analyze_level1_low_activity()

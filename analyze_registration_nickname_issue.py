#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析純註冊用戶的暱稱設置情況和可能的系統延遲問題
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

def get_zero_answer_users():
    """獲取答題數為0的用戶"""
    try:
        # 查詢答題數為0的用戶統計
        stats_response = supabase.table('user_stats').select('*').eq('correct', 0).eq('wrong', 0).execute()
        
        logger.info(f"📊 找到 {len(stats_response.data)} 個零答題用戶")
        return stats_response.data
        
    except Exception as e:
        logger.error(f"❌ 獲取零答題用戶失敗: {e}")
        return []

def get_user_details_batch(user_ids):
    """批量獲取用戶詳細信息"""
    try:
        # 批量查詢用戶信息
        response = supabase.table('users').select('*').in_('line_user_id', user_ids).execute()
        
        # 建立用戶ID到用戶信息的映射
        user_map = {}
        for user in response.data:
            user_map[user['line_user_id']] = user
        
        logger.info(f"📊 獲取到 {len(user_map)} 個用戶的詳細信息")
        return user_map
        
    except Exception as e:
        logger.error(f"❌ 批量獲取用戶詳細信息失敗: {e}")
        return {}

def analyze_nickname_and_timing():
    """分析暱稱設置和時間模式"""
    print("🔍 純註冊用戶暱稱設置和系統延遲分析")
    print("=" * 80)
    
    # 獲取零答題用戶
    zero_answer_users = get_zero_answer_users()
    
    if not zero_answer_users:
        print("❌ 沒有找到零答題用戶")
        return
    
    print(f"\n📊 找到 {len(zero_answer_users)} 個零答題用戶")
    
    # 獲取用戶ID列表
    user_ids = [user.get('user_id') for user in zero_answer_users]
    
    # 批量獲取用戶詳細信息
    user_details_map = get_user_details_batch(user_ids)
    
    # 分析數據
    nickname_analysis = {
        'has_nickname': 0,
        'no_nickname': 0,
        'nickname_users': [],
        'no_nickname_users': []
    }
    
    timing_analysis = {
        'same_day_registration': 0,
        'old_registrations': 0,
        'recent_registrations': 0,  # 最近3天
        'timing_details': []
    }
    
    system_delay_indicators = {
        'quick_nickname_setup': 0,  # 註冊後很快設置暱稱但沒答題
        'potential_system_issues': [],
        'normal_abandonment': 0
    }
    
    print(f"\n📋 詳細分析:")
    print(f"{'序號':<4} {'用戶ID':<20} {'暱稱':<15} {'註冊時間':<20} {'最後更新':<20} {'分析':<20}")
    print("-" * 110)
    
    now = datetime.now()
    recent_threshold = now - timedelta(days=3)
    
    for i, user_stats in enumerate(zero_answer_users, 1):
        user_id = user_stats.get('user_id', 'Unknown')
        last_update = user_stats.get('last_update', '')
        
        # 獲取用戶詳細信息
        user_details = user_details_map.get(user_id, {})
        nickname = user_details.get('game_nickname', '')
        created_at = user_details.get('created_at', '')
        
        # 暱稱分析
        has_nickname = bool(nickname and nickname.strip() and nickname != '未設置')
        if has_nickname:
            nickname_analysis['has_nickname'] += 1
            nickname_analysis['nickname_users'].append({
                'user_id': user_id,
                'nickname': nickname,
                'created_at': created_at,
                'last_update': last_update
            })
        else:
            nickname_analysis['no_nickname'] += 1
            nickname_analysis['no_nickname_users'].append({
                'user_id': user_id,
                'created_at': created_at,
                'last_update': last_update
            })
        
        # 時間分析
        analysis_note = ""
        if created_at:
            try:
                created_time = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                
                if created_time > recent_threshold:
                    timing_analysis['recent_registrations'] += 1
                    analysis_note = "最近註冊"
                else:
                    timing_analysis['old_registrations'] += 1
                    analysis_note = "較早註冊"
                
                # 檢查是否為同日註冊和最後更新
                if last_update:
                    try:
                        last_update_time = datetime.fromisoformat(last_update.replace('Z', '+00:00'))
                        if created_time.date() == last_update_time.date():
                            timing_analysis['same_day_registration'] += 1
                            
                            # 檢查系統延遲指標
                            time_diff = last_update_time - created_time
                            if has_nickname and time_diff.total_seconds() > 300:  # 5分鐘後設置暱稱但沒答題
                                system_delay_indicators['quick_nickname_setup'] += 1
                                system_delay_indicators['potential_system_issues'].append({
                                    'user_id': user_id,
                                    'nickname': nickname,
                                    'created_at': created_at,
                                    'last_update': last_update,
                                    'time_diff_minutes': time_diff.total_seconds() / 60,
                                    'issue_type': '設置暱稱但未答題'
                                })
                                analysis_note += " (可能系統問題)"
                            elif not has_nickname:
                                system_delay_indicators['normal_abandonment'] += 1
                                analysis_note += " (正常放棄)"
                    except:
                        pass
                
                timing_analysis['timing_details'].append({
                    'user_id': user_id,
                    'nickname': nickname,
                    'has_nickname': has_nickname,
                    'created_at': created_at,
                    'last_update': last_update,
                    'analysis': analysis_note
                })
                
            except:
                analysis_note = "時間解析失敗"
        
        # 隱藏部分用戶ID
        masked_id = user_id[:8] + "..." + user_id[-4:] if len(user_id) > 12 else user_id
        display_nickname = nickname if nickname else "未設置"
        
        print(f"{i:<4} {masked_id:<20} {display_nickname:<15} {created_at[:19] if created_at else 'N/A':<20} {last_update[:19] if last_update else 'N/A':<20} {analysis_note:<20}")
    
    # 統計結果
    print(f"\n📈 暱稱設置統計:")
    print("-" * 50)
    nickname_percentage = (nickname_analysis['has_nickname'] / len(zero_answer_users)) * 100
    print(f"   有設置暱稱: {nickname_analysis['has_nickname']} 人 ({nickname_percentage:.1f}%)")
    print(f"   未設置暱稱: {nickname_analysis['no_nickname']} 人 ({100-nickname_percentage:.1f}%)")
    
    print(f"\n⏰ 時間模式統計:")
    print("-" * 50)
    print(f"   最近3天註冊: {timing_analysis['recent_registrations']} 人")
    print(f"   較早註冊: {timing_analysis['old_registrations']} 人")
    print(f"   同日註冊和更新: {timing_analysis['same_day_registration']} 人")
    
    print(f"\n🚨 系統延遲指標分析:")
    print("-" * 50)
    print(f"   設置暱稱但未答題: {system_delay_indicators['quick_nickname_setup']} 人")
    print(f"   正常放棄用戶: {system_delay_indicators['normal_abandonment']} 人")
    
    # 深度分析
    print(f"\n🔍 深度分析:")
    print("-" * 50)
    
    if nickname_analysis['has_nickname'] > 0:
        print(f"📌 有暱稱但未答題用戶 ({nickname_analysis['has_nickname']} 人):")
        print("   這些用戶花時間設置了暱稱，顯示有使用意圖")
        
        if system_delay_indicators['quick_nickname_setup'] > 0:
            print(f"   其中 {system_delay_indicators['quick_nickname_setup']} 人可能遇到系統問題:")
            for issue in system_delay_indicators['potential_system_issues'][:5]:  # 顯示前5個
                print(f"     - {issue['nickname']}: 註冊後 {issue['time_diff_minutes']:.1f} 分鐘設置暱稱但未收到題目")
        
        print("   可能原因:")
        print("     1. 系統未能及時推送第一道題目")
        print("     2. 用戶不知道如何開始答題")
        print("     3. 介面缺乏明確的'開始答題'指引")
    
    if nickname_analysis['no_nickname'] > 0:
        print(f"📌 無暱稱且未答題用戶 ({nickname_analysis['no_nickname']} 人):")
        print("   這些用戶可能:")
        print("     1. 只是好奇註冊，沒有真正使用意圖")
        print("     2. 在設置暱稱階段就放棄了")
        print("     3. 不理解需要設置暱稱才能開始")
    
    # 系統問題診斷
    print(f"\n🔧 系統問題診斷:")
    print("-" * 50)
    
    potential_system_issues = len(system_delay_indicators['potential_system_issues'])
    if potential_system_issues > 0:
        issue_rate = (potential_system_issues / nickname_analysis['has_nickname']) * 100 if nickname_analysis['has_nickname'] > 0 else 0
        print(f"⚠️  潛在系統問題用戶: {potential_system_issues} 人")
        print(f"   佔有暱稱用戶比例: {issue_rate:.1f}%")
        
        if issue_rate > 30:
            print("🚨 警告: 系統可能存在題目推送延遲問題!")
            print("   建議檢查:")
            print("   1. Webhook 響應時間")
            print("   2. 題目推送邏輯")
            print("   3. LINE API 調用是否成功")
        elif issue_rate > 15:
            print("⚠️  注意: 可能存在輕微的系統延遲")
            print("   建議優化用戶引導流程")
        else:
            print("✅ 系統延遲問題不嚴重")
            print("   主要是用戶引導問題")
    
    # 改善建議
    print(f"\n💡 改善建議:")
    print("-" * 50)
    
    if nickname_analysis['has_nickname'] > nickname_analysis['no_nickname']:
        print("1. 重點優化系統響應:")
        print("   - 檢查暱稱設置後的題目推送邏輯")
        print("   - 確保 Webhook 及時響應")
        print("   - 添加'開始答題'按鈕或指引")
    else:
        print("1. 重點優化用戶引導:")
        print("   - 簡化註冊流程")
        print("   - 強化暱稱設置的必要性說明")
        print("   - 提供清晰的操作指引")
    
    print("2. 通用改善:")
    print("   - 發送歡迎訊息包含操作指南")
    print("   - 添加'如何開始'的幫助功能")
    print("   - 實施用戶引導檢查點")
    
    # 保存分析結果
    analysis_result = {
        'analysis_date': datetime.now().isoformat(),
        'total_zero_answer_users': len(zero_answer_users),
        'nickname_analysis': nickname_analysis,
        'timing_analysis': timing_analysis,
        'system_delay_indicators': system_delay_indicators
    }
    
    filename = f'registration_nickname_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(analysis_result, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 詳細分析結果已保存到: {filename}")
    print("=" * 80)

if __name__ == "__main__":
    analyze_nickname_and_timing()

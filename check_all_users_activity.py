#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查看所有用戶活動統計
"""

import os
from datetime import datetime, timedelta
from supabase import create_client, Client
import logging

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

def get_recent_users(days=7):
    """獲取最近幾天的用戶"""
    try:
        # 獲取最近 N 天的日期範圍
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        logger.info(f"🔍 查詢最近 {days} 天的用戶: {start_date} 到 {end_date}")
        
        # 查詢最近創建的用戶
        users_response = supabase.table('users').select(
            'line_user_id', 'game_nickname', 'created_at', 'is_admin', 'test_mode'
        ).gte('created_at', start_date.isoformat()).order('created_at', desc=True).execute()
        
        logger.info(f"📊 找到 {len(users_response.data)} 個最近 {days} 天的用戶記錄")
        return users_response.data
        
    except Exception as e:
        logger.error(f"❌ 獲取最近用戶失敗: {e}")
        return []

def get_all_user_stats():
    """獲取所有用戶統計"""
    try:
        stats_response = supabase.table('user_stats').select('*').order('last_update', desc=True).execute()
        logger.info(f"📊 獲取到 {len(stats_response.data)} 個用戶的統計數據")
        return stats_response.data
    except Exception as e:
        logger.error(f"❌ 獲取用戶統計失敗: {e}")
        return []

def get_user_nickname_from_db(user_id):
    """從資料庫獲取用戶暱稱"""
    try:
        response = supabase.table('users').select('game_nickname').eq('line_user_id', user_id).execute()
        if response.data and len(response.data) > 0:
            return response.data[0].get('game_nickname', '未設置')
        return '未設置'
    except:
        return '未設置'

def estimate_messages_sent(user_stats):
    """估算用戶發送的訊息數量"""
    try:
        correct = user_stats.get('correct', 0)
        wrong = user_stats.get('wrong', 0)
        total_answers = correct + wrong
        
        # 保守估計每個答題動作對應1.5則訊息
        estimated_messages = int(total_answers * 1.5)
        
        # 如果用戶有其他活動，再加一些
        if user_stats.get('level', 1) > 1:
            estimated_messages += 2  # 升級相關訊息
            
        return estimated_messages
    except:
        return 0

def analyze_all_activity():
    """分析所有用戶活動"""
    print("🔍 LINE Bot 用戶活動總覽")
    print("=" * 60)
    
    # 1. 獲取最近7天的新用戶
    recent_users = get_recent_users(7)
    today_users = [u for u in recent_users if u.get('created_at', '').startswith(datetime.now().strftime('%Y-%m-%d'))]
    
    print(f"\n📅 今天新加入用戶: {len(today_users)} 人")
    print(f"📅 最近7天新加入用戶: {len(recent_users)} 人")
    
    if today_users:
        print(f"\n👥 今天的新用戶:")
        for i, user in enumerate(today_users, 1):
            user_id = user.get('line_user_id', 'Unknown')
            nickname = user.get('game_nickname', '未設置')
            created_at = user.get('created_at', 'Unknown')
            
            # 隱藏部分用戶ID
            masked_id = user_id[:8] + "..." + user_id[-8:] if len(user_id) > 16 else user_id
            print(f"   {i}. ID: {masked_id}, 暱稱: {nickname}, 時間: {created_at}")
    
    if recent_users and not today_users:
        print(f"\n👥 最近7天的新用戶 (前10個):")
        for i, user in enumerate(recent_users[:10], 1):
            user_id = user.get('line_user_id', 'Unknown')
            nickname = user.get('game_nickname', '未設置')
            created_at = user.get('created_at', 'Unknown')
            
            # 隱藏部分用戶ID
            masked_id = user_id[:8] + "..." + user_id[-8:] if len(user_id) > 16 else user_id
            print(f"   {i}. ID: {masked_id}, 暱稱: {nickname}, 時間: {created_at}")
    
    # 2. 獲取所有用戶統計
    all_stats = get_all_user_stats()
    
    if all_stats:
        print(f"\n📊 所有用戶統計 (共 {len(all_stats)} 人):")
        
        # 今天有活動的用戶
        today_str = datetime.now().strftime('%Y-%m-%d')
        today_active = [s for s in all_stats if s.get('last_update', '').startswith(today_str)]
        
        print(f"   今天有活動: {len(today_active)} 人")
        
        if today_active:
            total_estimated_messages = 0
            print(f"\n💬 今天活躍用戶詳情:")
            print(f"{'序號':<4} {'用戶ID':<20} {'暱稱':<15} {'答對':<6} {'答錯':<6} {'等級':<6} {'估計訊息':<8}")
            print("-" * 80)
            
            for i, user_stats in enumerate(today_active, 1):
                user_id = user_stats.get('user_id', 'Unknown')
                correct = user_stats.get('correct', 0)
                wrong = user_stats.get('wrong', 0)
                level = user_stats.get('level', 1)
                
                # 獲取暱稱
                nickname = get_user_nickname_from_db(user_id)
                if not nickname or nickname == '未設置':
                    nickname = f"用戶{i}"
                
                # 估算發送的訊息數量
                estimated_messages = estimate_messages_sent(user_stats)
                total_estimated_messages += estimated_messages
                
                # 隱藏部分用戶ID
                masked_id = user_id[:8] + "..." + user_id[-4:] if len(user_id) > 12 else user_id
                
                print(f"{i:<4} {masked_id:<20} {nickname:<15} {correct:<6} {wrong:<6} {level:<6} {estimated_messages:<8}")
            
            print("-" * 80)
            print(f"今天估計總訊息數: {total_estimated_messages} 則")
        
        # 整體統計
        print(f"\n📈 整體統計:")
        total_questions = sum(s.get('correct', 0) + s.get('wrong', 0) for s in all_stats)
        total_correct = sum(s.get('correct', 0) for s in all_stats)
        total_wrong = sum(s.get('wrong', 0) for s in all_stats)
        
        print(f"   總用戶數: {len(all_stats)} 人")
        print(f"   總答題數: {total_questions} 題")
        print(f"   總答對數: {total_correct} 題")
        print(f"   總答錯數: {total_wrong} 題")
        print(f"   整體準確率: {(total_correct/max(total_questions,1)*100):.1f}%")
        
        # 活躍度分析
        high_activity = [s for s in all_stats if (s.get('correct', 0) + s.get('wrong', 0)) >= 20]
        medium_activity = [s for s in all_stats if 5 <= (s.get('correct', 0) + s.get('wrong', 0)) < 20]
        low_activity = [s for s in all_stats if (s.get('correct', 0) + s.get('wrong', 0)) < 5]
        
        print(f"\n🎯 活躍度分析:")
        print(f"   高活躍用戶 (≥20題): {len(high_activity)} 人")
        print(f"   中活躍用戶 (5-19題): {len(medium_activity)} 人")
        print(f"   低活躍用戶 (<5題): {len(low_activity)} 人")
        
        # 等級分佈
        level_distribution = {}
        for s in all_stats:
            level = s.get('level', 1)
            level_distribution[level] = level_distribution.get(level, 0) + 1
        
        print(f"\n🏆 等級分佈:")
        for level in sorted(level_distribution.keys()):
            count = level_distribution[level]
            print(f"   等級 {level}: {count} 人")
    
    print("=" * 60)

if __name__ == "__main__":
    analyze_all_activity()

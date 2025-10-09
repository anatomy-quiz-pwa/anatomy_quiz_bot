#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查看昨天的用戶活動統計
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

def get_yesterday_active_users():
    """獲取昨天有活動的用戶"""
    try:
        # 獲取昨天的日期範圍
        yesterday = datetime.now() - timedelta(days=1)
        yesterday_start = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday_end = yesterday_start + timedelta(days=1)
        
        logger.info(f"🔍 查詢昨天的活動: {yesterday_start} 到 {yesterday_end}")
        
        # 查詢昨天更新的用戶統計
        stats_response = supabase.table('user_stats').select('*').gte(
            'last_update', yesterday_start.isoformat()
        ).lt('last_update', yesterday_end.isoformat()).execute()
        
        logger.info(f"📊 找到 {len(stats_response.data)} 個昨天有活動的用戶")
        return stats_response.data
        
    except Exception as e:
        logger.error(f"❌ 獲取昨天活動用戶失敗: {e}")
        return []

def get_yesterday_new_users():
    """獲取昨天新加入的用戶"""
    try:
        # 獲取昨天的日期範圍
        yesterday = datetime.now() - timedelta(days=1)
        yesterday_start = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday_end = yesterday_start + timedelta(days=1)
        
        # 查詢昨天創建的用戶
        users_response = supabase.table('users').select(
            'line_user_id', 'game_nickname', 'created_at', 'is_admin', 'test_mode'
        ).gte('created_at', yesterday_start.isoformat()).lt('created_at', yesterday_end.isoformat()).execute()
        
        logger.info(f"📊 找到 {len(users_response.data)} 個昨天新加入的用戶")
        return users_response.data
        
    except Exception as e:
        logger.error(f"❌ 獲取昨天新用戶失敗: {e}")
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

def analyze_yesterday_activity():
    """分析昨天的用戶活動"""
    yesterday_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    print(f"🔍 LINE Bot 昨天 ({yesterday_date}) 用戶活動分析")
    print("=" * 60)
    
    # 1. 獲取昨天新加入的用戶
    new_users = get_yesterday_new_users()
    print(f"\n📅 昨天新加入用戶: {len(new_users)} 人")
    
    if new_users:
        print(f"\n👥 昨天新用戶詳情:")
        for i, user in enumerate(new_users, 1):
            user_id = user.get('line_user_id', 'Unknown')
            nickname = user.get('game_nickname', '未設置')
            created_at = user.get('created_at', 'Unknown')
            is_admin = user.get('is_admin', False)
            test_mode = user.get('test_mode', False)
            
            # 隱藏部分用戶ID
            masked_id = user_id[:8] + "..." + user_id[-8:] if len(user_id) > 16 else user_id
            
            print(f"   {i}. ID: {masked_id}")
            print(f"      暱稱: {nickname}")
            print(f"      加入時間: {created_at}")
            print(f"      管理員: {'是' if is_admin else '否'}")
            print(f"      測試模式: {'是' if test_mode else '否'}")
            print()
    
    # 2. 獲取昨天有活動的用戶
    active_users = get_yesterday_active_users()
    print(f"📊 昨天有活動的用戶: {len(active_users)} 人")
    
    if active_users:
        total_estimated_messages = 0
        print(f"\n💬 昨天活躍用戶統計:")
        print(f"{'序號':<4} {'用戶ID':<20} {'暱稱':<15} {'答對':<6} {'答錯':<6} {'等級':<6} {'估計訊息':<8}")
        print("-" * 80)
        
        for i, user_stats in enumerate(active_users, 1):
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
        print(f"昨天估計總訊息數: {total_estimated_messages} 則")
        
        # 活動統計
        print(f"\n📈 昨天活動統計:")
        if len(active_users) > 0:
            avg_messages_per_user = total_estimated_messages / len(active_users)
            print(f"   平均每用戶訊息數: {avg_messages_per_user:.1f} 則")
            
            # 按活動程度分類
            high_activity = [u for u in active_users if estimate_messages_sent(u) >= 10]
            medium_activity = [u for u in active_users if 5 <= estimate_messages_sent(u) < 10]
            low_activity = [u for u in active_users if estimate_messages_sent(u) < 5]
            
            print(f"   高活躍用戶 (≥10則): {len(high_activity)} 人")
            print(f"   中活躍用戶 (5-9則): {len(medium_activity)} 人")
            print(f"   低活躍用戶 (<5則): {len(low_activity)} 人")
        
        print(f"\n💡 分析結論:")
        print(f"   - 昨天有 {len(active_users)} 位用戶與 Bot 互動")
        print(f"   - 新加入用戶: {len(new_users)} 人")
        print(f"   - 估計產生 {total_estimated_messages} 則用戶訊息")
        print(f"   - Bot 需要回覆這些訊息（回覆不計入配額）")
        print(f"   - 配額主要用於主動推送（如升級通知、排行榜等）")
    
    print("=" * 60)

if __name__ == "__main__":
    analyze_yesterday_activity()

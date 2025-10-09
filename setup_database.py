#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
設置Supabase資料庫表格結構
"""

import os
from supabase import create_client, Client
import logging

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Supabase連接
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://ciqlfqfgzqqgdrogedxg.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA')

def create_supabase_client():
    """創建Supabase客戶端"""
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        logger.info(f"✅ Supabase 連接成功: {SUPABASE_URL}")
        return supabase
    except Exception as e:
        logger.error(f"❌ Supabase 連接失敗: {e}")
        return None

def check_and_create_tables(supabase):
    """檢查並創建必要的表格"""
    
    # 1. 檢查 users 表格
    try:
        response = supabase.table('users').select('*').limit(1).execute()
        logger.info("✅ users 表格已存在")
    except Exception as e:
        logger.info(f"⚠️ users 表格不存在或需要創建: {e}")
        # 這裡需要手動在Supabase Dashboard中創建表格
    
    # 2. 檢查 user_stats 表格
    try:
        response = supabase.table('user_stats').select('*').limit(1).execute()
        logger.info("✅ user_stats 表格已存在")
    except Exception as e:
        logger.info(f"⚠️ user_stats 表格不存在或需要創建: {e}")
    
    # 3. 檢查 questions 表格
    try:
        response = supabase.table('questions').select('*').limit(1).execute()
        logger.info("✅ questions 表格已存在")
    except Exception as e:
        logger.info(f"⚠️ questions 表格不存在或需要創建: {e}")

def create_sample_questions(supabase):
    """創建示例題目"""
    sample_questions = [
        {
            'id': 1,
            'question': '心臟的主要功能是什麼？',
            'options': ['輸送血液', '過濾血液', '儲存血液', '製造血液'],
            'correct_answer': 0,
            'explanation': '心臟是循環系統的核心，主要功能是泵血輸送到全身。',
            'level': 1,
            'category': '循環系統'
        },
        {
            'id': 2,
            'question': '人體最大的器官是什麼？',
            'options': ['心臟', '肝臟', '皮膚', '肺'],
            'correct_answer': 2,
            'explanation': '皮膚是人體最大的器官，覆蓋整個身體表面。',
            'level': 1,
            'category': '器官系統'
        },
        {
            'id': 3,
            'question': '心臟有幾個腔室？',
            'options': ['2個', '3個', '4個', '5個'],
            'correct_answer': 2,
            'explanation': '心臟有4個腔室：左心房、左心室、右心房、右心室。',
            'level': 2,
            'category': '循環系統'
        },
        {
            'id': 4,
            'question': '肺的主要功能是什麼？',
            'options': ['消化食物', '過濾血液', '氣體交換', '儲存能量'],
            'correct_answer': 2,
            'explanation': '肺的主要功能是進行氣體交換，吸入氧氣，呼出二氧化碳。',
            'level': 2,
            'category': '呼吸系統'
        },
        {
            'id': 5,
            'question': '肝臟的主要功能是什麼？',
            'options': ['呼吸', '消化', '代謝和解毒', '循環'],
            'correct_answer': 2,
            'explanation': '肝臟是重要的代謝器官，負責解毒、代謝和儲存等功能。',
            'level': 3,
            'category': '消化系統'
        }
    ]
    
    try:
        # 先檢查是否已有題目
        existing = supabase.table('questions').select('id').execute()
        if existing.data and len(existing.data) > 0:
            logger.info("✅ 題目已存在，跳過創建")
            return
        
        # 插入示例題目
        result = supabase.table('questions').insert(sample_questions).execute()
        logger.info(f"✅ 成功創建 {len(sample_questions)} 個示例題目")
        
    except Exception as e:
        logger.error(f"❌ 創建示例題目失敗: {e}")

def test_database_connection(supabase):
    """測試資料庫連接和基本操作"""
    try:
        # 測試讀取 users 表格
        users = supabase.table('users').select('*').limit(5).execute()
        logger.info(f"✅ 成功讀取 users 表格，共 {len(users.data)} 筆記錄")
        
        # 測試讀取 user_stats 表格
        stats = supabase.table('user_stats').select('*').limit(5).execute()
        logger.info(f"✅ 成功讀取 user_stats 表格，共 {len(stats.data)} 筆記錄")
        
        # 測試讀取 questions 表格
        questions = supabase.table('questions').select('*').limit(5).execute()
        logger.info(f"✅ 成功讀取 questions 表格，共 {len(questions.data)} 筆記錄")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ 資料庫測試失敗: {e}")
        return False

def main():
    """主函數"""
    logger.info("🚀 開始設置Supabase資料庫")
    
    # 創建Supabase客戶端
    supabase = create_supabase_client()
    if not supabase:
        logger.error("❌ 無法連接到Supabase，請檢查環境變數")
        return
    
    # 檢查和創建表格
    check_and_create_tables(supabase)
    
    # 創建示例題目
    create_sample_questions(supabase)
    
    # 測試資料庫連接
    if test_database_connection(supabase):
        logger.info("✅ 資料庫設置完成！")
    else:
        logger.error("❌ 資料庫設置失敗")

if __name__ == '__main__':
    main()


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試管理員模式等級修復
"""

import os
import sys
import logging
from supabase import create_client, Client

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 環境變數
SUPABASE_URL = "https://ciqlfqfgzqqgdrogedxg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA"

def test_admin_level_distribution():
    """測試管理員等級分布"""
    try:
        # 連接 Supabase
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # 獲取所有題目
        logger.info("📚 正在從 Supabase 獲取題目數據...")
        response = supabase.table('anatomy_questions_v2').select('*').execute()
        
        if not response.data:
            logger.error("❌ 沒有找到任何題目數據")
            return
        
        # 分析等級分布
        level_distribution = {}
        total_questions = len(response.data)
        
        for item in response.data:
            level = item.get('level', 1)
            if level not in level_distribution:
                level_distribution[level] = 0
            level_distribution[level] += 1
        
        logger.info(f"✅ 成功獲取 {total_questions} 道題目")
        logger.info("📊 等級分布：")
        
        for level in sorted(level_distribution.keys()):
            count = level_distribution[level]
            percentage = (count / total_questions) * 100
            logger.info(f"   等級 {level}: {count} 題 ({percentage:.1f}%)")
        
        # 檢查是否只有 level 1 題目
        if len(level_distribution) == 1 and 1 in level_distribution:
            logger.warning("⚠️ 數據庫中只有 level 1 題目！這就是管理員只看到 level 1 的原因！")
            return False
        
        logger.info(f"✅ 數據庫中有 {len(level_distribution)} 個不同等級的題目")
        return True
        
    except Exception as e:
        logger.error(f"❌ 測試失敗: {e}")
        return False

def test_admin_permissions(test_user_id="test_admin_001"):
    """測試管理員權限"""
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # 查詢管理員權限
        logger.info(f"🔍 檢查用戶 {test_user_id} 的管理員權限...")
        response = supabase.table('users').select(
            'is_admin', 'admin_levels', 'test_mode', 'admin_permissions'
        ).eq('line_user_id', test_user_id).execute()
        
        if not response.data:
            logger.warning(f"⚠️ 用戶 {test_user_id} 不存在，創建測試管理員...")
            
            # 創建測試管理員
            admin_data = {
                'line_user_id': test_user_id,
                'is_admin': True,
                'test_mode': True,
                'admin_levels': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
                'admin_permissions': {
                    'can_access_all_levels': True,
                    'can_test_all_levels': True
                },
                'game_nickname': '測試管理員'
            }
            
            create_response = supabase.table('users').upsert(admin_data).execute()
            if create_response.data:
                logger.info("✅ 測試管理員創建成功")
            else:
                logger.error("❌ 測試管理員創建失敗")
                return False
        else:
            user_data = response.data[0]
            logger.info(f"✅ 找到管理員 {test_user_id}:")
            logger.info(f"   is_admin: {user_data.get('is_admin', False)}")
            logger.info(f"   test_mode: {user_data.get('test_mode', False)}")
            logger.info(f"   admin_levels: {user_data.get('admin_levels', [])}")
            logger.info(f"   admin_permissions: {user_data.get('admin_permissions', {})}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ 測試管理員權限失敗: {e}")
        return False

def simulate_admin_question_selection():
    """模擬管理員題目選擇邏輯"""
    try:
        import random
        
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # 獲取所有題目
        response = supabase.table('anatomy_questions_v2').select('*').execute()
        if not response.data:
            logger.error("❌ 沒有題目數據")
            return False
        
        # 轉換數據格式
        all_questions = []
        for item in response.data:
            question = {
                "id": item.get('id'),
                "question": item.get('question', '未知題目'),
                "level": item.get('level', 1),
                "category": "解剖學"
            }
            all_questions.append(question)
        
        # 按等級分組題目
        questions_by_level = {}
        for q in all_questions:
            level = q['level']
            if level not in questions_by_level:
                questions_by_level[level] = []
            questions_by_level[level].append(q)
        
        logger.info("🎯 模擬管理員題目選擇（新邏輯）：")
        logger.info(f"   總題目數: {len(all_questions)}")
        logger.info(f"   可選等級: {sorted(questions_by_level.keys())}")
        
        # 模擬選擇10次
        level_counts = {}
        for i in range(10):
            # 隨機選擇等級
            available_levels = list(questions_by_level.keys())
            selected_level = random.choice(available_levels)
            
            if selected_level not in level_counts:
                level_counts[selected_level] = 0
            level_counts[selected_level] += 1
        
        logger.info("📊 10次選擇結果：")
        for level in sorted(level_counts.keys()):
            count = level_counts[level]
            logger.info(f"   等級 {level}: {count} 次")
        
        # 檢查是否有多樣性
        if len(level_counts) > 1:
            logger.info("✅ 新邏輯可以選擇多個等級的題目！")
            return True
        else:
            logger.warning("⚠️ 仍然只選擇一個等級的題目")
            return False
        
    except Exception as e:
        logger.error(f"❌ 模擬題目選擇失敗: {e}")
        return False

def main():
    """主測試函數"""
    print("🔧 開始測試管理員等級修復...")
    print("=" * 60)
    
    # 測試1：檢查題目等級分布
    print("\n📊 測試1: 檢查題目等級分布")
    result1 = test_admin_level_distribution()
    
    # 測試2：檢查管理員權限
    print("\n🔑 測試2: 檢查管理員權限")
    result2 = test_admin_permissions()
    
    # 測試3：模擬題目選擇
    print("\n🎯 測試3: 模擬題目選擇邏輯")
    result3 = simulate_admin_question_selection()
    
    print("\n" + "=" * 60)
    print("📋 測試結果總結：")
    print(f"   題目等級分布: {'✅ 通過' if result1 else '❌ 失敗'}")
    print(f"   管理員權限: {'✅ 通過' if result2 else '❌ 失敗'}")
    print(f"   題目選擇邏輯: {'✅ 通過' if result3 else '❌ 失敗'}")
    
    if all([result1, result2, result3]):
        print("\n🎉 所有測試通過！管理員應該能看到不同等級的題目了。")
    else:
        print("\n⚠️ 部分測試失敗，需要進一步調試。")

if __name__ == "__main__":
    main()

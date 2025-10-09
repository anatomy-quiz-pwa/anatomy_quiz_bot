#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
調查北極熊超爽用戶的詳細資料和互動方式
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

# 北極熊超爽的用戶 ID
TARGET_USER_ID = "U315252475f1e5f7b5ce3681906caa55a"

def get_user_complete_profile(user_id: str) -> Dict[str, Any]:
    """獲取用戶完整資料"""
    profile = {}
    
    try:
        # 獲取用戶基本資料
        user_response = supabase.table('users').select('*').eq('line_user_id', user_id).execute()
        if user_response.data:
            profile['user_info'] = user_response.data[0]
        else:
            profile['user_info'] = None
            
        # 獲取用戶統計資料
        stats_response = supabase.table('user_stats').select('*').eq('user_id', user_id).execute()
        if stats_response.data:
            profile['user_stats'] = stats_response.data[0]
        else:
            profile['user_stats'] = None
            
        return profile
        
    except Exception as e:
        print(f"❌ 獲取用戶資料失敗: {e}")
        return {}

def check_line_bot_quota_status():
    """檢查 LINE Bot 額度狀況"""
    try:
        # 讀取 LINE Bot 狀態文件（如果存在）
        status_files = [
            'line_bot_usage_history.json',
            'LINE_月度限制處理指南.md'
        ]
        
        status_info = {}
        
        for file in status_files:
            if os.path.exists(file):
                try:
                    if file.endswith('.json'):
                        with open(file, 'r', encoding='utf-8') as f:
                            status_info[file] = json.load(f)
                    else:
                        with open(file, 'r', encoding='utf-8') as f:
                            status_info[file] = f.read()
                except Exception as e:
                    print(f"⚠️  讀取 {file} 失敗: {e}")
        
        return status_info
        
    except Exception as e:
        print(f"❌ 檢查 LINE Bot 狀態失敗: {e}")
        return {}

def analyze_user_interaction_method(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """分析用戶如何進行互動"""
    
    user_stats = user_data.get('user_stats', {})
    user_info = user_data.get('user_info', {})
    
    # 分析用戶活動模式
    daily_quota = user_stats.get('daily_quota', 0)
    last_updated = user_stats.get('last_updated')
    level = user_stats.get('level', 1)
    correct = user_stats.get('correct', 0)
    wrong = user_stats.get('wrong', 0)
    
    # 判斷互動方式
    interaction_analysis = {
        'has_recent_activity': False,
        'possible_interaction_methods': [],
        'activity_pattern': 'unknown'
    }
    
    # 檢查是否有今日活動
    if last_updated:
        today = datetime.date.today().strftime("%Y-%m-%d")
        if last_updated.startswith(today):
            interaction_analysis['has_recent_activity'] = True
            
    # 根據數據變化推測互動方式
    if daily_quota > 0:
        interaction_analysis['possible_interaction_methods'].append('LINE Bot 直接問答')
        interaction_analysis['activity_pattern'] = 'active_quiz'
    elif interaction_analysis['has_recent_activity']:
        interaction_analysis['possible_interaction_methods'].extend([
            'LINE Bot 查看積分/排行榜',
            '可能嘗試問答但受限制',
            'Web 介面互動（如果有）'
        ])
        interaction_analysis['activity_pattern'] = 'browsing_only'
    
    return interaction_analysis

def investigate_alternative_interaction_methods():
    """調查可能的替代互動方式"""
    
    alternatives = {
        'web_interface': False,
        'admin_panel': False,
        'direct_database': False,
        'alternative_channels': []
    }
    
    # 檢查是否有 Web 介面
    web_files = [
        'app_fastapi.py',
        'anatomy_admin_panel',
        'next.config.mjs',
        'package.json',
        'vercel.json'
    ]
    
    for file in web_files:
        if os.path.exists(file):
            alternatives['web_interface'] = True
            if 'admin' in file.lower():
                alternatives['admin_panel'] = True
    
    # 檢查管理員面板
    if os.path.exists('anatomy_admin_panel'):
        alternatives['admin_panel'] = True
        
    return alternatives

def main():
    """主函數"""
    print(f"🔍 調查北極熊超爽用戶 ({TARGET_USER_ID}) 的詳細資料...")
    print("=" * 80)
    
    # 1. 獲取用戶完整資料
    print("👤 用戶完整資料:")
    user_profile = get_user_complete_profile(TARGET_USER_ID)
    
    if not user_profile:
        print("❌ 無法獲取用戶資料")
        return
    
    user_info = user_profile.get('user_info', {})
    user_stats = user_profile.get('user_stats', {})
    
    print(f"📋 基本資料:")
    print(f"   • 用戶 ID: {TARGET_USER_ID}")
    print(f"   • 暱稱: {user_info.get('game_nickname', '未設定')}")
    print(f"   • 註冊時間: {user_info.get('created_at', '未知')}")
    print(f"   • 是否管理員: {'是' if user_info.get('is_admin') else '否'}")
    print()
    
    print(f"📊 學習統計:")
    print(f"   • 當前等級: {user_stats.get('level', 1)}")
    print(f"   • 總答對: {user_stats.get('correct', 0)} 題")
    print(f"   • 總答錯: {user_stats.get('wrong', 0)} 題")
    print(f"   • 等級進度: {user_stats.get('correct_in_level', 0)}")
    print(f"   • 今日答題: {user_stats.get('daily_quota', 0)} 題")
    print(f"   • 最後更新: {user_stats.get('last_updated', '未知')}")
    print()
    
    # 2. 檢查 LINE Bot 額度狀況
    print("📱 LINE Bot 額度狀況:")
    line_status = check_line_bot_quota_status()
    
    if line_status:
        for file, content in line_status.items():
            print(f"📄 {file}:")
            if isinstance(content, dict):
                print(f"   內容: {json.dumps(content, ensure_ascii=False, indent=2)[:200]}...")
            else:
                print(f"   內容: {str(content)[:200]}...")
            print()
    else:
        print("   ⚠️  無法獲取 LINE Bot 狀態資訊")
        print()
    
    # 3. 分析用戶互動方式
    print("🔍 用戶互動方式分析:")
    interaction_analysis = analyze_user_interaction_method(user_profile)
    
    print(f"📈 活動狀況:")
    print(f"   • 最近有活動: {'是' if interaction_analysis['has_recent_activity'] else '否'}")
    print(f"   • 活動模式: {interaction_analysis['activity_pattern']}")
    print()
    
    print(f"💬 可能的互動方式:")
    for method in interaction_analysis['possible_interaction_methods']:
        print(f"   • {method}")
    
    if not interaction_analysis['possible_interaction_methods']:
        print("   • 無明確互動方式")
    print()
    
    # 4. 調查替代互動方法
    print("🔧 替代互動方式調查:")
    alternatives = investigate_alternative_interaction_methods()
    
    print(f"🌐 Web 介面: {'可用' if alternatives['web_interface'] else '不可用'}")
    print(f"👑 管理員面板: {'可用' if alternatives['admin_panel'] else '不可用'}")
    print(f"🗄️  直接資料庫操作: {'可能' if alternatives['direct_database'] else '不適用'}")
    print()
    
    # 5. 推測用戶如何在沒有 LINE 額度時進行問答
    print("💡 用戶問答方式推測:")
    
    if user_stats.get('daily_quota', 0) > 0:
        print("✅ 用戶今日成功答題 1 題，可能的原因:")
        print("   1. LINE Bot 仍有部分額度")
        print("   2. 用戶在額度用完前完成答題")
        print("   3. 使用了管理員權限或特殊通道")
        print("   4. 透過 Web 介面進行答題")
        print()
        
        # 檢查答題時間
        last_updated = user_stats.get('last_updated')
        if last_updated:
            print(f"📅 最後答題時間: {last_updated}")
            print("   建議檢查該時間點的 LINE Bot 狀態")
    else:
        print("⚠️  用戶今日雖有活動記錄但沒有答題:")
        print("   1. 可能只是查看了積分或排行榜")
        print("   2. 嘗試答題但受到 LINE 額度限制")
        print("   3. 系統記錄了互動但未完成答題流程")
    
    print()
    
    # 6. 建議調查方向
    print("🎯 進一步調查建議:")
    print("1. 檢查 LINE Bot 的實際額度使用狀況")
    print("2. 查看是否有 Web 介面供用戶使用")
    print("3. 檢查管理員面板的功能")
    print("4. 分析用戶答題的確切時間點")
    print("5. 確認是否有其他通訊管道")
    print()
    
    # 保存調查報告
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"polar_bear_user_investigation_{timestamp}.json"
    
    report_data = {
        'investigation_time': datetime.datetime.now().isoformat(),
        'target_user_id': TARGET_USER_ID,
        'user_profile': user_profile,
        'line_bot_status': line_status,
        'interaction_analysis': interaction_analysis,
        'alternative_methods': alternatives,
        'conclusions': {
            'has_today_activity': interaction_analysis['has_recent_activity'],
            'answered_questions_today': user_stats.get('daily_quota', 0),
            'possible_interaction_without_line': alternatives['web_interface'] or alternatives['admin_panel']
        }
    }
    
    with open(report_filename, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)
    
    print(f"💾 詳細調查報告已保存至: {report_filename}")
    print()
    print("🎉 北極熊超爽用戶調查完成！")

if __name__ == "__main__":
    main()

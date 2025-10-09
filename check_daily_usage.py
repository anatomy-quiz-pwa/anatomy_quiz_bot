#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LINE Bot 每日訊息用量監控腳本
"""

import os
import json
import requests
from datetime import datetime, timedelta
import logging

# 設置日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# LINE Bot 設定
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', 
    "AhZFgYWfEMeFSDxJJhzcvJoKx78lVrfRH3cqqusfiZhug/f5wRhQTkDD9fW7+IJLA3xpoQtunFWoVKnHtaE9p+U1QVFUz1o8CQ5AnNpPicjK32KAD5Z1ouF1HNKATv/BhUHIS3OjcndnUGpOqPDYKAdB04t89/1O/w1cDnyilFU=")

def get_quota_info():
    """獲取配額信息"""
    try:
        headers = {'Authorization': f'Bearer {LINE_CHANNEL_ACCESS_TOKEN}'}
        
        # 獲取總配額
        quota_response = requests.get('https://api.line.me/v2/bot/message/quota', headers=headers)
        quota_data = quota_response.json()
        
        # 獲取已使用配額
        consumption_response = requests.get('https://api.line.me/v2/bot/message/quota/consumption', headers=headers)
        consumption_data = consumption_response.json()
        
        return {
            'total_quota': quota_data.get('value', 0),
            'quota_type': quota_data.get('type', 'unknown'),
            'total_usage': consumption_data.get('totalUsage', 0)
        }
    except Exception as e:
        logger.error(f"獲取配額信息失敗: {e}")
        return None

def get_insight_data(date_str):
    """獲取特定日期的統計數據"""
    try:
        headers = {'Authorization': f'Bearer {LINE_CHANNEL_ACCESS_TOKEN}'}
        
        # 嘗試獲取訊息傳送統計
        delivery_url = f'https://api.line.me/v2/bot/insight/message/delivery?date={date_str}'
        delivery_response = requests.get(delivery_url, headers=headers)
        delivery_data = delivery_response.json()
        
        return delivery_data
    except Exception as e:
        logger.error(f"獲取 {date_str} 統計數據失敗: {e}")
        return None

def save_usage_history(data):
    """保存使用記錄到文件"""
    history_file = 'line_bot_usage_history.json'
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 讀取現有記錄
    history = {}
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
        except:
            history = {}
    
    # 添加今天的記錄
    history[today] = {
        'timestamp': datetime.now().isoformat(),
        'total_usage': data['total_usage'],
        'total_quota': data['total_quota'],
        'quota_type': data['quota_type'],
        'remaining': data['total_quota'] - data['total_usage']
    }
    
    # 保存記錄
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    
    return history

def calculate_daily_usage(history):
    """計算每日用量變化"""
    dates = sorted(history.keys())
    if len(dates) < 2:
        return None
    
    today = dates[-1]
    yesterday = dates[-2] if len(dates) >= 2 else None
    
    if yesterday:
        today_usage = history[today]['total_usage']
        yesterday_usage = history[yesterday]['total_usage']
        daily_increase = today_usage - yesterday_usage
        return daily_increase
    
    return None

def main():
    print("🤖 LINE Bot 訊息用量監控")
    print("=" * 50)
    
    # 獲取配額信息
    quota_info = get_quota_info()
    if not quota_info:
        print("❌ 無法獲取配額信息")
        return
    
    # 保存使用記錄
    history = save_usage_history(quota_info)
    
    # 計算每日用量
    daily_usage = calculate_daily_usage(history)
    
    # 顯示結果
    total_quota = quota_info['total_quota']
    total_usage = quota_info['total_usage']
    remaining = total_quota - total_usage
    usage_percentage = (total_usage / total_quota) * 100 if total_quota > 0 else 0
    
    print(f"📊 配額狀況:")
    print(f"   總配額: {total_quota:,} 則訊息")
    print(f"   已使用: {total_usage:,} 則訊息")
    print(f"   剩餘: {remaining:,} 則訊息")
    print(f"   使用率: {usage_percentage:.1f}%")
    print(f"   配額類型: {quota_info['quota_type']}")
    
    if daily_usage is not None:
        print(f"\n📈 今日用量變化:")
        if daily_usage > 0:
            print(f"   今日新增: +{daily_usage:,} 則訊息")
        elif daily_usage < 0:
            print(f"   配額已重置: {daily_usage:,} 則訊息")
        else:
            print(f"   今日新增: 0 則訊息")
    
    # 警告提示
    if remaining <= 0:
        print("\n⚠️  警告: 配額已用完！")
        print("   - 無法主動推送訊息")
        print("   - 仍可回覆用戶訊息")
        print("   - 下月初會自動重置")
    elif remaining < 500:
        print(f"\n⚠️  警告: 配額不足 ({remaining} 則剩餘)")
        print("   建議優化訊息發送策略")
    
    # 嘗試獲取今天的詳細統計
    today_str = datetime.now().strftime('%Y%m%d')
    yesterday_str = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
    
    print(f"\n🔍 嘗試獲取詳細統計...")
    
    # 今天的統計
    today_insight = get_insight_data(today_str)
    if today_insight and today_insight.get('status') != 'unready':
        print(f"📅 今天 ({today_str}) 統計: {json.dumps(today_insight, ensure_ascii=False, indent=2)}")
    else:
        print(f"📅 今天 ({today_str}) 統計: 數據尚未準備好")
    
    # 昨天的統計
    yesterday_insight = get_insight_data(yesterday_str)
    if yesterday_insight and yesterday_insight.get('status') != 'unready':
        print(f"📅 昨天 ({yesterday_str}) 統計: {json.dumps(yesterday_insight, ensure_ascii=False, indent=2)}")
    else:
        print(f"📅 昨天 ({yesterday_str}) 統計: 數據尚未準備好")
    
    print(f"\n💾 使用記錄已保存到: line_bot_usage_history.json")
    print("=" * 50)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
實際測試積分訊息發送功能
測試從Supabase抓取數據並發送Flex Message到LINE
"""

import os
import sys
import json
import requests
from supabase import create_client, Client
from typing import Optional, Dict, Any

# 設定環境變數
SUPABASE_URL = "https://ciqlfqfgzqqgdrogedxg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA"

# LINE設定
LINE_CHANNEL_ACCESS_TOKEN = "AhZFgYWfEMeFSDxJJhzcvJoKx78lVrfRH3cqqusfiZhug/f5wRhQTkDD9fW7+IJLA3xpoQtunFWoVKnHtaE9p+U1QVFUz1o8CQ5AnNpPicjK32KAD5Z1ouF1HNKATv/BhUHIS3OjcndnUGpOqPDYKAdB04t89/1O/w1cDnyilFU="

# 測試用戶ID（使用寶的帳號進行測試）
TEST_USER_ID = "U977c24d1fec3a2bf07035504e1444911"

def create_supabase_client():
    """創建Supabase客戶端"""
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"❌ 創建Supabase客戶端失敗: {e}")
        return None

def get_user_stats(supabase: Client, user_id: str) -> Optional[dict]:
    """獲取用戶統計資料"""
    try:
        response = supabase.table('user_stats').select('*').eq('user_id', user_id).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        print(f"❌ 獲取用戶統計失敗: {e}")
        return None

def get_user_nickname(supabase: Client, user_id: str) -> str:
    """獲取用戶暱稱"""
    try:
        response = supabase.table('users').select('game_nickname').eq('line_user_id', user_id).execute()
        
        if response.data and len(response.data) > 0:
            nickname = response.data[0].get('game_nickname')
            if nickname:
                return nickname
        
        return f"用戶{user_id[-4:]}"
        
    except Exception as e:
        print(f"❌ 獲取暱稱失敗: {e}")
        return f"用戶{user_id[-4:]}"

def create_score_flex_message(user_stats: dict, nickname: str) -> dict:
    """創建積分的 Flex Message"""
    try:
        correct_answers = user_stats.get('correct', 0)
        wrong_answers = user_stats.get('wrong', 0)
        level = user_stats.get('level', 1)
        correct_in_level = user_stats.get('correct_in_level', 0)
        
        # 計算總題數和準確率
        total_questions = correct_answers + wrong_answers
        accuracy = round((correct_answers / max(total_questions, 1)) * 100, 1)
        
        # 根據等級設定顏色主題
        if level >= 10:
            header_color = "#FFD700"  # 金色
            bg_color = "#FFFACD"      # 淺金色
            level_emoji = "👑"
        elif level >= 5:
            header_color = "#4169E1"  # 皇家藍
            bg_color = "#F0F8FF"      # 愛麗絲藍
            level_emoji = "⭐"
        else:
            header_color = "#32CD32"  # 萊姆綠
            bg_color = "#F0FFF0"      # 蜜露綠
            level_emoji = "🌟"
        
        # 創建進度條
        progress_percentage = min((correct_in_level / max(level * 5, 1)) * 100, 100)
        progress_bar = "█" * int(progress_percentage / 10) + "░" * (10 - int(progress_percentage / 10))
        
        flex_message = {
            "type": "flex",
            "altText": f"📊 {nickname} 的遊戲積分",
            "contents": {
                "type": "bubble",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": f"📊 {nickname} 的遊戲積分",
                            "weight": "bold",
                            "size": "lg",
                            "color": "#FFFFFF",
                            "align": "center"
                        },
                        {
                            "type": "text",
                            "text": f"{level_emoji} 等級 {level} 學習者",
                            "size": "sm",
                            "color": "#FFFFFF",
                            "align": "center",
                            "margin": "sm"
                        }
                    ],
                    "backgroundColor": header_color,
                    "paddingAll": "lg",
                    "cornerRadius": "10px"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "✅ 答對題數",
                                    "size": "sm",
                                    "color": "#666666",
                                    "flex": 2
                                },
                                {
                                    "type": "text",
                                    "text": f"{correct_answers} 題",
                                    "weight": "bold",
                                    "size": "sm",
                                    "color": "#28a745",
                                    "align": "end",
                                    "flex": 1
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "❌ 答錯題數",
                                    "size": "sm",
                                    "color": "#666666",
                                    "flex": 2
                                },
                                {
                                    "type": "text",
                                    "text": f"{wrong_answers} 題",
                                    "weight": "bold",
                                    "size": "sm",
                                    "color": "#dc3545",
                                    "align": "end",
                                    "flex": 1
                                }
                            ],
                            "margin": "md"
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "🎯 準確率",
                                    "size": "sm",
                                    "color": "#666666",
                                    "flex": 2
                                },
                                {
                                    "type": "text",
                                    "text": f"{accuracy}%",
                                    "weight": "bold",
                                    "size": "sm",
                                    "color": "#17a2b8",
                                    "align": "end",
                                    "flex": 1
                                }
                            ],
                            "margin": "md"
                        },
                        {
                            "type": "separator",
                            "margin": "lg"
                        },
                        {
                            "type": "text",
                            "text": f"📈 本級進度：{correct_in_level} 題",
                            "size": "sm",
                            "color": "#333333",
                            "margin": "lg"
                        },
                        {
                            "type": "text",
                            "text": progress_bar,
                            "size": "xs",
                            "color": "#666666",
                            "margin": "sm"
                        }
                    ],
                    "backgroundColor": bg_color,
                    "paddingAll": "lg",
                    "spacing": "sm"
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "🚀 繼續挑戰",
                                "text": "開始"
                            },
                            "style": "primary",
                            "color": header_color
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "🏆 查看排行榜",
                                "text": "排行榜"
                            },
                            "style": "secondary"
                        }
                    ],
                    "spacing": "sm",
                    "paddingAll": "lg"
                }
            }
        }
        
        return flex_message
        
    except Exception as e:
        print(f"❌ 創建積分 Flex Message 失敗: {e}")
        return None

def send_line_message(user_id: str, message: dict) -> bool:
    """發送LINE訊息"""
    try:
        url = "https://api.line.me/v2/bot/message/push"
        headers = {
            "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "to": user_id,
            "messages": [message]
        }
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            print("✅ 訊息發送成功")
            return True
        else:
            print(f"❌ 訊息發送失敗: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 發送LINE訊息時發生錯誤: {e}")
        return False

def test_score_message_flow():
    """測試完整的積分訊息流程"""
    print("🚀 開始測試積分訊息發送流程")
    print("="*60)
    
    # 1. 創建Supabase客戶端
    print("1️⃣ 連接Supabase...")
    supabase = create_supabase_client()
    if not supabase:
        print("❌ 無法連接Supabase，測試終止")
        return False
    print("✅ Supabase連接成功")
    
    # 2. 獲取用戶數據
    print(f"\n2️⃣ 獲取用戶數據 (User ID: {TEST_USER_ID})...")
    user_stats = get_user_stats(supabase, TEST_USER_ID)
    
    if not user_stats:
        print("❌ 無法獲取用戶統計數據")
        return False
    
    print("✅ 成功獲取用戶統計數據:")
    print(f"   - 答對題數: {user_stats.get('correct', 0)}")
    print(f"   - 答錯題數: {user_stats.get('wrong', 0)}")
    print(f"   - 當前等級: {user_stats.get('level', 1)}")
    print(f"   - 本級答對: {user_stats.get('correct_in_level', 0)}")
    
    # 3. 獲取暱稱
    print("\n3️⃣ 獲取用戶暱稱...")
    nickname = get_user_nickname(supabase, TEST_USER_ID)
    print(f"✅ 用戶暱稱: {nickname}")
    
    # 4. 創建Flex Message
    print("\n4️⃣ 創建積分Flex Message...")
    flex_message = create_score_flex_message(user_stats, nickname)
    
    if not flex_message:
        print("❌ 創建Flex Message失敗")
        return False
    
    print("✅ 成功創建Flex Message")
    
    # 5. 保存Flex Message到檔案供檢查
    print("\n5️⃣ 保存Flex Message到檔案...")
    try:
        with open("live_score_flex_message.json", "w", encoding="utf-8") as f:
            json.dump(flex_message, f, ensure_ascii=False, indent=2)
        print("✅ Flex Message已保存至: live_score_flex_message.json")
    except Exception as e:
        print(f"⚠️ 保存Flex Message失敗: {e}")
    
    # 6. 發送到LINE
    print("\n6️⃣ 發送Flex Message到LINE...")
    success = send_line_message(TEST_USER_ID, flex_message)
    
    if success:
        print("✅ 積分訊息已成功發送到LINE！")
        print(f"📱 請檢查LINE用戶 {nickname} 是否收到積分訊息")
    else:
        print("❌ 發送積分訊息失敗")
        return False
    
    # 7. 測試備用文字訊息
    print("\n7️⃣ 測試備用文字訊息...")
    
    correct_answers = user_stats.get('correct', 0)
    wrong_answers = user_stats.get('wrong', 0)
    level = user_stats.get('level', 1)
    correct_in_level = user_stats.get('correct_in_level', 0)
    
    score_text = f"""📊 {nickname} 的遊戲積分

🏆 當前等級：第 {level} 級
✅ 答對題數：{correct_answers} 題
❌ 答錯題數：{wrong_answers} 題
📈 本級答對：{correct_in_level} 題

💡 提示：每答對 3 題即可升級到下一等級！
輸入「開始」繼續挑戰，輸入「排行榜」查看排名。"""
    
    text_message = {"type": "text", "text": score_text}
    
    print("發送備用文字訊息...")
    backup_success = send_line_message(TEST_USER_ID, text_message)
    
    if backup_success:
        print("✅ 備用文字訊息發送成功")
    else:
        print("❌ 備用文字訊息發送失敗")
    
    print(f"\n{'='*60}")
    print("📊 測試完成總結")
    print(f"{'='*60}")
    print(f"✅ Flex Message發送: {'成功' if success else '失敗'}")
    print(f"✅ 文字訊息發送: {'成功' if backup_success else '失敗'}")
    print(f"📱 請檢查LINE用戶 {nickname} 的訊息")
    
    return success

if __name__ == "__main__":
    test_score_message_flow()

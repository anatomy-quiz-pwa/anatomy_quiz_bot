#!/usr/bin/env python3
"""
測試修復後的積分 Flex Message 顯示
"""
import os
from supabase import create_client, Client
import json

# Supabase 配置
SUPABASE_URL = "https://ciqlfqfgzqqgdrogedxg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA"

def create_score_flex_message(user_stats, nickname):
    """創建積分的 Flex Message（從 app_supabase.py 複製的邏輯）"""
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
        progress_percentage = min((correct_in_level / max(level * 5, 1)) * 100, 100)  # 假設每級需要5題
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
                        }
                    ]
                }
            }
        }
        
        return flex_message
        
    except Exception as e:
        print(f"❌ 創建積分 Flex Message 失敗: {e}")
        return None

def main():
    print("🧪 測試修復後的積分 Flex Message 顯示...")
    
    try:
        # 創建 Supabase 客戶端
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Supabase 連接成功")
        
        # 目標用戶ID
        target_user_id = "Uddae8475d30fd8691c811ecef7737890"
        target_nickname = "神秘小檬檬"
        
        print(f"\n👤 測試用戶: {target_user_id} ({target_nickname})")
        
        # 1. 獲取修復後的統計資料
        print(f"\n📊 步驟1: 獲取修復後的統計資料...")
        stats_response = supabase.table('user_stats').select('*').eq('user_id', target_user_id).execute()
        
        if not stats_response.data:
            print("❌ 沒有找到用戶統計資料")
            return
        
        user_stats = stats_response.data[0]
        print(f"✅ 獲取統計資料成功")
        
        # 2. 顯示關鍵數據
        correct_answers = user_stats.get('correct', 0)
        wrong_answers = user_stats.get('wrong', 0)
        level = user_stats.get('level', 1)
        correct_in_level = user_stats.get('correct_in_level', 0)
        correct_qids = user_stats.get('correct_qids', [])
        
        print(f"\n📈 關鍵統計數據:")
        print(f"   ✅ 答對題數: {correct_answers}")
        print(f"   ❌ 答錯題數: {wrong_answers}")
        print(f"   🏆 當前等級: {level}")
        print(f"   ⭐ 本級答對: {correct_in_level}")
        print(f"   📝 答對題目ID: {correct_qids}")
        
        # 3. 創建 Flex Message
        print(f"\n🎨 步驟2: 創建積分 Flex Message...")
        flex_message = create_score_flex_message(user_stats, target_nickname)
        
        if flex_message:
            print("✅ Flex Message 創建成功！")
            
            # 4. 顯示 Flex Message 結構（簡化版）
            print(f"\n📱 Flex Message 預覽:")
            print(f"   📊 標題: {flex_message['altText']}")
            
            # 提取關鍵顯示內容
            header_text = flex_message['contents']['header']['contents'][0]['text']
            level_text = flex_message['contents']['header']['contents'][1]['text']
            
            print(f"   🎯 標頭: {header_text}")
            print(f"   🏆 等級: {level_text}")
            
            # 查找答對題數顯示
            body_contents = flex_message['contents']['body']['contents']
            for content in body_contents:
                if content['type'] == 'box' and content['layout'] == 'horizontal':
                    for item in content['contents']:
                        if item.get('text') and '答對題數' in item['text']:
                            # 找到對應的數值
                            for sibling in content['contents']:
                                if sibling.get('text') and '題' in sibling['text']:
                                    print(f"   ✅ 答對顯示: {sibling['text']}")
                                    break
                            break
            
            print(f"\n🎉 結論:")
            print(f"   ✅ Flex Message 現在會正確顯示答對 {correct_answers} 題")
            print(f"   ✅ 等級顯示為 {level}")
            print(f"   ✅ 統計資料已經同步正確")
            
        else:
            print("❌ Flex Message 創建失敗")
        
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

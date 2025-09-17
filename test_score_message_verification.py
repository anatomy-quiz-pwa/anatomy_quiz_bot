#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
積分訊息驗證測試腳本
驗證積分的flex訊息是否正確從Supabase抓取相關資料
"""

import os
import sys
import json
from supabase import create_client, Client
from typing import Optional, Dict, Any

# 設定環境變數
SUPABASE_URL = "https://ciqlfqfgzqqgdrogedxg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA"

# 測試用戶ID（從記憶體中獲取）
TEST_USER_IDS = {
    "蘇的測試帳號": "U9a9df49945755ef651d067743f3c7ea7",
    "寶的測試帳號": "U977c24d1fec3a2bf07035504e1444911"
}

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
    """獲取用戶暱稱 - 從users表格的game_nickname欄位"""
    try:
        # 查詢 users 表格中的 game_nickname
        response = supabase.table('users').select('game_nickname').eq('line_user_id', user_id).execute()
        
        if response.data and len(response.data) > 0:
            nickname = response.data[0].get('game_nickname')
            if nickname:
                print(f"✅ 找到用戶暱稱: {nickname}")
                return nickname
        
        # 如果沒有找到暱稱，生成默認名稱
        print(f"⚠️ 用戶 {user_id} 沒有暱稱，使用默認名稱")
        return f"用戶{user_id[-4:]}"
        
    except Exception as e:
        print(f"❌ 獲取暱稱失敗: {e}")
        return f"用戶{user_id[-4:]}"

def create_score_flex_message(user_stats: dict, nickname: str) -> dict:
    """創建積分的 Flex Message - 複製自主程式"""
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
                }
            }
        }
        
        return flex_message
        
    except Exception as e:
        print(f"❌ 創建積分 Flex Message 失敗: {e}")
        return None

def validate_flex_message(flex_message: dict) -> tuple[bool, list]:
    """驗證Flex Message格式"""
    errors = []
    
    try:
        # 檢查基本結構
        if not isinstance(flex_message, dict):
            errors.append("Flex message 必須是字典格式")
            return False, errors
        
        if flex_message.get("type") != "flex":
            errors.append("消息類型必須是 'flex'")
        
        if "altText" not in flex_message:
            errors.append("缺少 altText 欄位")
        
        if "contents" not in flex_message:
            errors.append("缺少 contents 欄位")
            return False, errors
        
        contents = flex_message["contents"]
        
        # 檢查bubble結構
        if contents.get("type") != "bubble":
            errors.append("contents類型必須是 'bubble'")
        
        # 檢查header
        if "header" in contents:
            header = contents["header"]
            if header.get("type") != "box":
                errors.append("header類型必須是 'box'")
            if "contents" not in header:
                errors.append("header缺少contents")
        
        # 檢查body
        if "body" in contents:
            body = contents["body"]
            if body.get("type") != "box":
                errors.append("body類型必須是 'box'")
            if "contents" not in body:
                errors.append("body缺少contents")
        
        return len(errors) == 0, errors
        
    except Exception as e:
        errors.append(f"驗證過程發生錯誤: {e}")
        return False, errors

def test_user_score_message(supabase: Client, user_id: str, user_name: str):
    """測試單個用戶的積分訊息"""
    print(f"\n{'='*60}")
    print(f"🧪 測試用戶: {user_name} ({user_id})")
    print(f"{'='*60}")
    
    # 1. 獲取用戶統計數據
    print("1️⃣ 獲取用戶統計數據...")
    user_stats = get_user_stats(supabase, user_id)
    
    if not user_stats:
        print("❌ 無法獲取用戶統計數據")
        return False
    
    print("✅ 成功獲取用戶統計數據:")
    print(f"   - 答對題數: {user_stats.get('correct', 0)}")
    print(f"   - 答錯題數: {user_stats.get('wrong', 0)}")
    print(f"   - 當前等級: {user_stats.get('level', 1)}")
    print(f"   - 本級答對: {user_stats.get('correct_in_level', 0)}")
    
    # 2. 獲取用戶暱稱
    print("\n2️⃣ 獲取用戶暱稱...")
    nickname = get_user_nickname(supabase, user_id)
    print(f"✅ 用戶暱稱: {nickname}")
    
    # 3. 創建Flex Message
    print("\n3️⃣ 創建積分Flex Message...")
    flex_message = create_score_flex_message(user_stats, nickname)
    
    if not flex_message:
        print("❌ 創建Flex Message失敗")
        return False
    
    print("✅ 成功創建Flex Message")
    
    # 4. 驗證Flex Message格式
    print("\n4️⃣ 驗證Flex Message格式...")
    is_valid, errors = validate_flex_message(flex_message)
    
    if is_valid:
        print("✅ Flex Message格式驗證通過")
    else:
        print("❌ Flex Message格式驗證失敗:")
        for error in errors:
            print(f"   - {error}")
        return False
    
    # 5. 檢查數據一致性
    print("\n5️⃣ 檢查數據一致性...")
    
    # 從Flex Message中提取顯示的數據
    try:
        body_contents = flex_message["contents"]["body"]["contents"]
        
        # 找到答對題數
        correct_display = None
        wrong_display = None
        accuracy_display = None
        
        for content in body_contents:
            if content.get("type") == "box" and content.get("layout") == "horizontal":
                text_contents = content.get("contents", [])
                if len(text_contents) >= 2:
                    label_text = text_contents[0].get("text", "")
                    value_text = text_contents[1].get("text", "")
                    
                    if "答對題數" in label_text:
                        correct_display = int(value_text.replace(" 題", ""))
                    elif "答錯題數" in label_text:
                        wrong_display = int(value_text.replace(" 題", ""))
                    elif "準確率" in label_text:
                        accuracy_display = float(value_text.replace("%", ""))
        
        # 計算期望的準確率
        total_questions = user_stats.get('correct', 0) + user_stats.get('wrong', 0)
        expected_accuracy = round((user_stats.get('correct', 0) / max(total_questions, 1)) * 100, 1)
        
        # 驗證數據一致性
        consistency_errors = []
        
        if correct_display != user_stats.get('correct', 0):
            consistency_errors.append(f"答對題數不一致: DB={user_stats.get('correct', 0)}, Flex={correct_display}")
        
        if wrong_display != user_stats.get('wrong', 0):
            consistency_errors.append(f"答錯題數不一致: DB={user_stats.get('wrong', 0)}, Flex={wrong_display}")
        
        if abs(accuracy_display - expected_accuracy) > 0.1:
            consistency_errors.append(f"準確率不一致: 期望={expected_accuracy}%, Flex={accuracy_display}%")
        
        if consistency_errors:
            print("❌ 數據一致性檢查失敗:")
            for error in consistency_errors:
                print(f"   - {error}")
            return False
        else:
            print("✅ 數據一致性檢查通過")
    
    except Exception as e:
        print(f"❌ 數據一致性檢查過程發生錯誤: {e}")
        return False
    
    # 6. 保存測試結果
    print("\n6️⃣ 保存測試結果...")
    result_filename = f"score_flex_message_test_{user_name.replace('的測試帳號', '')}.json"
    try:
        with open(result_filename, 'w', encoding='utf-8') as f:
            json.dump({
                "user_id": user_id,
                "user_name": user_name,
                "user_stats": user_stats,
                "nickname": nickname,
                "flex_message": flex_message,
                "validation_result": {
                    "is_valid": is_valid,
                    "errors": errors
                },
                "test_timestamp": str(datetime.datetime.now())
            }, f, ensure_ascii=False, indent=2)
        print(f"✅ 測試結果已保存至: {result_filename}")
    except Exception as e:
        print(f"⚠️ 保存測試結果失敗: {e}")
    
    print(f"\n✅ 用戶 {user_name} 的積分訊息測試完成")
    return True

def main():
    """主測試函數"""
    print("🚀 開始積分訊息驗證測試")
    print("="*60)
    
    # 創建Supabase客戶端
    print("🔗 連接Supabase...")
    supabase = create_supabase_client()
    if not supabase:
        print("❌ 無法連接Supabase，測試終止")
        return
    
    print("✅ Supabase連接成功")
    
    # 測試所有用戶
    test_results = {}
    for user_name, user_id in TEST_USER_IDS.items():
        try:
            result = test_user_score_message(supabase, user_id, user_name)
            test_results[user_name] = result
        except Exception as e:
            print(f"❌ 測試用戶 {user_name} 時發生錯誤: {e}")
            test_results[user_name] = False
    
    # 總結測試結果
    print(f"\n{'='*60}")
    print("📊 測試總結")
    print(f"{'='*60}")
    
    passed_count = sum(1 for result in test_results.values() if result)
    total_count = len(test_results)
    
    print(f"✅ 測試通過: {passed_count}/{total_count}")
    
    for user_name, result in test_results.items():
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"   - {user_name}: {status}")
    
    if passed_count == total_count:
        print("\n🎉 所有測試都通過！積分訊息功能正常運作。")
    else:
        print(f"\n⚠️ 有 {total_count - passed_count} 個測試失敗，請檢查相關問題。")

if __name__ == "__main__":
    import datetime
    main()

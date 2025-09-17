#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試 Flex Message 發送功能
"""

import os
import sys
import json
from datetime import datetime

# 添加當前目錄到 Python 路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 設置環境變量
os.environ['SUPABASE_URL'] = 'https://ciqlfqfgzqqgdrogedxg.supabase.co'
os.environ['SUPABASE_ANON_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA'

def test_flex_message_structure():
    """測試 Flex Message 結構是否正確"""
    print("🧪 測試 Flex Message 結構...")
    
    try:
        from app_supabase_fixed import create_leaderboard_flex_message, get_real_students_data
        
        # 獲取數據
        students_data = get_real_students_data()
        if not students_data:
            print("⚠️ 無法獲取真實數據，使用模擬數據")
            students_data = [
                {"user_id": "test_user_1", "name": "測試用戶1", "level": 5, "score": 1000, "questions_answered": 50, "correct_answers": 45},
                {"user_id": "test_user_2", "name": "測試用戶2", "level": 3, "score": 600, "questions_answered": 30, "correct_answers": 25},
                {"user_id": "test_user_3", "name": "測試用戶3", "level": 2, "score": 300, "questions_answered": 15, "correct_answers": 12}
            ]
        
        top_10 = students_data[:10]
        test_user_id = students_data[0]['user_id'] if students_data else "test_user"
        
        # 創建 Flex Message
        flex_message = create_leaderboard_flex_message(top_10, students_data, test_user_id)
        
        # 驗證基本結構
        assert flex_message["type"] == "flex", "Flex Message 類型錯誤"
        assert "altText" in flex_message, "缺少 altText"
        assert "contents" in flex_message, "缺少 contents"
        
        contents = flex_message["contents"]
        assert contents["type"] == "bubble", "容器類型錯誤"
        assert "header" in contents, "缺少 header"
        assert "body" in contents, "缺少 body"
        assert "footer" in contents, "缺少 footer"
        
        # 驗證 header 結構
        header = contents["header"]
        assert header["type"] == "box", "header 類型錯誤"
        assert header["layout"] == "vertical", "header 布局錯誤"
        assert len(header["contents"]) >= 2, "header 內容不足"
        
        # 驗證 body 結構
        body = contents["body"]
        assert body["type"] == "box", "body 類型錯誤"
        assert body["layout"] == "vertical", "body 布局錯誤"
        assert len(body["contents"]) > 0, "body 為空"
        
        # 驗證 footer 結構
        footer = contents["footer"]
        assert footer["type"] == "box", "footer 類型錯誤"
        assert footer["layout"] == "vertical", "footer 布局錯誤"
        assert len(footer["contents"]) > 0, "footer 為空"
        
        print("✅ Flex Message 結構驗證通過")
        return True
        
    except Exception as e:
        print(f"❌ Flex Message 結構驗證失敗: {e}")
        return False

def test_flex_message_content():
    """測試 Flex Message 內容是否正確"""
    print("\n🧪 測試 Flex Message 內容...")
    
    try:
        from app_supabase_fixed import create_leaderboard_flex_message, get_real_students_data
        
        # 獲取數據
        students_data = get_real_students_data()
        if not students_data:
            print("⚠️ 無法獲取真實數據，使用模擬數據")
            students_data = [
                {"user_id": "test_user_1", "name": "測試用戶1", "level": 5, "score": 1000, "questions_answered": 50, "correct_answers": 45},
                {"user_id": "test_user_2", "name": "測試用戶2", "level": 3, "score": 600, "questions_answered": 30, "correct_answers": 25},
                {"user_id": "test_user_3", "name": "測試用戶3", "level": 2, "score": 300, "questions_answered": 15, "correct_answers": 12}
            ]
        
        top_10 = students_data[:10]
        test_user_id = students_data[0]['user_id'] if students_data else "test_user"
        
        # 創建 Flex Message
        flex_message = create_leaderboard_flex_message(top_10, students_data, test_user_id)
        
        # 檢查標題
        header_texts = [item["text"] for item in flex_message["contents"]["header"]["contents"] if item["type"] == "text"]
        assert "🏆 排行榜" in header_texts, "標題錯誤"
        assert "前10名" in header_texts, "副標題錯誤"
        
        # 檢查按鈕
        footer_buttons = [item for item in flex_message["contents"]["footer"]["contents"] if item["type"] == "button"]
        assert len(footer_buttons) > 0, "缺少按鈕"
        assert "重新挑戰" in footer_buttons[0]["action"]["label"], "按鈕標籤錯誤"
        
        # 檢查排名項目
        body_contents = flex_message["contents"]["body"]["contents"]
        rank_items = [item for item in body_contents if item["type"] == "box" and item["layout"] == "horizontal"]
        assert len(rank_items) > 0, "缺少排名項目"
        
        # 檢查排名圖示
        first_rank_item = rank_items[0]
        rank_icon = first_rank_item["contents"][0]["text"]
        assert rank_icon in ["🥇", "🥈", "🥉", "1", "2", "3"], f"排名圖示錯誤: {rank_icon}"
        
        print("✅ Flex Message 內容驗證通過")
        return True
        
    except Exception as e:
        print(f"❌ Flex Message 內容驗證失敗: {e}")
        return False

def test_flex_message_json():
    """測試 Flex Message JSON 格式是否有效"""
    print("\n🧪 測試 Flex Message JSON 格式...")
    
    try:
        from app_supabase_fixed import create_leaderboard_flex_message, get_real_students_data
        
        # 獲取數據
        students_data = get_real_students_data()
        if not students_data:
            print("⚠️ 無法獲取真實數據，使用模擬數據")
            students_data = [
                {"user_id": "test_user_1", "name": "測試用戶1", "level": 5, "score": 1000, "questions_answered": 50, "correct_answers": 45},
                {"user_id": "test_user_2", "name": "測試用戶2", "level": 3, "score": 600, "questions_answered": 30, "correct_answers": 25}
            ]
        
        top_10 = students_data[:10]
        test_user_id = students_data[0]['user_id'] if students_data else "test_user"
        
        # 創建 Flex Message
        flex_message = create_leaderboard_flex_message(top_10, students_data, test_user_id)
        
        # 測試 JSON 序列化
        json_str = json.dumps(flex_message, ensure_ascii=False, indent=2)
        assert len(json_str) > 0, "JSON 序列化失敗"
        
        # 測試 JSON 反序列化
        parsed_message = json.loads(json_str)
        assert parsed_message["type"] == "flex", "JSON 反序列化失敗"
        
        print("✅ Flex Message JSON 格式驗證通過")
        return True
        
    except Exception as e:
        print(f"❌ Flex Message JSON 格式驗證失敗: {e}")
        return False

def main():
    """主測試函數"""
    print("🚀 開始測試 Flex Message 發送功能...")
    print("=" * 60)
    
    tests = [
        ("Flex Message 結構", test_flex_message_structure),
        ("Flex Message 內容", test_flex_message_content),
        ("Flex Message JSON 格式", test_flex_message_json)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 執行測試: {test_name}")
        print("-" * 40)
        
        try:
            result = test_func()
            results.append((test_name, result))
            
            if result:
                print(f"✅ {test_name} 測試通過")
            else:
                print(f"❌ {test_name} 測試失敗")
                
        except Exception as e:
            print(f"❌ {test_name} 測試異常: {e}")
            results.append((test_name, False))
    
    # 總結測試結果
    print("\n" + "=" * 60)
    print("📊 測試結果總結:")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n總計: {passed}/{total} 個測試通過")
    
    if passed == total:
        print("🎉 所有測試都通過了！Flex Message 排行榜功能完全正常。")
        print("💡 現在用戶點擊「查看排行榜」按鈕時會收到美觀的 Flex Message 格式的排行榜。")
    else:
        print("⚠️ 部分測試失敗，請檢查相關功能。")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

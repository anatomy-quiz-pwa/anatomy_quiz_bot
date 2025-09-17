#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試 Flex Message 排行榜功能
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

def test_flex_leaderboard_creation():
    """測試 Flex Message 排行榜創建"""
    print("🧪 測試 Flex Message 排行榜創建...")
    
    try:
        # 導入相關函數
        from app_supabase_fixed import get_real_students_data, create_leaderboard_flex_message
        
        # 獲取真實數據
        print("📊 正在獲取真實排行榜數據...")
        students_data = get_real_students_data()
        
        if not students_data:
            print("⚠️ 無法獲取真實數據，使用模擬數據測試")
            students_data = [
                {"user_id": "test_user_1", "name": "測試用戶1", "level": 5, "score": 1000, "questions_answered": 50, "correct_answers": 45},
                {"user_id": "test_user_2", "name": "測試用戶2", "level": 3, "score": 600, "questions_answered": 30, "correct_answers": 25},
                {"user_id": "test_user_3", "name": "測試用戶3", "level": 2, "score": 300, "questions_answered": 15, "correct_answers": 12},
                {"user_id": "test_user_4", "name": "測試用戶4", "level": 1, "score": 100, "questions_answered": 10, "correct_answers": 8},
                {"user_id": "test_user_5", "name": "測試用戶5", "level": 1, "score": 50, "questions_answered": 5, "correct_answers": 3}
            ]
        
        # 限制顯示前10名
        top_10 = students_data[:10]
        test_user_id = "test_user_1"
        
        # 創建 Flex Message
        print("🎨 正在創建 Flex Message...")
        flex_message = create_leaderboard_flex_message(top_10, students_data, test_user_id)
        
        # 驗證 Flex Message 結構
        if flex_message.get("type") == "flex":
            print("✅ Flex Message 類型正確")
        else:
            print("❌ Flex Message 類型錯誤")
            return False
        
        if "contents" in flex_message:
            print("✅ Flex Message 包含內容")
        else:
            print("❌ Flex Message 缺少內容")
            return False
        
        # 檢查基本結構
        contents = flex_message["contents"]
        if contents.get("type") == "bubble":
            print("✅ 使用 Bubble 容器")
        else:
            print("❌ 未使用 Bubble 容器")
            return False
        
        # 檢查標題
        if "header" in contents:
            print("✅ 包含標題區域")
        else:
            print("❌ 缺少標題區域")
            return False
        
        # 檢查主體
        if "body" in contents and "contents" in contents["body"]:
            body_contents = contents["body"]["contents"]
            print(f"✅ 主體包含 {len(body_contents)} 個項目")
        else:
            print("❌ 主體結構錯誤")
            return False
        
        # 檢查底部按鈕
        if "footer" in contents:
            print("✅ 包含底部按鈕區域")
        else:
            print("❌ 缺少底部按鈕區域")
            return False
        
        # 顯示 Flex Message 結構摘要
        print("\n📋 Flex Message 結構摘要:")
        print(f"  - 類型: {flex_message.get('type')}")
        print(f"  - 替代文字: {flex_message.get('altText')}")
        print(f"  - 容器類型: {contents.get('type')}")
        print(f"  - 主體項目數: {len(contents['body']['contents'])}")
        
        # 保存 Flex Message 到文件供檢查
        with open('flex_leaderboard_sample.json', 'w', encoding='utf-8') as f:
            json.dump(flex_message, f, ensure_ascii=False, indent=2)
        print("💾 Flex Message 已保存到 flex_leaderboard_sample.json")
        
        return True
        
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        return False

def test_flex_message_validation():
    """測試 Flex Message 格式驗證"""
    print("\n🧪 測試 Flex Message 格式驗證...")
    
    try:
        # 讀取剛才創建的 Flex Message
        with open('flex_leaderboard_sample.json', 'r', encoding='utf-8') as f:
            flex_message = json.load(f)
        
        # 基本驗證
        required_fields = ["type", "altText", "contents"]
        for field in required_fields:
            if field not in flex_message:
                print(f"❌ 缺少必要欄位: {field}")
                return False
            else:
                print(f"✅ 包含必要欄位: {field}")
        
        # 檢查 contents 結構
        contents = flex_message["contents"]
        required_content_fields = ["type", "header", "body", "footer"]
        for field in required_content_fields:
            if field not in contents:
                print(f"❌ contents 缺少必要欄位: {field}")
                return False
            else:
                print(f"✅ contents 包含必要欄位: {field}")
        
        # 檢查 body 內容
        body_contents = contents["body"]["contents"]
        if len(body_contents) > 0:
            print(f"✅ body 包含 {len(body_contents)} 個項目")
        else:
            print("❌ body 為空")
            return False
        
        # 檢查每個排名項目的結構
        for i, item in enumerate(body_contents):
            if item.get("type") == "box" and item.get("layout") == "horizontal":
                print(f"✅ 排名項目 {i+1} 結構正確")
            elif item.get("type") == "text":
                print(f"✅ 文字項目 {i+1} 結構正確")
            elif item.get("type") == "separator":
                print(f"✅ 分隔線項目 {i+1} 結構正確")
            else:
                print(f"❌ 項目 {i+1} 結構錯誤: {item.get('type')}")
                return False
        
        print("✅ Flex Message 格式驗證通過")
        return True
        
    except Exception as e:
        print(f"❌ 格式驗證失敗: {e}")
        return False

def test_leaderboard_display():
    """測試排行榜顯示效果"""
    print("\n🧪 測試排行榜顯示效果...")
    
    try:
        from app_supabase_fixed import get_real_students_data, create_leaderboard_flex_message
        
        # 獲取數據
        students_data = get_real_students_data()
        if not students_data:
            print("⚠️ 無法獲取真實數據，跳過顯示測試")
            return True
        
        top_10 = students_data[:10]
        test_user_id = students_data[0]['user_id'] if students_data else "test_user"
        
        # 創建 Flex Message
        flex_message = create_leaderboard_flex_message(top_10, students_data, test_user_id)
        
        # 顯示前5名信息
        print("🏆 前5名排行榜預覽:")
        for i, student in enumerate(top_10[:5], 1):
            accuracy = (student["correct_answers"] / student["questions_answered"] * 100) if student["questions_answered"] > 0 else 0
            print(f"  {i}. {student['name']} - {student['score']}分 (等級:{student['level']}, 準確率:{accuracy:.1f}%)")
        
        print("✅ 排行榜顯示效果測試完成")
        return True
        
    except Exception as e:
        print(f"❌ 顯示效果測試失敗: {e}")
        return False

def main():
    """主測試函數"""
    print("🚀 開始測試 Flex Message 排行榜功能...")
    print("=" * 60)
    
    tests = [
        ("Flex Message 排行榜創建", test_flex_leaderboard_creation),
        ("Flex Message 格式驗證", test_flex_message_validation),
        ("排行榜顯示效果", test_leaderboard_display)
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
        print("🎉 所有測試都通過了！Flex Message 排行榜功能應該可以正常運作。")
        print("💡 現在用戶點擊「查看排行榜」按鈕時會收到美觀的 Flex Message 格式的排行榜。")
    else:
        print("⚠️ 部分測試失敗，請檢查相關功能。")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

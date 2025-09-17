#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試新的歡迎訊息設計
"""

import os
import sys
import json
from datetime import datetime

# 添加當前目錄到 Python 路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_welcome_message_design():
    """測試新的歡迎訊息設計"""
    print("🧪 測試新的歡迎訊息設計...")
    
    try:
        from app_supabase import create_welcome_flex_message
        
        # 測試創建歡迎訊息
        welcome_message = create_welcome_flex_message("測試用戶")
        
        # 驗證基本結構
        assert welcome_message["type"] == "bubble", "Flex Message 類型錯誤"
        assert "hero" in welcome_message, "缺少 hero 區域"
        assert "body" in welcome_message, "缺少 body"
        assert "footer" in welcome_message, "缺少 footer"
        
        # 檢查 Hero 圖片
        hero_image = welcome_message["hero"]
        assert hero_image["type"] == "image", "Hero 圖片類型錯誤"
        assert "url" in hero_image, "Hero 圖片缺少 URL"
        assert hero_image["url"].startswith("https://"), "Hero 圖片 URL 格式錯誤"
        
        body = welcome_message["body"]
        assert body["type"] == "box", "body 類型錯誤"
        assert body["layout"] == "vertical", "body 布局錯誤"
        assert len(body["contents"]) >= 5, "body 內容不足"
        
        # 檢查標題文字
        title_texts = []
        for content in body["contents"]:
            if content.get("type") == "text":
                title_texts.append(content.get("text", ""))
        
        assert "🎉 歡迎來到《解剖咬一口》！" in title_texts, "缺少主標題"
        # 檢查副標題和行動呼籲（在同一個文字區塊中）
        found_subtitle = any("每天一口小小解剖，探索人體奧秘！" in text for text in title_texts)
        assert found_subtitle, "缺少副標題"
        found_action = any("👉 第一步：請輸入你的「暱稱」開始挑戰！" in text for text in title_texts)
        assert found_action, "缺少行動呼籲"
        
        # 檢查暱稱要求區塊和範例暱稱區塊
        found_nickname_requirements = any("✏️ 暱稱規則：" in text for text in title_texts)
        found_example_nicknames = any("💡 範例暱稱：" in text for text in title_texts)
        
        assert found_nickname_requirements, "缺少暱稱要求區塊"
        assert found_example_nicknames, "缺少範例暱稱區塊"
        
        print("✅ 歡迎訊息設計結構驗證通過")
        return True
        
    except Exception as e:
        print(f"❌ 歡迎訊息設計驗證失敗: {e}")
        return False

def test_welcome_message_content():
    """測試歡迎訊息內容"""
    print("\n🧪 測試歡迎訊息內容...")
    
    try:
        from app_supabase import create_welcome_flex_message
        
        # 創建歡迎訊息
        welcome_message = create_welcome_flex_message("測試用戶")
        
        # 檢查所有文字內容
        all_texts = []
        def extract_texts(content):
            if isinstance(content, dict):
                if content.get("type") == "text" and "text" in content:
                    all_texts.append(content["text"])
                for key, value in content.items():
                    if isinstance(value, (list, dict)):
                        extract_texts(value)
            elif isinstance(content, list):
                for item in content:
                    extract_texts(item)
        
        extract_texts(welcome_message)
        
        # 檢查關鍵內容
        required_texts = [
            "🎉 歡迎來到《解剖咬一口》！",
            "每天一口小小解剖，探索人體奧秘！",
            "👉 第一步：請輸入你的「暱稱」開始挑戰！",
            "✏️ 暱稱規則：",
            "2–10 個字",
            "中文 / 英文 / 數字",
            "不能包含特殊符號",
            "💡 範例暱稱：",
            "解剖大師、Brain、醫學生001、小醫生"
        ]
        
        for required_text in required_texts:
            found = any(required_text in text for text in all_texts)
            assert found, f"缺少必要文字: {required_text}"
        
        print("✅ 歡迎訊息內容驗證通過")
        return True
        
    except Exception as e:
        print(f"❌ 歡迎訊息內容驗證失敗: {e}")
        return False

def test_welcome_message_json():
    """測試歡迎訊息 JSON 格式"""
    print("\n🧪 測試歡迎訊息 JSON 格式...")
    
    try:
        from app_supabase import create_welcome_flex_message
        
        # 創建歡迎訊息
        welcome_message = create_welcome_flex_message("測試用戶")
        
        # 測試 JSON 序列化
        json_str = json.dumps(welcome_message, ensure_ascii=False, indent=2)
        assert len(json_str) > 0, "JSON 序列化失敗"
        
        # 測試 JSON 反序列化
        parsed_message = json.loads(json_str)
        assert parsed_message["type"] == "bubble", "JSON 反序列化失敗"
        
        print("✅ 歡迎訊息 JSON 格式驗證通過")
        return True
        
    except Exception as e:
        print(f"❌ 歡迎訊息 JSON 格式驗證失敗: {e}")
        return False

def save_welcome_message_sample():
    """保存歡迎訊息範例到檔案"""
    print("\n💾 保存歡迎訊息範例...")
    
    try:
        from app_supabase import create_welcome_flex_message
        
        # 創建歡迎訊息
        welcome_message = create_welcome_flex_message("測試用戶")
        
        # 保存到檔案
        with open("welcome_message_sample.json", "w", encoding="utf-8") as f:
            json.dump(welcome_message, f, ensure_ascii=False, indent=2)
        
        print("✅ 歡迎訊息範例已保存到 welcome_message_sample.json")
        return True
        
    except Exception as e:
        print(f"❌ 保存歡迎訊息範例失敗: {e}")
        return False

def main():
    """主測試函數"""
    print("🚀 開始測試新的歡迎訊息設計...")
    print("=" * 60)
    
    tests = [
        ("歡迎訊息設計結構", test_welcome_message_design),
        ("歡迎訊息內容", test_welcome_message_content),
        ("歡迎訊息 JSON 格式", test_welcome_message_json),
        ("保存歡迎訊息範例", save_welcome_message_sample)
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
        print("\n🎉 所有測試都通過了！新的歡迎訊息設計完全正常。")
        print("💡 現在新用戶登入時會收到完整的歡迎 Flex Message，包含：")
        print("   - 解剖學主題的 Hero 圖片")
        print("   - 完整的歡迎流程文字")
        print("   - 詳細的暱稱設定指導")
        print("   - 範例暱稱")
        print("   - 清晰的輸入提示")
    else:
        print("⚠️ 部分測試失敗，請檢查相關功能。")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

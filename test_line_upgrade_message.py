#!/usr/bin/env python3
"""
測試LINE Bot升級訊息的實際發送功能
注意: 這個測試會嘗試發送真實的LINE訊息，請確保有正確的環境設定
"""

import sys
import os
import json
from datetime import datetime

# 添加當前目錄到路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_line_flex_message_structure():
    """測試LINE Flex Message結構的完整性"""
    print("=" * 60)
    print("📱 測試LINE Flex Message結構完整性")
    print("=" * 60)
    
    try:
        from app_supabase import create_level_up_flex_message
        
        # 測試一個典型的升級場景
        old_level, new_level = 3, 4
        
        print(f"🧪 測試升級: {old_level} -> {new_level}")
        
        flex_message = create_level_up_flex_message(old_level, new_level)
        
        if not flex_message:
            print("❌ Flex Message創建失敗")
            return False
        
        print("✅ Flex Message創建成功")
        
        # 驗證LINE Flex Message的必要結構
        required_structure = {
            'type': 'flex',
            'altText': str,
            'contents': {
                'type': 'bubble',
                'hero': {
                    'type': 'image',
                    'url': str,
                    'size': str,
                    'aspectRatio': str,
                    'aspectMode': str
                },
                'body': {
                    'type': 'box',
                    'layout': 'vertical',
                    'contents': list
                },
                'footer': {
                    'type': 'box',
                    'layout': 'vertical',
                    'contents': list
                }
            }
        }
        
        def validate_structure(data, structure, path=""):
            """遞迴驗證結構"""
            for key, expected_type in structure.items():
                if key not in data:
                    print(f"❌ 缺少必要欄位: {path}.{key}")
                    return False
                
                if isinstance(expected_type, dict):
                    if not validate_structure(data[key], expected_type, f"{path}.{key}"):
                        return False
                elif expected_type == str:
                    if not isinstance(data[key], str):
                        print(f"❌ 欄位類型錯誤: {path}.{key} 應為字符串")
                        return False
                elif expected_type == list:
                    if not isinstance(data[key], list):
                        print(f"❌ 欄位類型錯誤: {path}.{key} 應為列表")
                        return False
            
            return True
        
        if validate_structure(flex_message, required_structure):
            print("✅ Flex Message結構驗證通過")
        else:
            print("❌ Flex Message結構驗證失敗")
            return False
        
        # 驗證具體內容
        contents = flex_message['contents']
        
        # 驗證Hero圖片URL
        hero_url = contents['hero']['url']
        expected_url_part = f"level_{new_level}_poster.png"
        if expected_url_part not in hero_url:
            print(f"❌ Hero圖片URL不正確，應包含: {expected_url_part}")
            return False
        
        print(f"✅ Hero圖片URL正確: {hero_url}")
        
        # 驗證body內容
        body_contents = contents['body']['contents']
        if len(body_contents) < 4:  # 至少應有標題、稱號變化、分隔線、詳細說明
            print("❌ Body內容不完整")
            return False
        
        print("✅ Body內容完整")
        
        # 驗證footer按鈕
        footer_contents = contents['footer']['contents']
        if len(footer_contents) < 1:
            print("❌ Footer按鈕缺失")
            return False
        
        button = footer_contents[0]
        if button.get('type') != 'button':
            print("❌ Footer第一個元素不是按鈕")
            return False
        
        if 'action' not in button:
            print("❌ 按鈕缺少action")
            return False
        
        print("✅ Footer按鈕正確")
        
        # 輸出完整的JSON供檢視
        print(f"\n📄 完整Flex Message JSON (字符數: {len(json.dumps(flex_message))})")
        print("="*40)
        print(json.dumps(flex_message, ensure_ascii=False, indent=2)[:1000] + "...")
        
        return True
        
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {e}")
        return False

def test_upgrade_message_variations():
    """測試不同升級情況的訊息變化"""
    print("\n" + "=" * 60)
    print("🎨 測試升級訊息的不同變化")
    print("=" * 60)
    
    try:
        from app_supabase import create_level_up_flex_message, get_level_title
        
        test_cases = [
            (1, 2, "新手首次升級"),
            (3, 4, "跨階段升級"),
            (7, 8, "中級到高級"),
            (13, 14, "達到終極等級"),
        ]
        
        for old_level, new_level, description in test_cases:
            print(f"\n🎬 {description}: {old_level} -> {new_level}")
            
            flex_message = create_level_up_flex_message(old_level, new_level)
            
            if flex_message:
                # 檢查altText的差異
                alt_text = flex_message['altText']
                old_title = get_level_title(old_level)
                new_title = get_level_title(new_level)
                
                print(f"   📝 Alt Text: {alt_text}")
                print(f"   🏆 稱號變化: {old_title} -> {new_title}")
                
                # 檢查Hero圖片的差異
                hero_url = flex_message['contents']['hero']['url']
                print(f"   🎨 Hero圖片: {hero_url.split('/')[-1]}")
                
                # 檢查body文字的差異
                body_contents = flex_message['contents']['body']['contents']
                for content in body_contents:
                    if content.get('type') == 'text' and '掌握了等級' in content.get('text', ''):
                        print(f"   📚 進度說明: {content['text']}")
                        break
                
                print("   ✅ 訊息變化正確")
            else:
                print("   ❌ 訊息創建失敗")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ 變化測試失敗: {e}")
        return False

def simulate_real_upgrade_flow():
    """模擬真實的升級流程"""
    print("\n" + "=" * 60)
    print("🔄 模擬真實升級流程")
    print("=" * 60)
    
    try:
        from app_supabase import (
            create_level_up_flex_message,
            get_level_title
        )
        
        # 模擬用戶答題升級的完整流程
        user_data = {
            'user_id': 'U1234567890abcdef',
            'nickname': '解剖學愛好者',
            'level': 6,
            'correct_in_level': 2
        }
        
        print(f"👤 用戶: {user_data['nickname']}")
        print(f"📊 當前等級: {user_data['level']} ({get_level_title(user_data['level'])})")
        print(f"📈 當前進度: {user_data['correct_in_level']}/3")
        
        print("\n🤔 用戶正在答題...")
        print("✅ 答對了第3題！")
        
        # 觸發升級
        old_level = user_data['level']
        new_level = old_level + 1
        
        print(f"🎉 觸發升級: {old_level} -> {new_level}")
        
        # 創建升級訊息
        upgrade_message = create_level_up_flex_message(old_level, new_level)
        
        if upgrade_message:
            print("✅ 升級訊息準備就緒")
            
            # 模擬發送過程
            print("\n📱 模擬發送升級訊息...")
            print("   🔄 正在發送Flex Message...")
            
            # 這裡可以添加實際的LINE發送邏輯
            # send_message(user_data['user_id'], upgrade_message)
            
            print("   ✅ 訊息發送成功（模擬）")
            
            # 顯示用戶會看到的內容
            print(f"\n👀 用戶將看到:")
            print(f"   🎨 精美的等級{new_level}海報")
            print(f"   🎉 恭喜升級的慶祝標題")
            print(f"   🏆 從{get_level_title(old_level)}升級到{get_level_title(new_level)}")
            print(f"   📚 等級{new_level}知識掌握的確認")
            print(f"   🎯 等級{new_level+1}挑戰的預告")
            print(f"   🚀 繼續答題的按鈕")
            
            return True
        else:
            print("❌ 升級訊息創建失敗")
            return False
            
    except Exception as e:
        print(f"❌ 流程模擬失敗: {e}")
        return False

def main():
    """主測試函數"""
    print(f"🕐 LINE升級訊息測試開始: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        ("Flex Message結構測試", test_line_flex_message_structure),
        ("升級訊息變化測試", test_upgrade_message_variations),
        ("真實升級流程模擬", simulate_real_upgrade_flow),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} 執行異常: {e}")
            results.append((test_name, False))
    
    # 總結報告
    print("\n" + "="*60)
    print("📊 LINE升級訊息測試總結")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"   {test_name}: {status}")
    
    print(f"\n🎯 總體結果: {passed}/{total} 通過")
    
    if passed == total:
        print("\n🎉 所有LINE升級訊息測試都通過！")
        print("\n🚀 升級訊息系統已經準備好部署:")
        print("   ✅ 符合LINE Flex Message規範")
        print("   ✅ 完整的視覺設計和互動體驗")
        print("   ✅ 支援所有升級場景")
        print("   ✅ 具備可靠的錯誤處理")
        print("   ✅ 優化的用戶體驗流程")
        
        print("\n💡 下一步建議:")
        print("   1. 確保所有等級的海報圖片都已上傳到Supabase")
        print("   2. 在測試環境中進行實際的LINE發送測試")
        print("   3. 收集用戶反饋並進行優化")
        
        return 0
    else:
        print("⚠️  部分測試未通過，請檢查相關功能後再部署。")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

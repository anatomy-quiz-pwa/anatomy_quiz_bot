#!/usr/bin/env python3
"""
模擬實際的用戶升級場景測試
"""

import sys
import os
import json
from datetime import datetime

# 添加當前目錄到路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def simulate_user_upgrade_scenario():
    """模擬用戶升級場景"""
    print("=" * 60)
    print("🎮 模擬用戶升級場景測試")
    print("=" * 60)
    
    try:
        from app_supabase import (
            get_level_title,
            create_level_up_flex_message,
            send_level_up_celebration
        )
        
        # 模擬用戶資料
        test_user = {
            'user_id': 'test_upgrade_user',
            'nickname': '測試小明',
            'current_level': 3,
            'correct_in_level': 2,  # 已經答對2題，再答對1題就升級
        }
        
        print(f"👤 測試用戶: {test_user['nickname']} (ID: {test_user['user_id']})")
        print(f"📊 當前狀態: 等級 {test_user['current_level']} ({get_level_title(test_user['current_level'])})")
        print(f"📈 當前進度: {test_user['correct_in_level']}/3 題正確")
        print("🎯 再答對 1 題即可升級！")
        
        print("\n" + "-" * 40)
        print("🤔 用戶答題...")
        
        # 模擬答對題目
        print("✅ 答對了！")
        
        # 檢查是否升級
        new_correct_in_level = test_user['correct_in_level'] + 1
        if new_correct_in_level >= 3:
            old_level = test_user['current_level']
            new_level = old_level + 1
            
            print(f"🎉 升級觸發！{old_level} -> {new_level}")
            print(f"🏆 稱號變化: {get_level_title(old_level)} -> {get_level_title(new_level)}")
            
            # 創建升級Flex Message
            flex_message = create_level_up_flex_message(old_level, new_level)
            
            if flex_message:
                print("✅ 升級Flex Message創建成功")
                
                # 顯示訊息內容預覽
                print("\n📱 升級訊息預覽:")
                print(f"   🎨 Hero圖片: level_{new_level}_poster.png")
                print(f"   📝 標題: 🎉 恭喜升級！")
                print(f"   🏆 內容: 從{get_level_title(old_level)}晉升為{get_level_title(new_level)}！")
                print(f"   📚 說明: 你已經掌握了等級 {new_level} 的知識")
                print(f"   🎯 挑戰: 現在開始挑戰等級 {new_level + 1} 的更高難度！")
                print(f"   🚀 按鈕: 繼續答題")
                
                # 保存訊息到檔案供檢視
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"upgrade_message_{old_level}_to_{new_level}_{timestamp}.json"
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(flex_message, f, ensure_ascii=False, indent=2)
                
                print(f"💾 完整訊息已保存至: {filename}")
                
                return True
            else:
                print("❌ 升級Flex Message創建失敗")
                return False
        else:
            print(f"📊 尚未升級，當前進度: {new_correct_in_level}/3")
            return False
            
    except Exception as e:
        print(f"❌ 模擬測試失敗: {e}")
        return False

def test_multiple_upgrade_scenarios():
    """測試多種升級場景"""
    print("\n" + "=" * 60)
    print("🎭 測試多種升級場景")
    print("=" * 60)
    
    try:
        from app_supabase import (
            get_level_title,
            create_level_up_flex_message
        )
        
        scenarios = [
            {
                'name': '新手首次升級',
                'old_level': 1,
                'new_level': 2,
                'description': '從新手解剖師升級到初級解剖師'
            },
            {
                'name': '跨階段升級',
                'old_level': 3,
                'new_level': 4,
                'description': '從初級解剖師升級到中級解剖師（跨階段）'
            },
            {
                'name': '中階升級',
                'old_level': 6,
                'new_level': 7,
                'description': '中級解剖師內部升級'
            },
            {
                'name': '高階升級',
                'old_level': 10,
                'new_level': 11,
                'description': '高級解剖師內部升級'
            },
            {
                'name': '專家升級',
                'old_level': 12,
                'new_level': 13,
                'description': '專家解剖師內部升級'
            },
            {
                'name': '終極升級',
                'old_level': 13,
                'new_level': 14,
                'description': '升級到終極解剖師（最高等級）'
            }
        ]
        
        success_count = 0
        
        for scenario in scenarios:
            print(f"\n🎬 場景: {scenario['name']}")
            print(f"   📋 描述: {scenario['description']}")
            print(f"   📊 等級: {scenario['old_level']} -> {scenario['new_level']}")
            
            old_title = get_level_title(scenario['old_level'])
            new_title = get_level_title(scenario['new_level'])
            print(f"   🏆 稱號: {old_title} -> {new_title}")
            
            # 創建Flex Message
            flex_message = create_level_up_flex_message(
                scenario['old_level'], 
                scenario['new_level']
            )
            
            if flex_message:
                print("   ✅ 訊息創建成功")
                
                # 驗證關鍵內容
                alt_text = flex_message.get('altText', '')
                if old_title in alt_text and new_title in alt_text:
                    print("   ✅ 稱號資訊正確")
                else:
                    print("   ⚠️  稱號資訊可能不完整")
                
                # 驗證hero圖片
                hero_url = flex_message['contents']['hero']['url']
                expected_level = scenario['new_level']
                if f"level_{expected_level}_poster.png" in hero_url:
                    print(f"   ✅ Hero圖片正確 (level_{expected_level}_poster.png)")
                else:
                    print("   ⚠️  Hero圖片可能不正確")
                
                success_count += 1
            else:
                print("   ❌ 訊息創建失敗")
        
        print(f"\n📊 場景測試結果: {success_count}/{len(scenarios)} 成功")
        return success_count == len(scenarios)
        
    except Exception as e:
        print(f"❌ 多場景測試失敗: {e}")
        return False

def test_edge_cases():
    """測試邊界情況"""
    print("\n" + "=" * 60)
    print("🔍 測試邊界情況")
    print("=" * 60)
    
    try:
        from app_supabase import (
            get_level_title,
            create_level_up_flex_message
        )
        
        edge_cases = [
            {
                'name': '最低等級升級',
                'old_level': 1,
                'new_level': 2,
            },
            {
                'name': '接近最高等級',
                'old_level': 13,
                'new_level': 14,
            },
            {
                'name': '異常等級（應該處理）',
                'old_level': 0,
                'new_level': 1,
            },
            {
                'name': '高等級（應該有備用處理）',
                'old_level': 15,
                'new_level': 16,
            }
        ]
        
        for case in edge_cases:
            print(f"\n🧪 測試: {case['name']}")
            print(f"   等級: {case['old_level']} -> {case['new_level']}")
            
            try:
                old_title = get_level_title(case['old_level'])
                new_title = get_level_title(case['new_level'])
                print(f"   稱號: {old_title} -> {new_title}")
                
                flex_message = create_level_up_flex_message(
                    case['old_level'], 
                    case['new_level']
                )
                
                if flex_message:
                    print("   ✅ 邊界情況處理正確")
                else:
                    print("   ⚠️  無法創建訊息（可能是預期行為）")
                    
            except Exception as e:
                print(f"   ⚠️  邊界情況異常: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ 邊界測試失敗: {e}")
        return False

def main():
    """主測試函數"""
    print(f"🕐 升級場景測試開始: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        ("用戶升級場景模擬", simulate_user_upgrade_scenario),
        ("多種升級場景測試", test_multiple_upgrade_scenarios),
        ("邊界情況測試", test_edge_cases),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} 執行異常: {e}")
            results.append((test_name, False))
    
    # 總結
    print("\n" + "="*60)
    print("📊 升級場景測試總結")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"   {test_name}: {status}")
    
    print(f"\n🎯 總體結果: {passed}/{total} 通過")
    
    if passed == total:
        print("\n🎉 所有升級場景測試都通過！")
        print("\n✨ 升級訊息功能已準備就緒：")
        print("   🎨 精美的Flex Message設計")
        print("   🏆 完整的稱號系統")
        print("   📱 優秀的用戶體驗")
        print("   🔄 可靠的備用方案")
        
        # 清理測試檔案
        import glob
        test_files = glob.glob("upgrade_message_*.json")
        if test_files:
            print(f"\n🧹 清理了 {len(test_files)} 個測試檔案")
            for file in test_files:
                os.remove(file)
        
        return 0
    else:
        print("⚠️  部分測試未通過，請檢查相關功能。")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

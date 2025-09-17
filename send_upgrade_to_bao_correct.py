#!/usr/bin/env python3
"""
發送升級Flex Message測試訊息到寶的正確LINE帳號
使用正確的用戶ID: U977c24d1fec3a2bf07035504e1444911
"""

import sys
import os
import json
import time
from datetime import datetime

# 添加當前目錄到路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 正確的測試帳號ID對應
TEST_ACCOUNTS = {
    'bao': 'U977c24d1fec3a2bf07035504e1444911',  # 寶的測試帳號
    'su': 'U9a9df49945755ef651d067743f3c7ea7'    # 蘇的測試帳號
}

def send_upgrade_test_to_bao():
    """發送升級測試訊息到寶的正確帳號"""
    print("=" * 60)
    print("📱 發送升級Flex Message測試到寶的LINE帳號")
    print("=" * 60)
    
    try:
        from app_supabase import (
            create_level_up_flex_message,
            send_message,
            get_level_title
        )
        
        # 使用正確的寶的用戶ID
        bao_user_id = TEST_ACCOUNTS['bao']
        
        print(f"👤 目標用戶: 寶")
        print(f"🆔 用戶ID: {bao_user_id}")
        
        # 創建一個精彩的升級場景
        old_level = 3
        new_level = 4
        
        print(f"🎬 測試場景: 等級 {old_level} -> {new_level}")
        print(f"🏆 稱號變化: {get_level_title(old_level)} -> {get_level_title(new_level)}")
        
        # 發送準備訊息
        preparation_message = {
            "text": "🧪 升級Flex Message測試開始！\n\n📊 測試場景：初級解剖師 → 中級解剖師\n🎨 即將展示完整的升級慶祝介面\n\n⏰ 3秒後發送..."
        }
        
        print("📤 發送準備訊息...")
        send_message(bao_user_id, preparation_message)
        print("✅ 準備訊息已發送")
        
        # 等待
        time.sleep(3)
        
        # 創建並發送升級Flex Message
        print("🎨 創建升級Flex Message...")
        upgrade_flex_message = create_level_up_flex_message(old_level, new_level)
        
        if upgrade_flex_message:
            print("✅ Flex Message創建成功")
            
            # 顯示詳細預覽
            print(f"\n📱 Flex Message詳細內容:")
            print(f"   🎨 Hero圖片: level_{new_level}_poster.png")
            print(f"   📝 Alt Text: {upgrade_flex_message['altText']}")
            print(f"   🎉 主標題: 恭喜升級！")
            print(f"   🏆 稱號變化: {get_level_title(old_level)} → {get_level_title(new_level)}")
            print(f"   📚 進度說明: 掌握等級{new_level}知識")
            print(f"   🎯 挑戰預告: 等級{new_level+1}更高難度")
            print(f"   🚀 互動按鈕: 繼續答題")
            
            # 發送升級Flex Message
            print("\n🚀 發送升級Flex Message...")
            send_message(bao_user_id, upgrade_flex_message)
            print("✅ 升級Flex Message已發送！")
            
            # 等待並發送說明
            time.sleep(2)
            explanation_message = {
                "text": """🎉 升級Flex Message測試完成！

📊 這個訊息包含了：
✅ 精美的等級4海報圖片
✅ 慶祝升級的橙色主題設計
✅ 從初級解剖師到中級解剖師的稱號變化
✅ 清晰的學習進度說明
✅ 下一階段挑戰的預告
✅ 繼續答題的互動按鈕

🎨 設計特色：
• 20:13比例的hero圖片
• 居中對齊的文字排版
• 橙色(#FF6B35)主題色彩
• 鼓勵性的學習引導

這就是用戶升級時會看到的完整體驗！用戶可以點擊「🚀 繼續答題」按鈕來繼續學習。"""
            }
            
            print("📤 發送詳細說明...")
            send_message(bao_user_id, explanation_message)
            print("✅ 詳細說明已發送")
            
            return True
            
        else:
            print("❌ Flex Message創建失敗")
            
            # 發送錯誤通知
            error_message = {
                "text": "❌ 升級Flex Message創建失敗\n請檢查系統設定和圖片資源。"
            }
            send_message(bao_user_id, error_message)
            return False
            
    except Exception as e:
        print(f"❌ 發送測試失敗: {e}")
        
        try:
            # 嘗試發送錯誤通知
            error_notification = {
                "text": f"❌ 升級訊息測試過程中發生錯誤:\n{str(e)}\n\n請檢查系統設定和網路連接。"
            }
            send_message(TEST_ACCOUNTS['bao'], error_notification)
        except:
            print("❌ 無法發送錯誤通知")
        
        return False

def send_multiple_upgrade_examples_to_bao():
    """發送多種升級範例到寶的帳號"""
    print("\n" + "=" * 60)
    print("🎭 發送多種升級範例到寶的LINE帳號")
    print("=" * 60)
    
    try:
        from app_supabase import (
            create_level_up_flex_message,
            send_message,
            get_level_title
        )
        
        bao_user_id = TEST_ACCOUNTS['bao']
        
        # 準備多個精彩的升級範例
        upgrade_examples = [
            {
                'old_level': 1,
                'new_level': 2,
                'description': '新手的第一次升級',
                'highlight': '學習旅程的開始'
            },
            {
                'old_level': 7,
                'new_level': 8,
                'description': '中級到高級的重要突破',
                'highlight': '跨階段的成就感'
            },
            {
                'old_level': 13,
                'new_level': 14,
                'description': '達到終極解剖師',
                'highlight': '最高榮譽的獲得'
            }
        ]
        
        # 發送範例介紹
        intro_message = {
            "text": f"🎨 準備展示 {len(upgrade_examples)} 種不同的升級場景：\n\n" + 
                   "\n".join([f"🎬 {i+1}. {ex['description']}\n   等級 {ex['old_level']} → {ex['new_level']} ({ex['highlight']})" 
                            for i, ex in enumerate(upgrade_examples)]) +
                   f"\n\n⏰ 每個範例間隔4秒發送，請準備欣賞！"
        }
        
        print("📤 發送範例介紹...")
        send_message(bao_user_id, intro_message)
        time.sleep(4)
        
        success_count = 0
        
        for i, example in enumerate(upgrade_examples, 1):
            old_level = example['old_level']
            new_level = example['new_level']
            description = example['description']
            highlight = example['highlight']
            
            print(f"\n🎬 發送範例 {i}: {description}")
            print(f"   等級變化: {old_level} -> {new_level}")
            print(f"   特色亮點: {highlight}")
            
            # 發送場景說明
            scene_message = {
                "text": f"🎬 範例 {i}: {description}\n\n🏆 {get_level_title(old_level)} → {get_level_title(new_level)}\n✨ {highlight}\n\n準備發送升級慶祝訊息..."
            }
            send_message(bao_user_id, scene_message)
            time.sleep(2)
            
            # 創建並發送升級Flex Message
            upgrade_flex = create_level_up_flex_message(old_level, new_level)
            
            if upgrade_flex:
                send_message(bao_user_id, upgrade_flex)
                print(f"   ✅ 範例 {i} 發送成功")
                success_count += 1
            else:
                print(f"   ❌ 範例 {i} 發送失敗")
            
            # 範例間隔
            if i < len(upgrade_examples):
                time.sleep(4)
        
        # 發送總結
        time.sleep(3)
        summary_message = {
            "text": f"""🎯 升級範例展示完成！

📊 發送結果: {success_count}/{len(upgrade_examples)} 成功

🎨 每個升級訊息都包含：
• 🖼️ 專屬的等級海報圖片
• 🏆 個性化的稱號變化展示
• 📚 鼓勵性的學習進度說明
• 🎯 下一階段的挑戰預告
• 🚀 一鍵繼續的互動按鈕
• 🎨 統一的橙色主題設計

這些就是用戶在不同學習階段升級時會看到的完整體驗！每個升級都是一個小小的慶祝時刻，激勵用戶繼續學習解剖學知識。"""
        }
        
        send_message(bao_user_id, summary_message)
        print(f"\n📊 範例展示完成: {success_count}/{len(upgrade_examples)} 成功")
        
        return success_count == len(upgrade_examples)
        
    except Exception as e:
        print(f"❌ 多範例發送失敗: {e}")
        return False

def main():
    """主函數"""
    print(f"🕐 開始時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 目標: 發送升級Flex Message測試到寶的LINE帳號")
    print(f"🆔 寶的用戶ID: {TEST_ACCOUNTS['bao']}")
    
    # 執行測試
    tests = [
        ("單一升級測試", send_upgrade_test_to_bao),
        ("多種升級範例", send_multiple_upgrade_examples_to_bao),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
            if result:
                print(f"✅ {test_name} 完成")
            else:
                print(f"❌ {test_name} 失敗")
        except Exception as e:
            print(f"❌ {test_name} 執行異常: {e}")
            results.append((test_name, False))
    
    # 總結報告
    print("\n" + "="*60)
    print("📊 升級Flex Message測試總結")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 成功" if result else "❌ 失敗"
        print(f"   {test_name}: {status}")
    
    print(f"\n🎯 總體結果: {passed}/{total} 成功")
    
    if passed > 0:
        print(f"\n🎉 升級Flex Message已成功發送到寶的LINE帳號！")
        print(f"📱 寶現在可以在LINE中看到：")
        print(f"   🎨 精美的升級慶祝Flex Message")
        print(f"   🏆 完整的稱號變化展示")
        print(f"   📚 鼓勵性的學習進度說明")
        print(f"   🚀 繼續答題的互動按鈕")
        print(f"   🎯 多種不同等級的升級範例")
        
        print(f"\n💡 用戶體驗特色：")
        print(f"   • 視覺衝擊力強的hero圖片")
        print(f"   • 清晰的資訊層次結構")
        print(f"   • 一致的橙色主題設計")
        print(f"   • 流暢的互動體驗")
        
        return 0
    else:
        print("⚠️  發送失敗，請檢查LINE設定和網路連接。")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

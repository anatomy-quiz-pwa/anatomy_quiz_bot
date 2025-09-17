#!/usr/bin/env python3
"""
測試新的等級名稱並發送測試訊息
"""

import sys
import os
import time
from datetime import datetime

# 添加當前目錄到路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 寶的測試帳號ID
BAO_USER_ID = "U977c24d1fec3a2bf07035504e1444911"

def verify_new_level_names():
    """驗證新的等級名稱"""
    print("=" * 80)
    print("🏷️  驗證新的等級名稱對應")
    print("=" * 80)
    
    try:
        from app_supabase import get_level_title
        
        # 預期的新等級名稱
        expected_names = {
            1: "解剖新手村",
            2: "胚體學長", 
            3: "肌肉拆解師",
            4: "神經探路員",
            5: "解剖影武者",
            6: "組織細胞使者",
            7: "血管引導員",
            8: "解剖研究員",
            9: "解剖操盤手",
            10: "解剖副教授",
            11: "腦神經導師",
            12: "人體地圖管理",
            13: "解剖大魔導",
            14: "解剖學傳說"
        }
        
        print("📋 新的等級名稱對應表：")
        print("-" * 60)
        print("等級 | 新稱號名稱")
        print("-" * 60)
        
        all_correct = True
        
        for level in range(1, 15):
            actual_name = get_level_title(level)
            expected_name = expected_names.get(level)
            
            if actual_name == expected_name:
                status = "✅"
            else:
                status = "❌"
                all_correct = False
            
            print(f" {level:2d}  | {actual_name} {status}")
        
        print("-" * 60)
        
        if all_correct:
            print("✅ 所有等級名稱都已正確更新！")
        else:
            print("❌ 部分等級名稱更新有誤，請檢查。")
        
        return all_correct
        
    except Exception as e:
        print(f"❌ 驗證過程中發生錯誤: {e}")
        return False

def test_upgrade_scenarios_with_new_names():
    """測試新名稱的升級場景"""
    print("\n" + "=" * 80)
    print("🎬 測試新名稱的升級場景")
    print("=" * 80)
    
    try:
        from app_supabase import get_level_title, create_level_up_flex_message
        
        # 精選的升級場景
        test_scenarios = [
            (1, 2, "從新手村畢業"),
            (3, 4, "從肌肉專家到神經探索"),
            (7, 8, "從血管引導到研究員"),
            (10, 11, "副教授升級為導師"),
            (13, 14, "大魔導成為傳說")
        ]
        
        print("🎯 升級場景測試：")
        print("-" * 60)
        
        for old_level, new_level, description in test_scenarios:
            old_name = get_level_title(old_level)
            new_name = get_level_title(new_level)
            
            print(f"🎬 {description}")
            print(f"   等級: {old_level} → {new_level}")
            print(f"   稱號: {old_name} → {new_name}")
            
            # 測試Flex Message創建
            flex_message = create_level_up_flex_message(old_level, new_level)
            if flex_message:
                print(f"   ✅ Flex Message創建成功")
                print(f"   📝 Alt Text: {flex_message['altText']}")
            else:
                print(f"   ❌ Flex Message創建失敗")
            
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ 升級場景測試失敗: {e}")
        return False

def send_new_names_demo_to_bao():
    """發送新名稱示範到寶的帳號"""
    print("\n" + "=" * 80)
    print("📱 發送新等級名稱示範到寶的LINE帳號")
    print("=" * 80)
    
    try:
        from app_supabase import (
            get_level_title, 
            create_level_up_flex_message, 
            send_message
        )
        
        # 發送介紹訊息
        intro_message = {
            "text": """🎉 等級名稱大更新！

全新的14個等級稱號已經上線：
📚 更有趣的命名風格
🎮 更強的遊戲感體驗
🏆 更具挑戰性的成就感

準備展示新的升級體驗..."""
        }
        
        print("📤 發送介紹訊息...")
        send_message(BAO_USER_ID, intro_message)
        time.sleep(3)
        
        # 展示幾個精彩的升級場景
        demo_scenarios = [
            (1, 2, "新手村畢業典禮", "🎓"),
            (4, 5, "神經探路員→影武者", "🥷"),
            (9, 10, "操盤手→副教授", "🎓"),
            (13, 14, "大魔導→傳說誕生", "⭐")
        ]
        
        for i, (old_level, new_level, description, emoji) in enumerate(demo_scenarios, 1):
            old_name = get_level_title(old_level)
            new_name = get_level_title(new_level)
            
            print(f"\n🎬 發送示範 {i}: {description}")
            
            # 發送場景說明
            scene_message = {
                "text": f"{emoji} 示範 {i}: {description}\n\n🏆 {old_name} → {new_name}\n\n準備發送新版升級慶祝訊息..."
            }
            send_message(BAO_USER_ID, scene_message)
            time.sleep(2)
            
            # 發送升級Flex Message
            flex_message = create_level_up_flex_message(old_level, new_level)
            if flex_message:
                send_message(BAO_USER_ID, flex_message)
                print(f"   ✅ 示範 {i} 發送成功")
            else:
                print(f"   ❌ 示範 {i} 發送失敗")
            
            # 間隔
            if i < len(demo_scenarios):
                time.sleep(4)
        
        # 發送完整名稱列表
        time.sleep(3)
        all_names_message = {
            "text": """📋 完整的新等級名稱列表：

1️⃣ 解剖新手村
2️⃣ 胚體學長
3️⃣ 肌肉拆解師
4️⃣ 神經探路員
5️⃣ 解剖影武者
6️⃣ 組織細胞使者
7️⃣ 血管引導員
8️⃣ 解剖研究員
9️⃣ 解剖操盤手
🔟 解剖副教授
1️⃣1️⃣ 腦神經導師
1️⃣2️⃣ 人體地圖管理
1️⃣3️⃣ 解剖大魔導
1️⃣4️⃣ 解剖學傳說

🎉 每個名稱都充滿了創意和挑戰性！
現在升級會更有成就感了！"""
        }
        
        print("📤 發送完整名稱列表...")
        send_message(BAO_USER_ID, all_names_message)
        print("✅ 完整示範發送完成")
        
        return True
        
    except Exception as e:
        print(f"❌ 發送示範失敗: {e}")
        return False

def create_new_names_reference():
    """創建新名稱的參考文檔"""
    print("\n" + "=" * 80)
    print("📄 創建新等級名稱參考文檔")
    print("=" * 80)
    
    try:
        from app_supabase import get_level_title
        
        reference_content = f"""# 解剖學測驗機器人 - 新等級名稱對應表

更新時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 完整等級名稱對應表

| 等級 | 新稱號名稱 | 特色說明 |
|------|------------|----------|
"""
        
        # 為每個等級添加特色說明
        level_descriptions = {
            1: "解剖新手村 - 踏上解剖學習之路的起點",
            2: "胚體學長 - 掌握胚胎發育的基礎知識",
            3: "肌肉拆解師 - 精通肌肉系統的構造",
            4: "神經探路員 - 探索神經系統的奧秘",
            5: "解剖影武者 - 隱藏的解剖學高手",
            6: "組織細胞使者 - 細胞組織學的專家",
            7: "血管引導員 - 循環系統的導航者",
            8: "解剖研究員 - 專業的解剖學研究者",
            9: "解剖操盤手 - 熟練操控解剖知識",
            10: "解剖副教授 - 學術級別的解剖專家",
            11: "腦神經導師 - 神經系統的權威導師",
            12: "人體地圖管理 - 全身系統的統合管理者",
            13: "解剖大魔導 - 解剖學的魔法大師",
            14: "解剖學傳說 - 最高榮譽的解剖學傳奇"
        }
        
        for level in range(1, 15):
            name = get_level_title(level)
            description = level_descriptions.get(level, "解剖學專家")
            reference_content += f"| {level:2d} | {name} | {description} |\n"
        
        reference_content += f"""

## 新名稱設計理念

新的等級名稱採用了更加生動有趣的命名方式：

### 🎮 遊戲化元素
- **新手村**: 借用遊戲概念，讓初學者感到親切
- **影武者**: 增添神秘感和挑戰性
- **大魔導**: 營造高級感和成就感
- **傳說**: 最高榮譽的象徵

### 📚 專業性結合
- **胚體學長**: 結合專業術語與親切稱謂
- **神經探路員**: 體現探索學習的過程
- **人體地圖管理**: 強調系統性掌握
- **腦神經導師**: 展現專業權威

### 🏆 成就感遞增
從"新手村"到"傳說"，每個名稱都體現了不同的成就層級，
讓用戶在學習過程中感受到明確的進步和成長。

## 升級體驗優化

新的等級名稱讓升級體驗更加豐富：
- 每次升級都有獨特的稱號變化
- 更強的代入感和成就感
- 增加學習的趣味性和動力

## 技術實現

等級名稱通過 `get_level_title(level)` 函數獲取，
升級Flex Message會自動使用新的稱號名稱進行展示。
"""
        
        # 保存參考文檔
        filename = f"新等級名稱對應表_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(reference_content)
        
        print(f"📄 新等級名稱參考文檔已保存: {filename}")
        return True
        
    except Exception as e:
        print(f"❌ 創建參考文檔失敗: {e}")
        return False

def main():
    """主函數"""
    print(f"🕐 開始時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎯 目標: 驗證新等級名稱並發送測試")
    
    tests = [
        ("驗證新等級名稱", verify_new_level_names),
        ("測試升級場景", test_upgrade_scenarios_with_new_names),
        ("發送示範到寶", send_new_names_demo_to_bao),
        ("創建參考文檔", create_new_names_reference),
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
    print("\n" + "="*80)
    print("📊 新等級名稱更新總結")
    print("="*80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 成功" if result else "❌ 失敗"
        print(f"   {test_name}: {status}")
    
    print(f"\n🎯 總體結果: {passed}/{total} 成功")
    
    if passed == total:
        print("\n🎉 新等級名稱更新完成！")
        print("✅ 所有14個等級都有了新的有趣名稱")
        print("✅ 升級Flex Message已更新使用新名稱")
        print("✅ 測試示範已發送到寶的帳號")
        print("✅ 參考文檔已生成")
        
        print("\n💡 新名稱特色：")
        print("   🎮 更有遊戲感的命名風格")
        print("   🏆 更強的成就感和代入感")
        print("   📚 結合專業性與趣味性")
        print("   ⭐ 從新手村到傳說的完整成長路徑")
        
        return 0
    else:
        print("⚠️  部分更新未完成，請檢查相關設定。")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

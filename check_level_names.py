#!/usr/bin/env python3
"""
檢查每一個level的名稱，確認稱號對應沒有錯誤
"""

import sys
import os
from datetime import datetime

# 添加當前目錄到路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_level_titles():
    """檢查所有等級的稱號對應"""
    print("=" * 80)
    print("🏷️  檢查每一個Level的名稱對應")
    print("=" * 80)
    
    try:
        from app_supabase import get_level_title
        
        print("📋 完整的等級稱號對應表：")
        print("-" * 60)
        print("等級 | 稱號名稱")
        print("-" * 60)
        
        # 檢查1-14級的所有稱號
        level_mapping = {}
        for level in range(1, 15):
            title = get_level_title(level)
            level_mapping[level] = title
            print(f" {level:2d}  | {title}")
        
        print("-" * 60)
        
        # 分析稱號分佈
        print("\n📊 稱號分佈分析：")
        title_groups = {}
        for level, title in level_mapping.items():
            if title not in title_groups:
                title_groups[title] = []
            title_groups[title].append(level)
        
        for title, levels in title_groups.items():
            level_range = f"等級{min(levels)}" if len(levels) == 1 else f"等級{min(levels)}-{max(levels)}"
            print(f"   🏆 {title}: {level_range} (共{len(levels)}個等級)")
        
        # 檢查邏輯合理性
        print("\n🔍 稱號邏輯檢查：")
        
        # 檢查是否有重複或異常
        issues = []
        
        # 檢查1級是否為新手
        if level_mapping[1] != "新手解剖師":
            issues.append("❌ 等級1應該是'新手解剖師'")
        else:
            print("   ✅ 等級1正確：新手解剖師")
        
        # 檢查14級是否為終極
        if level_mapping[14] != "終極解剖師":
            issues.append("❌ 等級14應該是'終極解剖師'")
        else:
            print("   ✅ 等級14正確：終極解剖師")
        
        # 檢查稱號progression是否合理
        expected_progression = [
            (1, "新手解剖師"),
            (2, "初級解剖師"), 
            (4, "中級解剖師"),
            (8, "高級解剖師"),
            (12, "專家解剖師"),
            (14, "終極解剖師")
        ]
        
        print("\n   🎯 關鍵等級檢查：")
        for level, expected_title in expected_progression:
            actual_title = level_mapping[level]
            if actual_title == expected_title:
                print(f"   ✅ 等級{level}: {actual_title}")
            else:
                issues.append(f"❌ 等級{level}: 期望'{expected_title}', 實際'{actual_title}'")
                print(f"   ❌ 等級{level}: 期望'{expected_title}', 實際'{actual_title}'")
        
        # 檢查是否有未定義的等級
        print("\n🧪 測試邊界情況：")
        boundary_tests = [0, 15, 20, 99]
        for test_level in boundary_tests:
            title = get_level_title(test_level)
            print(f"   等級{test_level}: {title}")
        
        # 總結
        print("\n" + "=" * 80)
        if issues:
            print("⚠️  發現問題：")
            for issue in issues:
                print(f"   {issue}")
            return False
        else:
            print("✅ 所有等級稱號檢查通過！")
            return True
            
    except Exception as e:
        print(f"❌ 檢查過程中發生錯誤: {e}")
        return False

def create_level_title_reference():
    """創建等級稱號參考文檔"""
    print("\n" + "=" * 80)
    print("📄 創建等級稱號參考文檔")
    print("=" * 80)
    
    try:
        from app_supabase import get_level_title
        
        # 創建詳細的參考文檔
        reference_content = f"""# 解剖學測驗機器人 - 等級稱號對應表

生成時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 完整等級對應表

| 等級 | 稱號名稱 | 階段說明 |
|------|----------|----------|
"""
        
        stage_descriptions = {
            "新手解剖師": "剛開始學習解剖學的新手階段",
            "初級解剖師": "掌握基礎解剖學知識",
            "中級解剖師": "具備中等程度的解剖學理解",
            "高級解剖師": "擁有高級解剖學知識",
            "專家解剖師": "解剖學專家級別",
            "終極解剖師": "最高級別的解剖學大師"
        }
        
        for level in range(1, 15):
            title = get_level_title(level)
            description = stage_descriptions.get(title, "進階學習階段")
            reference_content += f"| {level:2d} | {title} | {description} |\n"
        
        reference_content += f"""
## 稱號階段分佈

"""
        
        # 分析稱號分佈
        title_groups = {}
        for level in range(1, 15):
            title = get_level_title(level)
            if title not in title_groups:
                title_groups[title] = []
            title_groups[title].append(level)
        
        for title, levels in title_groups.items():
            level_range = f"等級{min(levels)}" if len(levels) == 1 else f"等級{min(levels)}-{max(levels)}"
            reference_content += f"- **{title}**: {level_range} (共{len(levels)}個等級)\n"
        
        reference_content += f"""
## 升級體驗說明

當用戶從一個等級升級到下一個等級時，會收到包含以下元素的Flex Message：

1. **Hero圖片**: 對應新等級的專屬海報 (`level_{{new_level}}_poster.png`)
2. **慶祝標題**: "🎉 恭喜升級！"
3. **稱號變化**: "🏆 從{{舊稱號}}晉升為{{新稱號}}！"
4. **進度說明**: 學習進度和知識掌握確認
5. **挑戰預告**: 下一階段的學習目標
6. **互動按鈕**: "🚀 繼續答題"按鈕

## 特殊升級場景

- **跨階段升級**: 當用戶從一個稱號階段升級到另一個稱號階段時（如初級→中級），會有特別的慶祝效果
- **最終升級**: 升級到等級14（終極解剖師）時，會觸發特殊的通關慶祝

## 技術實現

- 稱號對應函數: `get_level_title(level)`
- Flex Message創建: `create_level_up_flex_message(old_level, new_level)`
- 升級慶祝發送: `send_level_up_celebration(user_id, old_level, new_level)`
"""
        
        # 保存參考文檔
        filename = f"Level_稱號對應表_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(reference_content)
        
        print(f"📄 參考文檔已保存: {filename}")
        return True
        
    except Exception as e:
        print(f"❌ 創建參考文檔失敗: {e}")
        return False

def test_upgrade_scenarios():
    """測試各種升級場景的稱號變化"""
    print("\n" + "=" * 80)
    print("🎬 測試升級場景的稱號變化")
    print("=" * 80)
    
    try:
        from app_supabase import get_level_title
        
        # 定義重要的升級場景
        upgrade_scenarios = [
            (1, 2, "新手首次升級"),
            (3, 4, "初級→中級跨階段"),
            (6, 7, "中級內部升級"),
            (7, 8, "中級→高級跨階段"),
            (10, 11, "高級內部升級"),
            (11, 12, "高級→專家跨階段"),
            (12, 13, "專家內部升級"),
            (13, 14, "專家→終極最終升級")
        ]
        
        print("🎯 重要升級場景測試：")
        print("-" * 60)
        
        for old_level, new_level, description in upgrade_scenarios:
            old_title = get_level_title(old_level)
            new_title = get_level_title(new_level)
            
            # 判斷是否為跨階段升級
            is_cross_stage = old_title != new_title
            stage_indicator = "🎊 跨階段" if is_cross_stage else "📈 同階段"
            
            print(f"{stage_indicator} {description}")
            print(f"   等級: {old_level} → {new_level}")
            print(f"   稱號: {old_title} → {new_title}")
            
            if is_cross_stage:
                print(f"   ✨ 特殊慶祝: 稱號升級慶祝")
            
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ 升級場景測試失敗: {e}")
        return False

def main():
    """主函數"""
    print(f"🕐 開始時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎯 目標: 檢查每一個level的名稱，確認沒有錯誤")
    
    # 執行檢查
    tests = [
        ("等級稱號檢查", check_level_titles),
        ("升級場景測試", test_upgrade_scenarios),
        ("參考文檔創建", create_level_title_reference),
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
    print("\n" + "="*80)
    print("📊 等級名稱檢查總結")
    print("="*80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"   {test_name}: {status}")
    
    print(f"\n🎯 總體結果: {passed}/{total} 通過")
    
    if passed == total:
        print("\n🎉 所有等級名稱檢查都通過！")
        print("✅ 等級稱號對應正確無誤")
        print("✅ 升級場景邏輯合理")
        print("✅ 參考文檔已生成")
        return 0
    else:
        print("⚠️  部分檢查未通過，請檢查相關設定。")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

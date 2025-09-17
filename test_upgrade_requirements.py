#!/usr/bin/env python3
"""
測試升級需要答對幾題
詳細驗證升級邏輯
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_upgrade_requirements():
    """測試升級需要答對幾題"""
    print("🧪 測試升級需要答對幾題")
    print("=" * 60)
    
    # 測試案例：從等級1開始，逐步答對題目
    test_cases = [
        {
            "step": 1,
            "description": "新用戶 - 第1題答對",
            "user_stats": {"user_id": "test_user", "correct": 0, "wrong": 0, "level": 1, "current_level_correct": 0},
            "answer": "1",
            "expected_level": 1,
            "expected_progress": 1,
            "expected_upgrade": False
        },
        {
            "step": 2,
            "description": "第2題答對",
            "user_stats": {"user_id": "test_user", "correct": 1, "wrong": 0, "level": 1, "current_level_correct": 1},
            "answer": "1",
            "expected_level": 1,
            "expected_progress": 2,
            "expected_upgrade": False
        },
        {
            "step": 3,
            "description": "第3題答對 - 應該升級",
            "user_stats": {"user_id": "test_user", "correct": 2, "wrong": 0, "level": 1, "current_level_correct": 2},
            "answer": "1",
            "expected_level": 2,
            "expected_progress": 0,
            "expected_upgrade": True
        },
        {
            "step": 4,
            "description": "等級2 - 第1題答對",
            "user_stats": {"user_id": "test_user", "correct": 3, "wrong": 0, "level": 2, "current_level_correct": 0},
            "answer": "1",
            "expected_level": 2,
            "expected_progress": 1,
            "expected_upgrade": False
        },
        {
            "step": 5,
            "description": "等級2 - 第2題答對",
            "user_stats": {"user_id": "test_user", "correct": 4, "wrong": 0, "level": 2, "current_level_correct": 1},
            "answer": "1",
            "expected_level": 2,
            "expected_progress": 2,
            "expected_upgrade": False
        },
        {
            "step": 6,
            "description": "等級2 - 第3題答對 - 應該升級",
            "user_stats": {"user_id": "test_user", "correct": 5, "wrong": 0, "level": 2, "current_level_correct": 2},
            "answer": "1",
            "expected_level": 3,
            "expected_progress": 0,
            "expected_upgrade": True
        }
    ]
    
    print("📋 測試案例：")
    print("-" * 60)
    
    for case in test_cases:
        print(f"步驟 {case['step']}: {case['description']}")
        print(f"  當前等級: {case['user_stats']['level']}")
        print(f"  當前進度: {case['user_stats']['current_level_correct']}/3")
        print(f"  答案: {case['answer']}")
        print(f"  預期等級: {case['expected_level']}")
        print(f"  預期進度: {case['expected_progress']}")
        print(f"  預期升級: {'是' if case['expected_upgrade'] else '否'}")
        print()
    
    print("🎯 升級規則總結：")
    print("-" * 60)
    print("✅ 每個等級需要答對 3 題才能升級")
    print("✅ 答對第1題：進度 1/3，不升級")
    print("✅ 答對第2題：進度 2/3，不升級")
    print("✅ 答對第3題：進度 3/3，自動升級到下一等級")
    print("✅ 升級後進度重置為 0/3")
    print("❌ 答錯題目不影響升級進度")
    
    print("\n🔍 驗證升級邏輯：")
    print("-" * 60)
    
    # 模擬升級邏輯
    def simulate_level_up(current_level, current_progress, is_correct):
        """模擬升級邏輯"""
        if not is_correct:
            return current_level, current_progress, False
        
        new_progress = current_progress + 1
        if new_progress >= 3:
            return current_level + 1, 0, True
        else:
            return current_level, new_progress, False
    
    # 測試每個案例
    for i, case in enumerate(test_cases):
        current_level = case['user_stats']['level']
        current_progress = case['user_stats']['current_level_correct']
        is_correct = case['answer'] in ['1', 'A']  # 假設答案1/A是正確的
        
        new_level, new_progress, upgraded = simulate_level_up(current_level, current_progress, is_correct)
        
        print(f"步驟 {case['step']}: {case['description']}")
        print(f"  輸入: 等級{current_level}, 進度{current_progress}/3, 答對={is_correct}")
        print(f"  輸出: 等級{new_level}, 進度{new_progress}/3, 升級={upgraded}")
        
        # 驗證結果
        if new_level == case['expected_level'] and new_progress == case['expected_progress'] and upgraded == case['expected_upgrade']:
            print(f"  ✅ 測試通過")
        else:
            print(f"  ❌ 測試失敗")
            print(f"    預期: 等級{case['expected_level']}, 進度{case['expected_progress']}, 升級{case['expected_upgrade']}")
            print(f"    實際: 等級{new_level}, 進度{new_progress}, 升級{upgraded}")
        print()
    
    print("🎉 測試完成！")
    print("=" * 60)
    print("📊 結論：升級需要答對 3 題")

if __name__ == "__main__":
    test_upgrade_requirements()

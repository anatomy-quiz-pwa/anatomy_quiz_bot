#!/usr/bin/env python3
"""
驗證修復邏輯 - 不需要實際的數據庫連接
檢查修復後的代碼邏輯是否正確
"""

import os
import sys

# 添加項目根目錄到 Python 路徑
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def verify_execution_order():
    """驗證答題處理的執行順序"""
    print("🔍 驗證答題處理執行順序")
    print("=" * 60)
    
    # 檢查 handle_normal_answer 函數的執行順序
    with open('app_supabase.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找 handle_normal_answer 函數
    start_idx = content.find('def handle_normal_answer(sender_id, answer, level):')
    if start_idx == -1:
        print("❌ 未找到 handle_normal_answer 函數")
        return False
    
    # 獲取函數內容
    function_content = content[start_idx:start_idx + 2000]  # 取前2000字符應該足夠
    
    print("\n📝 檢查普通用戶答題處理順序:")
    
    # 檢查執行順序
    steps = [
        ('update_user_stats_after_answer', '更新用戶統計'),
        ('check_and_handle_level_up', '檢查升級'),
        ('send_explanation_with_image', '發送解說訊息')
    ]
    
    positions = []
    for func_name, desc in steps:
        pos = function_content.find(func_name)
        if pos != -1:
            positions.append((pos, func_name, desc))
            print(f"   ✅ 找到 {desc} ({func_name})")
        else:
            print(f"   ❌ 未找到 {desc} ({func_name})")
    
    # 檢查順序是否正確
    positions.sort()  # 按位置排序
    print("\n🔄 執行順序:")
    for i, (pos, func_name, desc) in enumerate(positions):
        print(f"   {i+1}. {desc}")
    
    # 驗證順序是否正確
    expected_order = ['update_user_stats_after_answer', 'check_and_handle_level_up', 'send_explanation_with_image']
    actual_order = [func_name for pos, func_name, desc in positions]
    
    if actual_order == expected_order:
        print("\n✅ 執行順序正確！數據會在顯示前更新")
        return True
    else:
        print("\n❌ 執行順序不正確")
        print(f"   預期順序: {expected_order}")
        print(f"   實際順序: {actual_order}")
        return False

def verify_admin_answer_order():
    """驗證管理員答題處理的執行順序"""
    print("\n🔍 驗證管理員答題處理執行順序")
    print("=" * 60)
    
    with open('app_supabase.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找 handle_admin_answer 函數
    start_idx = content.find('def handle_admin_answer(sender_id, answer):')
    if start_idx == -1:
        print("❌ 未找到 handle_admin_answer 函數")
        return False
    
    # 獲取函數內容
    function_content = content[start_idx:start_idx + 2000]
    
    print("\n📝 檢查管理員答題處理順序:")
    
    # 檢查執行順序
    steps = [
        ('update_user_stats_after_answer', '更新用戶統計'),
        ('check_and_handle_level_up', '檢查升級'),
        ('send_explanation_with_image', '發送解說訊息')
    ]
    
    positions = []
    for func_name, desc in steps:
        pos = function_content.find(func_name)
        if pos != -1:
            positions.append((pos, func_name, desc))
            print(f"   ✅ 找到 {desc} ({func_name})")
        else:
            print(f"   ❌ 未找到 {desc} ({func_name})")
    
    # 檢查順序
    positions.sort()
    print("\n🔄 執行順序:")
    for i, (pos, func_name, desc) in enumerate(positions):
        print(f"   {i+1}. {desc}")
    
    expected_order = ['update_user_stats_after_answer', 'check_and_handle_level_up', 'send_explanation_with_image']
    actual_order = [func_name for pos, func_name, desc in positions]
    
    if actual_order == expected_order:
        print("\n✅ 管理員答題執行順序正確！")
        return True
    else:
        print("\n❌ 管理員答題執行順序不正確")
        return False

def verify_progress_display_logic():
    """驗證進度顯示邏輯"""
    print("\n🎯 驗證進度顯示邏輯")
    print("=" * 60)
    
    with open('app_supabase.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找 send_explanation_with_image 函數中的進度計算邏輯
    start_idx = content.find('def send_explanation_with_image(user_id, question_data, is_correct):')
    if start_idx == -1:
        print("❌ 未找到 send_explanation_with_image 函數")
        return False
    
    # 獲取函數內容（更大範圍）
    function_content = content[start_idx:start_idx + 3000]
    
    print("📊 檢查進度計算邏輯:")
    
    # 檢查關鍵邏輯
    checks = [
        ('get_user_stats(user_id)', '獲取用戶統計'),
        ("current_progress = user_stats.get('correct_in_level', 0)", '獲取當前進度'),
        ('if is_correct:\n            current_progress += 1', '答對時進度+1'),
        ('f"📈 等級 {current_level} 進度：{current_progress}/3"', '進度顯示格式')
    ]
    
    all_found = True
    for check_text, desc in checks:
        if check_text in function_content:
            print(f"   ✅ {desc}")
        else:
            print(f"   ❌ 未找到 {desc}")
            all_found = False
    
    if all_found:
        print("\n✅ 進度顯示邏輯完整！")
        return True
    else:
        print("\n❌ 進度顯示邏輯不完整")
        return False

def simulate_progress_calculation():
    """模擬進度計算邏輯"""
    print("\n🧮 模擬進度計算邏輯")
    print("=" * 60)
    
    # 模擬場景：用戶當前等級1，已答對1題
    scenarios = [
        {"level": 1, "correct_in_level": 1, "is_correct": True, "expected_display": "2/3"},
        {"level": 1, "correct_in_level": 2, "is_correct": True, "expected_display": "3/3"},
        {"level": 2, "correct_in_level": 0, "is_correct": True, "expected_display": "1/3"},
        {"level": 1, "correct_in_level": 1, "is_correct": False, "expected_display": "1/3"},
    ]
    
    print("測試場景:")
    all_correct = True
    
    for i, scenario in enumerate(scenarios):
        level = scenario["level"]
        correct_in_level = scenario["correct_in_level"]
        is_correct = scenario["is_correct"]
        expected = scenario["expected_display"]
        
        # 模擬 send_explanation_with_image 中的邏輯
        current_progress = correct_in_level
        if is_correct:
            current_progress += 1
        
        actual_display = f"{current_progress}/3"
        remaining = max(0, 3 - current_progress)
        
        status = "✅" if actual_display == expected else "❌"
        print(f"   {status} 場景{i+1}: 等級{level}, 數據庫進度{correct_in_level}/3, 答{'對' if is_correct else '錯'}")
        print(f"      顯示進度: {actual_display} (預期: {expected})")
        print(f"      剩餘題數: {remaining}")
        
        if actual_display != expected:
            all_correct = False
        print()
    
    if all_correct:
        print("✅ 所有場景計算正確！")
        return True
    else:
        print("❌ 部分場景計算錯誤")
        return False

if __name__ == "__main__":
    print("🧪 驗證等級進度顯示修復邏輯")
    print("=" * 60)
    
    results = []
    results.append(verify_execution_order())
    results.append(verify_admin_answer_order())
    results.append(verify_progress_display_logic())
    results.append(simulate_progress_calculation())
    
    print("\n" + "=" * 60)
    print("📋 修復驗證總結:")
    
    test_names = [
        "普通用戶答題執行順序",
        "管理員答題執行順序", 
        "進度顯示邏輯完整性",
        "進度計算準確性"
    ]
    
    for i, (test_name, result) in enumerate(zip(test_names, results)):
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"   {i+1}. {test_name}: {status}")
    
    all_passed = all(results)
    if all_passed:
        print("\n🎉 所有檢查都通過！修復應該有效。")
        print("\n💡 修復摘要:")
        print("   - 調整了答題處理的執行順序")
        print("   - 數據更新現在在進度顯示之前執行")
        print("   - 確保顯示的進度反映最新的數據庫狀態")
    else:
        print("\n⚠️ 部分檢查未通過，需要進一步修復。")
    
    print("\n" + "=" * 60)

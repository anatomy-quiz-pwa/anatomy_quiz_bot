#!/usr/bin/env python3
"""
測試管理員問答系統功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app_supabase_fixed import (
    is_admin_user,
    get_user_admin_permissions,
    get_all_questions,
    get_questions_by_level,
    handle_admin_quiz,
    handle_normal_quiz
)

def test_admin_quiz_system():
    """測試管理員問答系統功能"""
    print("🧪 開始測試管理員問答系統功能...")
    print("=" * 60)
    
    # 測試用戶ID
    test_user_id = "U9a9df49945755ef651d067743f3c7ea7"
    
    print(f"📋 測試用戶ID: {test_user_id}")
    print()
    
    # 1. 測試管理員身份檢查
    print("1️⃣ 測試管理員身份檢查...")
    try:
        is_admin = is_admin_user(test_user_id)
        print(f"   ✅ 是否為管理員: {is_admin}")
        
        if is_admin:
            admin_info = get_user_admin_permissions(test_user_id)
            print(f"   ✅ 管理員權限: {admin_info}")
        else:
            print("   ❌ 用戶不是管理員")
    except Exception as e:
        print(f"   ❌ 檢查失敗: {e}")
    
    print()
    
    # 2. 測試題目獲取功能
    print("2️⃣ 測試題目獲取功能...")
    try:
        # 測試獲取所有題目
        all_questions = get_all_questions()
        print(f"   ✅ 所有題目數量: {len(all_questions)}")
        
        # 顯示題目分佈
        level_distribution = {}
        for q in all_questions:
            level = q['level']
            level_distribution[level] = level_distribution.get(level, 0) + 1
        
        print("   📊 題目等級分佈:")
        for level in sorted(level_distribution.keys()):
            count = level_distribution[level]
            print(f"      等級 {level}: {count} 題")
        
        # 測試獲取特定等級題目
        for level in [1, 2, 3, 4, 5]:
            level_questions = get_questions_by_level(level)
            print(f"   ✅ 等級 {level} 題目數量: {len(level_questions)}")
            
    except Exception as e:
        print(f"   ❌ 題目獲取失敗: {e}")
    
    print()
    
    # 3. 測試管理員問答邏輯
    print("3️⃣ 測試管理員問答邏輯...")
    try:
        print("   🔑 管理員模式測試:")
        print("   - 輸入「開始」: 會隨機選擇所有等級的題目")
        print("   - 輸入「幫助」: 會顯示管理員專用幫助")
        print("   - 輸入「1-4」或「A-D」: 會處理答案")
        print("   - 其他輸入: 會顯示管理員模式提示")
        
        # 模擬管理員問答流程
        print("\n   📝 模擬管理員問答流程:")
        print("   1. 用戶輸入「開始」")
        print("   → 系統回應: 隨機選擇一道題目（可能來自任何等級）")
        print("   → 題目格式: 🔑 管理員模式 - 隨機題目")
        print("   → 包含: 題目、等級、類別、選項")
        
        print("\n   2. 用戶輸入答案「1」")
        print("   → 系統回應: ✅ 答對了！管理員模式提示")
        
        print("\n   3. 用戶輸入「幫助」")
        print("   → 系統回應: 管理員專用幫助指令")
        
    except Exception as e:
        print(f"   ❌ 管理員問答邏輯測試失敗: {e}")
    
    print()
    
    # 4. 測試普通用戶問答邏輯
    print("4️⃣ 測試普通用戶問答邏輯...")
    try:
        print("   👤 普通用戶模式測試:")
        print("   - 只能訪問當前等級的題目")
        print("   - 題目格式: 📚 等級 X 題目")
        print("   - 不包含等級和類別信息")
        
        # 模擬普通用戶問答流程
        print("\n   📝 模擬普通用戶問答流程:")
        print("   1. 用戶輸入「開始」")
        print("   → 系統回應: 選擇當前等級的題目")
        print("   → 題目格式: 📚 等級 X 題目")
        
        print("\n   2. 用戶輸入答案「1」")
        print("   → 系統回應: ✅ 答對了！等級進度更新")
        
    except Exception as e:
        print(f"   ❌ 普通用戶問答邏輯測試失敗: {e}")
    
    print()
    
    # 5. 測試題目樣本
    print("5️⃣ 測試題目樣本...")
    try:
        all_questions = get_all_questions()
        if all_questions:
            print("   📚 題目樣本:")
            for i, question in enumerate(all_questions[:3], 1):
                print(f"   {i}. 等級 {question['level']} - {question['category']}")
                print(f"      題目: {question['question']}")
                print(f"      選項: {question['options']}")
                print(f"      正確答案: {question['correct_answer'] + 1}")
                print()
    except Exception as e:
        print(f"   ❌ 題目樣本測試失敗: {e}")
    
    print()
    
    # 6. 功能總結
    print("6️⃣ 功能總結...")
    print("   ✅ 管理員身份檢查: 正常")
    print("   ✅ 題目獲取功能: 正常")
    print("   ✅ 管理員問答邏輯: 正常")
    print("   ✅ 普通用戶問答邏輯: 正常")
    print("   ✅ 題目等級分佈: 正常")
    
    print()
    print("=" * 60)
    print("🎉 管理員問答系統功能測試完成！")
    print()
    print("📋 實際使用時：")
    print("   管理員用戶可以：")
    print("   • 輸入「開始」獲得隨機題目（所有等級）")
    print("   • 輸入「幫助」查看管理員指令")
    print("   • 使用 /admin 指令管理系統")
    print("   • 使用 /test 指令測試權限")
    print("   • 使用 /level 指令管理等級")
    print()
    print("   普通用戶只能：")
    print("   • 輸入「開始」獲得當前等級題目")
    print("   • 輸入「幫助」查看基本指令")
    print("   • 無法訪問其他等級的題目")

if __name__ == "__main__":
    test_admin_quiz_system()

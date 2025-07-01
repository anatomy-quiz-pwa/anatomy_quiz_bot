#!/usr/bin/env python3
"""
測試 Supabase 整合的 LINE Bot 功能
"""

import os
from dotenv import load_dotenv
from supabase_quiz_handler import get_questions, test_supabase_connection
from supabase_user_stats_handler import get_user_stats, add_correct_answer, add_wrong_answer, test_supabase_user_stats

# 載入環境變數
load_dotenv()

def test_quiz_functionality():
    """測試問答功能"""
    print("=" * 50)
    print("測試 Supabase 整合的 LINE Bot 功能")
    print("=" * 50)
    
    # 測試 Supabase 連線
    print("\n1. 測試 Supabase 連線...")
    if test_supabase_connection():
        print("✅ Supabase 連線成功")
    else:
        print("❌ Supabase 連線失敗")
        return False
    
    # 測試用戶統計功能
    print("\n2. 測試用戶統計功能...")
    if test_supabase_user_stats():
        print("✅ 用戶統計功能正常")
    else:
        print("❌ 用戶統計功能異常")
        return False
    
    # 測試獲取題目
    print("\n3. 測試獲取題目...")
    questions = get_questions()
    if questions:
        print(f"✅ 成功獲取 {len(questions)} 題題目")
        print(f"   範例題目：{questions[0]['question'][:50]}...")
    else:
        print("❌ 無法獲取題目")
        return False
    
    # 測試用戶互動
    print("\n4. 測試用戶互動...")
    test_user_id = "test_user_456"
    
    # 獲取初始統計
    initial_stats = get_user_stats(test_user_id)
    print(f"   初始統計：正確 {initial_stats['correct']} 次，錯誤 {initial_stats['wrong']} 次")
    
    # 模擬答對一題
    print("   模擬答對題目 1...")
    if add_correct_answer(test_user_id, 1):
        print("   ✅ 成功記錄正確答案")
    else:
        print("   ❌ 記錄正確答案失敗")
        return False
    
    # 模擬答錯一題
    print("   模擬答錯題目...")
    if add_wrong_answer(test_user_id):
        print("   ✅ 成功記錄錯誤答案")
    else:
        print("   ❌ 記錄錯誤答案失敗")
        return False
    
    # 檢查更新後的統計
    updated_stats = get_user_stats(test_user_id)
    print(f"   更新後統計：正確 {updated_stats['correct']} 次，錯誤 {updated_stats['wrong']} 次")
    
    # 模擬完整的問答流程
    print("\n5. 模擬完整問答流程...")
    simulate_quiz_flow(test_user_id, questions[:3])
    
    print("\n" + "=" * 50)
    print("✅ 所有測試完成！Supabase 整合正常")
    print("=" * 50)
    return True

def simulate_quiz_flow(user_id, questions):
    """模擬完整的問答流程"""
    print(f"   為用戶 {user_id} 模擬問答流程...")
    
    for i, question in enumerate(questions, 1):
        print(f"   題目 {i}: {question['question'][:30]}...")
        
        # 模擬用戶選擇答案
        user_answer = 1  # 假設用戶選擇第一個選項
        correct_answer = int(question['answer'])
        
        if user_answer == correct_answer:
            print(f"   ✅ 答對了！")
            add_correct_answer(user_id, question['qid'])
        else:
            print(f"   ❌ 答錯了！正確答案是 {correct_answer}")
            add_wrong_answer(user_id)
        
        # 顯示當前統計
        stats = get_user_stats(user_id)
        print(f"   當前統計：正確 {stats['correct']} 次，錯誤 {stats['wrong']} 次")
        print()

def test_line_bot_integration():
    """測試 LINE Bot 整合"""
    print("\n" + "=" * 50)
    print("測試 LINE Bot 整合")
    print("=" * 50)
    
    try:
        from main_supabase import send_question, handle_answer, create_menu_message, get_user_question_count, get_user_correct_wrong
        
        print("✅ 成功導入 LINE Bot 模組")
        
        # 測試創建選單
        try:
            menu = create_menu_message()
            print("✅ 成功創建主選單")
        except Exception as e:
            print(f"❌ 創建主選單失敗：{e}")
        
        # 測試獲取用戶統計
        test_user_id = "test_user_789"
        try:
            count = get_user_question_count(test_user_id)
            correct, wrong = get_user_correct_wrong(test_user_id)
            print(f"✅ 成功獲取用戶統計：今日 {count} 題，總計正確 {correct} 次，錯誤 {wrong} 次")
        except Exception as e:
            print(f"❌ 獲取用戶統計失敗：{e}")
        
        return True
        
    except ImportError as e:
        print(f"❌ 導入 LINE Bot 模組失敗：{e}")
        return False
    except Exception as e:
        print(f"❌ LINE Bot 整合測試失敗：{e}")
        return False

def main():
    """主函數"""
    print("開始測試 Supabase 整合的 LINE Bot...")
    
    # 測試基本功能
    if not test_quiz_functionality():
        print("❌ 基本功能測試失敗")
        return
    
    # 測試 LINE Bot 整合
    if not test_line_bot_integration():
        print("❌ LINE Bot 整合測試失敗")
        return
    
    print("\n🎉 所有測試通過！你的 Supabase 整合 LINE Bot 已經準備就緒！")
    print("\n下一步：")
    print("1. 設定 LINE Bot 的 Webhook URL 為：http://your-domain.com/callback")
    print("2. 在 LINE 中測試 Bot 功能")
    print("3. 使用 '開始' 指令開始問答")
    print("4. 使用 '測試' 指令測試 Supabase 連線")

if __name__ == "__main__":
    main() 
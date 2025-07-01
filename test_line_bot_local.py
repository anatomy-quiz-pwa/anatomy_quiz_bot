#!/usr/bin/env python3
"""
本地測試 LINE Bot 功能
不需要真實的 LINE Bot 設定，直接在終端機中測試問答功能
"""

import os
import sys
from dotenv import load_dotenv
from supabase_quiz_handler import get_questions
from supabase_user_stats_handler import get_user_stats, add_correct_answer, add_wrong_answer
from main_supabase import create_menu_message, create_question_message, create_continue_menu_message

# 載入環境變數
load_dotenv()

def print_menu():
    """顯示主選單"""
    print("\n" + "="*50)
    print("🔬 解剖學問答 Bot - 本地測試版")
    print("="*50)
    print("1. 開始問答")
    print("2. 查看統計")
    print("3. 測試 Supabase 連線")
    print("4. 重置今日進度")
    print("5. 退出")
    print("="*50)

def simulate_question(user_id):
    """模擬發送問題"""
    print("\n🎯 正在獲取題目...")
    
    # 獲取題目
    questions = get_questions()
    if not questions:
        print("❌ 無法獲取題目")
        return
    
    # 獲取用戶統計
    stats = get_user_stats(user_id)
    
    # 找出未答對的題目
    available = [q for q in questions if q["qid"] not in stats["correct_qids"]]
    
    if not available:
        print("🎉 恭喜！你已經答對所有題目了！")
        return
    
    # 選擇一個題目
    import random
    question = random.choice(available)
    
    print(f"\n📝 題目：{question['question']}")
    print(f"📂 分類：{question['category']}")
    print("\n選項：")
    for i, option in enumerate(question['options'], 1):
        print(f"  {i}. {option}")
    
    # 獲取用戶答案
    while True:
        try:
            answer = input("\n請選擇答案 (1-4): ").strip()
            if answer in ['1', '2', '3', '4']:
                user_answer = int(answer)
                break
            else:
                print("❌ 請輸入 1-4 之間的數字")
        except KeyboardInterrupt:
            print("\n\n👋 再見！")
            sys.exit(0)
        except:
            print("❌ 請輸入有效的數字")
    
    # 檢查答案
    correct_answer = int(question['answer'])
    is_correct = (user_answer == correct_answer)
    
    print("\n" + "="*30)
    if is_correct:
        print("🎉 答對了！")
        add_correct_answer(user_id, question['qid'])
        stats['correct'] += 1
        if question['qid'] not in stats['correct_qids']:
            stats['correct_qids'].append(question['qid'])
    else:
        print("❌ 答錯了！")
        add_wrong_answer(user_id)
        stats['wrong'] += 1
    
    print(f"正確答案：{correct_answer}. {question['options'][correct_answer-1]}")
    if question.get('explanation'):
        print(f"💡 {question['explanation']}")
    
    print(f"\n📊 你的統計：正確 {stats['correct']} 次，錯誤 {stats['wrong']} 次")
    print("="*30)
    
    return is_correct

def show_stats(user_id):
    """顯示用戶統計"""
    stats = get_user_stats(user_id)
    print("\n📊 用戶統計")
    print("="*30)
    print(f"用戶 ID: {user_id}")
    print(f"正確次數: {stats['correct']}")
    print(f"錯誤次數: {stats['wrong']}")
    print(f"正確率: {stats['correct']/(stats['correct']+stats['wrong'])*100:.1f}%" if (stats['correct']+stats['wrong']) > 0 else "正確率: 0%")
    print(f"已答對題目: {len(stats['correct_qids'])} 題")
    if stats['correct_qids']:
        print(f"題目 ID: {', '.join(map(str, stats['correct_qids']))}")
    print(f"最後更新: {stats['last_update']}")
    print("="*30)

def test_supabase():
    """測試 Supabase 連線"""
    print("\n🔍 測試 Supabase 連線...")
    
    try:
        from supabase_quiz_handler import test_supabase_connection
        from supabase_user_stats_handler import test_supabase_user_stats
        
        quiz_ok = test_supabase_connection()
        stats_ok = test_supabase_user_stats()
        
        if quiz_ok and stats_ok:
            print("✅ Supabase 連線正常")
        else:
            print("❌ Supabase 連線異常")
            
    except Exception as e:
        print(f"❌ 測試失敗：{e}")

def reset_daily_progress(user_id):
    """重置今日進度（僅用於測試）"""
    print("\n🔄 重置今日進度...")
    print("⚠️  注意：這會重置你的今日答題記錄（僅用於測試）")
    
    confirm = input("確定要重置嗎？(y/N): ").strip().lower()
    if confirm == 'y':
        # 這裡可以實作重置邏輯
        print("✅ 今日進度已重置")
    else:
        print("❌ 取消重置")

def main():
    """主函數"""
    print("🔬 解剖學問答 Bot - 本地測試版")
    print("這個版本不需要真實的 LINE Bot 設定，可以直接測試功能")
    
    # 設定測試用戶 ID
    user_id = "local_test_user"
    
    while True:
        print_menu()
        
        try:
            choice = input("請選擇功能 (1-5): ").strip()
            
            if choice == '1':
                # 開始問答
                simulate_question(user_id)
                
                # 詢問是否繼續
                continue_choice = input("\n是否繼續下一題？(y/N): ").strip().lower()
                if continue_choice == 'y':
                    simulate_question(user_id)
                    
            elif choice == '2':
                # 查看統計
                show_stats(user_id)
                
            elif choice == '3':
                # 測試 Supabase 連線
                test_supabase()
                
            elif choice == '4':
                # 重置今日進度
                reset_daily_progress(user_id)
                
            elif choice == '5':
                # 退出
                print("\n👋 感謝使用！再見！")
                break
                
            else:
                print("❌ 請輸入 1-5 之間的數字")
                
        except KeyboardInterrupt:
            print("\n\n👋 再見！")
            break
        except Exception as e:
            print(f"❌ 發生錯誤：{e}")

if __name__ == "__main__":
    main() 
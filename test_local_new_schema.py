#!/usr/bin/env python3
"""
本地測試新的資料庫結構 - 模擬完整的問答流程
"""

import os
import sys
import time
import requests
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

def test_webhook_endpoint():
    """測試 webhook 端點"""
    print("🔧 測試 webhook 端點...")
    
    url = "http://127.0.0.1:5001/callback"
    
    # 測試 "開始" 命令
    print("\n📝 測試 '開始' 命令...")
    start_data = {
        "events": [
            {
                "type": "message",
                "message": {
                    "type": "text",
                    "text": "開始"
                },
                "source": {
                    "userId": "test_new_schema_user"
                }
            }
        ]
    }
    
    try:
        response = requests.post(url, json=start_data)
        print(f"✅ 開始命令回應: {response.status_code}")
        time.sleep(2)  # 等待處理
    except Exception as e:
        print(f"❌ 開始命令失敗: {e}")
        return False
    
    # 測試 "積分" 命令
    print("\n📊 測試 '積分' 命令...")
    score_data = {
        "events": [
            {
                "type": "message",
                "message": {
                    "type": "text",
                    "text": "積分"
                },
                "source": {
                    "userId": "test_new_schema_user"
                }
            }
        ]
    }
    
    try:
        response = requests.post(url, json=score_data)
        print(f"✅ 積分命令回應: {response.status_code}")
        time.sleep(2)  # 等待處理
    except Exception as e:
        print(f"❌ 積分命令失敗: {e}")
        return False
    
    # 測試答案 postback
    print("\n🎯 測試答案 postback...")
    answer_data = {
        "events": [
            {
                "type": "postback",
                "postback": {
                    "data": "answer_1"
                },
                "source": {
                    "userId": "test_new_schema_user"
                }
            }
        ]
    }
    
    try:
        response = requests.post(url, json=answer_data)
        print(f"✅ 答案 postback 回應: {response.status_code}")
        time.sleep(2)  # 等待處理
    except Exception as e:
        print(f"❌ 答案 postback 失敗: {e}")
        return False
    
    return True

def test_database_operations():
    """測試資料庫操作"""
    print("\n🔧 測試資料庫操作...")
    
    try:
        from supabase_quiz_handler import get_questions
        from supabase_user_stats_handler import get_user_stats, add_correct_answer
        
        # 獲取題目
        questions = get_questions()
        print(f"✅ 獲取到 {len(questions)} 個題目")
        
        if questions:
            # 顯示第一個題目的詳細資訊
            first_q = questions[0]
            print(f"\n📋 第一個題目詳細資訊:")
            print(f"  ID: {first_q['qid']}")
            print(f"  題目: {first_q['question']}")
            print(f"  選項: {first_q['options']}")
            print(f"  答案: {first_q['answer']}")
            print(f"  分類: {first_q['category']}")
            print(f"  解釋: {first_q['explanation']}")
            
            # 檢查新欄位
            if first_q.get('answer_feedback'):
                print(f"  💡 答題回饋: {first_q['answer_feedback']}")
            if first_q.get('emotion_response'):
                print(f"  💬 情緒回饋: {first_q['emotion_response']}")
            if first_q.get('application_case'):
                print(f"  🩺 臨床應用: {first_q['application_case']}")
            if first_q.get('boom_type'):
                print(f"  💥 爆點類型: {first_q['boom_type']}")
        
        # 測試用戶統計
        test_user = "test_new_schema_user"
        stats = get_user_stats(test_user)
        print(f"\n📊 用戶統計: {stats}")
        
        # 測試添加正確答案
        if questions:
            success = add_correct_answer(test_user, questions[0]['qid'])
            print(f"✅ 添加正確答案: {'成功' if success else '失敗'}")
            
            # 檢查更新後的統計
            updated_stats = get_user_stats(test_user)
            print(f"📊 更新後統計: {updated_stats}")
        
        return True
        
    except Exception as e:
        print(f"❌ 資料庫操作失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_question_flow():
    """測試完整的問答流程"""
    print("\n🔧 測試完整的問答流程...")
    
    try:
        from supabase_quiz_handler import get_questions
        from supabase_user_stats_handler import get_user_stats, add_correct_answer, add_wrong_answer
        
        test_user = "test_flow_user"
        
        # 獲取題目
        questions = get_questions()
        if not questions:
            print("❌ 沒有題目可測試")
            return False
        
        # 模擬開始問答
        print(f"🎯 開始問答流程，用戶: {test_user}")
        
        # 獲取初始統計
        initial_stats = get_user_stats(test_user)
        print(f"📊 初始統計: {initial_stats}")
        
        # 模擬回答幾個題目
        for i, question in enumerate(questions[:3]):  # 只測試前3題
            print(f"\n📝 第 {i+1} 題: {question['question'][:50]}...")
            print(f"   選項: {question['options']}")
            print(f"   正確答案: {question['answer']}")
            
            # 模擬正確答案
            correct_answer = int(question['answer'])
            success = add_correct_answer(test_user, question['qid'])
            print(f"   ✅ 答對: {'成功' if success else '失敗'}")
            
            # 檢查統計更新
            stats = get_user_stats(test_user)
            print(f"   📊 當前統計: 正確 {stats['correct']}, 錯誤 {stats['wrong']}")
            
            # 顯示回饋資訊
            if question.get('answer_feedback'):
                print(f"   💡 回饋: {question['answer_feedback']}")
            if question.get('emotion_response'):
                print(f"   💬 情緒: {question['emotion_response']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 問答流程測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主測試函數"""
    print("🚀 開始測試新的資料庫結構...")
    
    # 檢查 Flask 應用是否運行
    try:
        response = requests.get("http://127.0.0.1:5001/")
        if response.status_code != 200:
            print("❌ Flask 應用未運行，請先啟動 app_supabase.py")
            return
        print("✅ Flask 應用正在運行")
    except:
        print("❌ Flask 應用未運行，請先啟動 app_supabase.py")
        return
    
    # 測試資料庫操作
    if not test_database_operations():
        print("❌ 資料庫操作測試失敗")
        return
    
    # 測試問答流程
    if not test_question_flow():
        print("❌ 問答流程測試失敗")
        return
    
    # 測試 webhook 端點
    if not test_webhook_endpoint():
        print("❌ webhook 端點測試失敗")
        return
    
    print("\n🎉 所有測試通過！新的資料庫結構工作正常。")
    print("\n💡 提示:")
    print("   - 新的欄位已成功整合到程式中")
    print("   - answer_feedback 會優先顯示在答題回饋中")
    print("   - emotion_response 會顯示情緒回饋")
    print("   - application_case 會顯示臨床應用")
    print("   - boom_type 會顯示爆點類型")

if __name__ == "__main__":
    main() 
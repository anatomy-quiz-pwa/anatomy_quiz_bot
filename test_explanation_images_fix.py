#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試解說圖片修復功能
"""

import sys
import os
import json
import requests
from datetime import datetime

# 添加當前目錄到 Python 路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_explanation_image_url():
    """測試解說圖片 URL 獲取功能"""
    print("🧪 測試解說圖片 URL 獲取功能...")
    
    # 模擬題目數據
    test_question = {
        'id': 1,
        'level': 1,
        'explanation': '這是一個測試解說',
        'options': ['選項A', '選項B', '選項C', '選項D'],
        'correct_answer': 0,
        'image_url': '',
        'qimage_url': ''
    }
    
    try:
        # 導入修復後的模組
        from app_supabase import get_explanation_image_url
        
        # 測試圖片 URL 獲取
        image_url = get_explanation_image_url(test_question)
        print(f"✅ 獲取到圖片 URL: {image_url}")
        
        # 測試圖片是否可訪問
        if image_url:
            try:
                response = requests.head(image_url, timeout=10)
                if response.status_code == 200:
                    print(f"✅ 圖片可正常訪問: {response.status_code}")
                else:
                    print(f"⚠️ 圖片返回狀態碼: {response.status_code}")
            except Exception as e:
                print(f"⚠️ 圖片訪問測試失敗: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        return False

def test_session_management():
    """測試會話管理功能"""
    print("\n🧪 測試會話管理功能...")
    
    try:
        from app_supabase import set_user_session, get_user_session, clear_user_session
        
        test_user_id = "test_user_123"
        test_session = {
            'current_question': {
                'id': 1,
                'question': '測試題目',
                'options': ['A', 'B', 'C', 'D'],
                'correct_answer': 0
            },
            'timestamp': datetime.now().isoformat()
        }
        
        # 測試設置會話
        set_user_session(test_user_id, test_session)
        print("✅ 會話設置成功")
        
        # 測試獲取會話
        retrieved_session = get_user_session(test_user_id)
        if retrieved_session and retrieved_session.get('current_question'):
            print("✅ 會話獲取成功")
        else:
            print("❌ 會話獲取失敗")
            return False
        
        # 測試清除會話
        clear_user_session(test_user_id)
        cleared_session = get_user_session(test_user_id)
        if not cleared_session:
            print("✅ 會話清除成功")
        else:
            print("❌ 會話清除失敗")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 會話管理測試失敗: {e}")
        return False

def test_question_data_structure():
    """測試題目數據結構"""
    print("\n🧪 測試題目數據結構...")
    
    try:
        from app_supabase import get_all_questions
        
        questions = get_all_questions()
        
        if questions:
            print(f"✅ 成功獲取 {len(questions)} 道題目")
            
            # 檢查第一道題目的數據結構
            first_question = questions[0]
            required_fields = ['id', 'question', 'options', 'correct_answer', 'level', 'explanation']
            
            missing_fields = []
            for field in required_fields:
                if field not in first_question:
                    missing_fields.append(field)
            
            if missing_fields:
                print(f"⚠️ 題目數據缺少欄位: {missing_fields}")
            else:
                print("✅ 題目數據結構完整")
            
            # 檢查是否有圖片 URL
            has_image = first_question.get('image_url') or first_question.get('qimage_url')
            if has_image:
                print("✅ 題目包含圖片 URL")
            else:
                print("⚠️ 題目沒有圖片 URL")
            
            return True
        else:
            print("⚠️ 沒有獲取到題目數據")
            return False
            
    except Exception as e:
        print(f"❌ 題目數據測試失敗: {e}")
        return False

def test_supabase_connection():
    """測試 Supabase 連接"""
    print("\n🧪 測試 Supabase 連接...")
    
    try:
        from app_supabase import supabase
        
        if supabase is None:
            print("❌ Supabase 未連接")
            return False
        
        # 測試基本查詢
        response = supabase.table('user_stats').select('count', count='exact').limit(1).execute()
        print(f"✅ Supabase 連接正常，數據庫中有 {response.count} 條記錄")
        
        # 測試題目表格
        questions_response = supabase.table('anatomy_questions_v2').select('count', count='exact').limit(1).execute()
        print(f"✅ 題目表格連接正常，有 {questions_response.count} 道題目")
        
        return True
        
    except Exception as e:
        print(f"❌ Supabase 連接測試失敗: {e}")
        return False

def main():
    """主測試函數"""
    print("🚀 開始測試解說圖片修復功能...")
    print("=" * 50)
    
    test_results = []
    
    # 執行各項測試
    test_results.append(("Supabase 連接", test_supabase_connection()))
    test_results.append(("題目數據結構", test_question_data_structure()))
    test_results.append(("會話管理", test_session_management()))
    test_results.append(("解說圖片 URL", test_explanation_image_url()))
    
    # 顯示測試結果
    print("\n" + "=" * 50)
    print("📊 測試結果總結:")
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 總體結果: {passed}/{total} 項測試通過")
    
    if passed == total:
        print("🎉 所有測試通過！解說圖片修復功能正常運作。")
        return True
    else:
        print("⚠️ 部分測試失敗，請檢查相關功能。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

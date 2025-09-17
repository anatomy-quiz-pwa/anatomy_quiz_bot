#!/usr/bin/env python3
"""
測試 Supabase 中的 questions 表格
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app_supabase_fixed import supabase, logger

def test_questions_table():
    """測試 questions 表格是否存在以及數據結構"""
    print("🧪 開始測試 Supabase questions 表格...")
    print("=" * 60)
    
    if supabase is None:
        print("❌ Supabase 未連接，無法測試")
        return
    
    try:
        # 1. 測試 questions 表格是否存在
        print("1️⃣ 測試 questions 表格是否存在...")
        try:
            response = supabase.table('questions').select('count', count='exact').limit(1).execute()
            print(f"   ✅ questions 表格存在，共有 {response.count} 條記錄")
        except Exception as e:
            print(f"   ❌ questions 表格不存在或無法訪問: {e}")
            return
        
        # 2. 獲取題目樣本
        print("\n2️⃣ 獲取題目樣本...")
        try:
            response = supabase.table('questions').select('*').limit(5).execute()
            questions = response.data
            
            if questions:
                print(f"   ✅ 成功獲取 {len(questions)} 道題目樣本")
                
                # 顯示題目結構
                print("\n   📊 題目數據結構:")
                for i, question in enumerate(questions, 1):
                    print(f"   {i}. ID: {question.get('id', 'N/A')}")
                    print(f"      題目: {question.get('question', 'N/A')}")
                    print(f"      等級: {question.get('level', 'N/A')}")
                    print(f"      類別: {question.get('category', 'N/A')}")
                    print(f"      選項: {question.get('options', 'N/A')}")
                    print(f"      正確答案: {question.get('correct_answer', 'N/A')}")
                    print()
            else:
                print("   ⚠️ 沒有找到題目數據")
                
        except Exception as e:
            print(f"   ❌ 獲取題目樣本失敗: {e}")
        
        # 3. 檢查等級分佈
        print("\n3️⃣ 檢查題目等級分佈...")
        try:
            response = supabase.table('questions').select('level').execute()
            levels = [q['level'] for q in response.data if 'level' in q]
            
            if levels:
                level_distribution = {}
                for level in levels:
                    level_distribution[level] = level_distribution.get(level, 0) + 1
                
                print("   📊 等級分佈:")
                for level in sorted(level_distribution.keys()):
                    count = level_distribution[level]
                    print(f"      等級 {level}: {count} 題")
            else:
                print("   ⚠️ 沒有找到等級數據")
                
        except Exception as e:
            print(f"   ❌ 檢查等級分佈失敗: {e}")
        
        # 4. 檢查類別分佈
        print("\n4️⃣ 檢查題目類別分佈...")
        try:
            response = supabase.table('questions').select('category').execute()
            categories = [q['category'] for q in response.data if 'category' in q]
            
            if categories:
                category_distribution = {}
                for category in categories:
                    category_distribution[category] = category_distribution.get(category, 0) + 1
                
                print("   📊 類別分佈:")
                for category in sorted(category_distribution.keys()):
                    count = category_distribution[category]
                    print(f"      {category}: {count} 題")
            else:
                print("   ⚠️ 沒有找到類別數據")
                
        except Exception as e:
            print(f"   ❌ 檢查類別分佈失敗: {e}")
        
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 questions 表格測試完成！")

if __name__ == "__main__":
    test_questions_table()

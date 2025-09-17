#!/usr/bin/env python3
"""
檢查特定用戶「神秘小檬檬」的詳細統計資料和積分顯示問題
"""
import os
from supabase import create_client, Client
import json

# Supabase 配置
SUPABASE_URL = "https://ciqlfqfgzqqgdrogedxg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA"

def main():
    print("🔍 檢查用戶「神秘小檬檬」的詳細統計資料...")
    
    try:
        # 創建 Supabase 客戶端
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Supabase 連接成功")
        
        # 目標用戶ID
        target_user_id = "Uddae8475d30fd8691c811ecef7737890"
        target_nickname = "神秘小檬檬"
        
        print(f"\n👤 目標用戶: {target_user_id} ({target_nickname})")
        
        # 1. 檢查用戶基本資料
        print(f"\n📋 步驟1: 檢查用戶基本資料...")
        user_response = supabase.table('users').select('*').eq('line_user_id', target_user_id).execute()
        
        if user_response.data:
            user_data = user_response.data[0]
            print(f"✅ 用戶資料:")
            print(f"📝 {json.dumps(user_data, ensure_ascii=False, indent=2)}")
        else:
            print("❌ 沒有找到用戶基本資料")
        
        # 2. 檢查用戶統計資料
        print(f"\n📊 步驟2: 檢查用戶統計資料...")
        stats_response = supabase.table('user_stats').select('*').eq('user_id', target_user_id).execute()
        
        if stats_response.data:
            user_stats = stats_response.data[0]
            print(f"✅ 統計資料:")
            print(f"📊 {json.dumps(user_stats, ensure_ascii=False, indent=2)}")
            
            # 詳細分析
            correct_answers = user_stats.get('correct', 0)
            wrong_answers = user_stats.get('wrong', 0)
            level = user_stats.get('level', 1)
            correct_in_level = user_stats.get('correct_in_level', 0)
            total_questions = correct_answers + wrong_answers
            accuracy = round((correct_answers / max(total_questions, 1)) * 100, 1) if total_questions > 0 else 0
            
            print(f"\n📈 統計分析:")
            print(f"✅ 答對題數: {correct_answers}")
            print(f"❌ 答錯題數: {wrong_answers}")
            print(f"📈 總題數: {total_questions}")
            print(f"🎯 準確率: {accuracy}%")
            print(f"🏆 當前等級: {level}")
            print(f"⭐ 本級答對: {correct_in_level}")
            
        else:
            print("❌ 沒有找到用戶統計資料")
            return
        
        # 3. 檢查答題記錄（如果有相關表格）
        print(f"\n📝 步驟3: 檢查可能的答題記錄...")
        try:
            # 嘗試查找答題記錄或相關表格
            tables_to_check = ['user_answers', 'quiz_results', 'answer_history']
            for table_name in tables_to_check:
                try:
                    answer_response = supabase.table(table_name).select('*').eq('user_id', target_user_id).execute()
                    if answer_response.data:
                        print(f"✅ 在 {table_name} 表中找到 {len(answer_response.data)} 條記錄")
                        for i, record in enumerate(answer_response.data[:3], 1):  # 只顯示前3條
                            print(f"   {i}. {json.dumps(record, ensure_ascii=False, indent=6)}")
                    else:
                        print(f"⚠️ 在 {table_name} 表中沒有找到記錄")
                except Exception as e:
                    print(f"⚠️ 無法查詢 {table_name} 表: {e}")
        except Exception as e:
            print(f"⚠️ 檢查答題記錄時出錯: {e}")
        
        # 4. 模擬積分 Flex Message 創建
        print(f"\n🎨 步驟4: 模擬積分 Flex Message 創建...")
        
        def simulate_flex_message_creation(user_stats, nickname):
            """模擬 Flex Message 創建過程"""
            print(f"🔧 模擬 create_score_flex_message 函數:")
            
            # 從 user_stats 提取數據（模擬實際函數邏輯）
            correct_answers = user_stats.get('correct', 0)
            wrong_answers = user_stats.get('wrong', 0)
            level = user_stats.get('level', 1)
            correct_in_level = user_stats.get('correct_in_level', 0)
            
            print(f"   📊 原始數據提取:")
            print(f"      - user_stats.get('correct', 0) = {correct_answers}")
            print(f"      - user_stats.get('wrong', 0) = {wrong_answers}")
            print(f"      - user_stats.get('level', 1) = {level}")
            print(f"      - user_stats.get('correct_in_level', 0) = {correct_in_level}")
            
            # 計算總題數和準確率
            total_questions = correct_answers + wrong_answers
            accuracy = round((correct_answers / max(total_questions, 1)) * 100, 1)
            
            print(f"   🧮 計算結果:")
            print(f"      - total_questions = {total_questions}")
            print(f"      - accuracy = {accuracy}%")
            
            # 檢查 Flex Message 中會顯示的數值
            print(f"   📱 Flex Message 顯示數值:")
            print(f"      - 答對題數: {correct_answers} 題")
            print(f"      - 答錯題數: {wrong_answers} 題")
            print(f"      - 準確率: {accuracy}%")
            print(f"      - 等級: {level}")
            print(f"      - 本級答對: {correct_in_level} 題")
            
            return {
                "correct_answers": correct_answers,
                "wrong_answers": wrong_answers,
                "total_questions": total_questions,
                "accuracy": accuracy,
                "level": level,
                "correct_in_level": correct_in_level
            }
        
        flex_result = simulate_flex_message_creation(user_stats, target_nickname)
        
        # 5. 問題診斷
        print(f"\n🔍 步驟5: 問題診斷...")
        if flex_result['correct_answers'] == 0:
            print(f"❌ 問題確認: Flex Message 會顯示答對 0 題")
            print(f"🤔 可能的原因:")
            print(f"   1. 用戶統計資料中 'correct' 欄位確實為 0")
            print(f"   2. 答題記錄沒有正確更新到統計資料")
            print(f"   3. 統計資料更新邏輯有問題")
            print(f"   4. 數據庫同步問題")
        else:
            print(f"✅ Flex Message 應該會正確顯示答對 {flex_result['correct_answers']} 題")
        
        # 6. 建議解決方案
        print(f"\n💡 建議解決方案:")
        print(f"   1. 檢查答題記錄更新邏輯")
        print(f"   2. 檢查 update_user_stats_after_answer 函數")
        print(f"   3. 檢查是否有答題但沒有更新統計的情況")
        print(f"   4. 考慮手動修復該用戶的統計資料")
        
    except Exception as e:
        print(f"❌ 檢查過程中發生錯誤: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

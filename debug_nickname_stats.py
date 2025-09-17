#!/usr/bin/env python3
"""
檢查暱稱「神秘小濛濛」的用戶統計資料和積分顯示問題
"""
import os
from supabase import create_client, Client
import json

# Supabase 配置
SUPABASE_URL = "https://ciqlfqfgzqqgdrogedxg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA"

def main():
    print("🔍 開始檢查暱稱「神秘小濛濛」的用戶統計資料...")
    
    try:
        # 創建 Supabase 客戶端
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Supabase 連接成功")
        
        # 1. 在 users 表中查找暱稱為「神秘小濛濛」的用戶
        print("\n📋 步驟1: 查找暱稱為「神秘小濛濛」的用戶...")
        users_response = supabase.table('users').select('*').eq('game_nickname', '神秘小濛濛').execute()
        
        if not users_response.data:
            print("❌ 沒有找到暱稱為「神秘小濛濛」的用戶")
            return
        
        user_data = users_response.data[0]
        user_id = user_data.get('line_user_id')
        print(f"✅ 找到用戶: {user_id}")
        print(f"📝 用戶資料: {json.dumps(user_data, ensure_ascii=False, indent=2)}")
        
        # 2. 查找該用戶的統計資料
        print(f"\n📊 步驟2: 查找用戶 {user_id} 的統計資料...")
        stats_response = supabase.table('user_stats').select('*').eq('user_id', user_id).execute()
        
        if not stats_response.data:
            print("❌ 沒有找到該用戶的統計資料")
            return
        
        user_stats = stats_response.data[0]
        print(f"✅ 找到統計資料:")
        print(f"📊 統計資料: {json.dumps(user_stats, ensure_ascii=False, indent=2)}")
        
        # 3. 分析統計資料
        print(f"\n🔍 步驟3: 分析統計資料...")
        correct_answers = user_stats.get('correct', 0)
        wrong_answers = user_stats.get('wrong', 0)
        level = user_stats.get('level', 1)
        correct_in_level = user_stats.get('correct_in_level', 0)
        total_questions = correct_answers + wrong_answers
        accuracy = round((correct_answers / max(total_questions, 1)) * 100, 1) if total_questions > 0 else 0
        
        print(f"✅ 答對題數: {correct_answers}")
        print(f"❌ 答錯題數: {wrong_answers}")
        print(f"📈 總題數: {total_questions}")
        print(f"🎯 準確率: {accuracy}%")
        print(f"🏆 當前等級: {level}")
        print(f"⭐ 本級答對: {correct_in_level}")
        
        # 4. 檢查是否有其他相關記錄
        print(f"\n🔍 步驟4: 檢查其他可能的記錄...")
        
        # 檢查是否有重複的用戶記錄
        all_users_with_nickname = supabase.table('users').select('*').eq('game_nickname', '神秘小濛濛').execute()
        print(f"📋 找到 {len(all_users_with_nickname.data)} 個暱稱為「神秘小濛濛」的用戶記錄")
        
        # 檢查是否有其他統計記錄
        all_stats = supabase.table('user_stats').select('*').eq('user_id', user_id).execute()
        print(f"📊 找到 {len(all_stats.data)} 個該用戶的統計記錄")
        
        # 5. 模擬 flex message 創建
        print(f"\n🎨 步驟5: 模擬創建積分 Flex Message...")
        
        def create_score_flex_message_debug(user_stats, nickname):
            """調試版本的積分 Flex Message 創建"""
            correct_answers = user_stats.get('correct', 0)
            wrong_answers = user_stats.get('wrong', 0)
            level = user_stats.get('level', 1)
            correct_in_level = user_stats.get('correct_in_level', 0)
            
            print(f"🔧 Flex Message 數據來源:")
            print(f"   - correct_answers: {correct_answers}")
            print(f"   - wrong_answers: {wrong_answers}")
            print(f"   - level: {level}")
            print(f"   - correct_in_level: {correct_in_level}")
            
            # 計算總題數和準確率
            total_questions = correct_answers + wrong_answers
            accuracy = round((correct_answers / max(total_questions, 1)) * 100, 1)
            
            print(f"🧮 計算結果:")
            print(f"   - total_questions: {total_questions}")
            print(f"   - accuracy: {accuracy}%")
            
            return {
                "debug_info": {
                    "correct_answers": correct_answers,
                    "wrong_answers": wrong_answers,
                    "total_questions": total_questions,
                    "accuracy": accuracy,
                    "level": level,
                    "correct_in_level": correct_in_level
                }
            }
        
        flex_debug = create_score_flex_message_debug(user_stats, '神秘小濛濛')
        print(f"🎨 Flex Message 調試信息: {json.dumps(flex_debug, ensure_ascii=False, indent=2)}")
        
        # 6. 總結
        print(f"\n📋 總結:")
        if correct_answers > 0:
            print(f"✅ 用戶確實有 {correct_answers} 題答對記錄")
            print(f"🤔 如果 Flex Message 顯示0題，可能是:")
            print(f"   1. Flex Message 創建邏輯有問題")
            print(f"   2. 數據抓取時機有問題")
            print(f"   3. 缓存或同步問題")
        else:
            print(f"❌ 用戶統計資料顯示答對題數為0")
            print(f"🤔 可能的原因:")
            print(f"   1. 統計資料更新有問題")
            print(f"   2. 答題記錄沒有正確保存")
            print(f"   3. 數據庫同步問題")
        
    except Exception as e:
        print(f"❌ 檢查過程中發生錯誤: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

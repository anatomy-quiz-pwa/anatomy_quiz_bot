#!/usr/bin/env python3
"""
修復用戶「神秘小檬檬」的統計資料同步問題
"""
import os
from supabase import create_client, Client
import json

# Supabase 配置
SUPABASE_URL = "https://ciqlfqfgzqqgdrogedxg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA"

def main():
    print("🔧 開始修復用戶「神秘小檬檬」的統計資料...")
    
    try:
        # 創建 Supabase 客戶端
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Supabase 連接成功")
        
        # 目標用戶ID
        target_user_id = "Uddae8475d30fd8691c811ecef7737890"
        target_nickname = "神秘小檬檬"
        
        print(f"\n👤 目標用戶: {target_user_id} ({target_nickname})")
        
        # 1. 獲取當前統計資料
        print(f"\n📊 步驟1: 獲取當前統計資料...")
        stats_response = supabase.table('user_stats').select('*').eq('user_id', target_user_id).execute()
        
        if not stats_response.data:
            print("❌ 沒有找到用戶統計資料")
            return
        
        current_stats = stats_response.data[0]
        print(f"📊 當前統計資料: {json.dumps(current_stats, ensure_ascii=False, indent=2)}")
        
        # 2. 分析問題
        correct_answers = current_stats.get('correct', 0)
        wrong_answers = current_stats.get('wrong', 0)
        correct_qids = current_stats.get('correct_qids', [])
        level = current_stats.get('level', 1)
        correct_in_level = current_stats.get('correct_in_level', 0)
        
        print(f"\n🔍 步驟2: 分析問題...")
        print(f"📈 統計中的答對題數: {correct_answers}")
        print(f"📝 實際答對的題目ID: {correct_qids}")
        print(f"🧮 實際答對題目數量: {len(correct_qids)}")
        
        if len(correct_qids) != correct_answers:
            print(f"❌ 發現不一致：統計顯示答對{correct_answers}題，但實際記錄了{len(correct_qids)}題")
            
            # 3. 修復統計資料
            print(f"\n🔧 步驟3: 修復統計資料...")
            
            # 計算正確的統計數據
            actual_correct = len(correct_qids)
            
            # 計算等級（假設每3題升一級）
            new_level = min(14, (actual_correct // 3) + 1)
            new_correct_in_level = actual_correct % 3
            
            print(f"🧮 計算結果:")
            print(f"   - 實際答對題數: {actual_correct}")
            print(f"   - 計算等級: {new_level}")
            print(f"   - 本級答對: {new_correct_in_level}")
            
            # 更新統計資料
            update_data = {
                'user_id': target_user_id,
                'correct': actual_correct,
                'wrong': wrong_answers,  # 保持原有的錯誤題數
                'level': new_level,
                'correct_in_level': new_correct_in_level,
                'correct_qids': correct_qids,
                'last_update': '2025-09-17'
            }
            
            print(f"\n💾 步驟4: 更新統計資料...")
            print(f"📝 更新數據: {json.dumps(update_data, ensure_ascii=False, indent=2)}")
            
            # 確認是否要執行更新
            confirmation = input("\n❓ 是否要執行統計資料修復？(y/N): ")
            
            if confirmation.lower() == 'y':
                result = supabase.table('user_stats').upsert(update_data, on_conflict='user_id').execute()
                
                if result.data:
                    print("✅ 統計資料修復成功！")
                    
                    # 驗證修復結果
                    print(f"\n🔍 步驟5: 驗證修復結果...")
                    verify_response = supabase.table('user_stats').select('*').eq('user_id', target_user_id).execute()
                    
                    if verify_response.data:
                        updated_stats = verify_response.data[0]
                        print(f"✅ 修復後的統計資料:")
                        print(f"📊 {json.dumps(updated_stats, ensure_ascii=False, indent=2)}")
                        
                        # 模擬 Flex Message 顯示
                        print(f"\n🎨 步驟6: 模擬 Flex Message 顯示...")
                        new_correct = updated_stats.get('correct', 0)
                        new_wrong = updated_stats.get('wrong', 0)
                        new_level = updated_stats.get('level', 1)
                        new_correct_in_level = updated_stats.get('correct_in_level', 0)
                        
                        total_questions = new_correct + new_wrong
                        accuracy = round((new_correct / max(total_questions, 1)) * 100, 1) if total_questions > 0 else 0
                        
                        print(f"📱 Flex Message 將顯示:")
                        print(f"   - 答對題數: {new_correct} 題")
                        print(f"   - 答錯題數: {new_wrong} 題")
                        print(f"   - 準確率: {accuracy}%")
                        print(f"   - 等級: {new_level}")
                        print(f"   - 本級答對: {new_correct_in_level} 題")
                        
                    else:
                        print("❌ 驗證失敗：無法獲取更新後的統計資料")
                else:
                    print("❌ 統計資料修復失敗")
            else:
                print("❌ 取消修復操作")
        else:
            print(f"✅ 統計資料一致，無需修復")
        
    except Exception as e:
        print(f"❌ 修復過程中發生錯誤: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
快取管理工具
用於清空快取資料和重置用戶會話
"""

import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 全域快取字典
user_state = {}
question_cache = {}

def clear_all_cache():
    """清空所有快取資料"""
    global user_state, question_cache
    
    print("🧹 清空所有快取資料...")
    
    # 清空用戶狀態快取
    user_state.clear()
    print(f"✅ 已清空用戶狀態快取 (原本有 {len(user_state)} 個用戶)")
    
    # 清空題目快取
    question_cache.clear()
    print(f"✅ 已清空題目快取 (原本有 {len(question_cache)} 個題目)")
    
    print("🎉 所有快取資料已清空完成！")
    return True

def clear_user_cache(user_id):
    """清空特定用戶的快取資料"""
    global user_state
    
    print(f"🧹 清空用戶 {user_id} 的快取資料...")
    
    if user_id in user_state:
        del user_state[user_id]
        print(f"✅ 已清空用戶 {user_id} 的快取資料")
    else:
        print(f"ℹ️ 用戶 {user_id} 沒有快取資料")
    
    return True

def reset_user_session(user_id, topic=None):
    """重置用戶會話，可選擇性指定主題"""
    global user_state
    
    print(f"🔄 重置用戶 {user_id} 的會話...")
    
    # 清空該用戶的現有快取
    if user_id in user_state:
        del user_state[user_id]
        print(f"✅ 已清空用戶 {user_id} 的現有會話")
    
    # 如果指定了主題，重新初始化會話
    if topic:
        try:
            from supabase_quiz_handler import supabase
            
            # 從 Supabase 獲取題目
            question_list = supabase.table("questions").select("*").eq("topic", topic).limit(7).execute().data
            
            # 初始化新的用戶狀態
            user_state[user_id] = {
                "topic": topic,
                "questions": question_list,
                "current_index": 0,
                "score": {
                    "correct": 0,
                    "wrong": 0
                }
            }
            
            print(f"✅ 已為用戶 {user_id} 初始化主題 '{topic}' 的會話")
            print(f"📝 載入了 {len(question_list)} 個題目")
            
        except Exception as e:
            print(f"❌ 初始化用戶會話失敗: {str(e)}")
            return False
    else:
        print(f"ℹ️ 用戶 {user_id} 的會話已重置，但未指定新主題")
    
    return True

def get_cache_status():
    """獲取快取狀態"""
    global user_state, question_cache
    
    status = {
        "user_cache_count": len(user_state),
        "question_cache_count": len(question_cache),
        "cached_users": list(user_state.keys()),
        "cached_questions": list(question_cache.keys()) if question_cache else []
    }
    
    return status

def print_cache_status():
    """印出快取狀態"""
    status = get_cache_status()
    
    print("📊 快取狀態:")
    print(f"   用戶快取數量: {status['user_cache_count']}")
    print(f"   題目快取數量: {status['question_cache_count']}")
    
    if status['cached_users']:
        print(f"   快取用戶: {', '.join(status['cached_users'])}")
    else:
        print("   快取用戶: 無")
    
    if status['cached_questions']:
        print(f"   快取題目: {', '.join(status['cached_questions'])}")
    else:
        print("   快取題目: 無")

# 測試函數
def test_cache_utils():
    """測試快取工具函數"""
    print("🧪 測試快取工具函數...")
    print("=" * 50)
    
    # 測試清空所有快取
    clear_all_cache()
    
    # 測試獲取快取狀態
    print_cache_status()
    
    # 測試重置用戶會話
    test_user_id = "test_user_123"
    reset_user_session(test_user_id, "anatomy")
    
    # 再次檢查狀態
    print("\n重置後的狀態:")
    print_cache_status()
    
    print("\n✅ 快取工具測試完成！")

if __name__ == "__main__":
    test_cache_utils() 
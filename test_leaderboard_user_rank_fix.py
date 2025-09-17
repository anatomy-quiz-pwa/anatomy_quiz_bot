#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試排行榜用戶排名修復
確保排行榜能顯示前三名以及用戶自己的排名
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app_supabase import (
    get_leaderboard_data, 
    get_user_rank_info, 
    create_leaderboard_flex_message,
    send_leaderboard_message,
    logger
)

def test_leaderboard_data_fetch():
    """測試排行榜數據獲取"""
    print("🔍 測試排行榜數據獲取...")
    
    try:
        data = get_leaderboard_data()
        print(f"✅ 成功獲取排行榜數據，共 {len(data)} 條記錄")
        
        if data:
            print("📊 前3名數據樣本：")
            for i, student in enumerate(data[:3], 1):
                nickname = student.get('nickname', '未知用戶')
                correct = student.get('correct', 0)
                print(f"  {i}. {nickname} - {correct} 題正確")
        
        return data
    except Exception as e:
        print(f"❌ 獲取排行榜數據失敗: {e}")
        return None

def test_user_rank_query():
    """測試用戶排名查詢功能"""
    print("\n🔍 測試用戶排名查詢功能...")
    
    # 測試保的帳號
    test_user_id = "U977c24d1fec3a2bf07035504e1444911"  # 保的帳號
    
    try:
        user_rank_info = get_user_rank_info(test_user_id)
        
        if user_rank_info:
            print(f"✅ 成功查詢到用戶排名信息:")
            print(f"   用戶ID: {user_rank_info['user_id']}")
            print(f"   暱稱: {user_rank_info['nickname']}")
            print(f"   排名: 第{user_rank_info['rank']}名")
            print(f"   正確答案: {user_rank_info['correct']} 題")
            print(f"   錯誤答案: {user_rank_info['wrong']} 題")
            print(f"   等級: {user_rank_info['level']}")
            print(f"   準確率: {user_rank_info['accuracy']}%")
        else:
            print("❌ 無法查詢到用戶排名信息")
        
        return user_rank_info
    except Exception as e:
        print(f"❌ 查詢用戶排名失敗: {e}")
        return None

def test_leaderboard_flex_message():
    """測試排行榜 Flex Message 創建"""
    print("\n🔍 測試排行榜 Flex Message 創建...")
    
    try:
        # 獲取排行榜數據
        leaderboard_data = get_leaderboard_data()
        if not leaderboard_data:
            print("❌ 無法獲取排行榜數據")
            return
        
        # 測試用戶ID
        test_user_id = "U977c24d1fec3a2bf07035504e1444911"  # 保的帳號
        
        # 創建 Flex Message
        flex_message = create_leaderboard_flex_message(
            leaderboard_data[:10], 
            leaderboard_data, 
            test_user_id
        )
        
        if flex_message:
            print("✅ 成功創建排行榜 Flex Message")
            
            # 檢查是否包含用戶排名信息
            body_contents = flex_message.get('contents', {}).get('body', {}).get('contents', [])
            
            # 查找是否有分隔線和用戶排名信息
            has_separator = any(item.get('type') == 'separator' for item in body_contents)
            has_user_rank = any('你的排名' in str(item) for item in body_contents)
            
            print(f"   包含分隔線: {'✅' if has_separator else '❌'}")
            print(f"   包含用戶排名: {'✅' if has_user_rank else '❌'}")
            
            # 輸出部分內容用於檢查
            print("\n📄 Flex Message 結構樣本:")
            print(f"   總內容項目數: {len(body_contents)}")
            for i, item in enumerate(body_contents):
                item_type = item.get('type', 'unknown')
                if item_type == 'box':
                    # 檢查是否是排名項目
                    contents = item.get('contents', [])
                    if contents and len(contents) > 1:
                        text_content = contents[1].get('contents', [])
                        if text_content and text_content[0].get('text'):
                            first_text = text_content[0]['text']
                            print(f"   項目 {i+1}: {item_type} - {first_text[:30]}...")
                elif item_type == 'separator':
                    print(f"   項目 {i+1}: 分隔線")
                elif item_type == 'text':
                    text = item.get('text', '')
                    print(f"   項目 {i+1}: {item_type} - {text[:30]}...")
            
        else:
            print("❌ 創建排行榜 Flex Message 失敗")
        
        return flex_message
    except Exception as e:
        print(f"❌ 測試 Flex Message 創建失敗: {e}")
        return None

def test_send_leaderboard():
    """測試發送排行榜訊息"""
    print("\n🔍 測試發送排行榜訊息...")
    
    # 測試用戶ID
    test_user_id = "U977c24d1fec3a2bf07035504e1444911"  # 保的帳號
    
    try:
        print(f"📤 發送排行榜給用戶: {test_user_id}")
        send_leaderboard_message(test_user_id)
        print("✅ 排行榜訊息發送完成")
        
    except Exception as e:
        print(f"❌ 發送排行榜訊息失敗: {e}")

def main():
    """主測試函數"""
    print("🧪 開始測試排行榜用戶排名修復")
    print("=" * 60)
    
    # 測試1: 數據獲取
    leaderboard_data = test_leaderboard_data_fetch()
    
    # 測試2: 用戶排名查詢
    user_rank_info = test_user_rank_query()
    
    # 測試3: Flex Message 創建
    flex_message = test_leaderboard_flex_message()
    
    # 測試4: 發送訊息
    test_send_leaderboard()
    
    print("\n" + "=" * 60)
    print("🏁 測試完成")
    
    # 總結
    print("\n📋 測試結果總結:")
    print(f"   排行榜數據獲取: {'✅' if leaderboard_data else '❌'}")
    print(f"   用戶排名查詢: {'✅' if user_rank_info else '❌'}")
    print(f"   Flex Message 創建: {'✅' if flex_message else '❌'}")
    
    if leaderboard_data and user_rank_info:
        print(f"\n🎯 關鍵信息:")
        print(f"   排行榜數據條數: {len(leaderboard_data)}")
        print(f"   用戶排名: 第{user_rank_info['rank']}名")
        print(f"   用戶是否在前3名: {'是' if user_rank_info['rank'] <= 3 else '否'}")
        print(f"   應該顯示用戶排名: {'是' if user_rank_info['rank'] > 3 else '否'}")

if __name__ == "__main__":
    main()

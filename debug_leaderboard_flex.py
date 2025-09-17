#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
調試排行榜 Flex Messenger 問題
"""

import os
import sys
import json
import requests
from datetime import datetime

# 添加當前目錄到 Python 路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 導入主應用程序的函數
from app_supabase_fixed import (
    get_leaderboard_data, 
    create_leaderboard_flex_message, 
    send_leaderboard_message,
    send_line_message,
    get_user_nickname
)

def test_leaderboard_data():
    """測試排行榜數據獲取"""
    print("🔍 測試排行榜數據獲取...")
    
    try:
        data = get_leaderboard_data()
        print(f"✅ 成功獲取排行榜數據，共 {len(data)} 條記錄")
        
        if data:
            print("📊 前3名數據樣本：")
            for i, student in enumerate(data[:3], 1):
                print(f"  {i}. {student['name']} - {student['score']}分 (等級{student['level']})")
        
        return data
    except Exception as e:
        print(f"❌ 獲取排行榜數據失敗: {e}")
        return None

def test_flex_message_creation():
    """測試 Flex Message 創建"""
    print("\n🔍 測試 Flex Message 創建...")
    
    try:
        # 獲取排行榜數據
        students_data = get_leaderboard_data()
        if not students_data:
            print("❌ 沒有排行榜數據，無法創建 Flex Message")
            return None
        
        # 測試用戶ID
        test_user_id = "test_user_001"
        
        # 創建 Flex Message
        flex_message = create_leaderboard_flex_message(
            students_data[:10],  # 前10名
            students_data,       # 所有數據
            test_user_id
        )
        
        print("✅ 成功創建 Flex Message")
        print(f"📱 Flex Message 類型: {flex_message.get('type', 'unknown')}")
        
        if flex_message.get('type') == 'flex':
            print("📋 Flex Message 內容結構:")
            contents = flex_message.get('contents', {})
            print(f"  - 類型: {contents.get('type', 'unknown')}")
            print(f"  - 標題: {contents.get('header', {}).get('contents', [{}])[0].get('text', 'N/A')}")
            
            body_contents = contents.get('body', {}).get('contents', [])
            print(f"  - 排行榜項目數: {len(body_contents)}")
        
        return flex_message
        
    except Exception as e:
        print(f"❌ 創建 Flex Message 失敗: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_line_message_sending():
    """測試 LINE 訊息發送"""
    print("\n🔍 測試 LINE 訊息發送...")
    
    try:
        # 測試用戶ID
        test_user_id = "test_user_001"
        
        # 檢查環境變數
        line_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
        if not line_token:
            print("⚠️ LINE_CHANNEL_ACCESS_TOKEN 未設置，使用預設值")
            line_token = "AhZFgYWfEMeFSDxJJhzcvJoKx78lVrfRH3cqqusfiZhug/f5wRhQTkDD9fW7+IJLA3xpoQtunFWoVKnHtaE9p+U1QVFUz1o8CQ5AnNpPicjK32KAD5Z1ouF1HNKATv/BhUHIS3OjcndnUGpOqPDYKAdB04t89/1O/w1cDnyilFU="
        
        # 創建測試訊息
        test_message = {
            "text": f"🧪 測試訊息 - {datetime.now().strftime('%H:%M:%S')}\n\n這是一個測試訊息，用於驗證 LINE 訊息發送功能。"
        }
        
        # 發送測試訊息
        result = send_line_message(test_user_id, test_message)
        print(f"📤 LINE 訊息發送結果: {result}")
        
        if 'error' in result:
            print(f"❌ 發送失敗: {result['error']}")
        else:
            print("✅ 測試訊息發送成功")
        
        return result
        
    except Exception as e:
        print(f"❌ 測試 LINE 訊息發送失敗: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_leaderboard_message_sending():
    """測試排行榜訊息發送"""
    print("\n🔍 測試排行榜訊息發送...")
    
    try:
        # 測試用戶ID
        test_user_id = "test_user_001"
        
        # 發送排行榜訊息
        send_leaderboard_message(test_user_id)
        print("✅ 排行榜訊息發送完成")
        
    except Exception as e:
        print(f"❌ 發送排行榜訊息失敗: {e}")
        import traceback
        traceback.print_exc()

def test_flex_message_structure():
    """測試 Flex Message 結構"""
    print("\n🔍 測試 Flex Message 結構...")
    
    try:
        # 獲取排行榜數據
        students_data = get_leaderboard_data()
        if not students_data:
            print("❌ 沒有排行榜數據")
            return
        
        # 創建 Flex Message
        flex_message = create_leaderboard_flex_message(
            students_data[:5],  # 前5名
            students_data,
            "test_user_001"
        )
        
        # 檢查 Flex Message 結構
        print("📋 Flex Message 結構分析:")
        print(f"  - 類型: {flex_message.get('type')}")
        print(f"  - altText: {flex_message.get('altText')}")
        
        contents = flex_message.get('contents', {})
        print(f"  - contents 類型: {contents.get('type')}")
        
        header = contents.get('header', {})
        print(f"  - header 類型: {header.get('type')}")
        
        body = contents.get('body', {})
        print(f"  - body 類型: {body.get('type')}")
        print(f"  - body 內容數量: {len(body.get('contents', []))}")
        
        footer = contents.get('footer', {})
        print(f"  - footer 類型: {footer.get('type')}")
        print(f"  - footer 按鈕數量: {len(footer.get('contents', []))}")
        
        # 檢查是否為有效的 Flex Message
        if flex_message.get('type') == 'flex' and contents.get('type') == 'bubble':
            print("✅ Flex Message 結構正確")
        else:
            print("❌ Flex Message 結構有問題")
            
    except Exception as e:
        print(f"❌ 測試 Flex Message 結構失敗: {e}")
        import traceback
        traceback.print_exc()

def main():
    """主函數"""
    print("🚀 開始調試排行榜 Flex Messenger 問題")
    print("=" * 50)
    
    # 1. 測試排行榜數據獲取
    leaderboard_data = test_leaderboard_data()
    
    # 2. 測試 Flex Message 創建
    flex_message = test_flex_message_creation()
    
    # 3. 測試 Flex Message 結構
    test_flex_message_structure()
    
    # 4. 測試 LINE 訊息發送
    line_result = test_line_message_sending()
    
    # 5. 測試排行榜訊息發送
    test_leaderboard_message_sending()
    
    print("\n" + "=" * 50)
    print("🏁 調試完成")
    
    # 總結
    print("\n📊 調試結果總結:")
    print(f"  - 排行榜數據: {'✅' if leaderboard_data else '❌'}")
    print(f"  - Flex Message 創建: {'✅' if flex_message else '❌'}")
    print(f"  - LINE 訊息發送: {'✅' if line_result and 'error' not in line_result else '❌'}")

if __name__ == "__main__":
    main()

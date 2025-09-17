#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試真實用戶場景的排行榜功能
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
    handle_text_message,
    send_leaderboard_message,
    send_line_message
)

def test_real_user_leaderboard():
    """測試真實用戶輸入排行榜指令"""
    print("🧪 測試真實用戶排行榜功能")
    print("=" * 50)
    
    # 模擬真實用戶的 LINE 訊息
    test_user_id = "U977c24d1fec3a2bf07035504e1444911"  # 從日誌中看到的真實用戶ID
    
    # 模擬 LINE webhook 訊息格式
    line_message = {
        "text": "排行榜"
    }
    
    print(f"👤 測試用戶ID: {test_user_id}")
    print(f"📝 輸入訊息: {line_message['text']}")
    print()
    
    try:
        # 直接調用文字訊息處理函數
        print("🔄 處理文字訊息...")
        handle_text_message(test_user_id, line_message)
        print("✅ 文字訊息處理完成")
        
    except Exception as e:
        print(f"❌ 處理失敗: {e}")
        import traceback
        traceback.print_exc()

def test_direct_leaderboard_send():
    """直接測試排行榜訊息發送"""
    print("\n🧪 直接測試排行榜訊息發送")
    print("=" * 50)
    
    test_user_id = "U977c24d1fec3a2bf07035504e1444911"
    
    try:
        print(f"👤 發送排行榜給用戶: {test_user_id}")
        send_leaderboard_message(test_user_id)
        print("✅ 排行榜訊息發送完成")
        
    except Exception as e:
        print(f"❌ 發送失敗: {e}")
        import traceback
        traceback.print_exc()

def test_flex_message_validation():
    """測試 Flex Message 格式驗證"""
    print("\n🧪 測試 Flex Message 格式驗證")
    print("=" * 50)
    
    from app_supabase_fixed import create_leaderboard_flex_message, get_leaderboard_data
    
    try:
        # 獲取排行榜數據
        students_data = get_leaderboard_data()
        if not students_data:
            print("❌ 無法獲取排行榜數據")
            return
        
        # 創建 Flex Message
        test_user_id = "U977c24d1fec3a2bf07035504e1444911"
        flex_message = create_leaderboard_flex_message(
            students_data[:10],
            students_data,
            test_user_id
        )
        
        print("📋 Flex Message 結構驗證:")
        print(f"  - 類型: {flex_message.get('type')}")
        print(f"  - altText: {flex_message.get('altText')}")
        
        # 檢查 Flex Message 是否符合 LINE API 規範
        if flex_message.get('type') == 'flex':
            contents = flex_message.get('contents', {})
            if contents.get('type') == 'bubble':
                print("✅ Flex Message 格式正確")
                
                # 檢查是否有必要的欄位
                required_fields = ['header', 'body', 'footer']
                for field in required_fields:
                    if field in contents:
                        print(f"  ✅ {field} 存在")
                    else:
                        print(f"  ❌ {field} 缺失")
                
                # 檢查 body 內容
                body_contents = contents.get('body', {}).get('contents', [])
                print(f"  📊 排行榜項目數: {len(body_contents)}")
                
                # 檢查 footer 按鈕
                footer_contents = contents.get('footer', {}).get('contents', [])
                print(f"  🔘 按鈕數量: {len(footer_contents)}")
                
            else:
                print("❌ Flex Message contents 類型錯誤")
        else:
            print("❌ Flex Message 類型錯誤")
            
    except Exception as e:
        print(f"❌ 驗證失敗: {e}")
        import traceback
        traceback.print_exc()

def test_line_api_validation():
    """測試 LINE API 請求格式"""
    print("\n🧪 測試 LINE API 請求格式")
    print("=" * 50)
    
    from app_supabase_fixed import create_leaderboard_flex_message, get_leaderboard_data
    
    try:
        # 獲取排行榜數據並創建 Flex Message
        students_data = get_leaderboard_data()
        test_user_id = "U977c24d1fec3a2bf07035504e1444911"
        flex_message = create_leaderboard_flex_message(
            students_data[:10],
            students_data,
            test_user_id
        )
        
        # 模擬 LINE API 請求格式
        line_api_data = {
            "to": test_user_id,
            "messages": [flex_message]
        }
        
        print("📤 LINE API 請求格式:")
        print(f"  - to: {line_api_data['to']}")
        print(f"  - messages 數量: {len(line_api_data['messages'])}")
        print(f"  - 第一個訊息類型: {line_api_data['messages'][0].get('type')}")
        
        # 檢查用戶ID格式
        if test_user_id.startswith('U') and len(test_user_id) > 10:
            print("✅ 用戶ID格式正確")
        else:
            print("❌ 用戶ID格式錯誤")
        
        # 檢查 Flex Message 結構
        if flex_message.get('type') == 'flex':
            print("✅ Flex Message 類型正確")
        else:
            print("❌ Flex Message 類型錯誤")
            
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        import traceback
        traceback.print_exc()

def main():
    """主函數"""
    print("🚀 開始測試真實用戶排行榜功能")
    print("=" * 60)
    
    # 1. 測試 Flex Message 格式驗證
    test_flex_message_validation()
    
    # 2. 測試 LINE API 請求格式
    test_line_api_validation()
    
    # 3. 直接測試排行榜訊息發送
    test_direct_leaderboard_send()
    
    # 4. 測試真實用戶輸入排行榜指令
    test_real_user_leaderboard()
    
    print("\n" + "=" * 60)
    print("🏁 測試完成")
    print("\n💡 請檢查日誌文件 app.log 查看詳細的錯誤信息")

if __name__ == "__main__":
    main()

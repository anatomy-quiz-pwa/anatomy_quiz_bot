#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
診斷排行榜 Flex 訊息問題
"""

import os
import sys
import json
import requests
from datetime import datetime

# 添加當前目錄到 Python 路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 設置環境變量
os.environ['SUPABASE_URL'] = 'https://ciqlfqfgzqqgdrogedxg.supabase.co'
os.environ['SUPABASE_ANON_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA'
os.environ['LINE_CHANNEL_ACCESS_TOKEN'] = 'AhZFgYWfEMeFSDxJJhzcvJoKx78lVrfRH3cqqusfiZhug/f5wRhQTkDD9fW7+IJLA3xpoQtunFWoVKnHtaE9p+U1QVFUz1o8CQ5AnNpPicjK32KAD5Z1ouF1HNKATv/BhUHIS3OjcndnUGpOqPDYKAdB04t89/1O/w1cDnyilFU='

def test_leaderboard_data():
    """測試排行榜數據獲取"""
    print("🔍 測試排行榜數據獲取...")
    
    try:
        from app_supabase_fixed import get_leaderboard_data
        
        data = get_leaderboard_data()
        print(f"✅ 成功獲取排行榜數據，共 {len(data)} 條記錄")
        
        if data:
            print("📊 前3名數據樣本：")
            for i, student in enumerate(data[:3], 1):
                print(f"  {i}. {student.get('name', 'N/A')} - {student.get('score', 0)}分 (等級{student.get('level', 0)})")
                print(f"     答題: {student.get('questions_answered', 0)}, 正確: {student.get('correct_answers', 0)}")
        
        return data
    except Exception as e:
        print(f"❌ 獲取排行榜數據失敗: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_flex_message_creation():
    """測試 Flex Message 創建"""
    print("\n🔍 測試 Flex Message 創建...")
    
    try:
        from app_supabase_fixed import get_leaderboard_data, create_leaderboard_flex_message
        
        # 獲取排行榜數據
        students_data = get_leaderboard_data()
        if not students_data:
            print("❌ 沒有排行榜數據，無法創建 Flex Message")
            return None
        
        # 測試用戶ID
        test_user_id = "U977c24d1fec3a2bf07035504e1444911"
        
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
            
            header = contents.get('header', {})
            if header and 'contents' in header:
                header_text = header['contents'][0].get('text', 'N/A') if header['contents'] else 'N/A'
                print(f"  - 標題: {header_text}")
            
            body = contents.get('body', {})
            body_contents = body.get('contents', [])
            print(f"  - 排行榜項目數: {len(body_contents)}")
            
            footer = contents.get('footer', {})
            footer_contents = footer.get('contents', [])
            print(f"  - 底部按鈕數: {len(footer_contents)}")
        
        # 保存 Flex Message 到文件供檢查
        with open('diagnose_flex_message.json', 'w', encoding='utf-8') as f:
            json.dump(flex_message, f, ensure_ascii=False, indent=2)
        print("💾 Flex Message 已保存到 diagnose_flex_message.json")
        
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
        from app_supabase_fixed import send_line_message
        
        # 測試用戶ID
        test_user_id = "U977c24d1fec3a2bf07035504e1444911"
        
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

def test_flex_message_sending():
    """測試 Flex Message 發送"""
    print("\n🔍 測試 Flex Message 發送...")
    
    try:
        from app_supabase_fixed import get_leaderboard_data, create_leaderboard_flex_message, send_line_message
        
        # 獲取數據並創建 Flex Message
        students_data = get_leaderboard_data()
        if not students_data:
            print("❌ 沒有排行榜數據")
            return None
        
        test_user_id = "U977c24d1fec3a2bf07035504e1444911"
        flex_message = create_leaderboard_flex_message(
            students_data[:10],
            students_data,
            test_user_id
        )
        
        # 發送 Flex Message
        result = send_line_message(test_user_id, flex_message)
        print(f"📤 Flex Message 發送結果: {result}")
        
        if 'error' in result:
            print(f"❌ 發送失敗: {result['error']}")
        else:
            print("✅ Flex Message 發送成功")
        
        return result
        
    except Exception as e:
        print(f"❌ 測試 Flex Message 發送失敗: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_leaderboard_message_sending():
    """測試排行榜訊息發送（完整流程）"""
    print("\n🔍 測試排行榜訊息發送（完整流程）...")
    
    try:
        from app_supabase_fixed import send_leaderboard_message
        
        # 測試用戶ID
        test_user_id = "U977c24d1fec3a2bf07035504e1444911"
        
        # 發送排行榜訊息
        send_leaderboard_message(test_user_id)
        print("✅ 排行榜訊息發送完成")
        
    except Exception as e:
        print(f"❌ 發送排行榜訊息失敗: {e}")
        import traceback
        traceback.print_exc()

def test_flex_message_validation():
    """測試 Flex Message 格式驗證"""
    print("\n🔍 測試 Flex Message 格式驗證...")
    
    try:
        # 讀取剛才創建的 Flex Message
        with open('diagnose_flex_message.json', 'r', encoding='utf-8') as f:
            flex_message = json.load(f)
        
        # 基本驗證
        required_fields = ["type", "altText", "contents"]
        for field in required_fields:
            if field not in flex_message:
                print(f"❌ 缺少必要欄位: {field}")
                return False
            else:
                print(f"✅ 包含必要欄位: {field}")
        
        # 檢查 contents 結構
        contents = flex_message["contents"]
        required_content_fields = ["type", "header", "body", "footer"]
        for field in required_content_fields:
            if field not in contents:
                print(f"❌ contents 缺少必要欄位: {field}")
                return False
            else:
                print(f"✅ contents 包含必要欄位: {field}")
        
        # 檢查 body 內容
        body_contents = contents["body"]["contents"]
        if len(body_contents) > 0:
            print(f"✅ body 包含 {len(body_contents)} 個項目")
        else:
            print("❌ body 為空")
            return False
        
        print("✅ Flex Message 格式驗證通過")
        return True
        
    except Exception as e:
        print(f"❌ 格式驗證失敗: {e}")
        return False

def main():
    """主函數"""
    print("🚀 開始診斷排行榜 Flex 訊息問題")
    print("=" * 60)
    
    # 1. 測試排行榜數據獲取
    leaderboard_data = test_leaderboard_data()
    
    # 2. 測試 Flex Message 創建
    flex_message = test_flex_message_creation()
    
    # 3. 測試 Flex Message 格式驗證
    if flex_message:
        test_flex_message_validation()
    
    # 4. 測試 LINE 訊息發送
    line_result = test_line_message_sending()
    
    # 5. 測試 Flex Message 發送
    flex_result = test_flex_message_sending()
    
    # 6. 測試排行榜訊息發送（完整流程）
    test_leaderboard_message_sending()
    
    print("\n" + "=" * 60)
    print("🏁 診斷完成")
    
    # 總結
    print("\n📊 診斷結果總結:")
    print(f"  - 排行榜數據: {'✅' if leaderboard_data else '❌'}")
    print(f"  - Flex Message 創建: {'✅' if flex_message else '❌'}")
    print(f"  - LINE 訊息發送: {'✅' if line_result and 'error' not in line_result else '❌'}")
    print(f"  - Flex Message 發送: {'✅' if flex_result and 'error' not in flex_result else '❌'}")
    
    # 提供建議
    print("\n💡 建議:")
    if not leaderboard_data:
        print("  - 檢查 Supabase 連接和數據庫結構")
    if not flex_message:
        print("  - 檢查 create_leaderboard_flex_message 函數")
    if line_result and 'error' in line_result:
        print("  - 檢查 LINE_CHANNEL_ACCESS_TOKEN 和用戶ID")
    if flex_result and 'error' in flex_result:
        print("  - 檢查 Flex Message 格式和 LINE API 限制")

if __name__ == "__main__":
    main()

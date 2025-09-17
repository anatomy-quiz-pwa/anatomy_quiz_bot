#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試用戶輸入「排行榜」觸發功能
"""

import os
import sys
import json
from datetime import datetime

# 添加當前目錄到 Python 路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 設置環境變量
os.environ['SUPABASE_URL'] = 'https://ciqlfqfgzqqgdrogedxg.supabase.co'
os.environ['SUPABASE_ANON_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA'
os.environ['LINE_CHANNEL_ACCESS_TOKEN'] = 'AhZFgYWfEMeFSDxJJhzcvJoKx78lVrfRH3cqqusfiZhug/f5wRhQTkDD9fW7+IJLA3xpoQtunFWoVKnHtaE9p+U1QVFUz1o8CQ5AnNpPicjK32KAD5Z1ouF1HNKATv/BhUHIS3OjcndnUGpOqPDYKAdB04t89/1O/w1cDnyilFU='

def test_leaderboard_keywords():
    """測試排行榜關鍵字觸發"""
    print("🔍 測試排行榜關鍵字觸發...")
    
    try:
        from app_supabase_fixed import handle_text_message
        
        # 測試用戶ID
        test_user_id = "U977c24d1fec3a2bf07035504e1444911"
        
        # 測試各種排行榜關鍵字
        keywords = ['排行榜', 'leaderboard', '排名', '排行', '排行榜 ', ' 排行榜', '排行榜！']
        
        for keyword in keywords:
            print(f"\n📝 測試關鍵字: '{keyword}'")
            
            # 模擬 LINE 訊息格式
            message = {
                'type': 'text',
                'text': keyword
            }
            
            try:
                # 調用處理函數
                handle_text_message(test_user_id, message)
                print(f"✅ 關鍵字 '{keyword}' 處理完成")
            except Exception as e:
                print(f"❌ 關鍵字 '{keyword}' 處理失敗: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_webhook_simulation():
    """模擬 webhook 請求"""
    print("\n🔍 模擬 webhook 請求...")
    
    try:
        from app_supabase_fixed import webhook
        from flask import Flask, request
        
        # 創建測試 Flask 應用
        test_app = Flask(__name__)
        
        # 模擬 LINE webhook 數據
        webhook_data = {
            "events": [
                {
                    "type": "message",
                    "source": {
                        "userId": "U977c24d1fec3a2bf07035504e1444911"
                    },
                    "message": {
                        "type": "text",
                        "text": "排行榜"
                    }
                }
            ]
        }
        
        # 模擬請求
        with test_app.test_request_context('/webhook', 
                                         method='POST', 
                                         json=webhook_data):
            # 直接調用 webhook 函數
            result = webhook()
            print(f"✅ Webhook 處理結果: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Webhook 模擬失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_user_admin_status():
    """測試用戶管理員狀態"""
    print("\n🔍 測試用戶管理員狀態...")
    
    try:
        from app_supabase_fixed import is_admin_user, get_user_admin_permissions
        
        test_user_id = "U977c24d1fec3a2bf07035504e1444911"
        
        # 檢查管理員狀態
        is_admin = is_admin_user(test_user_id)
        print(f"👤 用戶 {test_user_id} 管理員狀態: {is_admin}")
        
        # 獲取詳細管理員信息
        admin_info = get_user_admin_permissions(test_user_id)
        print(f"📋 管理員信息: {admin_info}")
        
        return True
        
    except Exception as e:
        print(f"❌ 測試管理員狀態失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_message_flow():
    """測試完整訊息流程"""
    print("\n🔍 測試完整訊息流程...")
    
    try:
        from app_supabase_fixed import handle_text_message, is_admin_user
        
        test_user_id = "U977c24d1fec3a2bf07035504e1444911"
        
        # 檢查用戶類型
        is_admin = is_admin_user(test_user_id)
        print(f"👤 用戶類型: {'管理員' if is_admin else '普通用戶'}")
        
        # 模擬訊息
        message = {
            'type': 'text',
            'text': '排行榜'
        }
        
        print(f"📨 模擬用戶輸入: {message['text']}")
        
        # 處理訊息
        handle_text_message(test_user_id, message)
        
        print("✅ 完整訊息流程測試完成")
        return True
        
    except Exception as e:
        print(f"❌ 完整訊息流程測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函數"""
    print("🚀 開始測試排行榜輸入觸發功能")
    print("=" * 60)
    
    # 1. 測試用戶管理員狀態
    test_user_admin_status()
    
    # 2. 測試排行榜關鍵字觸發
    test_leaderboard_keywords()
    
    # 3. 測試完整訊息流程
    test_message_flow()
    
    # 4. 測試 webhook 模擬
    test_webhook_simulation()
    
    print("\n" + "=" * 60)
    print("🏁 測試完成")
    
    print("\n💡 如果排行榜功能仍然沒有出現，請檢查：")
    print("  1. 用戶是否正確輸入「排行榜」、「leaderboard」、「排名」或「排行」")
    print("  2. 用戶ID是否正確（LINE 用戶ID應以 'U' 開頭）")
    print("  3. LINE Bot 是否正確配置和部署")
    print("  4. 檢查應用程式日誌以獲取更多詳細信息")

if __name__ == "__main__":
    main()

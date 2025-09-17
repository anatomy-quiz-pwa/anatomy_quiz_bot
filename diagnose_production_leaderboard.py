#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
診斷生產環境排行榜問題
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

def test_production_webhook():
    """測試生產環境 webhook"""
    print("🔍 測試生產環境 webhook...")
    
    try:
        # 生產環境 URL
        webhook_url = "https://anatomy-quiz-bot.onrender.com/webhook"
        
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
        
        # 發送請求
        headers = {'Content-Type': 'application/json'}
        response = requests.post(webhook_url, json=webhook_data, headers=headers, timeout=30)
        
        print(f"📤 Webhook 請求狀態碼: {response.status_code}")
        print(f"📤 Webhook 響應內容: {response.text}")
        
        if response.status_code == 200:
            print("✅ Webhook 請求成功")
            return True
        else:
            print(f"❌ Webhook 請求失敗: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Webhook 測試失敗: {e}")
        return False

def test_production_health():
    """測試生產環境健康狀態"""
    print("\n🔍 測試生產環境健康狀態...")
    
    try:
        # 測試基本連接
        base_url = "https://anatomy-quiz-bot.onrender.com"
        
        # 測試根路徑
        response = requests.get(base_url, timeout=10)
        print(f"📤 根路徑狀態碼: {response.status_code}")
        
        # 測試 webhook 路徑（應該返回 405 Method Not Allowed，因為我們用的是 GET）
        response = requests.get(f"{base_url}/webhook", timeout=10)
        print(f"📤 Webhook GET 狀態碼: {response.status_code}")
        
        if response.status_code == 405:
            print("✅ Webhook 端點存在（405 是預期的，因為我們用 GET 而不是 POST）")
            return True
        else:
            print(f"⚠️ Webhook 端點響應異常: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 健康檢查失敗: {e}")
        return False

def test_local_vs_production():
    """比較本地和生產環境的差異"""
    print("\n🔍 比較本地和生產環境...")
    
    try:
        # 檢查本地檔案
        local_file = "/Users/baobaoc/Dev/anatomy_quiz_bot/app_supabase.py"
        if os.path.exists(local_file):
            print(f"✅ 本地檔案存在: {local_file}")
            
            # 檢查本地檔案大小
            local_size = os.path.getsize(local_file)
            print(f"📊 本地檔案大小: {local_size} bytes")
            
            # 檢查是否有排行榜功能
            with open(local_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'send_leaderboard_message' in content:
                    print("✅ 本地檔案包含排行榜功能")
                else:
                    print("❌ 本地檔案缺少排行榜功能")
                    
                if 'create_leaderboard_flex_message' in content:
                    print("✅ 本地檔案包含 Flex Message 創建功能")
                else:
                    print("❌ 本地檔案缺少 Flex Message 創建功能")
        else:
            print(f"❌ 本地檔案不存在: {local_file}")
            
    except Exception as e:
        print(f"❌ 比較失敗: {e}")

def test_environment_variables():
    """測試環境變數"""
    print("\n🔍 檢查環境變數...")
    
    required_vars = [
        'SUPABASE_URL',
        'SUPABASE_ANON_KEY', 
        'LINE_CHANNEL_ACCESS_TOKEN',
        'LINE_CHANNEL_SECRET'
    ]
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # 只顯示前20個字符
            display_value = value[:20] + "..." if len(value) > 20 else value
            print(f"✅ {var}: {display_value}")
        else:
            print(f"❌ {var}: 未設置")

def simulate_user_input():
    """模擬用戶輸入排行榜"""
    print("\n🔍 模擬用戶輸入排行榜...")
    
    try:
        # 導入本地函數進行測試
        sys.path.append('/Users/baobaoc/Dev/anatomy_quiz_bot')
        from app_supabase import handle_text_message
        
        # 模擬訊息
        message = {
            'type': 'text',
            'text': '排行榜'
        }
        
        # 測試用戶ID
        test_user_id = "U977c24d1fec3a2bf07035504e1444911"
        
        print(f"📨 模擬用戶 {test_user_id} 輸入: {message['text']}")
        
        # 處理訊息
        handle_text_message(test_user_id, message)
        
        print("✅ 本地模擬測試完成")
        return True
        
    except Exception as e:
        print(f"❌ 本地模擬測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函數"""
    print("🚀 開始診斷生產環境排行榜問題")
    print("=" * 60)
    
    # 1. 檢查環境變數
    test_environment_variables()
    
    # 2. 測試生產環境健康狀態
    health_ok = test_production_health()
    
    # 3. 比較本地和生產環境
    test_local_vs_production()
    
    # 4. 本地模擬測試
    local_ok = simulate_user_input()
    
    # 5. 測試生產環境 webhook
    if health_ok:
        webhook_ok = test_production_webhook()
    else:
        webhook_ok = False
    
    print("\n" + "=" * 60)
    print("🏁 診斷完成")
    
    # 總結
    print("\n📊 診斷結果總結:")
    print(f"  - 環境變數: {'✅' if all(os.getenv(var) for var in ['SUPABASE_URL', 'SUPABASE_ANON_KEY', 'LINE_CHANNEL_ACCESS_TOKEN']) else '❌'}")
    print(f"  - 生產環境健康: {'✅' if health_ok else '❌'}")
    print(f"  - 本地功能測試: {'✅' if local_ok else '❌'}")
    print(f"  - 生產環境 Webhook: {'✅' if webhook_ok else '❌'}")
    
    # 提供建議
    print("\n💡 建議:")
    if not health_ok:
        print("  - 檢查生產環境部署狀態")
    if not webhook_ok:
        print("  - 檢查 LINE Bot webhook 配置")
        print("  - 確認 LINE Bot 是否正確連接到生產環境")
    if local_ok and not webhook_ok:
        print("  - 本地功能正常，問題可能在生產環境配置")
        print("  - 建議檢查 Render 部署日誌")

if __name__ == "__main__":
    main()

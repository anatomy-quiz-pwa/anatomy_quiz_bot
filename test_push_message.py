#!/usr/bin/env python3
import os
import requests
from linebot import LineBotApi
from linebot.models import TextSendMessage
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

def test_push_message():
    """測試推送訊息到真實的 LINE userId"""
    channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
    user_id = "U977c24d1fec3a2bf07035504e1444911"  # 你的真實 userId
    
    print("=== 測試推送訊息 ===")
    print(f"Channel Access Token: {channel_access_token[:20] if channel_access_token else 'None'}...")
    print(f"User ID: {user_id}")
    
    if not channel_access_token:
        print("❌ 缺少 Channel Access Token")
        return False
    
    try:
        # 建立 LineBotApi 實例
        line_bot_api = LineBotApi(channel_access_token)
        
        # 測試推送訊息
        message = TextSendMessage(text="🔧 這是一個測試訊息，如果你看到這則訊息，表示 LINE Bot 設定正確！")
        
        print("📤 正在發送測試訊息...")
        line_bot_api.push_message(user_id, message)
        
        print("✅ 測試訊息發送成功！")
        print("💡 請檢查你的 LINE App，應該會收到這則測試訊息")
        return True
        
    except Exception as e:
        print(f"❌ 推送訊息失敗: {str(e)}")
        
        # 詳細錯誤分析
        if "400" in str(e) and "Invalid reply token" in str(e):
            print("💡 這是 reply_message 的錯誤，不是 push_message 的問題")
        elif "400" in str(e) and "The property, 'to', in the request body is invalid" in str(e):
            print("💡 userId 格式有問題，請確認是否為正確的 LINE userId")
        elif "401" in str(e):
            print("💡 Channel Access Token 無效或過期")
        elif "403" in str(e):
            print("💡 Bot 沒有權限發送訊息給此用戶")
        elif "404" in str(e):
            print("💡 用戶不存在或未加 Bot 為好友")
        
        return False

def test_bot_profile():
    """測試 Bot Profile API"""
    channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
    
    print("\n=== 測試 Bot Profile API ===")
    
    headers = {
        'Authorization': f'Bearer {channel_access_token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get('https://api.line.me/v2/bot/profile/U977c24d1fec3a2bf07035504e1444911', headers=headers)
        print(f"Bot Profile API 狀態碼: {response.status_code}")
        print(f"Bot Profile API 回應: {response.text}")
        
        if response.status_code == 200:
            print("✅ Bot Profile API 正常")
            return True
        else:
            print("❌ Bot Profile API 失敗")
            return False
            
    except Exception as e:
        print(f"❌ Bot Profile API 錯誤: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔍 開始測試 LINE Bot 功能...")
    
    # 測試 Bot Profile API
    bot_profile_ok = test_bot_profile()
    
    # 測試推送訊息
    push_ok = test_push_message()
    
    print("\n=== 測試總結 ===")
    if bot_profile_ok and push_ok:
        print("🎉 所有測試都通過！LINE Bot 設定正確")
    elif push_ok:
        print("✅ 推送訊息功能正常，但 Bot Profile API 有問題")
        print("💡 這可能是因為 Bot 尚未加為好友")
    else:
        print("❌ 有問題需要解決")
        print("💡 請檢查：")
        print("   1. Channel Access Token 是否正確")
        print("   2. 是否已經加 Bot 為好友")
        print("   3. Bot 是否已啟用") 
#!/usr/bin/env python3
import os
import requests
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

def test_line_credentials():
    """測試 LINE Bot 憑證是否有效"""
    channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
    channel_secret = os.getenv('LINE_CHANNEL_SECRET')
    
    print("=== LINE Bot 憑證測試 ===")
    print(f"Channel Access Token: {channel_access_token[:20] if channel_access_token else 'None'}...")
    print(f"Channel Secret: {channel_secret[:10] if channel_secret else 'None'}...")
    
    if not channel_access_token or not channel_secret:
        print("❌ 缺少 LINE Bot 憑證")
        return False
    
    # 測試 LINE Bot API
    headers = {
        'Authorization': f'Bearer {channel_access_token}',
        'Content-Type': 'application/json'
    }
    
    try:
        # 獲取 bot 資訊
        response = requests.get('https://api.line.me/v2/bot/profile', headers=headers)
        print(f"Bot Profile API 回應: {response.status_code}")
        
        if response.status_code == 200:
            bot_info = response.json()
            print(f"✅ Bot 名稱: {bot_info.get('displayName', 'Unknown')}")
            print(f"✅ Bot ID: {bot_info.get('userId', 'Unknown')}")
            return True
        else:
            print(f"❌ Bot Profile API 失敗: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        return False

def test_webhook_url():
    """測試 webhook URL 是否可訪問"""
    print("\n=== Webhook URL 測試 ===")
    
    # 檢查本地服務器
    try:
        response = requests.get('http://localhost:5001/', timeout=5)
        if response.status_code == 200:
            print("✅ 本地服務器正常運行")
        else:
            print(f"❌ 本地服務器回應異常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 無法連接到本地服務器: {e}")
        return False
    
    # 檢查 webhook 端點
    try:
        response = requests.get('http://localhost:5001/callback', timeout=5)
        if response.status_code == 200:
            print("✅ Webhook 端點正常")
        else:
            print(f"❌ Webhook 端點回應異常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 無法連接到 webhook 端點: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🔍 開始診斷 LINE Bot 問題...")
    
    credentials_ok = test_line_credentials()
    webhook_ok = test_webhook_url()
    
    print("\n=== 診斷結果 ===")
    if credentials_ok and webhook_ok:
        print("✅ 所有測試通過")
        print("\n💡 建議:")
        print("1. 確保 LINE Developers Console 中的 webhook URL 設定為: http://localhost:5001/callback")
        print("2. 確保 webhook 已啟用")
        print("3. 在 LINE 中發送訊息給 bot 測試")
    else:
        print("❌ 發現問題")
        if not credentials_ok:
            print("- LINE Bot 憑證有問題")
        if not webhook_ok:
            print("- Webhook URL 有問題") 
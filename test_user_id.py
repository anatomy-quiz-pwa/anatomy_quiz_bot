#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from linebot import LineBotApi
from linebot.exceptions import LineBotApiError

# 載入環境變數
load_dotenv()

def test_line_api():
    """測試 LINE API 連線和 user_id 格式"""
    LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
    USER_ID = os.getenv('USER_ID')
    
    if not LINE_CHANNEL_ACCESS_TOKEN:
        print("❌ LINE_CHANNEL_ACCESS_TOKEN 未設定")
        return
    
    if not USER_ID:
        print("❌ USER_ID 未設定")
        return
    
    print(f"✅ LINE_CHANNEL_ACCESS_TOKEN: {LINE_CHANNEL_ACCESS_TOKEN[:20]}...")
    print(f"✅ USER_ID: {USER_ID}")
    print(f"✅ USER_ID 長度: {len(USER_ID)}")
    print(f"✅ USER_ID 格式檢查: {'U' if USER_ID.startswith('U') else '非U開頭'}")
    
    try:
        line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
        
        # 測試獲取 profile
        profile = line_bot_api.get_profile(USER_ID)
        print(f"✅ 成功獲取用戶資料: {profile.display_name}")
        
        # 測試發送測試訊息
        from linebot.models import TextSendMessage
        result = line_bot_api.push_message(USER_ID, TextSendMessage(text="🔧 這是一個測試訊息"))
        print("✅ 成功發送測試訊息")
        
    except LineBotApiError as e:
        print(f"❌ LINE API 錯誤: {e}")
        print(f"   錯誤代碼: {e.status_code}")
        print(f"   錯誤訊息: {e.error_response}")
    except Exception as e:
        print(f"❌ 其他錯誤: {e}")

if __name__ == "__main__":
    test_line_api() 
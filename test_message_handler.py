#!/usr/bin/env python3
"""
直接測試訊息處理函數
"""

import os
import sys
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

def test_message_handler():
    """直接測試訊息處理函數"""
    print("🧪 直接測試訊息處理函數...")
    
    try:
        # 模擬 LINE 事件
        from linebot.models import MessageEvent, TextMessage, Source, User
        
        # 創建模擬的事件對象
        source = User(user_id="test_user_123")
        message = TextMessage(text="開始")
        event = MessageEvent(
            type="message",
            mode="active",
            timestamp=1234567890,
            source=source,
            webhook_event_id="test_event_id",
            delivery_context=None,
            reply_token="test_reply_token",
            message=message
        )
        
        print(f"📝 模擬事件: {event}")
        print(f"📝 訊息內容: {event.message.text}")
        print(f"📝 用戶ID: {event.source.user_id}")
        
        # 測試 safe_reply_message 函數
        from app_supabase import safe_reply_message
        from linebot.models import TextSendMessage
        
        test_message = TextSendMessage(text="測試訊息")
        result = safe_reply_message("test_reply_token", test_message)
        print(f"📤 發送測試訊息結果: {result}")
        
        # 測試 get_user_correct_wrong 函數
        from main_supabase import get_user_correct_wrong
        
        correct, wrong = get_user_correct_wrong("test_user_123")
        print(f"📊 用戶統計: correct={correct}, wrong={wrong}")
        
        print("✅ 直接測試完成")
        
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_message_handler() 
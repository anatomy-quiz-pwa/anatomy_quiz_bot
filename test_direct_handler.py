#!/usr/bin/env python3
"""
直接調用處理函數測試
"""

import sys
import os

# 添加當前目錄到 Python 路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_direct_handler():
    """直接測試處理函數"""
    
    try:
        from app_supabase import handle_message
        from linebot.models import MessageEvent, TextMessage, Source, UserSource
        
        # 創建模擬的事件對象
        user_id = "U1234567890abcdef1234567890abcdef"
        text = "開始"
        
        # 創建模擬的用戶源
        source = UserSource(user_id=user_id)
        
        # 創建模擬的文本訊息
        message = TextMessage(text=text)
        
        # 創建模擬的事件
        event = MessageEvent(
            message=message,
            reply_token="test_reply_token_direct",
            source=source,
            timestamp=1234567890
        )
        
        print("🧪 直接測試處理函數...")
        print(f"🔍 模擬用戶 ID: {user_id}")
        print(f"📝 模擬訊息: {text}")
        
        # 直接調用處理函數
        handle_message(event)
        
        print("✅ 測試完成！")
        
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_direct_handler() 
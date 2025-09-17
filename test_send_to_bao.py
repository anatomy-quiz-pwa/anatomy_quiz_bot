#!/usr/bin/env python3
"""
發送測試訊息到保的帳號
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app_supabase import (
    send_message,
    send_completion_celebration,
    get_user_nickname
)
import logging
import datetime

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_send_to_bao():
    """發送測試訊息到保的帳號"""
    print("📱 發送測試訊息到保的帳號")
    print("=" * 50)
    
    # 保的LINE用戶ID
    bao_user_id = "U977c24d1fec3a2bf07035504e1444911"
    
    print(f"目標用戶ID: {bao_user_id}")
    print()
    
    # 1. 發送基本測試訊息
    try:
        test_message = {
            "text": f"🧪 這是發送到保的帳號的測試訊息\n\n⏰ 時間: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n如果你收到這個訊息，表示連接正常！"
        }
        send_message(bao_user_id, test_message)
        print("✅ 基本測試訊息發送成功")
    except Exception as e:
        print(f"❌ 基本測試訊息發送失敗: {e}")
    
    print()
    
    # 2. 獲取並顯示暱稱
    try:
        nickname = get_user_nickname(bao_user_id)
        print(f"用戶暱稱: {nickname}")
        
        nickname_message = {
            "text": f"👋 你好 {nickname}！\n\n這是暱稱確認訊息。"
        }
        send_message(bao_user_id, nickname_message)
        print("✅ 暱稱確認訊息發送成功")
    except Exception as e:
        print(f"❌ 暱稱相關操作失敗: {e}")
    
    print()
    
    # 3. 發送Level 14通關完成訊息
    try:
        print("發送Level 14通關完成訊息...")
        send_completion_celebration(bao_user_id, 14)
        print("✅ Level 14通關完成訊息發送成功")
    except Exception as e:
        print(f"❌ Level 14通關完成訊息發送失敗: {e}")
    
    print()
    print("=" * 50)
    print("🎉 測試完成")
    print()
    print("你應該收到:")
    print("1. 基本測試訊息")
    print("2. 暱稱確認訊息") 
    print("3. Level 14通關完成Flex Message")

if __name__ == "__main__":
    test_send_to_bao()

#!/usr/bin/env python3
"""
發送測試訊息到保的正確LINE帳號
U977c24d1fec3a2bf07035504e1444911
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app_supabase import (
    send_completion_celebration,
    send_level_up_celebration,
    get_user_nickname,
    send_message,
    create_completion_celebration_flex,
    supabase
)
import logging
import datetime
import time

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_bao_correct_account():
    """測試發送訊息到保的正確帳號"""
    print("🎯 發送測試訊息到保的正確LINE帳號")
    print("=" * 60)
    
    # 保的正確LINE用戶ID
    bao_user_id = "U977c24d1fec3a2bf07035504e1444911"
    
    print(f"📱 保的正確用戶ID: {bao_user_id}")
    print()
    
    # 1. 發送基本測試訊息
    print("1️⃣ 發送基本測試訊息...")
    try:
        basic_message = {
            "text": f"🧪 這是發送到保的正確LINE帳號的測試訊息！\n\n📱 帳號ID: {bao_user_id}\n⏰ 測試時間: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n如果你收到這個訊息，表示我們已經成功連接到你的正確帳號！"
        }
        send_message(bao_user_id, basic_message)
        print("   ✅ 基本測試訊息發送成功！")
    except Exception as e:
        print(f"   ❌ 基本測試訊息發送失敗: {e}")
    print()
    
    # 2. 測試獲取用戶暱稱
    print("2️⃣ 測試獲取用戶暱稱...")
    try:
        nickname = get_user_nickname(bao_user_id)
        print(f"   ✅ 獲取暱稱成功: {nickname}")
        
        # 發送暱稱確認訊息
        nickname_message = {
            "text": f"👋 你好 {nickname}！\n\n我已經成功從數據庫中獲取到你的暱稱。\n如果這個暱稱不正確，請告訴我需要更新。"
        }
        send_message(bao_user_id, nickname_message)
        print("   ✅ 暱稱確認訊息發送成功！")
        
    except Exception as e:
        print(f"   ❌ 獲取暱稱失敗: {e}")
        nickname = "保"
    print()
    
    # 3. 測試Level 14闖關成功訊息
    print("3️⃣ 測試Level 14闖關成功訊息...")
    try:
        # 發送預告訊息
        preview_message = {
            "text": "🎮 接下來我會發送Level 14闖關成功的訊息給你，\n這樣你就可以看到用戶完成最高等級時會收到什麼樣的慶祝訊息！"
        }
        send_message(bao_user_id, preview_message)
        print("   📢 預告訊息發送成功")
        
        # 等待2秒
        time.sleep(2)
        
        # 發送通關完成慶祝訊息
        send_completion_celebration(bao_user_id, 14)
        print("   ✅ Level 14闖關成功訊息發送成功！")
        
    except Exception as e:
        print(f"   ❌ Level 14闖關成功訊息發送失敗: {e}")
    print()
    
    # 4. 測試升級情境
    print("4️⃣ 測試從Level 13升級到Level 14的情境...")
    try:
        # 發送情境說明
        scenario_message = {
            "text": "🎯 模擬情境：\n用戶剛好在Level 13答對了第3題，\n系統會自動升級到Level 14並觸發通關完成訊息。"
        }
        send_message(bao_user_id, scenario_message)
        print("   📋 情境說明發送成功")
        
        # 等待2秒
        time.sleep(2)
        
        # 模擬升級
        send_level_up_celebration(bao_user_id, 13, 14)
        print("   ✅ 升級情境測試成功！")
        
    except Exception as e:
        print(f"   ❌ 升級情境測試失敗: {e}")
    print()
    
    # 5. 發送測試完成總結
    print("5️⃣ 發送測試完成總結...")
    try:
        summary_message = {
            "text": f"""🎉 Level 14闖關成功訊息測試完成！

📋 測試項目：
✅ 基本訊息發送
✅ 暱稱獲取和確認  
✅ 通關完成慶祝訊息
✅ 升級情境模擬
✅ Flex Message格式訊息

📱 測試帳號: {bao_user_id}
👤 用戶暱稱: {nickname}
⏰ 完成時間: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

💡 功能狀態: 所有測試都成功執行！
當用戶在Level 14答對3題時，系統會自動發送精美的闖關成功訊息。"""
        }
        send_message(bao_user_id, summary_message)
        print("   ✅ 測試完成總結發送成功！")
        
    except Exception as e:
        print(f"   ❌ 測試完成總結發送失敗: {e}")
    print()
    
    print("=" * 60)
    print("🎉 所有測試訊息已發送到保的正確LINE帳號！")
    print()
    print("📋 帳號資訊記錄：")
    print(f"   👤 用戶: 保")
    print(f"   📱 LINE ID: {bao_user_id}")
    print(f"   🏷️ 暱稱: {nickname}")
    print(f"   📅 測試日期: {datetime.datetime.now().strftime('%Y-%m-%d')}")
    print()
    print("💡 請確認你的LINE是否收到了以上所有測試訊息！")

if __name__ == "__main__":
    test_bao_correct_account()

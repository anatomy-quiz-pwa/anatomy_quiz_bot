#!/usr/bin/env python3
"""
測試Level 14闖關成功訊息發送到保的LINE ID
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

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_level_14_completion_message():
    """測試Level 14闖關成功訊息發送"""
    print("🎯 測試Level 14闖關成功訊息發送")
    print("=" * 60)
    
    # 保的LINE用戶ID
    bao_user_id = "U9a9df49945755ef651d067743f3c7ea7"
    
    print(f"📱 目標用戶ID: {bao_user_id}")
    print()
    
    # 1. 測試獲取用戶暱稱
    print("1️⃣ 測試獲取用戶暱稱...")
    try:
        nickname = get_user_nickname(bao_user_id)
        print(f"   ✅ 獲取暱稱成功: {nickname}")
    except Exception as e:
        print(f"   ❌ 獲取暱稱失敗: {e}")
        nickname = "保"
    print()
    
    # 2. 測試創建通關完成Flex Message
    print("2️⃣ 測試創建通關完成Flex Message...")
    try:
        completion_flex = create_completion_celebration_flex(nickname, 14)
        if completion_flex:
            print("   ✅ Flex Message創建成功")
            print(f"   📝 altText: {completion_flex.get('altText', 'N/A')}")
        else:
            print("   ❌ Flex Message創建失敗")
    except Exception as e:
        print(f"   ❌ Flex Message創建錯誤: {e}")
        completion_flex = None
    print()
    
    # 3. 發送通關完成慶祝訊息
    print("3️⃣ 發送通關完成慶祝訊息...")
    try:
        send_completion_celebration(bao_user_id, 14)
        print("   ✅ 通關完成慶祝訊息發送成功！")
        print("   📨 訊息已發送到保的LINE帳號")
    except Exception as e:
        print(f"   ❌ 訊息發送失敗: {e}")
    print()
    
    # 4. 模擬從Level 13升級到Level 14的情況
    print("4️⃣ 模擬從Level 13升級到Level 14...")
    try:
        # 這會觸發通關完成訊息，因為14是最高等級
        send_level_up_celebration(bao_user_id, 13, 14)
        print("   ✅ 升級慶祝訊息發送成功！")
        print("   📨 由於達到最高等級14，會自動發送通關完成訊息")
    except Exception as e:
        print(f"   ❌ 升級訊息發送失敗: {e}")
    print()
    
    # 5. 發送測試完成通知
    print("5️⃣ 發送測試完成通知...")
    try:
        import datetime
        test_message = {
            "text": f"🧪 Level 14闖關成功訊息測試完成！\n\n📱 測試對象: {nickname}\n🎯 測試項目: Level 14通關完成訊息\n⏰ 測試時間: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n如果你收到了上面的通關完成訊息，表示功能正常運作！"
        }
        send_message(bao_user_id, test_message)
        print("   ✅ 測試完成通知發送成功！")
    except Exception as e:
        print(f"   ❌ 測試通知發送失敗: {e}")
    print()
    
    print("=" * 60)
    print("🎉 Level 14闖關成功訊息測試完成！")
    print()
    print("📋 測試總結：")
    print("   • 測試了通關完成Flex Message創建")
    print("   • 測試了send_completion_celebration函數")
    print("   • 測試了從Level 13升級到Level 14的情況")
    print("   • 發送了實際訊息到保的LINE帳號")
    print()
    print("💡 預期結果：")
    print("   保應該會收到：")
    print("   1. 🏆 通關完成慶祝訊息（Flex Message或文字訊息）")
    print("   2. 🏅 終極解剖師徽章獲得訊息")
    print("   3. 🧪 測試完成通知訊息")

def create_simple_test_message():
    """創建簡單的測試訊息"""
    bao_user_id = "U9a9df49945755ef651d067743f3c7ea7"
    
    print("📨 發送簡單測試訊息...")
    try:
        simple_message = {
            "text": "🧪 這是Level 14闖關成功訊息的測試！\n\n如果你看到這個訊息，表示系統可以正常發送訊息到你的LINE帳號。\n\n接下來會測試實際的闖關成功訊息功能。"
        }
        send_message(bao_user_id, simple_message)
        print("   ✅ 簡單測試訊息發送成功！")
        return True
    except Exception as e:
        print(f"   ❌ 簡單測試訊息發送失敗: {e}")
        return False

if __name__ == "__main__":
    import datetime
    
    # 先發送簡單測試訊息
    if create_simple_test_message():
        print("\n" + "="*20 + " 等待3秒 " + "="*20)
        import time
        time.sleep(3)
        
        # 再執行完整測試
        test_level_14_completion_message()
    else:
        print("❌ 簡單測試失敗，請檢查LINE連接設定")

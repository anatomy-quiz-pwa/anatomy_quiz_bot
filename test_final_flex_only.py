#!/usr/bin/env python3
"""
發送最終版本的Level 14通關恭喜訊息 - 只有Flex Message
包含新的等級稱號系統
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app_supabase import (
    send_completion_celebration,
    send_message,
    get_user_nickname,
    get_level_title
)
import logging
import datetime

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_final_flex_only():
    """測試最終版本的通關恭喜訊息"""
    print("🎯 發送最終版本的Level 14通關恭喜訊息")
    print("=" * 60)
    
    # 保的LINE用戶ID
    bao_user_id = "U977c24d1fec3a2bf07035504e1444911"
    
    print(f"📱 目標用戶ID: {bao_user_id}")
    print("✨ 新功能: 更新的等級稱號系統")
    print("🎯 訊息類型: 只發送Flex Message，無任何額外文字")
    print()
    
    # 1. 顯示新的等級稱號
    print("1️⃣ 新的等級稱號系統...")
    try:
        level_14_title = get_level_title(14)
        print(f"   🏆 Level 14稱號: {level_14_title}")
        print("   📋 完整稱號系統:")
        for level in range(1, 15):
            title = get_level_title(level)
            print(f"      Level {level:2d}: {title}")
    except Exception as e:
        print(f"   ❌ 獲取稱號失敗: {e}")
    print()
    
    # 2. 發送更新通知
    print("2️⃣ 發送更新通知...")
    try:
        update_message = {
            "text": f"🎉 Level 14通關恭喜訊息最終版本！\n\n✨ 新功能:\n• 全新的等級稱號系統\n• Level 14: 解剖學傳說\n• 只發送精美Flex Message\n• 移除所有額外文字訊息\n\n📅 更新時間: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n接下來會發送最終版本的通關恭喜訊息！"
        }
        send_message(bao_user_id, update_message)
        print("   ✅ 更新通知發送成功！")
    except Exception as e:
        print(f"   ❌ 更新通知發送失敗: {e}")
    print()
    
    # 3. 獲取用戶暱稱
    print("3️⃣ 獲取用戶暱稱...")
    try:
        nickname = get_user_nickname(bao_user_id)
        print(f"   ✅ 用戶暱稱: {nickname}")
    except Exception as e:
        print(f"   ❌ 獲取暱稱失敗: {e}")
        nickname = "pao"
    print()
    
    # 4. 發送最終版本的通關恭喜訊息
    print("4️⃣ 發送最終版本的通關恭喜訊息...")
    print("   📋 預期行為:")
    print("      • 只會發送1則精美的Flex Message")
    print("      • 包含新的等級稱號「解剖學傳說」")
    print("      • 不會有任何額外的文字訊息")
    print("      • 即使發送失敗也不會有備用文字訊息")
    try:
        send_completion_celebration(bao_user_id, 14)
        print("   ✅ 通關恭喜訊息發送成功！")
        print("   📨 請檢查你的LINE:")
        print("      • 應該只收到1則精美的Flex Message")
        print("      • 稱號應該顯示為「解剖學傳說」")
        print("      • 沒有任何額外的文字訊息")
    except Exception as e:
        print(f"   ❌ 通關恭喜訊息發送失敗: {e}")
    print()
    
    # 5. 發送測試完成確認
    print("5️⃣ 發送測試完成確認...")
    try:
        confirm_message = {
            "text": f"🎉 Level 14通關恭喜訊息最終版本測試完成！\n\n📋 功能確認:\n✅ 新等級稱號系統已啟用\n✅ Level 14 = 解剖學傳說\n✅ 只發送Flex Message\n✅ 移除所有備用文字訊息\n✅ 移除徽章額外通知\n\n🎯 用戶體驗:\n• 乾淨簡潔的通關體驗\n• 精美的視覺呈現\n• 避免訊息洗版\n\n如果上面只收到1則Flex Message（顯示「解剖學傳說」），表示所有功能都正常運作！"
        }
        send_message(bao_user_id, confirm_message)
        print("   ✅ 測試完成確認發送成功！")
    except Exception as e:
        print(f"   ❌ 測試完成確認發送失敗: {e}")
    print()
    
    print("=" * 60)
    print("🎉 Level 14通關恭喜訊息最終版本測試完成！")
    print()
    print("📋 最終版本特色：")
    print("   ✨ 全新等級稱號系統 (Level 14: 解剖學傳說)")
    print("   🏆 只發送1則精美的Flex Message")
    print("   ❌ 移除所有額外文字訊息")
    print("   ❌ 移除所有備用文字訊息")
    print("   ❌ 移除徽章獲得通知")
    print()
    print("🔍 請確認：")
    print("   1. 你是否只收到了1則Flex Message？")
    print("   2. Flex Message中是否顯示「解剖學傳說」稱號？")
    print("   3. 沒有收到任何額外的文字訊息？")
    print()
    print("💡 現在所有Level 14通關的用戶都會獲得「解剖學傳說」稱號，")
    print("   並只收到1則精美的Flex Message慶祝訊息！")

if __name__ == "__main__":
    test_final_flex_only()

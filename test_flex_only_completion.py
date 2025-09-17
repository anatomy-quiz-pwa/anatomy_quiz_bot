#!/usr/bin/env python3
"""
測試修改後的Level 14通關完成訊息 - 只發送Flex Message
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app_supabase import (
    send_completion_celebration,
    send_message,
    get_user_nickname
)
import logging
import datetime

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_flex_only_completion():
    """測試只發送Flex Message的通關完成訊息"""
    print("🎯 測試修改後的Level 14通關完成訊息")
    print("=" * 60)
    
    # 保的LINE用戶ID
    bao_user_id = "U977c24d1fec3a2bf07035504e1444911"
    
    print(f"📱 目標用戶ID: {bao_user_id}")
    print("🎯 修改內容: 移除額外的徽章文字訊息，只保留Flex Message")
    print()
    
    # 1. 發送修改說明
    print("1️⃣ 發送修改說明...")
    try:
        update_message = {
            "text": f"🔄 Level 14通關完成訊息已優化！\n\n✅ 修改內容:\n• 移除額外的徽章文字訊息\n• 只保留精美的Flex Message\n• 徽章資訊已包含在Flex Message中\n\n📅 修改時間: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n接下來會發送修改後的通關完成訊息測試！"
        }
        send_message(bao_user_id, update_message)
        print("   ✅ 修改說明發送成功！")
    except Exception as e:
        print(f"   ❌ 修改說明發送失敗: {e}")
    print()
    
    # 2. 獲取用戶暱稱
    print("2️⃣ 獲取用戶暱稱...")
    try:
        nickname = get_user_nickname(bao_user_id)
        print(f"   ✅ 用戶暱稱: {nickname}")
    except Exception as e:
        print(f"   ❌ 獲取暱稱失敗: {e}")
        nickname = "pao"
    print()
    
    # 3. 發送修改後的通關完成訊息
    print("3️⃣ 發送修改後的通關完成訊息...")
    print("   📋 預期行為: 只會發送1則Flex Message，不會有額外的文字訊息")
    try:
        send_completion_celebration(bao_user_id, 14)
        print("   ✅ 通關完成訊息發送成功！")
        print("   📨 請檢查你的LINE:")
        print("      • 應該只收到1則精美的Flex Message")
        print("      • 不應該收到額外的徽章文字訊息")
    except Exception as e:
        print(f"   ❌ 通關完成訊息發送失敗: {e}")
    print()
    
    # 4. 發送確認訊息
    print("4️⃣ 發送確認訊息...")
    try:
        confirm_message = {
            "text": f"✅ Level 14通關完成訊息修改完成！\n\n📋 修改結果:\n• 移除了額外的徽章文字訊息\n• 現在只會發送1則精美的Flex Message\n• 徽章資訊已包含在Flex Message的內容中\n\n🎯 用戶體驗優化:\n• 減少訊息數量，避免洗版\n• 保持通關慶祝的儀式感\n• 所有重要資訊都在Flex Message中呈現\n\n如果上面只收到1則Flex Message（沒有額外文字），表示修改成功！"
        }
        send_message(bao_user_id, confirm_message)
        print("   ✅ 確認訊息發送成功！")
    except Exception as e:
        print(f"   ❌ 確認訊息發送失敗: {e}")
    print()
    
    print("=" * 60)
    print("🎉 Level 14通關完成訊息修改測試完成！")
    print()
    print("📋 修改總結：")
    print("   ✅ 移除了 badge_message 的發送")
    print("   ✅ 保留了精美的Flex Message")
    print("   ✅ 徽章資訊已包含在Flex Message內容中")
    print()
    print("🔍 請確認：")
    print("   1. 你是否只收到了1則Flex Message（通關恭喜）？")
    print("   2. 沒有收到額外的徽章文字訊息？")
    print("   3. Flex Message中是否包含了完整的通關資訊？")
    print()
    print("💡 現在所有Level 14通關的用戶都只會收到1則精美的Flex Message！")

if __name__ == "__main__":
    test_flex_only_completion()

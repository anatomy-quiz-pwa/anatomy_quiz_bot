#!/usr/bin/env python3
"""
純粹的Level 14通關完成訊息測試 - 不包含任何測試說明訊息
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app_supabase import send_completion_celebration
import logging

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_pure_completion():
    """純粹的通關完成訊息測試"""
    print("🎯 發送純粹的Level 14通關完成訊息（無測試說明）")
    print("=" * 60)
    
    # 保的LINE用戶ID
    bao_user_id = "U977c24d1fec3a2bf07035504e1444911"
    
    print(f"📱 目標用戶ID: {bao_user_id}")
    print("📋 測試內容: 只調用 send_completion_celebration() 函數")
    print("🎯 預期結果: 只會收到1則Flex Message，沒有任何額外訊息")
    print()
    
    # 直接發送通關完成訊息，不包含任何測試說明
    print("發送通關完成訊息...")
    try:
        send_completion_celebration(bao_user_id, 14)
        print("✅ 通關完成訊息發送成功")
        print("📨 請檢查LINE: 應該只收到1則Flex Message")
    except Exception as e:
        print(f"❌ 發送失敗: {e}")
    
    print()
    print("=" * 60)
    print("🎉 純粹通關訊息測試完成")
    print()
    print("💡 這次你應該只收到:")
    print("   • 1則Flex Message（顯示「解剖學傳說」）")
    print("   • 沒有任何額外的文字訊息")
    print("   • 沒有任何測試說明訊息")

if __name__ == "__main__":
    test_pure_completion()

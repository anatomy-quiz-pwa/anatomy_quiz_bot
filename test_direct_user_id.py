#!/usr/bin/env python3
"""
直接測試用戶 ID 顯示功能
"""

import sys
import os

# 添加當前目錄到 Python 路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_user_id_display():
    """測試用戶 ID 顯示功能"""
    
    # 模擬用戶 ID 和訊息
    user_id = "U1234567890abcdef1234567890abcdef"
    text = "開始"
    
    print(f"🔍 收到訊息 - 用戶 ID: {user_id}")
    print(f"📝 訊息內容: {text}")
    
    # 測試不同的用戶 ID
    test_user_ids = [
        "U1234567890abcdef1234567890abcdef",
        "U9876543210fedcba0987654321fedcba",
        "Uabcdef1234567890abcdef1234567890"
    ]
    
    print("\n🧪 測試多個用戶 ID:")
    for i, test_id in enumerate(test_user_ids, 1):
        print(f"   {i}. 用戶 ID: {test_id}")
    
    print("\n💡 現在請在 LINE 中發送任何訊息，然後查看 Flask 應用的控制台輸出")
    print("   你應該會看到類似的輸出：")
    print("   🔍 收到訊息 - 用戶 ID: [你的真實用戶 ID]")
    print("   📝 訊息內容: [你的訊息內容]")

if __name__ == "__main__":
    test_user_id_display() 
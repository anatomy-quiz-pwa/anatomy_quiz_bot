#!/usr/bin/env python3
"""
測試本地排行榜功能
"""

import sys
import os

# 添加當前目錄到 Python 路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_leaderboard_functions():
    """測試排行榜相關函數"""
    try:
        # 導入修復後的應用程式
        from app_supabase_fixed import (
            get_leaderboard_data,
            send_leaderboard_message,
            create_leaderboard_flex_message
        )
        
        print("✅ 成功導入排行榜相關函數")
        
        # 測試獲取排行榜數據
        print("\n🧪 測試獲取排行榜數據...")
        leaderboard_data = get_leaderboard_data()
        print(f"📊 獲取到 {len(leaderboard_data)} 條排行榜數據")
        
        if leaderboard_data:
            print("✅ 排行榜數據獲取成功")
            for i, user in enumerate(leaderboard_data[:3]):
                print(f"  {i+1}. {user.get('nickname', 'N/A')} - {user.get('score', 0)}分")
        else:
            print("⚠️ 沒有獲取到排行榜數據")
        
        # 測試生成 Flex Message
        print("\n🧪 測試生成 Flex Message...")
        test_user_id = "U977c24d1fec3a2bf07035504e1444911"
        flex_message = create_leaderboard_flex_message(leaderboard_data, leaderboard_data, test_user_id)
        print("✅ Flex Message 生成成功")
        print(f"📊 Flex Message 類型: {flex_message.get('type')}")
        print(f"📊 Alt Text: {flex_message.get('altText', 'N/A')}")
        
        # 測試發送排行榜訊息（使用測試用戶ID）
        print("\n🧪 測試發送排行榜訊息...")
        send_leaderboard_message(test_user_id)
        print("✅ 排行榜訊息發送成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函數"""
    print("🔧 測試本地排行榜功能...")
    
    success = test_leaderboard_functions()
    
    if success:
        print("\n🎉 本地排行榜功能測試通過！")
        print("📋 修復後的代碼可以正常工作")
    else:
        print("\n❌ 本地排行榜功能測試失敗")
        print("📋 需要進一步檢查代碼問題")

if __name__ == "__main__":
    main()

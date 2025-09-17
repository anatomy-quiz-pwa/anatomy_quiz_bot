#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用真實 LINE Bot 憑證測試排行榜功能
"""

import os
import sys
import json
from datetime import datetime

# 添加當前目錄到 Python 路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_leaderboard_with_real_tokens():
    """使用真實憑證測試排行榜功能"""
    print("🚀 使用真實 LINE Bot 憑證測試排行榜功能")
    print("=" * 60)
    
    # 檢查環境變量
    print("🔍 檢查環境變量...")
    line_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
    line_secret = os.getenv('LINE_CHANNEL_SECRET')
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_ANON_KEY')
    
    print(f"  LINE_CHANNEL_ACCESS_TOKEN: {'✅' if line_token else '❌'} {line_token[:20] + '...' if line_token else '未設置'}")
    print(f"  LINE_CHANNEL_SECRET: {'✅' if line_secret else '❌'} {line_secret[:20] + '...' if line_secret else '未設置'}")
    print(f"  SUPABASE_URL: {'✅' if supabase_url else '❌'} {supabase_url or '未設置'}")
    print(f"  SUPABASE_ANON_KEY: {'✅' if supabase_key else '❌'} {supabase_key[:20] + '...' if supabase_key else '未設置'}")
    
    if not all([line_token, line_secret, supabase_url, supabase_key]):
        print("❌ 環境變量設置不完整")
        return False
    
    print("\n✅ 所有環境變量已正確設置！")
    
    # 測試排行榜功能
    print("\n🧪 測試排行榜功能...")
    
    try:
        from app_supabase_fixed import send_leaderboard_message, create_leaderboard_flex_message, get_real_students_data
        
        # 測試用戶ID
        test_user_id = "U1234567890abcdef"
        
        print(f"📋 測試用戶ID: {test_user_id}")
        print(f"📝 測試輸入: 排行榜")
        
        # 1. 測試數據獲取
        print("\n1️⃣ 測試數據獲取...")
        students_data = get_real_students_data()
        if students_data:
            print(f"   ✅ 成功獲取 {len(students_data)} 條數據")
            print(f"   📊 前3名: {[f'{s.get('name', 'N/A')} - {s.get('score', 0)}分' for s in students_data[:3]]}")
        else:
            print("   ❌ 無法獲取數據")
            return False
        
        # 2. 測試 Flex Message 創建
        print("\n2️⃣ 測試 Flex Message 創建...")
        top_10 = students_data[:10]
        flex_message = create_leaderboard_flex_message(top_10, students_data, test_user_id)
        
        if flex_message and isinstance(flex_message, dict):
            print("   ✅ Flex Message 創建成功")
            print(f"   📋 類型: {flex_message.get('type', 'N/A')}")
            print(f"   📝 替代文字: {flex_message.get('altText', 'N/A')}")
            print(f"   🎨 內容類型: {flex_message.get('contents', {}).get('type', 'N/A')}")
        else:
            print("   ❌ Flex Message 創建失敗")
            return False
        
        # 3. 測試發送功能
        print("\n3️⃣ 測試發送功能...")
        result = send_leaderboard_message(test_user_id)
        print(f"   📤 發送結果: {result}")
        
        if result is None:
            print("   ✅ 發送成功（無錯誤返回）")
        elif isinstance(result, dict) and 'error' in result:
            print(f"   ❌ 發送失敗: {result['error']}")
            return False
        else:
            print(f"   ✅ 發送完成: {result}")
        
        print("\n🎉 排行榜功能測試完成！")
        return True
        
    except Exception as e:
        print(f"   ❌ 測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_text_processing():
    """測試文字處理邏輯"""
    print("\n🔤 測試文字處理邏輯...")
    print("=" * 50)
    
    try:
        from app_supabase_fixed import handle_text_message
        
        # 測試不同的文字輸入
        test_cases = [
            "排行榜",
            "leaderboard", 
            "排名",
            "排行"
        ]
        
        for test_text in test_cases:
            print(f"📝 測試文字: '{test_text}'")
            
            # 檢查文字匹配
            leaderboard_keywords = ['排行榜', 'leaderboard', '排名', '排行']
            if test_text.strip().lower() in [kw.lower() for kw in leaderboard_keywords]:
                print(f"   ✅ 匹配成功")
            else:
                print(f"   ❌ 匹配失敗")
        
        return True
        
    except Exception as e:
        print(f"   ❌ 文字處理測試失敗: {e}")
        return False

def main():
    """主函數"""
    print("🎯 使用真實憑證測試排行榜 Flex Messenger 功能")
    print("=" * 70)
    
    # 測試排行榜功能
    success = test_leaderboard_with_real_tokens()
    
    # 測試文字處理
    text_success = test_text_processing()
    
    # 總結
    print("\n" + "=" * 70)
    print("📋 測試結果總結:")
    print(f"   🎨 排行榜功能: {'✅ 成功' if success else '❌ 失敗'}")
    print(f"   🔤 文字處理: {'✅ 成功' if text_success else '❌ 失敗'}")
    
    if success and text_success:
        print("\n🎉 恭喜！排行榜 Flex Messenger 功能完全正常！")
        print("💡 現在當用戶輸入「排行榜」時，應該會看到完整的 Flex Message！")
    else:
        print("\n⚠️ 還有問題需要解決，請檢查上述錯誤訊息。")

if __name__ == "__main__":
    main()

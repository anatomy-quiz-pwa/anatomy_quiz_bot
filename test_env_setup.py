#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試環境變量設置
"""

import os
import sys

def test_environment_variables():
    """測試環境變量設置"""
    print("🔍 檢查環境變量設置...")
    print("=" * 50)
    
    # 檢查 Supabase 配置
    print("📊 Supabase 配置:")
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_ANON_KEY')
    
    if supabase_url:
        print(f"  ✅ SUPABASE_URL: {supabase_url}")
    else:
        print("  ❌ SUPABASE_URL: 未設置")
    
    if supabase_key:
        print(f"  ✅ SUPABASE_ANON_KEY: {supabase_key[:20]}...")
    else:
        print("  ❌ SUPABASE_ANON_KEY: 未設置")
    
    # 檢查 LINE Bot 配置
    print("\n📱 LINE Bot 配置:")
    line_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
    line_secret = os.getenv('LINE_CHANNEL_SECRET')
    
    if line_token:
        print(f"  ✅ LINE_CHANNEL_ACCESS_TOKEN: {line_token[:20]}...")
    else:
        print("  ❌ LINE_CHANNEL_ACCESS_TOKEN: 未設置")
        print("     💡 請設置: export LINE_CHANNEL_ACCESS_TOKEN='your_token_here'")
    
    if line_secret:
        print(f"  ✅ LINE_CHANNEL_SECRET: {line_secret[:20]}...")
    else:
        print("  ❌ LINE_CHANNEL_SECRET: 未設置")
        print("     💡 請設置: export LINE_CHANNEL_SECRET='your_secret_here'")
    
    # 檢查 Facebook Messenger 配置
    print("\n📘 Facebook Messenger 配置:")
    page_token = os.getenv('PAGE_ACCESS_TOKEN')
    verify_token = os.getenv('VERIFY_TOKEN')
    
    if page_token:
        print(f"  ✅ PAGE_ACCESS_TOKEN: {page_token[:20]}...")
    else:
        print("  ⚠️ PAGE_ACCESS_TOKEN: 未設置 (可選)")
    
    if verify_token:
        print(f"  ✅ VERIFY_TOKEN: {verify_token[:20]}...")
    else:
        print("  ⚠️ VERIFY_TOKEN: 未設置 (可選)")
    
    # 總結
    print("\n" + "=" * 50)
    print("📋 設置狀態總結:")
    
    required_vars = ['SUPABASE_URL', 'SUPABASE_ANON_KEY', 'LINE_CHANNEL_ACCESS_TOKEN', 'LINE_CHANNEL_SECRET']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if not missing_vars:
        print("🎉 所有必需的環境變量都已設置！")
        print("✅ 排行榜功能應該可以正常工作")
        return True
    else:
        print(f"⚠️ 缺少 {len(missing_vars)} 個必需的環境變量:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n💡 請按照 '環境變量設置指南.md' 中的說明設置缺少的環境變量")
        return False

def test_leaderboard_functionality():
    """測試排行榜功能"""
    print("\n🧪 測試排行榜功能...")
    
    try:
        # 設置環境變量
        os.environ['SUPABASE_URL'] = 'https://ciqlfqfgzqqgdrogedxg.supabase.co'
        os.environ['SUPABASE_ANON_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA'
        
        from app_supabase_fixed import create_leaderboard_flex_message, get_real_students_data
        
        # 測試數據獲取
        print("  📊 測試數據獲取...")
        students_data = get_real_students_data()
        if students_data:
            print(f"  ✅ 成功獲取 {len(students_data)} 條數據")
        else:
            print("  ❌ 無法獲取數據")
            return False
        
        # 測試 Flex Message 創建
        print("  🎨 測試 Flex Message 創建...")
        top_10 = students_data[:10]
        test_user_id = "U1234567890abcdef"
        flex_message = create_leaderboard_flex_message(top_10, students_data, test_user_id)
        
        if flex_message and isinstance(flex_message, dict):
            print("  ✅ Flex Message 創建成功")
            print(f"  📋 類型: {flex_message.get('type', 'N/A')}")
            print(f"  📝 替代文字: {flex_message.get('altText', 'N/A')}")
        else:
            print("  ❌ Flex Message 創建失敗")
            return False
        
        print("  🎉 排行榜功能測試通過！")
        return True
        
    except Exception as e:
        print(f"  ❌ 測試失敗: {e}")
        return False

if __name__ == "__main__":
    print("🚀 環境變量設置測試")
    print("=" * 60)
    
    # 測試環境變量
    env_ok = test_environment_variables()
    
    # 測試排行榜功能
    if env_ok:
        test_leaderboard_functionality()
    
    print("\n" + "=" * 60)
    if env_ok:
        print("🎉 所有測試通過！您的環境設置正確。")
    else:
        print("⚠️ 請先設置缺少的環境變量，然後重新運行測試。")

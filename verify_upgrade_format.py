#!/usr/bin/env python3
"""
升級訊息驗證腳本
用於確認升級訊息使用正確的LINE格式
"""

import os
import json

# 設置環境變數
os.environ['SUPABASE_URL'] = "https://ciqlfqfgzqqgdrogedxg.supabase.co"
os.environ['SUPABASE_KEY'] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA"

def verify_upgrade_message():
    """驗證升級訊息格式"""
    try:
        from app_supabase import create_level_up_flex_message
        
        # 測試創建升級訊息
        flex_message = create_level_up_flex_message(1, 2)
        
        if flex_message and flex_message.get('type') == 'flex':
            print("✅ 升級訊息使用正確的LINE Flex格式")
            print(f"📝 替代文字: {flex_message.get('altText')}")
            return True
        else:
            print("❌ 升級訊息格式錯誤")
            if flex_message:
                print(f"實際格式: {json.dumps(flex_message, ensure_ascii=False, indent=2)}")
            return False
            
    except Exception as e:
        print(f"❌ 驗證失敗: {e}")
        return False

if __name__ == "__main__":
    print("🔧 升級訊息格式驗證")
    verify_upgrade_message()

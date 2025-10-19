#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試 LINE Bot 和網頁的帳號互通功能
"""

import os
import requests
import json
from datetime import datetime, timedelta
from supabase import create_client, Client

# 環境變數
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://ciqlfqfgzqqgdrogedxg.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA')

# 測試用戶ID（使用記憶中的真實用戶ID）
TEST_USER_ID = "U977c24d1fec3a2bf07035504e1444911"  # 保的測試帳號

def test_link_token_creation():
    """測試創建連結token"""
    print("🧪 測試1: 創建連結token")
    
    try:
        # 模擬LINE Bot創建token的API調用
        api_url = "http://localhost:5000/api/create-link-token"
        data = {"line_user_id": TEST_USER_ID}
        
        response = requests.post(api_url, json=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('ok'):
                token = result.get('token')
                print(f"✅ Token創建成功: {token}")
                return token
            else:
                print(f"❌ Token創建失敗: {result.get('reason')}")
                return None
        else:
            print(f"❌ API調用失敗: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        return None

def test_token_verification(token):
    """測試token驗證"""
    print(f"\n🧪 測試2: 驗證token {token}")
    
    try:
        # 檢查Supabase中的token
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        response = supabase.table('link_tokens').select('*').eq('token', token).execute()
        
        if response.data:
            token_data = response.data[0]
            print(f"✅ Token存在於數據庫")
            print(f"   - 用戶ID: {token_data['line_user_id']}")
            print(f"   - 過期時間: {token_data['expires_at']}")
            print(f"   - 已使用: {token_data['used']}")
            
            # 檢查是否過期
            expires_at = datetime.fromisoformat(token_data['expires_at'].replace('Z', '+00:00'))
            if datetime.now(expires_at.tzinfo) < expires_at:
                print("✅ Token未過期")
                return True
            else:
                print("❌ Token已過期")
                return False
        else:
            print("❌ Token不存在於數據庫")
            return False
            
    except Exception as e:
        print(f"❌ 驗證失敗: {e}")
        return False

def test_web_link_access(token):
    """測試網頁連結訪問"""
    print(f"\n🧪 測試3: 網頁連結訪問")
    
    try:
        # 模擬訪問網頁連結
        web_url = f"http://localhost:5001/link?token={token}"
        
        response = requests.get(web_url, timeout=10)
        
        if response.status_code == 200:
            print("✅ 網頁連結訪問成功")
            return True
        elif response.status_code == 302:  # 重定向到遊戲頁面
            print("✅ 網頁連結重定向成功（正常行為）")
            return True
        else:
            print(f"❌ 網頁連結訪問失敗: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 網頁訪問失敗: {e}")
        return False

def test_user_data_sync():
    """測試用戶數據同步"""
    print(f"\n🧪 測試4: 用戶數據同步")
    
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # 檢查用戶是否存在
        user_response = supabase.table('users').select('*').eq('line_user_id', TEST_USER_ID).execute()
        
        if user_response.data:
            user_data = user_response.data[0]
            print(f"✅ 用戶存在於數據庫")
            print(f"   - 顯示名稱: {user_data.get('display_name', 'N/A')}")
            print(f"   - 遊戲暱稱: {user_data.get('game_nickname', 'N/A')}")
        else:
            print("❌ 用戶不存在於數據庫")
            return False
        
        # 檢查用戶統計數據
        stats_response = supabase.table('user_stats').select('*').eq('user_id', TEST_USER_ID).execute()
        
        if stats_response.data:
            stats_data = stats_response.data[0]
            print(f"✅ 用戶統計數據存在")
            print(f"   - 正確題數: {stats_data.get('correct', 0)}")
            print(f"   - 總題數: {stats_data.get('total', 0)}")
            print(f"   - 等級: {stats_data.get('level', 1)}")
        else:
            print("⚠️ 用戶統計數據不存在（可能為新用戶）")
        
        return True
        
    except Exception as e:
        print(f"❌ 數據同步測試失敗: {e}")
        return False

def cleanup_test_data(token):
    """清理測試數據"""
    print(f"\n🧹 清理測試數據")
    
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # 刪除測試token
        supabase.table('link_tokens').delete().eq('token', token).execute()
        print("✅ 測試token已清理")
        
    except Exception as e:
        print(f"❌ 清理失敗: {e}")

def main():
    """主測試函數"""
    print("🚀 開始測試 LINE Bot 和網頁的帳號互通功能")
    print(f"📋 測試用戶ID: {TEST_USER_ID}")
    print("=" * 60)
    
    # 測試1: 創建token
    token = test_link_token_creation()
    if not token:
        print("\n❌ 測試終止：無法創建token")
        return
    
    # 測試2: 驗證token
    if not test_token_verification(token):
        print("\n❌ 測試終止：token驗證失敗")
        cleanup_test_data(token)
        return
    
    # 測試3: 網頁連結訪問
    if not test_web_link_access(token):
        print("\n❌ 測試終止：網頁連結訪問失敗")
        cleanup_test_data(token)
        return
    
    # 測試4: 用戶數據同步
    if not test_user_data_sync():
        print("\n❌ 測試終止：用戶數據同步失敗")
        cleanup_test_data(token)
        return
    
    # 清理測試數據
    cleanup_test_data(token)
    
    print("\n" + "=" * 60)
    print("🎉 所有測試通過！LINE Bot 和網頁的帳號互通功能正常運作")
    print("\n📝 使用流程：")
    print("1. 用戶在LINE Bot輸入「網站」")
    print("2. LINE Bot生成連結token並發送給用戶")
    print("3. 用戶點擊連結進入網頁")
    print("4. 網頁自動驗證token並登入用戶")
    print("5. 用戶可以繼續遊戲，數據與LINE Bot同步")

if __name__ == '__main__':
    main()

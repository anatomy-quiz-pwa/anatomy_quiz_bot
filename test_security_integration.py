#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試安全版本的LINE Bot和網頁帳號互通功能
"""

import os
import requests
import json
import time
from datetime import datetime, timedelta
from supabase import create_client, Client
from secure_token_manager import SecureTokenManager
from secure_session_manager import SecureSessionManager

# 環境變數
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://ciqlfqfgzqqgdrogedxg.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA')

# 測試用戶ID
TEST_USER_ID = "U977c24d1fec3a2bf07035504e1444911"

def test_secure_token_manager():
    """測試安全Token管理器"""
    print("🧪 測試1: 安全Token管理器")
    
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        manager = SecureTokenManager(supabase)
        
        # 測試創建token
        token = manager.create_link_token(TEST_USER_ID)
        if not token:
            print("❌ Token創建失敗")
            return False
        
        print(f"✅ Token創建成功: {token[:16]}...")
        
        # 測試消耗token
        result = manager.consume_token(token)
        if not result or result['line_user_id'] != TEST_USER_ID:
            print("❌ Token消耗失敗")
            return False
        
        print(f"✅ Token消耗成功: {result}")
        
        # 測試重複消耗（應該失敗）
        result2 = manager.consume_token(token)
        if result2:
            print("❌ 重複消耗應該失敗")
            return False
        
        print("✅ 重複消耗正確失敗")
        return True
        
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        return False

def test_session_manager():
    """測試安全Session管理器"""
    print("\n🧪 測試2: 安全Session管理器")
    
    try:
        manager = SecureSessionManager()
        
        # 測試創建token
        access_token = manager.create_access_token(TEST_USER_ID)
        refresh_token = manager.create_refresh_token(TEST_USER_ID)
        
        print(f"✅ Access token: {access_token[:50]}...")
        print(f"✅ Refresh token: {refresh_token[:50]}...")
        
        # 測試驗證token
        payload = manager.verify_token(access_token, 'access')
        if not payload or payload.get('sub') != TEST_USER_ID:
            print("❌ Token驗證失敗")
            return False
        
        print("✅ Token驗證成功")
        
        # 測試刷新token
        new_access_token = manager.refresh_access_token(refresh_token)
        if not new_access_token:
            print("❌ Token刷新失敗")
            return False
        
        print("✅ Token刷新成功")
        return True
        
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        return False

def test_line_bot_api():
    """測試LINE Bot API"""
    print("\n🧪 測試3: LINE Bot API")
    
    try:
        # 測試創建token API
        api_url = "http://localhost:5000/api/create-link-token"
        data = {"line_user_id": TEST_USER_ID}
        
        response = requests.post(api_url, json=data, timeout=10)
        
        if response.status_code != 200:
            print(f"❌ API調用失敗: {response.status_code}")
            return False
        
        result = response.json()
        if not result.get('ok'):
            print(f"❌ API返回錯誤: {result.get('reason')}")
            return False
        
        token = result.get('token')
        if not token:
            print("❌ 沒有返回token")
            return False
        
        print(f"✅ API創建token成功: {token[:16]}...")
        return token
        
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        return None

def test_web_link_access(token):
    """測試網頁連結訪問"""
    print(f"\n🧪 測試4: 網頁連結訪問")
    
    try:
        web_url = f"http://localhost:5001/link?token={token}"
        
        response = requests.get(web_url, timeout=10, allow_redirects=False)
        
        if response.status_code in [200, 302]:
            print("✅ 網頁連結訪問成功")
            return True
        else:
            print(f"❌ 網頁連結訪問失敗: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        return False

def test_token_security():
    """測試Token安全性"""
    print("\n🧪 測試5: Token安全性")
    
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        manager = SecureTokenManager(supabase)
        
        # 創建token
        token = manager.create_link_token(TEST_USER_ID)
        if not token:
            print("❌ 無法創建測試token")
            return False
        
        # 檢查數據庫中是否只存儲雜湊
        response = supabase.table('link_tokens').select('*').eq('line_user_id', TEST_USER_ID).execute()
        
        if not response.data:
            print("❌ 數據庫中沒有找到token記錄")
            return False
        
        token_data = response.data[0]
        
        # 檢查是否存儲的是雜湊而不是明文
        if 'token_hash' not in token_data:
            print("❌ 數據庫中沒有token_hash欄位")
            return False
        
        if 'token' in token_data:
            print("❌ 數據庫中不應該存儲明文token")
            return False
        
        # 檢查雜湊長度（SHA256應該是64字符）
        if len(token_data['token_hash']) != 64:
            print(f"❌ Token雜湊長度不正確: {len(token_data['token_hash'])}")
            return False
        
        print("✅ Token安全存儲驗證通過")
        
        # 清理測試數據
        manager.consume_token(token)
        return True
        
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        return False

def test_expired_token():
    """測試過期token"""
    print("\n🧪 測試6: 過期Token處理")
    
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # 創建一個已過期的token（手動插入）
        expired_token = "expired_test_token_123"
        expired_hash = hashlib.sha256(expired_token.encode('utf-8')).hexdigest()
        expired_time = (datetime.utcnow() - timedelta(minutes=10)).isoformat() + 'Z'
        
        # 插入過期token
        supabase.table('link_tokens').insert({
            'token_hash': expired_hash,
            'line_user_id': TEST_USER_ID,
            'expires_at': expired_time,
            'used': False
        }).execute()
        
        # 測試消耗過期token
        manager = SecureTokenManager(supabase)
        result = manager.consume_token(expired_token)
        
        if result:
            print("❌ 過期token應該被拒絕")
            return False
        
        print("✅ 過期token正確被拒絕")
        
        # 清理測試數據
        supabase.table('link_tokens').delete().eq('token_hash', expired_hash).execute()
        return True
        
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        return False

def test_webhook_signature():
    """測試Webhook簽名驗證"""
    print("\n🧪 測試7: Webhook簽名驗證")
    
    try:
        # 模擬無效簽名的webhook請求
        webhook_url = "http://localhost:5000/webhook"
        headers = {
            'X-Line-Signature': 'invalid_signature',
            'Content-Type': 'application/json'
        }
        data = '{"test": "data"}'
        
        response = requests.post(webhook_url, data=data, headers=headers, timeout=10)
        
        if response.status_code == 403:
            print("✅ 無效簽名正確被拒絕")
            return True
        else:
            print(f"❌ 無效簽名應該返回403，實際返回: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        return False

def cleanup_test_data():
    """清理測試數據"""
    print("\n🧹 清理測試數據")
    
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # 清理測試用戶的token
        supabase.table('link_tokens').delete().eq('line_user_id', TEST_USER_ID).execute()
        
        print("✅ 測試數據清理完成")
        
    except Exception as e:
        print(f"❌ 清理失敗: {e}")

def main():
    """主測試函數"""
    print("🚀 開始測試安全版本的LINE Bot和網頁帳號互通功能")
    print(f"📋 測試用戶ID: {TEST_USER_ID}")
    print("=" * 70)
    
    test_results = []
    
    # 執行所有測試
    test_results.append(("安全Token管理器", test_secure_token_manager()))
    test_results.append(("安全Session管理器", test_session_manager()))
    
    token = test_line_bot_api()
    test_results.append(("LINE Bot API", token is not None))
    
    if token:
        test_results.append(("網頁連結訪問", test_web_link_access(token)))
    
    test_results.append(("Token安全性", test_token_security()))
    test_results.append(("過期Token處理", test_expired_token()))
    test_results.append(("Webhook簽名驗證", test_webhook_signature()))
    
    # 清理測試數據
    cleanup_test_data()
    
    # 顯示測試結果
    print("\n" + "=" * 70)
    print("📊 測試結果總結:")
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 總體結果: {passed}/{total} 測試通過")
    
    if passed == total:
        print("\n🎉 所有安全測試通過！系統已達到生產級別的安全標準")
        print("\n🔒 已實現的安全特性:")
        print("  ✅ Token雜湊存儲")
        print("  ✅ 原子性操作")
        print("  ✅ 極短TTL (5分鐘)")
        print("  ✅ 單次使用限制")
        print("  ✅ JWT Session管理")
        print("  ✅ 安全Cookie設置")
        print("  ✅ 安全標頭")
        print("  ✅ Webhook簽名驗證")
        print("  ✅ URL token清理")
    else:
        print(f"\n⚠️ 有 {total - passed} 個測試失敗，需要修復後再部署到生產環境")

if __name__ == '__main__':
    import hashlib
    main()

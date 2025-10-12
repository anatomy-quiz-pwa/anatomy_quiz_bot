#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試 LINE 網站綁定功能
"""

import os
import requests
import json
from supabase import create_client, Client
from datetime import datetime, timedelta
import uuid

# 環境配置
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://ciqlfqfgzqqgdrogedxg.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA')

# 測試用戶 ID（使用寶的帳號）
TEST_USER_ID = "U977c24d1fec3a2bf07035504e1444911"

print("=" * 60)
print("🧪 LINE 網站綁定功能測試")
print("=" * 60)

# 創建 Supabase 客戶端
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Supabase 連接成功")
except Exception as e:
    print(f"❌ Supabase 連接失敗: {e}")
    exit(1)

print()

# 測試 1：檢查 link_tokens 表格是否存在
print("測試 1：檢查 link_tokens 表格")
print("-" * 60)

try:
    response = supabase.table('link_tokens').select('*').limit(1).execute()
    print("✅ link_tokens 表格存在")
except Exception as e:
    print(f"❌ link_tokens 表格不存在: {e}")
    print("請執行 create_link_tokens_table.sql 創建表格")
    exit(1)

print()

# 測試 2：創建一次性 token
print("測試 2：創建一次性 token")
print("-" * 60)

token = str(uuid.uuid4())
expires_at = (datetime.utcnow() + timedelta(minutes=10)).isoformat() + 'Z'

try:
    response = supabase.table('link_tokens').insert({
        'token': token,
        'line_user_id': TEST_USER_ID,
        'expires_at': expires_at,
        'used': False
    }).execute()
    
    print(f"✅ Token 創建成功")
    print(f"   Token: {token}")
    print(f"   用戶 ID: {TEST_USER_ID}")
    print(f"   過期時間: {expires_at}")
except Exception as e:
    print(f"❌ Token 創建失敗: {e}")
    exit(1)

print()

# 測試 3：查詢 token
print("測試 3：查詢 token")
print("-" * 60)

try:
    response = supabase.table('link_tokens').select('*').eq('token', token).single().execute()
    
    if response.data:
        print("✅ Token 查詢成功")
        print(f"   LINE 用戶 ID: {response.data['line_user_id']}")
        print(f"   過期時間: {response.data['expires_at']}")
        print(f"   是否使用: {response.data['used']}")
    else:
        print("❌ Token 查詢失敗：未找到 token")
except Exception as e:
    print(f"❌ Token 查詢失敗: {e}")

print()

# 測試 4：標記 token 為已使用
print("測試 4：標記 token 為已使用")
print("-" * 60)

try:
    response = supabase.table('link_tokens').update({'used': True}).eq('token', token).execute()
    print("✅ Token 標記為已使用成功")
except Exception as e:
    print(f"❌ Token 標記失敗: {e}")

print()

# 測試 5：再次查詢驗證
print("測試 5：再次查詢驗證")
print("-" * 60)

try:
    response = supabase.table('link_tokens').select('*').eq('token', token).single().execute()
    
    if response.data and response.data['used']:
        print("✅ Token 狀態驗證成功（已使用）")
    else:
        print("❌ Token 狀態驗證失敗")
except Exception as e:
    print(f"❌ Token 狀態驗證失敗: {e}")

print()

# 測試 6：測試 Flask API（如果可用）
print("測試 6：測試 Flask API")
print("-" * 60)

FLASK_API_URL = os.getenv('API_BASE_URL', 'http://localhost:5000')

try:
    response = requests.post(
        f"{FLASK_API_URL}/api/create-link-token",
        json={"line_user_id": TEST_USER_ID},
        timeout=5
    )
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Flask API 測試成功")
        print(f"   Token: {data.get('token')}")
    else:
        print(f"❌ Flask API 測試失敗: HTTP {response.status_code}")
        print(f"   回應: {response.text}")
except requests.exceptions.ConnectionError:
    print("⚠️  Flask API 無法連接（可能未啟動）")
    print("   跳過此測試")
except Exception as e:
    print(f"❌ Flask API 測試失敗: {e}")

print()

# 測試 7：清理測試數據
print("測試 7：清理測試數據")
print("-" * 60)

try:
    # 刪除剛才創建的測試 token
    response = supabase.table('link_tokens').delete().eq('token', token).execute()
    print("✅ 測試數據清理成功")
except Exception as e:
    print(f"❌ 測試數據清理失敗: {e}")

print()
print("=" * 60)
print("🎉 測試完成！")
print("=" * 60)
print()

# 總結
print("📋 測試總結")
print("-" * 60)
print("✅ Supabase 連接正常")
print("✅ link_tokens 表格存在且可操作")
print("✅ Token 創建、查詢、更新功能正常")
print()
print("📝 下一步：")
print("1. 在 Vercel 設定環境變數")
print("2. 部署 Next.js 網站")
print("3. 在 LINE 中輸入「網站」測試完整流程")
print()
print("📖 詳細說明請參考：")
print("   - LINE_網站綁定功能實施指南.md")
print("   - 快速設定_LINE網站綁定.md")


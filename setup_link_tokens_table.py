#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
設置 link_tokens 表格，用於 LINE Bot 和網頁的帳號連結
"""

import os
from supabase import create_client, Client
from datetime import datetime, timedelta

# 環境變數
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://ciqlfqfgzqqgdrogedxg.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA')

def setup_link_tokens_table():
    """設置 link_tokens 表格"""
    try:
        # 創建 Supabase 客戶端
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Supabase 連接成功")
        
        # 檢查表格是否存在
        try:
            response = supabase.table('link_tokens').select('*').limit(1).execute()
            print("✅ link_tokens 表格已存在")
        except Exception as e:
            print(f"❌ link_tokens 表格不存在，需要手動創建")
            print("""
請在 Supabase Dashboard 中手動創建 link_tokens 表格，包含以下欄位：

CREATE TABLE link_tokens (
    id SERIAL PRIMARY KEY,
    token VARCHAR(255) UNIQUE NOT NULL,
    line_user_id VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    used_at TIMESTAMP WITH TIME ZONE
);

索引：
CREATE INDEX idx_link_tokens_token ON link_tokens(token);
CREATE INDEX idx_link_tokens_line_user_id ON link_tokens(line_user_id);
CREATE INDEX idx_link_tokens_expires_at ON link_tokens(expires_at);
            """)
            return False
        
        # 測試插入一條記錄
        test_token = "test_token_123"
        expires_at = (datetime.utcnow() + timedelta(minutes=10)).isoformat() + 'Z'
        
        test_data = {
            'token': test_token,
            'line_user_id': 'test_user_123',
            'expires_at': expires_at,
            'used': False
        }
        
        # 先刪除可能存在的測試記錄
        supabase.table('link_tokens').delete().eq('token', test_token).execute()
        
        # 插入測試記錄
        response = supabase.table('link_tokens').insert(test_data).execute()
        print("✅ 測試記錄插入成功")
        
        # 驗證插入
        response = supabase.table('link_tokens').select('*').eq('token', test_token).execute()
        if response.data:
            print("✅ 數據驗證成功")
            print(f"插入的記錄: {response.data[0]}")
        
        # 清理測試記錄
        supabase.table('link_tokens').delete().eq('token', test_token).execute()
        print("✅ 測試記錄清理完成")
        
        print("\n🎉 link_tokens 表格設置完成！")
        return True
        
    except Exception as e:
        print(f"❌ 設置失敗: {e}")
        return False

if __name__ == '__main__':
    print("🔧 開始設置 link_tokens 表格...")
    setup_link_tokens_table()

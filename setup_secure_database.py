#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
設置安全的數據庫結構
- 安全的link_tokens表
- RLS策略
- 索引優化
- 匿名用戶合併支持
"""

import os
from supabase import create_client, Client

# 環境變數
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://ciqlfqfgzqqgdrogedxg.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA')

def setup_secure_database():
    """設置安全的數據庫結構"""
    try:
        # 創建 Supabase 客戶端
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Supabase 連接成功")
        
        print("""
🔧 請在 Supabase Dashboard 中執行以下 SQL 來設置安全的數據庫結構：

-- 1. 創建安全的 link_tokens 表
CREATE TABLE IF NOT EXISTS link_tokens (
    id SERIAL PRIMARY KEY,
    token_hash VARCHAR(64) UNIQUE NOT NULL,
    line_user_id VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    used_at TIMESTAMP WITH TIME ZONE
);

-- 2. 創建索引
CREATE INDEX IF NOT EXISTS idx_link_tokens_hash ON link_tokens(token_hash);
CREATE INDEX IF NOT EXISTS idx_link_tokens_line_user_id ON link_tokens(line_user_id);
CREATE INDEX IF NOT EXISTS idx_link_tokens_expires_at ON link_tokens(expires_at);
CREATE INDEX IF NOT EXISTS idx_link_tokens_used ON link_tokens(used);

-- 3. 確保 users 表有唯一約束
ALTER TABLE users ADD CONSTRAINT IF NOT EXISTS users_line_user_id_unique UNIQUE (line_user_id);

-- 4. 添加匿名會話支持到 user_stats
ALTER TABLE user_stats ADD COLUMN IF NOT EXISTS anon_session_id VARCHAR(255);
CREATE INDEX IF NOT EXISTS idx_user_stats_anon_session ON user_stats(anon_session_id);

-- 5. 創建匿名會話表（用於合併）
CREATE TABLE IF NOT EXISTS anon_sessions (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) UNIQUE NOT NULL,
    user_agent TEXT,
    ip_address INET,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_activity TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 6. 創建匿名答題記錄表
CREATE TABLE IF NOT EXISTS anon_quiz_logs (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL,
    question_id INTEGER,
    user_answer INTEGER,
    is_correct BOOLEAN,
    answered_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (session_id) REFERENCES anon_sessions(session_id)
);

-- 7. 設置 RLS 策略（如果使用 Supabase Auth）
-- 注意：這需要 service_role key 來執行

-- 啟用 RLS
ALTER TABLE user_stats ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE anon_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE anon_quiz_logs ENABLE ROW LEVEL SECURITY;

-- 創建 RLS 策略（需要根據你的認證方式調整）
-- 方案A：使用 Supabase Auth
CREATE POLICY IF NOT EXISTS user_stats_self ON user_stats
    USING (user_id = auth.uid()::text);

CREATE POLICY IF NOT EXISTS users_self ON users
    USING (id = auth.uid());

-- 方案B：使用自簽 JWT（需要在應用層設置）
-- CREATE POLICY IF NOT EXISTS user_stats_self ON user_stats
--     USING (user_id = current_setting('request.jwt.claims.sub', true));

-- 8. 創建定期清理函數
CREATE OR REPLACE FUNCTION cleanup_expired_tokens()
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM link_tokens 
    WHERE expires_at < NOW() OR used = true;
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- 9. 創建用戶數據合併函數
CREATE OR REPLACE FUNCTION merge_anon_to_user(
    p_anon_session_id VARCHAR(255),
    p_line_user_id VARCHAR(255)
)
RETURNS BOOLEAN AS $$
DECLARE
    anon_stats RECORD;
    user_stats RECORD;
BEGIN
    -- 開始事務
    BEGIN
        -- 獲取匿名統計
        SELECT * INTO anon_stats 
        FROM user_stats 
        WHERE anon_session_id = p_anon_session_id;
        
        -- 獲取或用戶統計
        SELECT * INTO user_stats 
        FROM user_stats 
        WHERE user_id = p_line_user_id;
        
        IF anon_stats IS NOT NULL THEN
            IF user_stats IS NOT NULL THEN
                -- 合併統計數據
                UPDATE user_stats SET
                    correct = COALESCE(user_stats.correct, 0) + COALESCE(anon_stats.correct, 0),
                    total = COALESCE(user_stats.total, 0) + COALESCE(anon_stats.total, 0),
                    level = GREATEST(COALESCE(user_stats.level, 1), COALESCE(anon_stats.level, 1))
                WHERE user_id = p_line_user_id;
            ELSE
                -- 創建新用戶統計
                INSERT INTO user_stats (user_id, correct, total, level)
                VALUES (p_line_user_id, anon_stats.correct, anon_stats.total, anon_stats.level);
            END IF;
            
            -- 轉移答題記錄
            UPDATE anon_quiz_logs 
            SET session_id = p_line_user_id 
            WHERE session_id = p_anon_session_id;
            
            -- 清理匿名數據
            DELETE FROM user_stats WHERE anon_session_id = p_anon_session_id;
            DELETE FROM anon_sessions WHERE session_id = p_anon_session_id;
            
            RETURN TRUE;
        END IF;
        
        RETURN FALSE;
    EXCEPTION
        WHEN OTHERS THEN
            RETURN FALSE;
    END;
END;
$$ LANGUAGE plpgsql;

-- 10. 設置定期清理任務（需要 pg_cron 擴展）
-- SELECT cron.schedule('cleanup-tokens', '*/5 * * * *', 'SELECT cleanup_expired_tokens();');

        """)
        
        print("✅ 數據庫結構設置指令已生成")
        print("\n📋 重要提醒：")
        print("1. 請在 Supabase Dashboard 的 SQL Editor 中執行上述 SQL")
        print("2. 確保使用 service_role key 來設置 RLS 策略")
        print("3. 根據你的認證方式選擇對應的 RLS 策略")
        print("4. 考慮啟用 pg_cron 擴展來定期清理過期 token")
        
        return True
        
    except Exception as e:
        print(f"❌ 設置失敗: {e}")
        return False

if __name__ == '__main__':
    print("🔧 開始設置安全數據庫結構...")
    setup_secure_database()

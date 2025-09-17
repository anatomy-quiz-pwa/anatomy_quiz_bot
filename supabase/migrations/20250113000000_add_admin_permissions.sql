-- 添加管理員權限字段的遷移文件
-- 變更摘要: 為 users 表添加管理員權限相關字段，並為指定用戶設置管理員測試模式權限
-- 預估影響行數: 1行 (僅影響指定用戶)
-- 索引/觸發器兼容性: 無影響

-- 1. 為 users 表添加管理員權限字段
DO $$
BEGIN
    -- 添加 is_admin 字段
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'users' 
        AND column_name = 'is_admin'
    ) THEN
        ALTER TABLE users ADD COLUMN is_admin BOOLEAN DEFAULT FALSE;
        RAISE NOTICE 'is_admin 字段已成功添加';
    ELSE
        RAISE NOTICE 'is_admin 字段已存在';
    END IF;
    
    -- 添加 admin_levels 字段 (JSON數組，存儲可訪問的level列表)
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'users' 
        AND column_name = 'admin_levels'
    ) THEN
        ALTER TABLE users ADD COLUMN admin_levels JSONB DEFAULT '[]'::jsonb;
        RAISE NOTICE 'admin_levels 字段已成功添加';
    ELSE
        RAISE NOTICE 'admin_levels 字段已存在';
    END IF;
    
    -- 添加 test_mode 字段 (測試模式標記)
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'users' 
        AND column_name = 'test_mode'
    ) THEN
        ALTER TABLE users ADD COLUMN test_mode BOOLEAN DEFAULT FALSE;
        RAISE NOTICE 'test_mode 字段已成功添加';
    ELSE
        RAISE NOTICE 'test_mode 字段已存在';
    END IF;
    
    -- 添加 admin_permissions 字段 (JSON對象，存儲詳細權限)
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'users' 
        AND column_name = 'admin_permissions'
    ) THEN
        ALTER TABLE users ADD COLUMN admin_permissions JSONB DEFAULT '{}'::jsonb;
        RAISE NOTICE 'admin_permissions 字段已成功添加';
    ELSE
        RAISE NOTICE 'admin_permissions 字段已存在';
    END IF;
END $$;

-- 2. 為指定用戶設置管理員權限
UPDATE users 
SET 
    is_admin = TRUE,
    admin_levels = '[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]'::jsonb,
    test_mode = TRUE,
    admin_permissions = '{
        "can_access_all_levels": true,
        "can_test_all_questions": true,
        "can_bypass_restrictions": true,
        "can_view_admin_panel": true,
        "test_mode_enabled": true,
        "max_level": 20
    }'::jsonb
WHERE line_user_id = 'U9a9df49945755ef651d067743f3c7ea7';

-- 3. 驗證更新結果
SELECT 
    line_user_id,
    game_nickname,
    is_admin,
    admin_levels,
    test_mode,
    admin_permissions
FROM users 
WHERE line_user_id = 'U9a9df49945755ef651d067743f3c7ea7';

-- 4. 添加索引以提高查詢性能
CREATE INDEX IF NOT EXISTS idx_users_is_admin ON users(is_admin);
CREATE INDEX IF NOT EXISTS idx_users_test_mode ON users(test_mode);
CREATE INDEX IF NOT EXISTS idx_users_admin_levels ON users USING GIN(admin_levels);
CREATE INDEX IF NOT EXISTS idx_users_admin_permissions ON users USING GIN(admin_permissions);

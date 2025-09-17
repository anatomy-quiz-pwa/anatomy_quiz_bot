-- 回滾管理員權限字段的遷移文件
-- 變更摘要: 移除管理員權限相關字段，恢復到原始狀態
-- 預估影響行數: 所有用戶記錄
-- 索引/觸發器兼容性: 將移除相關索引

-- 1. 移除索引
DROP INDEX IF EXISTS idx_users_admin_permissions;
DROP INDEX IF EXISTS idx_users_admin_levels;
DROP INDEX IF EXISTS idx_users_test_mode;
DROP INDEX IF EXISTS idx_users_is_admin;

-- 2. 移除管理員權限字段
DO $$
BEGIN
    -- 移除 admin_permissions 字段
    IF EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'users' 
        AND column_name = 'admin_permissions'
    ) THEN
        ALTER TABLE users DROP COLUMN admin_permissions;
        RAISE NOTICE 'admin_permissions 字段已成功移除';
    ELSE
        RAISE NOTICE 'admin_permissions 字段不存在';
    END IF;
    
    -- 移除 test_mode 字段
    IF EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'users' 
        AND column_name = 'test_mode'
    ) THEN
        ALTER TABLE users DROP COLUMN test_mode;
        RAISE NOTICE 'test_mode 字段已成功移除';
    ELSE
        RAISE NOTICE 'test_mode 字段不存在';
    END IF;
    
    -- 移除 admin_levels 字段
    IF EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'users' 
        AND column_name = 'admin_levels'
    ) THEN
        ALTER TABLE users DROP COLUMN admin_levels;
        RAISE NOTICE 'admin_levels 字段已成功移除';
    ELSE
        RAISE NOTICE 'admin_levels 字段不存在';
    END IF;
    
    -- 移除 is_admin 字段
    IF EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'users' 
        AND column_name = 'is_admin'
    ) THEN
        ALTER TABLE users DROP COLUMN is_admin;
        RAISE NOTICE 'is_admin 字段已成功移除';
    ELSE
        RAISE NOTICE 'is_admin 字段不存在';
    END IF;
END $$;

-- 3. 驗證回滾結果
SELECT column_name, data_type, is_nullable, column_default 
FROM information_schema.columns 
WHERE table_name = 'users' 
ORDER BY ordinal_position;

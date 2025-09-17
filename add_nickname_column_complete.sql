-- 完整的暱稱欄位添加腳本
-- 請在 Supabase SQL Editor 中執行

-- 1. 首先檢查當前表格結構
SELECT column_name, data_type, is_nullable, column_default 
FROM information_schema.columns 
WHERE table_name = 'user_stats' 
ORDER BY ordinal_position;

-- 2. 檢查是否已存在暱稱欄位
SELECT EXISTS (
    SELECT 1 
    FROM information_schema.columns 
    WHERE table_name = 'user_stats' 
    AND column_name = 'nickname'
) as nickname_exists;

-- 3. 如果不存在，添加暱稱欄位
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'user_stats' 
        AND column_name = 'nickname'
    ) THEN
        ALTER TABLE user_stats ADD COLUMN nickname VARCHAR(50) DEFAULT NULL;
        RAISE NOTICE '暱稱欄位已成功添加';
    ELSE
        RAISE NOTICE '暱稱欄位已存在';
    END IF;
END $$;

-- 4. 為現有記錄設置默認暱稱
UPDATE user_stats 
SET nickname = CASE 
    WHEN user_id LIKE 'U%' THEN '用戶_' || SUBSTRING(user_id FROM 2 FOR 8)
    WHEN user_id LIKE 'test%' THEN '測試用戶_' || SUBSTRING(user_id FROM 5)
    ELSE '用戶_' || user_id
END
WHERE nickname IS NULL;

-- 5. 查看更新結果
SELECT user_id, nickname, level, correct, wrong, last_update 
FROM user_stats 
ORDER BY correct DESC 
LIMIT 10;

-- 6. 確認欄位已添加
SELECT column_name, data_type, is_nullable, column_default 
FROM information_schema.columns 
WHERE table_name = 'user_stats' 
ORDER BY ordinal_position;


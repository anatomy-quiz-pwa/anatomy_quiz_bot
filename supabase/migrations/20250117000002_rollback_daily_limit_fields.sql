-- 回滾每日答題限制功能
-- 移除 user_stats 表的每日答題記錄欄位

-- 1. 移除觸發器
DROP TRIGGER IF EXISTS trigger_reset_daily_questions ON user_stats;

-- 2. 移除函數
DROP FUNCTION IF EXISTS reset_daily_questions_if_needed();

-- 3. 移除索引
DROP INDEX IF EXISTS idx_user_stats_daily_date;

-- 4. 移除欄位
ALTER TABLE user_stats 
DROP COLUMN IF EXISTS daily_questions_answered,
DROP COLUMN IF EXISTS last_question_date;

-- 5. 確認回滾結果
SELECT 
    column_name, 
    data_type, 
    is_nullable, 
    column_default
FROM information_schema.columns 
WHERE table_name = 'user_stats' 
AND table_schema = 'public'
ORDER BY ordinal_position;

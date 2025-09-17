-- 添加每日答題限制功能
-- 為 user_stats 表添加每日答題記錄欄位

-- 變更摘要：為 user_stats 表添加每日答題追蹤欄位
-- 預估影響行數：所有現有用戶記錄（約 100-500 行）
-- 索引/觸發器相容性：新增欄位不影響現有索引

-- 1. 添加每日答題記錄欄位
ALTER TABLE user_stats 
ADD COLUMN IF NOT EXISTS daily_questions_answered INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS last_question_date DATE DEFAULT CURRENT_DATE;

-- 2. 為現有記錄設置默認值
UPDATE user_stats 
SET 
    daily_questions_answered = 0,
    last_question_date = CURRENT_DATE
WHERE daily_questions_answered IS NULL OR last_question_date IS NULL;

-- 3. 添加註釋
COMMENT ON COLUMN user_stats.daily_questions_answered IS '今日已答題數量，每日重置';
COMMENT ON COLUMN user_stats.last_question_date IS '最後答題日期，用於每日重置';

-- 4. 創建索引以提高查詢效率
CREATE INDEX IF NOT EXISTS idx_user_stats_daily_date ON user_stats(last_question_date);

-- 5. 創建每日重置函數
CREATE OR REPLACE FUNCTION reset_daily_questions_if_needed()
RETURNS TRIGGER AS $$
BEGIN
    -- 如果是新的一天，重置每日答題數量
    IF NEW.last_question_date < CURRENT_DATE THEN
        NEW.daily_questions_answered = 0;
        NEW.last_question_date = CURRENT_DATE;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 6. 創建觸發器，在查詢時自動檢查是否需要重置
CREATE OR REPLACE TRIGGER trigger_reset_daily_questions
    BEFORE UPDATE ON user_stats
    FOR EACH ROW
    EXECUTE FUNCTION reset_daily_questions_if_needed();

-- 7. 查看更新結果
SELECT 
    user_id, 
    nickname,
    level, 
    correct, 
    wrong,
    daily_questions_answered,
    last_question_date,
    last_update 
FROM user_stats 
ORDER BY correct DESC 
LIMIT 10;

-- 每日答題限制功能實施計劃
-- 
-- 目的：為解剖學問答機器人添加每日三題限制功能
-- 
-- 變更內容：
-- 1. 在 user_stats 表中添加兩個新欄位：
--    - daily_questions_answered: 記錄今日已答題數量
--    - last_question_date: 記錄最後答題日期
-- 
-- 2. 創建自動重置機制：
--    - 當日期變更時，自動重置 daily_questions_answered 為 0
--    - 使用觸發器實現自動化處理
-- 
-- 風險評估：
-- - 低風險：只是添加新欄位，不影響現有功能
-- - 現有數據完全保留
-- - 可以完全回滾
-- 
-- 測試計劃：
-- 1. 在測試環境執行遷移
-- 2. 驗證欄位正確添加
-- 3. 測試觸發器功能
-- 4. 驗證每日重置機制
-- 5. 測試應用程式整合

-- 執行前檢查
BEGIN;

-- 檢查表是否存在
SELECT 
    table_name, 
    table_type 
FROM information_schema.tables 
WHERE table_name = 'user_stats' 
AND table_schema = 'public';

-- 檢查現有欄位
SELECT 
    column_name, 
    data_type, 
    is_nullable, 
    column_default
FROM information_schema.columns 
WHERE table_name = 'user_stats' 
AND table_schema = 'public'
ORDER BY ordinal_position;

-- 檢查現有記錄數量
SELECT COUNT(*) as total_records FROM user_stats;

-- 檢查是否已有相關欄位（避免重複執行）
SELECT 
    column_name
FROM information_schema.columns 
WHERE table_name = 'user_stats' 
AND table_schema = 'public'
AND column_name IN ('daily_questions_answered', 'last_question_date');

ROLLBACK;

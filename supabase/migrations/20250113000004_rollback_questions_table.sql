-- 回滾 questions 表格創建
-- 刪除 questions 表格及其相關對象

-- 刪除觸發器
DROP TRIGGER IF EXISTS update_questions_updated_at ON questions;

-- 刪除函數
DROP FUNCTION IF EXISTS update_updated_at_column();

-- 刪除表格
DROP TABLE IF EXISTS questions;

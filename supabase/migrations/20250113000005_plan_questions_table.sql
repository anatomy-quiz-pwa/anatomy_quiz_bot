-- 計劃創建 questions 表格
-- 此文件用於檢查創建 questions 表格的影響

-- 檢查當前數據庫狀態
SELECT 
    'Current database state' as status,
    COUNT(*) as table_count
FROM information_schema.tables 
WHERE table_schema = 'public';

-- 檢查是否已存在 questions 表格
SELECT 
    CASE 
        WHEN EXISTS (
            SELECT 1 FROM information_schema.tables 
            WHERE table_name = 'questions' AND table_schema = 'public'
        ) 
        THEN 'questions table already exists'
        ELSE 'questions table does not exist'
    END as questions_table_status;

-- 檢查相關權限
SELECT 
    'Database permissions check' as status,
    has_table_privilege('public', 'CREATE') as can_create_tables,
    has_schema_privilege('public', 'USAGE') as can_use_schema;

-- 預估影響
SELECT 
    'Estimated impact' as category,
    'Creating questions table with 60+ sample questions' as description,
    'Low risk - new table creation' as risk_level,
    'Will enable admin quiz functionality for all levels 1-20' as benefit;

-- 管理員權限變更的PLAN腳本
-- 在staging數據庫上執行，使用事務並自動回滾
-- 變更摘要: 為 users 表添加管理員權限相關字段，並為指定用戶設置管理員測試模式權限
-- 預估影響行數: 1行 (僅影響指定用戶 U9a9df49945755ef651d067743f3c7ea7)
-- 索引/觸發器兼容性: 無影響，僅添加新字段和索引

BEGIN;

-- 1. 檢查當前表結構
SELECT '=== 當前 users 表結構 ===' as info;
SELECT column_name, data_type, is_nullable, column_default 
FROM information_schema.columns 
WHERE table_name = 'users' 
ORDER BY ordinal_position;

-- 2. 檢查指定用戶當前狀態
SELECT '=== 指定用戶當前狀態 ===' as info;
SELECT 
    line_user_id,
    game_nickname,
    display_name,
    created_at
FROM users 
WHERE line_user_id = 'U9a9df49945755ef651d067743f3c7ea7';

-- 3. 模擬添加字段（不實際執行）
SELECT '=== 將要添加的字段 ===' as info;
SELECT 
    'is_admin' as field_name,
    'BOOLEAN' as data_type,
    'FALSE' as default_value,
    '管理員標記' as description
UNION ALL
SELECT 
    'admin_levels' as field_name,
    'JSONB' as data_type,
    '[]' as default_value,
    '可訪問的level列表' as description
UNION ALL
SELECT 
    'test_mode' as field_name,
    'BOOLEAN' as data_type,
    'FALSE' as default_value,
    '測試模式標記' as description
UNION ALL
SELECT 
    'admin_permissions' as field_name,
    'JSONB' as data_type,
    '{}' as default_value,
    '詳細權限配置' as description;

-- 4. 模擬更新指定用戶的權限
SELECT '=== 將要為指定用戶設置的權限 ===' as info;
SELECT 
    'U9a9df49945755ef651d067743f3c7ea7' as user_id,
    'SU' as nickname,
    'TRUE' as is_admin,
    '[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]' as admin_levels,
    'TRUE' as test_mode,
    '{"can_access_all_levels": true, "can_test_all_questions": true, "can_bypass_restrictions": true, "can_view_admin_panel": true, "test_mode_enabled": true, "max_level": 20}' as admin_permissions;

-- 5. 檢查風險點
SELECT '=== 風險評估 ===' as info;
SELECT 
    '低風險' as risk_level,
    '僅添加新字段，不修改現有數據' as risk_description,
    '建議在非高峰時段執行' as recommendation
UNION ALL
SELECT 
    '低風險' as risk_level,
    '僅影響單一指定用戶' as risk_description,
    '可隨時回滾' as recommendation
UNION ALL
SELECT 
    '無風險' as risk_level,
    '添加索引提高查詢性能' as risk_description,
    '對現有功能無影響' as recommendation;

-- 6. 檢查依賴關係
SELECT '=== 依賴關係檢查 ===' as info;
SELECT 
    'app_supabase_fixed.py' as dependent_file,
    '需要更新代碼以使用新字段' as dependency_type,
    '中等' as impact_level
UNION ALL
SELECT 
    'anatomy_admin_panel' as dependent_file,
    '管理員面板需要權限檢查' as dependency_type,
    '低' as impact_level;

-- 7. 執行計劃確認
SELECT '=== 執行計劃 ===' as info;
SELECT 
    '步驟1' as step,
    '添加管理員權限字段' as action,
    '預計耗時: 1-2秒' as duration
UNION ALL
SELECT 
    '步驟2' as step,
    '為指定用戶設置權限' as action,
    '預計耗時: <1秒' as duration
UNION ALL
SELECT 
    '步驟3' as step,
    '添加性能索引' as action,
    '預計耗時: 1-2秒' as duration
UNION ALL
SELECT 
    '步驟4' as step,
    '驗證更新結果' as action,
    '預計耗時: <1秒' as duration;

-- 8. 回滾計劃
SELECT '=== 回滾計劃 ===' as info;
SELECT 
    '步驟1' as step,
    '移除索引' as action,
    '預計耗時: <1秒' as duration
UNION ALL
SELECT 
    '步驟2' as step,
    '移除管理員權限字段' as action,
    '預計耗時: 1-2秒' as duration
UNION ALL
SELECT 
    '步驟3' as step,
    '驗證回滾結果' as action,
    '預計耗時: <1秒' as duration;

-- 自動回滾（不實際執行變更）
ROLLBACK;

SELECT '=== PLAN 執行完成，已自動回滾 ===' as info;
SELECT '如需實際執行，請輸入 "批准上線"' as next_step;

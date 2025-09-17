# 在 Supabase 中添加暱稱欄位的步驟指南

## 🔧 手動添加暱稱欄位

由於 Supabase 免費版本的限制，我們需要手動在 Supabase Dashboard 中添加 `nickname` 欄位。

### 步驟 1：登入 Supabase Dashboard
1. 前往 [https://supabase.com/dashboard](https://supabase.com/dashboard)
2. 登入您的帳戶
3. 選擇項目：`ciqlfqfgzqqgdrogedxg`

### 步驟 2：進入 SQL Editor
1. 在左側導航欄中點擊 "SQL Editor"
2. 點擊 "New query" 創建新的查詢

### 步驟 3：執行 SQL 腳本
複製並執行以下 SQL 腳本：

```sql
-- 1. 添加暱稱欄位
ALTER TABLE user_stats 
ADD COLUMN nickname VARCHAR(50) DEFAULT NULL;

-- 2. 為現有記錄設置默認暱稱
UPDATE user_stats 
SET nickname = CASE 
    WHEN user_id LIKE 'U%' THEN '用戶_' || SUBSTRING(user_id FROM 2 FOR 8)
    WHEN user_id LIKE 'test%' THEN '測試用戶_' || SUBSTRING(user_id FROM 5)
    ELSE '用戶_' || user_id
END
WHERE nickname IS NULL;

-- 3. 查看更新結果
SELECT user_id, nickname, level, correct, wrong, last_update 
FROM user_stats 
ORDER BY correct DESC 
LIMIT 10;
```

### 步驟 4：驗證結果
執行以下查詢確認欄位已添加：

```sql
-- 查看表格結構
SELECT column_name, data_type, is_nullable, column_default 
FROM information_schema.columns 
WHERE table_name = 'user_stats' 
ORDER BY ordinal_position;

-- 查看帶暱稱的數據
SELECT user_id, nickname, level, correct, wrong, last_update 
FROM user_stats 
ORDER BY correct DESC;
```

## 📝 預期的結果

執行後，您應該看到：

### 表格結構
```
column_name    | data_type | is_nullable | column_default
---------------+-----------+-------------+----------------
id             | bigint    | NO          | nextval('...')
user_id        | text      | NO          | 
correct        | integer   | YES         | 0
wrong          | integer   | YES         | 0
last_update    | date      | YES         | 
created_at     | timestamp | YES         | now()
daily_quota    | integer   | YES         | 3
streak_days    | integer   | YES         | 1
last_updated   | date      | YES         | 
level          | integer   | YES         | 1
correct_in_level | integer | YES         | 0
correct_qids   | integer[] | YES         | 
nickname       | character varying(50) | YES | NULL  ← 新添加的欄位
```

### 數據示例
```
user_id                                    | nickname        | level | correct | wrong
------------------------------------------|-----------------|-------|---------|-------
U977c24d1fec3a2bf07035504e1444911         | 用戶_977c24d1   | 8     | 20      | 0
test_comparison                           | 測試用戶_comparison | 1  | 19      | 11
test_correct_qids_fix                     | 測試用戶_correct_qids_fix | 2 | 3 | 0
```

## 🔄 更新應用程序代碼

添加欄位後，我們需要更新應用程序代碼以使用暱稱欄位。請執行以下步驟：

1. 在 Supabase Dashboard 中成功添加 `nickname` 欄位
2. 運行更新腳本為現有記錄設置暱稱
3. 更新應用程序代碼以使用暱稱欄位
4. 測試排行榜顯示

## 📞 需要幫助？

如果您在執行過程中遇到任何問題，請：
1. 檢查錯誤訊息
2. 確認您有足夠的權限修改表格
3. 聯繫 Supabase 支持或查看文檔


# Supabase 遷移指南

## 概述
本指南將幫助你將 LINE Bot 的資料庫從 Google Sheets 遷移到 Supabase，以提升效能和可擴展性。

## 步驟 1: 設定 Supabase 專案

1. 前往 [Supabase](https://supabase.com) 註冊並建立新專案
2. 在專案設定中獲取以下資訊：
   - Project URL (例如：`https://your-project-id.supabase.co`)
   - Anon Key (公開金鑰)

## 步驟 2: 建立資料庫表格

在 Supabase SQL Editor 中執行以下 SQL 語法：

### 1. 建立 questions 表格 (題目表)
```sql
CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    category TEXT DEFAULT '未分類',
    question TEXT NOT NULL,
    option1 TEXT NOT NULL,
    option2 TEXT NOT NULL,
    option3 TEXT NOT NULL,
    option4 TEXT NOT NULL,
    correct_answer INTEGER NOT NULL CHECK (correct_answer >= 1 AND correct_answer <= 4),
    explanation TEXT DEFAULT '',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### 2. 建立 user_stats 表格 (用戶統計表)
```sql
CREATE TABLE user_stats (
    id SERIAL PRIMARY KEY,
    user_id TEXT UNIQUE NOT NULL,
    correct INTEGER DEFAULT 0,
    wrong INTEGER DEFAULT 0,
    correct_qids TEXT DEFAULT '', -- 逗號分隔的正確題目ID
    last_update DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### 3. 建立索引
```sql
CREATE INDEX idx_questions_category ON questions(category);
CREATE INDEX idx_user_stats_user_id ON user_stats(user_id);
CREATE INDEX idx_user_stats_last_update ON user_stats(last_update);
```

## 步驟 3: 設定環境變數

1. 複製 `env_example.txt` 為 `.env`
2. 填入你的 Supabase 憑證：
   ```
   SUPABASE_URL=https://your-project-id.supabase.co
   SUPABASE_ANON_KEY=your_supabase_anon_key_here
   ```

## 步驟 4: 初始化資料庫

執行初始化腳本：
```bash
python init_supabase.py
```

這會：
- 顯示建議的表格結構
- 插入範例題目資料
- 建立必要的索引

## 步驟 5: 遷移現有資料 (可選)

如果你有現有的 Google Sheets 資料，可以執行遷移腳本：
```bash
python migrate_data.py
```

**注意：** 需要設定 `GOOGLE_CREDENTIALS` 環境變數才能執行遷移。

## 步驟 6: 更新主程式

### 方法 1: 逐步替換 (推薦)
1. 在 `main.py` 中將 `sheets_handler` 替換為 `supabase_handler`
2. 在 `user_stats_handler.py` 中將 Google Sheets 操作替換為 Supabase 操作
3. 測試功能是否正常

### 方法 2: 直接替換
直接使用新的 `supabase_handler.py` 替換現有的處理器。

## 步驟 7: 測試

1. 啟動 Bot：
   ```bash
   python main.py
   ```

2. 測試以下功能：
   - 獲取題目
   - 記錄用戶統計
   - 查看統計資料

## 效能提升

遷移到 Supabase 後，你應該會看到：
- **更快的響應時間**：從數秒縮短到數百毫秒
- **更好的並發處理**：支援多用戶同時使用
- **更穩定的服務**：減少 API 限制和超時問題

## 故障排除

### 常見問題

1. **連接錯誤**
   - 檢查 `SUPABASE_URL` 和 `SUPABASE_ANON_KEY` 是否正確
   - 確認網路連接正常

2. **表格不存在**
   - 執行 `init_supabase.py` 建立表格
   - 檢查 SQL 語法是否正確執行

3. **權限錯誤**
   - 確認使用正確的 Anon Key
   - 檢查 RLS (Row Level Security) 設定

### 回滾方案

如果遇到問題，可以：
1. 保留原有的 Google Sheets 程式碼
2. 使用環境變數切換資料來源
3. 逐步測試和除錯

## 下一步

完成遷移後，你可以考慮：
1. 移除 Google Sheets 相關的依賴
2. 優化查詢效能
3. 加入更多 Supabase 功能 (如即時訂閱)
4. 設定資料備份策略 
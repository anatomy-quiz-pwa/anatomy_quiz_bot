
# 生產環境排行榜問題修復指南

## 問題診斷結果
- ✅ 本地功能正常
- ✅ 排行榜 Flex Message 創建正常
- ❌ 生產環境 webhook 返回 500 錯誤

## 可能的原因
1. 環境變數配置問題
2. 依賴項缺失
3. 代碼錯誤
4. 數據庫連接問題
5. 應用程式崩潰

## 修復步驟

### 1. 檢查 Render 部署日誌
```bash
# 在 Render Dashboard 中查看部署日誌
# 尋找錯誤訊息和異常堆疊
```

### 2. 檢查環境變數
確保以下環境變數在 Render 中正確設置：
- SUPABASE_URL
- SUPABASE_ANON_KEY
- LINE_CHANNEL_ACCESS_TOKEN
- LINE_CHANNEL_SECRET

### 3. 檢查依賴項
確保 requirements.txt 包含所有必要的依賴項：
```
flask
requests
supabase
line-bot-sdk
```

### 4. 測試最小化版本
使用 minimal_webhook_test.py 進行測試，確認基本功能正常。

### 5. 逐步添加功能
從最小化版本開始，逐步添加功能直到找到問題所在。

## 建議的修復方案

### 方案 1: 重新部署
1. 檢查代碼是否有語法錯誤
2. 確保所有依賴項都在 requirements.txt 中
3. 重新部署到 Render

### 方案 2: 使用最小化版本
1. 使用 minimal_webhook_test.py 替換當前版本
2. 確認基本 webhook 功能正常
3. 逐步添加排行榜功能

### 方案 3: 檢查數據庫連接
1. 確認 Supabase 連接正常
2. 檢查數據庫權限
3. 測試數據庫查詢

## 測試命令
```bash
# 測試環境
python environment_check.py

# 測試最小化 webhook
python minimal_webhook_test.py

# 測試生產環境
curl -X POST https://anatomy-quiz-bot.onrender.com/webhook \
  -H "Content-Type: application/json" \
  -d '{"events":[{"type":"message","source":{"userId":"test"},"message":{"type":"text","text":"排行榜"}}]}'
```

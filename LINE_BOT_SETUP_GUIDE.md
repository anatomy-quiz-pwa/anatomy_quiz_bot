# LINE Bot 設定指南

## 🚨 問題診斷

你的 LINE Bot 沒有反應的原因是：`.env` 檔案中的 LINE Bot 設定還是預設值！

```env
# 目前的設定（錯誤）
LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token_here
LINE_CHANNEL_SECRET=your_line_channel_secret_here
USER_ID=your_user_id_here
```

## 🔧 解決步驟

### 步驟 1：建立 LINE Bot

1. **登入 LINE Developers Console**
   - 前往：https://developers.line.biz/
   - 使用你的 LINE 帳號登入

2. **建立新的 Provider**
   - 點擊「Create New Provider」
   - 輸入 Provider 名稱（例如：Anatomy Quiz Bot）

3. **建立新的 Channel**
   - 選擇「Messaging API」
   - 輸入 Channel 名稱（例如：Anatomy Quiz）
   - 輸入 Channel 描述
   - 選擇 Channel 圖示

### 步驟 2：獲取憑證

在 Channel 設定頁面，你會看到：

1. **Channel Secret**
   - 複製這個值
   - 格式類似：`1234567890abcdef1234567890abcdef`

2. **Channel Access Token**
   - 點擊「Issue」按鈕生成
   - 複製這個值
   - 格式類似：`1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef`

### 步驟 3：更新 .env 檔案

將真實的憑證填入 `.env` 檔案：

```env
# LINE Bot 設定
LINE_CHANNEL_ACCESS_TOKEN=你的真實_channel_access_token
LINE_CHANNEL_SECRET=你的真實_channel_secret
USER_ID=你的_line_user_id

# Supabase 設定
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_supabase_anon_key_here

# 應用程式設定
PORT=5000
QUESTION_TIME=09:00
```

### 步驟 4：獲取你的 LINE User ID

1. **方法一：使用 LINE Bot**
   - 在 LINE 中搜尋你的 Bot
   - 發送任何訊息給 Bot
   - 在 Bot 的日誌中查看 user_id

2. **方法二：使用 LINE Login**
   - 在 Channel 設定中啟用 LINE Login
   - 使用 LINE Login 獲取用戶 ID

### 步驟 5：設定 Webhook

1. **在 Channel 設定中**
   - 找到「Messaging API」設定
   - 設定 Webhook URL：
     - 本地測試：`http://localhost:5001/callback`
     - 生產環境：`https://your-domain.com/callback`
   - 啟用「Use webhook」

2. **驗證 Webhook**
   - 點擊「Verify」按鈕
   - 應該顯示「Success」

## 🧪 測試步驟

### 1. 重新啟動應用程式

```bash
# 停止當前應用程式
pkill -f "python.*app_supabase.py"

# 重新啟動
source venv311/bin/activate
PORT=5001 python app_supabase.py
```

### 2. 測試 Webhook

```bash
# 測試 Webhook 端點
curl http://localhost:5001/test
```

### 3. 在 LINE 中測試

1. 在 LINE 中搜尋你的 Bot
2. 發送「開始」訊息
3. 應該會收到問答選單

## 🚨 常見問題

### 問題 1：Webhook 驗證失敗

**解決方案：**
- 確保應用程式正在運行
- 檢查 Webhook URL 是否正確
- 確保端口沒有被佔用

### 問題 2：Bot 沒有回應

**解決方案：**
- 檢查 `.env` 檔案中的憑證是否正確
- 確保 Webhook 已啟用
- 檢查應用程式日誌

### 問題 3：簽名驗證失敗

**解決方案：**
- 確保 Channel Secret 正確
- 檢查 Webhook URL 設定

## 📱 本地測試替代方案

如果你暫時不想設定真實的 LINE Bot，可以使用本地測試版本：

```bash
# 運行本地測試版本
python test_line_bot_local.py
```

這個版本不需要真實的 LINE Bot 設定，可以直接測試所有功能。

## 🎯 下一步

1. **設定真實的 LINE Bot 憑證**
2. **更新 .env 檔案**
3. **重新啟動應用程式**
4. **在 LINE 中測試 Bot 功能**

設定完成後，你的 LINE Bot 就能正常回應「開始」指令了！🎉 
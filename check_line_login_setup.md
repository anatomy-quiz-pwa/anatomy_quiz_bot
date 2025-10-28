# 🔍 LINE 登入問題檢查清單

## 步驟 1: 檢查 Vercel 環境變數

前往 Vercel Dashboard → 您的專案 → Settings → Environment Variables

**必須設置以下環境變數：**

### LINE 登入憑證
- ✅ `LINE_LOGIN_CHANNEL_ID` = `2001129748`
- ✅ `LINE_LOGIN_CHANNEL_SECRET` = `36a169e0bf3d0339a4b4749137efea18`

### Supabase 資料庫
- ✅ `SUPABASE_URL` = `https://ciqlfqfgzqqgdrogedxg.supabase.co`
- ✅ `SUPABASE_SERVICE_KEY` = `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTIwNzA4NSwiZXhwIjoyMDY2NzgzMDg1fQ.B5as4Q7AAgXSHfrQS7_c30Kpog6Rmlw4d7Or6pi9wZM`

### Session 金鑰
- ✅ `APP_SESSION_SECRET` = `d8e91a2e4f463fb37a61a7dc3566f84b9f4a0e0fb07e7dce27e0b0a1b80f60cb8d512e8e2c6cb5cf26b0d640a2b44b5b9c65e7a34e19a8849b6a3b5312b0f3a9`

## 步驟 2: 檢查 LINE Console 設定

### LINE Login Channel
前往 [LINE Developers Console](https://developers.line.biz/console/)

1. 選擇您的 Channel ID: `2001129748`
2. 檢查 **Callback URL**:
   ```
   https://anatomy-quiz-bot.vercel.app/api/auth/line/callback
   ```
   ⚠️ 必須完全一致，包括 https:// 和結尾沒有斜線

3. 檢查 **Scopes**:
   - ✅ openid
   - ✅ profile

## 步驟 3: 等待 Vercel 部署完成

1. 前往 Vercel Dashboard → 您的專案 → Deployments
2. 確認最新的部署狀態是 "Ready"（綠色勾勾）
3. 通常需要 1-2 分鐘

## 步驟 4: 重新測試登入

部署完成後，訪問以下網址重新嘗試登入：

```
https://anatomy-quiz-bot.vercel.app/api/auth/line/login
```

這次如果失敗，您會看到詳細的錯誤訊息，例如：
```json
{
  "error": "callback_failed",
  "message": "具體的錯誤原因會顯示在這裡"
}
```

## 步驟 5: 如果還是失敗

將錯誤訊息截圖給我，我會根據具體錯誤進行修復。

## 常見錯誤及解決方案

### 1. "Cannot read property 'SUPABASE_URL' of undefined"
**原因**: Vercel 環境變數沒有設置
**解決**: 在 Vercel 設置所有環境變數並重新部署

### 2. "token_exchange_failed"
**原因**: LINE token 交換失敗
**可能是**:
- LINE_LOGIN_CHANNEL_ID 或 CHANNEL_SECRET 錯誤
- Callback URL 不匹配

### 3. "bad_state"
**原因**: Cookie 狀態驗證失敗
**可能是**:
- 瀏覽器阻擋了 Cookie
- 嘗試在無痕模式或清除 Cookie 後重試

### 4. "Cannot connect to Supabase"
**原因**: 資料庫連接失敗
**解決**: 檢查 SUPABASE_URL 和 SUPABASE_SERVICE_KEY 是否正確


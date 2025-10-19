# 🚀 Pages API 部署指南

## ✅ 已建立的 Pages API 路由

已成功建立 4 個 Pages API 檔案：

### 1. OIDC 登入啟動
**檔案**: `pages/api/auth/line/login.ts`
**功能**: 啟動 LINE OIDC 登入流程（PKCE）
**測試**: `https://anatomy-quiz-bot.vercel.app/api/auth/line/login`

### 2. OIDC 回調處理
**檔案**: `pages/api/auth/line/callback.ts`
**功能**: 處理 LINE 授權回調，換取 id_token，驗簽後設定 Session
**測試**: 由 LINE 自動調用

### 3. LIFF 驗證
**檔案**: `pages/api/auth/line/verify.ts`
**功能**: 驗證 LIFF 取得的 id_token，設定 Session
**測試**: POST `https://anatomy-quiz-bot.vercel.app/api/auth/line/verify`

### 4. 用戶統計
**檔案**: `pages/api/me/stats.ts`
**功能**: 使用 Session 讀取用戶真實進度
**測試**: `https://anatomy-quiz-bot.vercel.app/api/me/stats`

## 🔧 環境變數設定

確保 Vercel 環境變數已設定：

```
LINE_LOGIN_CHANNEL_ID=2001129748
LINE_LOGIN_CHANNEL_SECRET=36a169e0bf3d0339a4b4749137efea18
SUPABASE_URL=https://ciqlfqfgzqqgdrogedxg.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTIwNzA4NSwiZXhwIjoyMDY2NzgzMDg1fQ.B5as4Q7AAgXSHfrQS7_c30Kpog6Rmlw4d7Or6pi9wZM
LIFF_ID=2001129748-VY9zLnpq
NEXT_PUBLIC_LIFF_ID=2001129748-VY9zLnpq
APP_SESSION_SECRET=d8e91a2e4f463fb37a61a7dc3566f84b9f4a0e0fb07e7dce27e0b0a1b80f60cb8d512e8e2c6cb5cf26b0d640a2b44b5b9c65e7a34e19a8849b6a3b5312b0f3a9
```

## 📱 LINE Console 設定

### LINE Login Channel
- **Callback URL**: `https://anatomy-quiz-bot.vercel.app/api/auth/line/callback`
- **Scopes**: `openid profile`

### LIFF App
- **Endpoint URL**: `https://anatomy-quiz-bot.vercel.app/game-new`
- **LIFF ID**: `2001129748-VY9zLnpq`

## 🧪 測試流程

### 1. 測試 OIDC 登入
1. 開啟 `https://anatomy-quiz-bot.vercel.app/api/auth/line/login`
2. 應該跳轉到 LINE 授權頁面
3. 完成授權後回到 `/api/auth/line/callback`
4. 自動導向到 `/game` 頁面

### 2. 測試用戶統計
1. 登入後訪問 `https://anatomy-quiz-bot.vercel.app/api/me/stats`
2. 應該回傳 200 狀態碼和用戶資料
3. 未登入時應該回傳 401 狀態碼

### 3. 測試 LIFF 驗證
1. 在 LINE 中開啟 LIFF 應用程式
2. 自動調用 `/api/auth/line/verify` 進行驗證
3. 設定 Session Cookie

## 🚀 部署步驟

1. **設定環境變數**（使用上面的清單）
2. **設定 LINE Console**（使用上面的設定）
3. **部署到 Vercel**：
   ```bash
   vercel --prod
   ```
4. **測試所有 API 端點**

## 🔍 故障排除

### 404 錯誤
- 確認 Pages API 檔案路徑正確
- 確認檔案名稱和函數名稱正確
- 重新部署專案

### 401 錯誤
- 檢查環境變數是否正確設定
- 檢查 LINE Console 設定
- 檢查 Supabase 連接

### 500 錯誤
- 檢查 Supabase Service Key 是否正確
- 檢查資料表結構是否正確
- 查看 Vercel 函數日誌

## 📊 成功指標

部署成功後應該看到：
- ✅ `https://anatomy-quiz-bot.vercel.app/api/auth/line/login` 跳轉到 LINE 授權頁
- ✅ 授權後自動回到遊戲頁面
- ✅ `https://anatomy-quiz-bot.vercel.app/api/me/stats` 回傳用戶資料
- ✅ LIFF 應用程式正常運作

## 🎉 完成！

所有 Pages API 路由都已建立完成，現在可以部署並測試 LINE Login A/B 兩條路徑的完整功能！

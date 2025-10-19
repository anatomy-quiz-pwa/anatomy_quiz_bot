# 🚀 快速部署指南

## 📋 已準備好的資料

### LINE Login Channel 憑證
- **Channel ID**: `2001129748`
- **Channel Secret**: `36a169e0bf3d0339a4b4749137efea18`

## 🔧 Vercel 環境變數設定

請在 Vercel Dashboard → Project → Settings → Environment Variables 中設定：

### 已提供的憑證
```
LINE_LOGIN_CHANNEL_ID=2001129748
LINE_LOGIN_CHANNEL_SECRET=36a169e0bf3d0339a4b4749137efea18
```

### 待設定的變數
```
# LIFF ID（需要先在 LINE Console 建立 LIFF App）
LIFF_ID=你的 LIFF ID

# Session 簽章金鑰（至少64字元隨機字串）
APP_SESSION_SECRET=你的隨機字串

# Supabase 資料庫
SUPABASE_URL=你的 Supabase URL
SUPABASE_SERVICE_KEY=你的 Supabase Service Role Key

# 前端 LIFF ID（與上面相同）
NEXT_PUBLIC_LIFF_ID=你的 LIFF ID
```

## 📱 LINE Console 設定

### 1. LINE Login Channel 設定
- **Callback URL**: `https://YOUR-APP.vercel.app/api/auth/line/callback`
- **Scopes**: 勾選 `openid profile`

### 2. LIFF App 設定
- **Endpoint URL**: `https://YOUR-APP.vercel.app/game-new`
- 記錄 LIFF ID 並設定到環境變數

## 🗄️ Supabase 資料表設定

執行以下 SQL 確保 `users` 表有 `line_user_id` 欄位：

```sql
ALTER TABLE users ADD COLUMN IF NOT EXISTS line_user_id text UNIQUE;
```

## 🚀 部署步驟

1. **設定環境變數**（使用上面的清單）
2. **設定 LINE Console**（使用上面的設定）
3. **更新 Supabase 資料表**
4. **部署到 Vercel**：
   ```bash
   vercel --prod
   ```

## 🧪 測試

部署完成後測試：
- **情境 A（LIFF）**: `https://YOUR-APP.vercel.app/game-new`
- **情境 B（OIDC）**: `https://YOUR-APP.vercel.app/test-login`

## 📞 需要協助？

如果遇到問題，請檢查：
1. 環境變數是否正確設定
2. LINE Console 設定是否正確
3. Supabase 資料表結構是否正確
4. 網路連線是否正常

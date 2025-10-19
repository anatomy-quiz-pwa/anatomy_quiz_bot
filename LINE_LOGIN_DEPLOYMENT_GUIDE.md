# LINE Login A/B 兩條路徑部署指南

## 🎯 概述

這個專案實現了完整的 LINE Login 整合，支援兩種登入方式：
- **情境 A（LIFF）**：在 LINE 內開啟網頁，自動登入
- **情境 B（OIDC）**：一般瀏覽器，手動點擊登入按鈕

## 📋 部署前準備

### 1. LINE Developers Console 設定

#### 建立 LINE Login Channel
1. 前往 [LINE Developers Console](https://developers.line.biz/)
2. 建立新的 **LINE Login** Channel
3. 設定 Callback URL：`https://YOUR-APP.vercel.app/api/auth/line/callback`
4. 勾選 Scopes：`openid profile`

#### 建立 LIFF App
1. 在同一個 Provider 下建立 **LIFF** App
2. 設定 Endpoint URL：`https://YOUR-APP.vercel.app/game-new`
3. 記錄 LIFF ID

### 2. Supabase 資料表設定

確保你的 `users` 表有 `line_user_id` 欄位：

```sql
-- 如果還沒有 line_user_id 欄位，執行以下 SQL
ALTER TABLE users
  ADD COLUMN IF NOT EXISTS line_user_id text UNIQUE;

-- 建立索引（可選）
CREATE UNIQUE INDEX IF NOT EXISTS idx_users_line_user_id ON users(line_user_id);
```

## 🚀 Vercel 部署步驟

### 1. 設定環境變數

在 Vercel Dashboard → Project → Settings → Environment Variables 中設定：

```
# LINE Login（Web-first / OIDC）
LINE_LOGIN_CHANNEL_ID=你的 LINE Login Channel ID
LINE_LOGIN_CHANNEL_SECRET=你的 LINE Login Channel Secret

# LIFF（在 LINE 內開網頁）
LIFF_ID=你的 LIFF ID

# 你網站自己的簽章金鑰（簽發網站 Session Cookie）
APP_SESSION_SECRET=至少64字元的隨機字串

# Supabase（只在伺服器端使用）
SUPABASE_URL=你的 Supabase URL
SUPABASE_SERVICE_KEY=你的 Supabase Service Role Key

# 前端環境變數（用於 LIFF）
NEXT_PUBLIC_LIFF_ID=你的 LIFF ID
```

### 2. 部署到 Vercel

```bash
# 安裝依賴
npm install

# 本地測試
npm run dev

# 部署到 Vercel
vercel --prod
```

## 🧪 測試路徑

### 情境 A（LIFF）- 在 LINE 內測試
1. 在 LINE 中分享你的網址：`https://YOUR-APP.vercel.app/game-new`
2. 點擊連結開啟
3. 應該會自動跳轉到 LINE 登入頁面
4. 登入後自動回到遊戲頁面，顯示真實進度

### 情境 B（OIDC）- 一般瀏覽器測試
1. 在 PC 瀏覽器開啟：`https://YOUR-APP.vercel.app/test-login`
2. 點擊「用 LINE 登入」按鈕
3. 跳轉到 LINE 授權頁面
4. 授權後回到遊戲頁面，顯示真實進度

## 📁 檔案結構

```
app/
├── api/
│   ├── auth/
│   │   ├── line/
│   │   │   ├── login/route.ts      # OIDC 登入啟動
│   │   │   ├── callback/route.ts   # OIDC 回調處理
│   │   │   └── verify/route.ts     # LIFF 驗證
│   │   └── logout/route.ts         # 登出
│   └── me/
│       ├── route.ts                # 用戶資料
│       └── stats/route.ts          # 用戶統計
├── game-new/page.tsx               # 新遊戲頁面（支援 LIFF + OIDC）
└── test-login/page.tsx             # 登入測試頁面

lib/
├── supabase.ts                     # Supabase 伺服器端客戶端
├── session.ts                      # Session Cookie 管理
├── users.ts                        # 用戶查詢/建立
└── line_oidc.ts                    # LINE ID Token 驗證
```

## 🔧 API 端點說明

### 認證相關
- `GET /api/auth/line/login` - 啟動 OIDC 登入流程
- `GET /api/auth/line/callback` - OIDC 回調處理
- `POST /api/auth/line/verify` - LIFF ID Token 驗證
- `POST /api/auth/logout` - 登出

### 用戶資料
- `GET /api/me` - 取得用戶基本資料和統計
- `GET /api/me/stats` - 取得用戶統計資料

## 🎮 使用方式

### 在 LINE 內使用
1. 用戶在 LINE 中點擊分享的連結
2. 自動開啟 LIFF 頁面
3. 自動登入並顯示遊戲進度

### 在一般瀏覽器使用
1. 用戶開啟網頁
2. 點擊「用 LINE 登入」按鈕
3. 跳轉到 LINE 授權頁面
4. 授權後回到遊戲頁面

## 🔒 安全特性

- 使用 HttpOnly Cookie 儲存 Session
- JWT 簽章驗證
- PKCE 流程防止 CSRF 攻擊
- LINE ID Token 驗證
- Supabase Service Role Key 僅在伺服器端使用

## 🐛 常見問題

### 1. Callback URL 不匹配
確保 LINE Console 中的 Callback URL 與實際部署的 URL 完全一致。

### 2. LIFF 無法載入
檢查 `NEXT_PUBLIC_LIFF_ID` 環境變數是否正確設定。

### 3. 登入後無法取得用戶資料
檢查 Supabase 的 `users` 表是否有 `line_user_id` 欄位。

### 4. Session 無效
檢查 `APP_SESSION_SECRET` 是否設定且足夠長（至少64字元）。

## 📞 支援

如果遇到問題，請檢查：
1. 環境變數是否正確設定
2. LINE Console 設定是否正確
3. Supabase 資料表結構是否正確
4. 網路連線是否正常

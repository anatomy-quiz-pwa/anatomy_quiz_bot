# LINE 網站綁定功能實施指南

## 📋 概述

此系統實現了 LINE Bot 與網站登入的無縫綁定，讓學生可以：
1. 在 LINE 中輸入「網站」
2. 收到 Flex 按鈕「在網站中繼續遊戲」
3. 點擊按鈕即可自動綁定 LINE 帳號與網站登入
4. 等級與紀錄自動同步

## 🏗️ 系統架構

### 1. Supabase 資料庫

#### 新增的表格：`link_tokens`

```sql
create table if not exists link_tokens (
  token uuid primary key default gen_random_uuid(),
  line_user_id text not null,
  expires_at timestamptz not null,
  used boolean not null default false,
  created_at timestamptz default now()
);

create index if not exists link_tokens_line_user_id_idx on link_tokens(line_user_id);
create index if not exists link_tokens_expires_at_idx on link_tokens(expires_at);
create index if not exists link_tokens_used_idx on link_tokens(used);
```

### 2. Flask LINE Bot 後端

#### 新增的 API 端點：`/api/create-link-token`

**功能**：為 LINE 用戶創建一次性連結 token

**請求**：
```json
POST /api/create-link-token
{
  "line_user_id": "U9a9df49945755ef651d067743f3c7ea7"
}
```

**回應**：
```json
{
  "ok": true,
  "token": "550e8400-e29b-41d4-a716-446655440000"
}
```

#### 修改的 Webhook 處理

新增對「網站」關鍵字的處理：
- 關鍵字：`網站`、`website`、`網頁`、`web`
- 行為：創建 token 並回傳 Flex Message

### 3. Next.js 網站

#### 新增文件

1. **`lib/session.ts`**
   - JWT Session 管理
   - 從 Cookie 中解析 `line_user_id`

2. **`app/api/exchange/route.ts`**
   - Token 交換 API
   - 驗證 token 並創建 session

3. **`app/link/page.tsx`**
   - 連結頁面
   - 處理 token 交換流程

4. **`app/api/me/route.ts`**
   - 受保護的 API 範例
   - 取得用戶資料

5. **`app/api/answer/route.ts`**
   - 受保護的 API 範例
   - 記錄答題並更新統計

## 🔧 部署設定

### Vercel 環境變數

在 Vercel 專案設定中添加以下環境變數：

```bash
# Supabase 配置
NEXT_PUBLIC_SUPABASE_URL=https://ciqlfqfgzqqgdrogedxg.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_ROLE=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... (Service Role Key)

# Session 配置（自行生成 32+ 字元的隨機字串）
SESSION_SECRET=your_random_secret_key_at_least_32_characters
```

### Flask 後端環境變數

在 Render 或你的 Flask 部署平台添加：

```bash
# LINE Bot 配置
LINE_CHANNEL_ACCESS_TOKEN=your_token
LINE_CHANNEL_SECRET=your_secret

# Supabase 配置
SUPABASE_URL=https://ciqlfqfgzqqgdrogedxg.supabase.co
SUPABASE_KEY=your_anon_key

# API 配置
API_BASE_URL=https://your-flask-app.render.com
WEBSITE_URL=https://anatomy-quiz-bot.vercel.app
```

## 📝 使用流程

### 1. 用戶在 LINE 輸入「網站」

LINE Bot 收到訊息後：
1. 呼叫 `/api/create-link-token` 創建 token
2. 回傳包含連結的 Flex Message

### 2. 用戶點擊「一鍵連結」按鈕

瀏覽器打開：
```
https://anatomy-quiz-bot.vercel.app/link?token=<UUID>
```

### 3. 網站處理連結請求

1. `/link` 頁面載入
2. 呼叫 `/api/exchange` API
3. 驗證 token：
   - 檢查是否存在
   - 檢查是否已使用
   - 檢查是否過期（10 分鐘）
4. 創建 JWT session（30 天有效）
5. 設定 HttpOnly Cookie
6. 顯示「連結成功」訊息

### 4. 用戶在網站遊戲

所有 API 請求會自動攜帶 session Cookie：
- `/api/me` - 取得用戶資料
- `/api/answer` - 記錄答題
- 等級與紀錄自動與 LINE Bot 同步

## 🔒 安全性設計

### Token 安全

- **一次性使用**：使用後立即標記為已使用
- **短效期**：10 分鐘後自動失效
- **UUID 格式**：難以猜測

### Session 安全

- **HttpOnly Cookie**：防止 XSS 攻擊
- **Secure 標記**：僅透過 HTTPS 傳輸（生產環境）
- **SameSite=Lax**：防止 CSRF 攻擊
- **JWT 簽名**：使用 HS256 算法
- **30 天有效期**：平衡安全性與使用體驗

### 資料庫安全

- **Service Role Key**：僅在 Server Route 使用
- **不暴露在 Client**：避免濫用

## 🧪 測試流程

### 1. 測試 Supabase 表格創建

```bash
# 在 Supabase SQL Editor 執行
# 檔案：create_link_tokens_table.sql
```

### 2. 測試 Flask API

```bash
curl -X POST http://localhost:5000/api/create-link-token \
  -H "Content-Type: application/json" \
  -d '{"line_user_id":"U9a9df49945755ef651d067743f3c7ea7"}'
```

預期回應：
```json
{
  "ok": true,
  "token": "550e8400-e29b-41d4-a716-446655440000"
}
```

### 3. 測試 LINE Webhook

在 LINE 中輸入「網站」，應該收到 Flex Message

### 4. 測試網站連結

點擊 Flex Message 中的按鈕，應該：
1. 跳轉到 `/link?token=...`
2. 顯示「連結成功」
3. 可以點擊「開始遊戲」

### 5. 測試受保護的 API

```bash
# 在瀏覽器中訪問（需要先完成連結）
curl http://localhost:3000/api/me \
  -H "Cookie: session=<your_jwt_token>"
```

預期回應：
```json
{
  "ok": true,
  "line_user_id": "U9a9df49945755ef651d067743f3c7ea7",
  "stats": { ... },
  "user": { ... }
}
```

## 📦 相關文件

- `create_link_tokens_table.sql` - 資料庫表格創建腳本
- `app_production.py` - Flask 後端（已更新）
- `lib/session.ts` - Session 管理工具
- `app/api/exchange/route.ts` - Token 交換 API
- `app/link/page.tsx` - 連結頁面
- `app/api/me/route.ts` - 用戶資料 API
- `app/api/answer/route.ts` - 答題記錄 API

## 🚀 下一步

1. ✅ 在 Supabase 執行 SQL 創建表格
2. ✅ 部署 Flask 後端更新
3. ✅ 部署 Next.js 網站更新
4. ✅ 設定環境變數
5. ⏳ 測試完整流程
6. ⏳ 監控使用情況

## 💡 提示

- **SESSION_SECRET**：可以使用 `openssl rand -base64 32` 生成
- **Service Role Key**：在 Supabase Dashboard → Settings → API 中取得
- **本地測試**：可以使用 ngrok 暴露本地 Flask 服務器
- **日誌監控**：查看 Vercel 和 Render 的日誌以診斷問題

## 🎉 完成！

現在學生可以輕鬆地在 LINE 和網站之間切換，同時保持進度同步！


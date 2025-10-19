# 🚀 Vercel 環境變數設定指南

## 📋 已確認的變數（直接複製）

以下變數已經確認，可以直接複製到 Vercel：

```
LINE_LOGIN_CHANNEL_ID=2001129748
LINE_LOGIN_CHANNEL_SECRET=36a169e0bf3d0339a4b4749137efea18
SUPABASE_URL=https://ciqlfqfgzqqgdrogedxg.supabase.co
```

## 🔧 需要你填入的變數

### 1. LIFF_ID
- **說明**：在 LINE Console 建立 LIFF App 後取得
- **步驟**：
  1. 前往 [LINE Developers Console](https://developers.line.biz/)
  2. 選擇你的 Provider
  3. 建立新的 **LIFF** App
  4. 設定 Endpoint URL: `https://YOUR-APP.vercel.app/game-new`
  5. 記錄 LIFF ID（格式：`xxxxxxxx-xxxxxxxx`）

### 2. APP_SESSION_SECRET
- **說明**：用於簽發網站 Session Cookie 的密鑰
- **要求**：至少64字元的隨機字串
- **範例**：`your-super-long-random-string-at-least-64-characters-long-for-security`

### 3. SUPABASE_SERVICE_KEY
- **說明**：Supabase Service Role Key（不是 anon key）
- **步驟**：
  1. 前往 [Supabase Dashboard](https://supabase.com/dashboard)
  2. 選擇你的專案
  3. 進入 Settings → API
  4. 複製 **service_role** key（不是 anon key）

### 4. NEXT_PUBLIC_LIFF_ID
- **說明**：與 LIFF_ID 相同，但這是給前端使用的
- **值**：與上面的 LIFF_ID 相同

## 🎯 設定步驟

### 1. 前往 Vercel Dashboard
1. 登入 [Vercel Dashboard](https://vercel.com/dashboard)
2. 選擇你的專案

### 2. 設定環境變數
1. 點擊 **Settings** 標籤
2. 點擊左側的 **Environment Variables**
3. 逐一新增以下變數：

| 變數名稱 | 值 | 說明 |
|---------|---|------|
| `LINE_LOGIN_CHANNEL_ID` | `2001129748` | LINE Login Channel ID |
| `LINE_LOGIN_CHANNEL_SECRET` | `36a169e0bf3d0339a4b4749137efea18` | LINE Login Channel Secret |
| `SUPABASE_URL` | `https://ciqlfqfgzqqgdrogedxg.supabase.co` | Supabase URL |
| `LIFF_ID` | `你的 LIFF ID` | LIFF App ID |
| `APP_SESSION_SECRET` | `你的隨機字串` | Session 簽章金鑰 |
| `SUPABASE_SERVICE_KEY` | `你的 Service Role Key` | Supabase Service Role Key |
| `NEXT_PUBLIC_LIFF_ID` | `你的 LIFF ID` | 前端 LIFF ID |

### 3. 重新部署
設定完成後，點擊 **Deployments** 標籤，然後點擊 **Redeploy** 按鈕。

## 🧪 測試

部署完成後，測試以下網址：
- **測試頁面**：`https://YOUR-APP.vercel.app/test-login`
- **遊戲頁面**：`https://YOUR-APP.vercel.app/game-new`

## ❓ 常見問題

### Q: 如何取得 Supabase Service Role Key？
A: 前往 Supabase Dashboard → Settings → API → 複製 service_role key（不是 anon key）

### Q: LIFF_ID 格式是什麼？
A: 格式為 `xxxxxxxx-xxxxxxxx`，在 LINE Console 建立 LIFF App 後取得

### Q: APP_SESSION_SECRET 要多長？
A: 至少64字元，建議使用隨機字串產生器

### Q: 設定後需要重新部署嗎？
A: 是的，設定環境變數後需要重新部署專案

## 📞 需要協助？

如果遇到問題，請檢查：
1. 環境變數名稱是否正確
2. 環境變數值是否正確
3. 是否已重新部署專案
4. LINE Console 設定是否正確

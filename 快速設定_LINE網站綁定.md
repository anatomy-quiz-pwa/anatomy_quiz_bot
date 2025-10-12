# 快速設定：LINE 網站綁定功能

## ⚡ 5 分鐘快速設定

### 步驟 1：在 Supabase 創建表格（1 分鐘）

1. 進入 Supabase Dashboard
2. 點擊左側 **SQL Editor**
3. 複製 `create_link_tokens_table.sql` 的內容
4. 點擊 **Run** 執行

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

✅ 表格創建完成！

---

### 步驟 2：設定 Vercel 環境變數（2 分鐘）

1. 進入 [Vercel Dashboard](https://vercel.com/dashboard)
2. 選擇你的專案 `anatomy-quiz-bot`
3. 點擊 **Settings** → **Environment Variables**
4. 添加以下變數：

#### 必要變數

| 變數名稱 | 值 | 說明 |
|---------|---|------|
| `NEXT_PUBLIC_SUPABASE_URL` | `https://ciqlfqfgzqqgdrogedxg.supabase.co` | Supabase URL |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | （從 Supabase 取得） | Supabase Anon Key |
| `SUPABASE_SERVICE_ROLE` | （從 Supabase 取得） | Supabase Service Role Key |
| `SESSION_SECRET` | （自行生成） | JWT 簽名密鑰 |

#### 如何取得 Supabase Keys？

1. 進入 Supabase Dashboard
2. 點擊左側 **Settings** → **API**
3. 複製：
   - **anon public** → `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - **service_role** → `SUPABASE_SERVICE_ROLE` ⚠️ 保密！

#### 如何生成 SESSION_SECRET？

在終端機執行：
```bash
openssl rand -base64 32
```

或使用線上工具：https://generate-secret.now.sh/32

5. 點擊 **Save** 儲存所有變數
6. Vercel 會自動重新部署

✅ Vercel 環境變數設定完成！

---

### 步驟 3：設定 Flask 後端環境變數（1 分鐘）

如果你的 Flask 後端部署在 Render：

1. 進入 [Render Dashboard](https://render.com/)
2. 選擇你的 Flask 服務
3. 點擊 **Environment**
4. 添加以下變數：

| 變數名稱 | 值 |
|---------|---|
| `API_BASE_URL` | `https://your-flask-app.onrender.com` |
| `WEBSITE_URL` | `https://anatomy-quiz-bot.vercel.app` |

5. 點擊 **Save Changes**，Render 會自動重新部署

✅ Flask 後端環境變數設定完成！

---

### 步驟 4：測試功能（1 分鐘）

1. **在 LINE 中測試**：
   - 打開你的 LINE Bot
   - 輸入：`網站`
   - 應該收到一個 Flex Message

2. **點擊連結**：
   - 點擊「🔗 一鍵連結並開始」按鈕
   - 應該跳轉到網站並顯示「🎉 連結成功！」

3. **測試同步**：
   - 點擊「🎮 開始遊戲」
   - 在網站上答題
   - 回到 LINE Bot，等級和紀錄應該自動同步

✅ 功能測試完成！

---

## 🎯 完成檢查清單

- [ ] Supabase `link_tokens` 表格已創建
- [ ] Vercel 環境變數已設定（4 個變數）
- [ ] Flask 後端環境變數已設定（2 個變數）
- [ ] LINE 輸入「網站」能收到 Flex Message
- [ ] 點擊連結能成功綁定
- [ ] 網站答題能同步到 LINE Bot

---

## 🔧 疑難排解

### 問題 1：LINE 輸入「網站」沒有反應

**解決方法**：
1. 檢查 Flask 後端是否正常運行
2. 查看 Flask 日誌是否有錯誤
3. 確認 `API_BASE_URL` 設定正確

### 問題 2：點擊連結顯示「連結失敗」

**可能原因**：
- Token 已過期（10 分鐘）→ 重新在 LINE 輸入「網站」
- Token 已使用 → 重新在 LINE 輸入「網站」
- Supabase 連接失敗 → 檢查環境變數

**解決方法**：
1. 檢查 Vercel 日誌：`vercel logs`
2. 確認環境變數設定正確
3. 確認 Supabase 表格存在

### 問題 3：連結成功但答題沒有同步

**解決方法**：
1. 開啟瀏覽器開發者工具（F12）
2. 查看 Console 是否有錯誤
3. 檢查 `/api/answer` API 是否正常
4. 確認 Session Cookie 是否設定成功

---

## 📞 需要幫助？

查看完整文檔：`LINE_網站綁定功能實施指南.md`

---

## 🎉 恭喜！

你已經成功設定 LINE 網站綁定功能！

現在學生可以：
- ✅ 在 LINE 和網站之間無縫切換
- ✅ 等級和紀錄自動同步
- ✅ 使用大螢幕更好地學習解剖學

享受你的遊戲化學習系統吧！🚀


# 🚀 Vercel 部署指南 - 強制從 Supabase 抓取題目

## ✅ 已完成的修正

### 1. 強制從 Supabase 抓取題目
- ✅ 移除了預設題目的使用
- ✅ 所有題目必須從 Supabase 即時獲取
- ✅ 無法連接時會顯示錯誤訊息
- ✅ 確保題庫的即時性和準確性

### 2. 關閉本地服務器
- ✅ 已停止 localhost:8080
- ✅ 準備部署到 Vercel 雲端

### 3. 優化配置
- ✅ 創建 Vercel 配置文件
- ✅ 禁用緩存確保即時數據
- ✅ 詳細的錯誤日誌

---

## 🌐 部署到 Vercel（3種方法）

### 方法一：Vercel CLI（推薦）⭐

```bash
# 1. 安裝 Vercel CLI（如果還沒安裝）
npm install -g vercel

# 2. 進入 public 目錄
cd "/Users/baobaoc/Downloads/anatomy_quiz_bot 2/anatomy_quiz_bot/public"

# 3. 登入 Vercel
vercel login

# 4. 部署到生產環境
vercel --prod
```

**輸出示例：**
```
🔍 Inspect: https://vercel.com/...
✅ Production: https://anatomy-quiz-xxx.vercel.app
```

### 方法二：Vercel Dashboard（最簡單）🎯

#### 步驟：

1. **訪問 Vercel**
   ```
   https://vercel.com
   ```

2. **點擊 "Add New" → "Project"**

3. **選擇部署方式：**
   - **選項 A：拖放文件夾**
     - 直接拖放 `public` 文件夾到頁面
     - 等待上傳和部署
     - 完成！

   - **選項 B：連接 Git**
     - 先將代碼推送到 GitHub
     - 在 Vercel 選擇 "Import Git Repository"
     - 選擇你的倉庫

4. **配置項目**（如果使用 Git）
   ```
   Framework Preset: Other
   Root Directory: public
   Build Command: (留空)
   Output Directory: .
   Install Command: (留空)
   ```

5. **點擊 "Deploy"**

6. **等待部署完成**（通常 < 1分鐘）

7. **獲得你的網址**
   ```
   https://your-project-name.vercel.app
   ```

### 方法三：使用提供的腳本 🤖

```bash
# 運行部署腳本
cd "/Users/baobaoc/Downloads/anatomy_quiz_bot 2/anatomy_quiz_bot"
./deploy-to-vercel.sh
```

---

## 📋 部署前檢查清單

### ✅ 必須確認的事項

- [ ] **Supabase 數據庫已設置**
  - questions 表已創建
  - 題目已添加到數據庫
  - Supabase URL 和 Key 正確

- [ ] **題目格式正確**
  ```sql
  -- 檢查題目
  SELECT count(*) FROM questions;
  SELECT level, count(*) FROM questions GROUP BY level;
  ```

- [ ] **本地測試通過**
  - 可以從 Supabase 載入題目
  - 答題功能正常
  - 統計更新正確

---

## 🔧 Supabase 題庫設置

### 1. 確認 questions 表存在

```sql
-- 如果表不存在，創建它
CREATE TABLE IF NOT EXISTS questions (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    options JSONB NOT NULL,
    correct_answer INTEGER NOT NULL,
    explanation TEXT,
    level INTEGER NOT NULL CHECK (level BETWEEN 1 AND 14),
    category TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 2. 添加示例題目

```sql
-- 等級 1 題目
INSERT INTO questions (question, options, correct_answer, explanation, level, category)
VALUES 
('心臟的主要功能是什麼？', 
 '["輸送血液", "過濾血液", "儲存血液", "製造血液"]', 
 0, 
 '心臟是循環系統的核心，主要功能是泵血輸送到全身各個器官和組織。', 
 1, 
 '循環系統'),

('人體最大的器官是什麼？', 
 '["心臟", "肝臟", "皮膚", "肺"]', 
 2, 
 '皮膚是人體最大的器官，覆蓋整個身體表面。', 
 1, 
 '器官系統'),

('人體有多少塊骨頭？', 
 '["186塊", "206塊", "226塊", "246塊"]', 
 1, 
 '成年人體有206塊骨頭。', 
 2, 
 '骨骼系統');
```

### 3. 檢查數據

```sql
-- 查看所有題目
SELECT id, question, level, category FROM questions ORDER BY level, id;

-- 查看題目分佈
SELECT level, count(*) as count FROM questions GROUP BY level ORDER BY level;
```

### 4. 設置權限（重要！）

在 Supabase Dashboard：
1. 進入 **Authentication** → **Policies**
2. 為 `questions` 表添加政策：

```sql
-- 允許所有人讀取題目
CREATE POLICY "Enable read access for all users" 
ON questions 
FOR SELECT 
USING (true);
```

---

## 🎯 部署後測試

### 1. 訪問你的網站

```
https://your-project-name.vercel.app
```

### 2. 檢查功能

- [ ] 頁面正常載入
- [ ] 可以輸入暱稱
- [ ] 點擊「開始遊戲」
- [ ] 成功從 Supabase 載入題目
- [ ] 題目正常顯示
- [ ] 可以選擇答案
- [ ] 提交後顯示結果
- [ ] 統計正確更新
- [ ] 可以繼續答題

### 3. 查看控制台（F12）

**成功的日誌應該顯示：**
```
🔄 正在從 Supabase 載入題目...
✅ 成功從 Supabase 載入 XX 道題目
📊 題目分佈: {1: 10, 2: 15, ...}
```

**如果有錯誤：**
- 檢查 Supabase 連接
- 確認表名稱正確
- 檢查權限設置

---

## 🐛 常見問題排查

### 問題 1：無法連接到題庫

**錯誤訊息：**
```
❌ 載入題目失敗: ...
無法連接到題庫！請檢查網路連接或聯繫管理員。
```

**解決方案：**
1. 檢查 `game.js` 中的 Supabase 配置
2. 確認 SUPABASE_URL 和 SUPABASE_ANON_KEY 正確
3. 在 Supabase Dashboard 檢查表是否存在
4. 檢查 RLS 政策是否正確設置

### 問題 2：題庫為空

**錯誤訊息：**
```
❌ 題庫為空
題庫目前沒有題目！請聯繫管理員添加題目。
```

**解決方案：**
1. 登入 Supabase Dashboard
2. 執行上面的 INSERT 語句添加題目
3. 重新整理遊戲頁面

### 問題 3：部署失敗

**解決方案：**
```bash
# 重新登入
vercel login

# 清除緩存
vercel --force

# 重新部署
cd public
vercel --prod
```

### 問題 4：CORS 錯誤

**解決方案：**
在 Supabase Dashboard：
1. Settings → API
2. 確認 URL 配置正確
3. 檢查 CORS 設置

---

## 📊 系統架構

```
用戶瀏覽器
    ↓
Vercel CDN（全球加速）
    ↓
index.html + game.js（靜態文件）
    ↓
Supabase JavaScript SDK
    ↓
Supabase PostgreSQL（題庫）
    ↓
即時抓取題目（不使用緩存）
```

### 優勢：
- ⚡ **快速**：CDN 全球分發
- 🔄 **即時**：每次都從數據庫抓取
- 💰 **免費**：Vercel 和 Supabase 免費層
- 🌍 **全球**：自動優化訪問速度

---

## 🎮 使用流程

1. **用戶訪問** → Vercel URL
2. **載入遊戲** → 顯示歡迎畫面
3. **開始遊戲** → 從 Supabase 載入題目
4. **答題** → 即時驗證和反饋
5. **統計更新** → 保存到 Supabase
6. **繼續遊戲** → 循環

---

## 🔐 安全性

### 當前配置：
- ✅ 使用 Supabase Anon Key（公開安全）
- ✅ RLS 政策控制權限
- ✅ 只讀取 questions 表
- ✅ 寫入需要認證（可選）

### 建議：
- 啟用 Row Level Security (RLS)
- 限制 API 請求頻率
- 監控異常訪問

---

## 📱 自定義域名（可選）

在 Vercel Dashboard：
1. 進入你的項目
2. Settings → Domains
3. 添加自定義域名
4. 配置 DNS 記錄
5. 等待驗證

---

## 🎉 完成！

部署成功後，你將獲得：

✅ 一個全球可訪問的網址  
✅ 自動 HTTPS 加密  
✅ 全球 CDN 加速  
✅ 即時從 Supabase 抓取題目  
✅ 零維護成本  

**現在就開始部署吧！** 🚀

---

## 📞 需要幫助？

1. **檢查日誌**
   - 瀏覽器控制台（F12）
   - Vercel Dashboard → Logs
   - Supabase Dashboard → Logs

2. **測試連接**
   ```javascript
   // 在瀏覽器控制台執行
   console.log('Testing Supabase connection...');
   ```

3. **重新部署**
   ```bash
   vercel --prod --force
   ```

祝部署順利！🎊


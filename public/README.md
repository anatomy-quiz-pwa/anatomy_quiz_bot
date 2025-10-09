# 解剖學測驗 - 遊戲化問答系統

這是一個純前端的遊戲化學習平台，直接連接 Supabase 數據庫，提供快速、流暢的答題體驗。

## ✨ 特色功能

- 🚀 **即時回饋**：答題後立即顯示結果和解釋
- 🎮 **遊戲化設計**：14個等級，從新手到終極解剖師
- 📊 **實時統計**：追蹤你的答題記錄和進度
- 🏆 **連續答對**：記錄你的答題連勝紀錄
- ⚡ **快速載入**：無需後端服務器，直連 Supabase
- 📱 **響應式設計**：支援手機、平板、電腦

## 🎯 如何使用

### 線上遊玩

直接訪問部署的網址即可開始遊戲！

### 本地測試

1. 在瀏覽器中打開 `index.html`
2. 輸入你的暱稱（選填）
3. 點擊「開始遊戲」按鈕
4. 開始答題！

## 🚀 部署到 Vercel

### 方法一：使用 Vercel CLI

```bash
# 安裝 Vercel CLI
npm i -g vercel

# 部署到 Vercel
cd public
vercel --prod
```

### 方法二：通過 GitHub

1. 將代碼推送到 GitHub
2. 在 Vercel Dashboard 中導入項目
3. 設置構建目錄為 `public`
4. 點擊部署

## 🎮 遊戲規則

- **答對**：+10分，連勝數+1
- **答錯**：連勝數歸零
- **升級**：每答對5題升一級（最高14級）
- **題目難度**：根據你的等級自動調整

## 🏅 等級系統

| 等級 | 稱號 |
|------|------|
| 1 | 新手解剖師 |
| 2-3 | 初級解剖師 |
| 4-7 | 中級解剖師 |
| 8-11 | 高級解剖師 |
| 12-13 | 專家解剖師 |
| 14 | 終極解剖師 |

## 🔧 技術架構

- **前端**：純 HTML + CSS + JavaScript
- **數據庫**：Supabase (PostgreSQL)
- **UI 框架**：Bootstrap 5
- **圖標**：Font Awesome 6
- **部署**：Vercel (靜態託管)

## 📊 數據庫結構

### questions 表
- `id`: 題目ID
- `question`: 題目內容
- `options`: 選項陣列
- `correct_answer`: 正確答案索引
- `explanation`: 詳細解釋
- `level`: 難度等級 (1-14)
- `category`: 題目類別

### web_game_stats 表（可選）
- `user_id`: 用戶ID
- `nickname`: 暱稱
- `level`: 當前等級
- `score`: 總分
- `correct`: 答對數
- `total`: 總答題數
- `streak`: 連續答對數
- `last_played`: 最後遊玩時間

## 🎨 自定義配置

在 `game.js` 中修改：

```javascript
// Supabase 配置
const SUPABASE_URL = 'your_supabase_url';
const SUPABASE_ANON_KEY = 'your_anon_key';

// 等級稱號
const LEVEL_TITLES = {
    1: "新手解剖師",
    // ...
};
```

## 💡 預設題目

如果無法連接到 Supabase，系統會自動使用內建的預設題目，確保遊戲可以正常運行。

## 📱 響應式設計

- ✅ 桌面電腦 (1920x1080+)
- ✅ 筆記本電腦 (1366x768+)
- ✅ 平板電腦 (768x1024+)
- ✅ 手機 (375x667+)

## 🐛 問題排查

### 無法載入題目
- 檢查 Supabase 連接配置
- 確認數據庫表和欄位名稱正確
- 系統會自動使用預設題目

### 樣式顯示異常
- 確保有網絡連接（Bootstrap 和 Font Awesome 使用 CDN）
- 清除瀏覽器緩存

## 📄 許可證

MIT License

## 👥 貢獻

歡迎提交 Issue 和 Pull Request！


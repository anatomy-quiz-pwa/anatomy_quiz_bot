# 🖼️ Hero 圖片功能更新說明

## 更新日期
2025年10月12日

## 功能說明
根據 Supabase 資料庫的設計，當問題對應的圖片是空白時，系統會自動顯示對應等級的 poster 圖片。此功能已在 LINE Bot 中實現，現已同步到網頁版本。

## 已完成的更新

### 1. 網頁版本功能增強 ✅

#### 檔案：`public/game.html`
- **新增 Hero 圖片顯示區域**（第 493-497 行）
  ```html
  <div id="question-hero-image" class="mb-4" style="display: none;">
      <img id="hero-image" src="" alt="題目圖片">
  </div>
  ```

- **新增函數：`getQuestionHeroImageUrl()`**（第 743-766 行）
  - 與 LINE Bot 邏輯完全一致
  - 優先使用題目特定圖片（`qimage_url` 或 `image_url`）
  - 如果為空，使用用戶當前等級的 poster 圖片

- **新增函數：`getLevelPosterUrl()`**（第 768-799 行）
  - 支援等級 1-14 的 poster 映射
  - 超出範圍時自動使用 level 1 poster

#### 檔案：`templates/game.html`
- **新增函數：`getQuestionHeroImageUrl()`**（第 191-209 行）
- **新增函數：`getLevelPosterUrl()`**（第 211-242 行）
- **更新 `displayQuestion()` 函數**（第 244-287 行）
  - 動態生成包含 Hero 圖片的題目卡片

### 2. LINE Bot 現有功能總結 📱

#### 檔案：`app_supabase.py`
已實現的相關函數：
- `get_question_hero_image_url_with_fallback()` - 第 760-800 行
- `get_question_hero_image_url()` - 第 802-838 行
- `create_question_flex_message()` - 第 645-758 行

### 3. 測試工具 🧪

#### 新增測試檔案：`test_web_hero_image.html`
- 提供 4 個互動測試場景
- 驗證圖片顯示邏輯
- 測試所有等級（1-14）的 poster 圖片
- 測試邊界情況

使用方法：
```bash
# 在瀏覽器中直接打開
open test_web_hero_image.html
```

#### 現有測試檔案：`test_hero_and_supabase.py`
- 測試 Supabase 連線
- 測試 hero 圖片 URL
- 驗證等級海報圖片

使用方法：
```bash
python test_hero_and_supabase.py
```

### 4. 技術文檔 📚

#### 新增文件：`HERO_IMAGE_IMPLEMENTATION.md`
詳細記錄了：
- 功能概述
- 實現邏輯和優先順序
- 等級 Poster 映射表
- 程式碼位置說明
- 資料庫結構
- 使用範例
- 測試建議

## 圖片優先順序邏輯

```
1. 檢查 question.qimage_url
   ↓ (如果為空)
2. 檢查 question.image_url
   ↓ (如果為空)
3. 使用用戶當前等級的 poster 圖片
   └─ 如果沒有用戶等級，使用題目等級
   └─ 如果等級超過 14，使用 level 1 poster
```

## 等級 Poster 圖片

存儲位置：
```
https://ciqlfqfgzqqgdrogedxg.supabase.co/storage/v1/object/public/linebot/

level_1_poster.png  ~ level_14_poster.png
```

## 資料庫欄位

### `anatomy_questions_v2` 表格
- `qimage_url` - 題目特定圖片 URL（優先使用）
- `image_url` - 備用圖片 URL  
- `level` - 題目等級（1-14）

## 測試建議

### 1. 功能測試
```bash
# 1. 打開測試頁面
open test_web_hero_image.html

# 2. 依次執行所有測試
- 測試 1: 驗證有圖片的題目
- 測試 2: 驗證無圖片時使用 poster
- 測試 3: 驗證所有等級的 poster
- 測試 4: 驗證邊界情況
```

### 2. 整合測試
```bash
# 啟動網頁服務器（如果使用 Flask）
python app.py

# 或直接打開 HTML 檔案
open public/game.html
```

### 3. LINE Bot 測試
- 發送測試訊息給 Bot
- 驗證不同等級的題目圖片顯示
- 檢查無圖片題目是否顯示 poster

## 注意事項

### 1. 圖片載入失敗處理
- 網頁版會在圖片載入失敗時顯示錯誤提示
- LINE Bot 會 fallback 到預設圖片

### 2. 等級範圍
- 目前支援等級 1-14
- 超出範圍會自動使用 level 1 poster
- 如需擴展，請更新 `levelPosters` 映射

### 3. 效能考慮
- 圖片 URL 檢查採用輕量級方式
- LINE Bot 使用 `requests.head()` 驗證圖片存在
- 網頁版直接使用 URL，由瀏覽器處理載入

## 相關檔案清單

### 主要功能檔案
- `app_supabase.py` - LINE Bot 實現
- `public/game.html` - 獨立網頁版
- `templates/game.html` - Flask 模板版

### 測試檔案
- `test_web_hero_image.html` - 網頁版測試
- `test_hero_and_supabase.py` - LINE Bot 測試

### 文檔
- `HERO_IMAGE_IMPLEMENTATION.md` - 技術實現文檔
- `更新說明_Hero圖片功能.md` - 本文檔

## 後續建議

### 1. 圖片快取
考慮實現圖片快取機制以提升載入速度：
- 瀏覽器快取策略
- CDN 加速（如果需要）

### 2. 圖片預載入
在遊戲開始時預載入常用等級的 poster 圖片

### 3. 監控和日誌
- 追蹤圖片載入失敗率
- 記錄最常使用的 poster 等級

### 4. 擴展等級
如果未來需要支援更多等級：
1. 上傳新的 poster 圖片到 Supabase Storage
2. 更新 `levelPosters` 映射
3. 更新文檔

## 技術支援

如有問題，請檢查：
1. 瀏覽器控制台的日誌輸出
2. 圖片 URL 是否可訪問
3. Supabase Storage 權限設置

---

**更新完成！** 🎉

網頁版本現在已經與 LINE Bot 的圖片顯示邏輯完全一致。


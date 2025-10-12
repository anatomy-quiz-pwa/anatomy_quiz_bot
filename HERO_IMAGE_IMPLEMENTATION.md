# Hero 圖片實現說明

## 功能概述
在 LINE Bot 和網頁版本中，當問題的圖片欄位為空白時，系統會自動顯示對應等級的 poster 圖片。

## 實現邏輯

### 圖片優先順序
1. **優先順序 1**：使用題目特定的圖片
   - 檢查 `qimage_url` 欄位
   - 如果為空，檢查 `image_url` 欄位
   
2. **優先順序 2**：使用等級 poster 圖片
   - 如果題目圖片為空或無效
   - 使用用戶當前等級對應的 poster 圖片
   - 如果沒有用戶等級，使用題目等級

3. **優先順序 3**：使用預設圖片（僅 LINE Bot）
   - 當所有方式都失敗時使用

### 等級 Poster 映射

等級 poster 圖片存儲在 Supabase Storage 中：

```
基礎 URL: https://ciqlfqfgzqqgdrogedxg.supabase.co/storage/v1/object/public/linebot/

等級 1-14 的 poster 圖片：
- level_1_poster.png
- level_2_poster.png
- ...
- level_14_poster.png
```

## 程式碼位置

### LINE Bot (app_supabase.py)

#### 函數：`get_question_hero_image_url_with_fallback(question, user_level=None)`
- **位置**：第 760-800 行
- **功能**：獲取題目的 Hero 圖片 URL，包含完整的 fallback 邏輯
- **使用場景**：在創建題目 Flex Message 時調用

#### 函數：`get_question_hero_image_url(level)`
- **位置**：第 802-838 行
- **功能**：根據等級返回對應的 poster 圖片 URL
- **支援等級**：1-14

### 網頁版本

#### public/game.html

**函數：`getQuestionHeroImageUrl(question, userLevel = null)`**
- **位置**：第 743-766 行
- **功能**：與 LINE Bot 邏輯一致的圖片 URL 獲取

**函數：`getLevelPosterUrl(level)`**
- **位置**：第 768-799 行
- **功能**：返回等級對應的 poster 圖片 URL

**HTML 結構**：
```html
<div id="question-hero-image" class="mb-4" style="display: none;">
    <img id="hero-image" src="" alt="題目圖片" 
         style="width: 100%; max-height: 400px; object-fit: cover; 
                border-radius: 12px; border: 2px solid #1C1C1C; 
                box-shadow: 4px 4px 0 #1C1C1C;">
</div>
```

#### templates/game.html

**函數：`getQuestionHeroImageUrl(question, userLevel = null)`**
- **位置**：第 191-209 行
- **功能**：與 LINE Bot 邏輯一致

**函數：`getLevelPosterUrl(level)`**
- **位置**：第 211-242 行
- **功能**：返回等級對應的 poster 圖片 URL

**HTML 結構**：在 `displayQuestion()` 函數中動態生成
```javascript
<div class="card-img-top">
    <img src="${heroImageUrl}" alt="題目圖片" 
         style="width: 100%; max-height: 400px; object-fit: cover;">
</div>
```

## 資料庫結構

### anatomy_questions_v2 表格欄位
- `qimage_url`: 題目特定圖片 URL（優先使用）
- `image_url`: 備用圖片 URL
- `level`: 題目等級（1-14）

## 使用範例

### LINE Bot
```python
# 創建題目 Flex Message 時
flex_message = create_question_flex_message(
    question=question_data,
    is_admin=False,
    user_level=user_stats['level']  # 傳入用戶等級
)
```

### 網頁版本
```javascript
// 在 displayQuestion 函數中
const heroImageUrl = getQuestionHeroImageUrl(question, userStats.level);

// 設置圖片
heroImage.src = heroImageUrl;
heroImageContainer.style.display = 'block';
```

## 測試建議

1. **測試題目有圖片的情況**
   - 確認題目特定圖片正確顯示
   
2. **測試題目無圖片的情況**
   - 確認顯示對應等級的 poster 圖片
   - 測試不同等級（1-14）
   
3. **測試邊界情況**
   - 等級超過 14 時，應使用 level 1 poster
   - 圖片 URL 為空字串時的處理
   - 網絡錯誤時的處理（LINE Bot）

## 更新日期
2025-10-12

## 相關檔案
- `app_supabase.py` - LINE Bot 實現
- `public/game.html` - 獨立網頁版實現
- `templates/game.html` - Flask 模板版實現
- `test_hero_and_supabase.py` - Hero 圖片測試腳本


# 解說圖片 404 錯誤診斷報告

## 問題分析

根據診斷，解說圖片出現 `{"statusCode":"404","error":"not_found","message":"Object not found"}` 錯誤的原因如下：

### 1. 根本原因
- **資料庫結構缺失**：`questions` 表格中只有文字 `explanation` 欄位，沒有 `explanation_image` 或類似的圖片 URL 欄位
- **圖片路徑不存在**：程式嘗試訪問不存在的 Supabase 儲存桶路徑

### 2. 測試結果
- ✅ Supabase 儲存桶基本功能正常（level posters 可正常訪問）
- ✅ 升級圖片 (`levelup.png`) 正常
- ❌ 解說圖片路徑返回 400/404 錯誤

## 解決方案

### 方案一：新增解說圖片欄位（推薦）

1. **修改資料庫結構**
```sql
-- 新增解說圖片欄位到 questions 表格
ALTER TABLE questions ADD COLUMN explanation_image_url TEXT;
ALTER TABLE anatomy_questions_v2 ADD COLUMN explanation_image_url TEXT;

-- 為現有題目設置解說圖片 URL（如果有的話）
UPDATE questions SET explanation_image_url = 
  'https://ciqlfqfgzqqgdrogedxg.supabase.co/storage/v1/object/public/linebot/explanations/level_' || level || '_q' || id || '.png'
WHERE explanation IS NOT NULL AND explanation != '';
```

2. **上傳解說圖片到 Supabase 儲存桶**
- 路徑格式：`/linebot/explanations/level_{level}_q{question_id}.png`
- 確保圖片檔案存在於 Supabase Storage 中

3. **修改程式碼**
```python
# 在 get_all_questions() 函數中新增
"explanation_image_url": item.get('explanation_image_url', ''),
```

### 方案二：暫時移除解說圖片（快速修復）

1. **修改 Flex Message 模板**
- 移除解說圖片的顯示部分
- 只保留文字解說

2. **更新答案處理邏輯**
```python
def send_explanation(user_id, question_data, is_correct):
    explanation_text = f"""
{'✅ 答對了！' if is_correct else '❌ 答錯了！'}

📚 解說：
{question_data.get('explanation', '暫無解說')}

輸入「開始」繼續答題！
"""
    send_simple_text_message(user_id, explanation_text)
```

### 方案三：使用預設圖片

1. **設置預設解說圖片**
```python
def get_explanation_image_url(level, question_id):
    # 嘗試使用特定圖片
    specific_url = f"https://ciqlfqfgzqqgdrogedxg.supabase.co/storage/v1/object/public/linebot/explanations/level_{level}_q{question_id}.png"
    
    # 如果特定圖片不存在，使用預設圖片
    default_url = "https://ciqlfqfgzqqgdrogedxg.supabase.co/storage/v1/object/public/linebot/default_explanation.png"
    
    # 檢查圖片是否存在
    try:
        response = requests.head(specific_url, timeout=5)
        if response.status_code == 200:
            return specific_url
    except:
        pass
    
    return default_url
```

## 立即修復建議

**推薦使用方案二（暫時移除解說圖片）**，因為：

1. **快速見效**：不需要修改資料庫結構或上傳圖片
2. **用戶體驗**：避免 404 錯誤，保持功能正常運作
3. **後續擴展**：之後可以逐步添加解說圖片功能

## 實施步驟

1. 立即修改答案處理邏輯，移除解說圖片顯示
2. 確保解說文字正常顯示
3. 測試修復後的功能
4. 後續規劃解說圖片的完整實施方案

---

**診斷完成時間**：2025年9月17日  
**問題狀態**：已識別根本原因，提供多種解決方案

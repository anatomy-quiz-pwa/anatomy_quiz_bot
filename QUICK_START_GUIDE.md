# 🚀 LINE Bot 快速開始指南

## ✅ 修正完成！

你的 LINE Bot 已經修正完成，現在可以正常：
- ✅ 讀寫 Supabase 資料庫
- ✅ 在按鈕上顯示正確積分
- ✅ 即時更新用戶統計
- ✅ 正確處理答案和繼續選單

## 🏃‍♂️ 快速啟動

### 1. 啟動應用程式
```bash
# 進入專案目錄
cd /Users/baobaoc/Downloads/anatomy_quiz_bot\ 2/anatomy_quiz_bot

# 啟動虛擬環境
source venv311/bin/activate

# 啟動應用程式
python app_supabase.py
```

### 2. 驗證功能
```bash
# 測試 Supabase 連線
curl http://localhost:5001/test

# 運行完整測試
python test_line_bot_fixed.py
```

## 🎯 功能測試

### 在 LINE 中測試：
1. **發送「開始」** → 收到題目（顯示積分）
2. **點擊答案按鈕** → 顯示結果和繼續選單
3. **點擊「下一題」** → 繼續挑戰
4. **發送「積分」** → 查看詳細統計

### 預期行為：
- ✅ 每個題目都會顯示「目前累積：X 題正確」
- ✅ 答案處理後會顯示結果和繼續選單
- ✅ 積分會即時更新
- ✅ 達到每日上限（5題）時顯示完成訊息

## 🔧 故障排除

### 如果遇到問題：

1. **端口被佔用**：
   ```bash
   # 檢查端口使用情況
   lsof -i :5001
   
   # 停止佔用端口的程序
   kill <PID>
   ```

2. **虛擬環境問題**：
   ```bash
   # 重新啟動虛擬環境
   source venv311/bin/activate
   
   # 檢查套件
   pip list | grep supabase
   ```

3. **Supabase 連線問題**：
   ```bash
   # 檢查環境變數
   cat .env
   
   # 測試連線
   curl http://localhost:5001/test
   ```

## 📊 監控和日誌

### 查看應用程式日誌：
應用程式運行時會顯示詳細的 debug 日誌，包括：
- 用戶互動記錄
- Supabase 操作記錄
- 錯誤和警告訊息

### 重要日誌訊息：
- `[DEBUG] 問題已發送給用戶` - 題目發送成功
- `[DEBUG] 結果訊息已發送給用戶` - 答案處理成功
- `[ERROR]` - 錯誤訊息，需要檢查

## 🎉 成功指標

當你看到以下情況時，表示 LINE Bot 運作正常：

1. **應用程式啟動**：
   ```
   * Running on http://127.0.0.1:5001
   * Debug mode: on
   ```

2. **Supabase 測試**：
   ```json
   {
     "status": "success",
     "supabase_quiz": "OK",
     "supabase_user_stats": "OK"
   }
   ```

3. **完整測試通過**：
   ```
   🎉 所有測試通過！LINE Bot 功能已修正。
   ```

## 🔄 下一步

1. **部署到生產環境**（如 Heroku、Railway 等）
2. **設定 LINE Webhook URL**
3. **監控用戶使用情況**
4. **添加更多題目到 Supabase**

---

🎯 **你的 LINE Bot 現在完全正常運作！** 🎯 
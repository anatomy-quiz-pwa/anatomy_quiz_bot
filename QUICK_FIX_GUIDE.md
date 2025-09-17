# 🚀 快速修復指南

## 問題
輸入「排行榜」沒有出現對應的 flex 訊息，webhook 返回 500 錯誤。

## 根本原因
Render 使用 `uvicorn` 啟動 Flask 應用程式，但 uvicorn 是為 FastAPI 設計的，與 Flask 不兼容。

## 修復步驟

### 1. 上傳修復文件
將以下兩個文件上傳到您的 Render 專案根目錄：

#### `Procfile`
```
web: gunicorn app_supabase:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120
```

#### `requirements.txt`
```
flask==3.0.3
requests==2.32.5
supabase==2.6.0
line-bot-sdk==3.12.0
python-dotenv==1.0.1
gunicorn==22.0.0
```

### 2. 重新部署
1. 在 Render Dashboard 中點擊 "Manual Deploy"
2. 選擇 "Deploy latest commit"
3. 等待部署完成

### 3. 測試修復結果
```bash
# 測試 webhook
curl -X POST https://anatomy-quiz-bot.onrender.com/webhook \
  -H "Content-Type: application/json" \
  -d '{"events":[{"type":"message","source":{"userId":"test"},"message":{"type":"text","text":"排行榜"}}]}'
```

### 4. 驗證排行榜功能
在 LINE Bot 中輸入以下任一關鍵字：
- 排行榜
- leaderboard
- 排名
- 排行

應該會收到 Flex Message 格式的排行榜。

## 預期結果
- ✅ webhook 返回 200 狀態碼
- ✅ 用戶輸入「排行榜」收到 Flex Message
- ✅ 排行榜顯示前10名用戶數據

## 如果仍有問題
1. 檢查 Render 部署日誌
2. 確認環境變數設置正確
3. 運行 `python test_fix_verification.py` 進行詳細測試

## 技術說明
- **之前**: uvicorn (ASGI) + Flask (WSGI) = 不兼容
- **修復後**: gunicorn (WSGI) + Flask (WSGI) = 兼容 ✅

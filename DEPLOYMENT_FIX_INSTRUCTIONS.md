# 修復 uvicorn + Flask 兼容性問題

## 問題分析
生產環境使用 `uvicorn app_supabase:app` 啟動 Flask 應用程式，但 uvicorn 是為 FastAPI 設計的 ASGI 服務器，與 Flask（WSGI）存在兼容性問題。

## 解決方案

### 方案 1: 使用 Gunicorn（推薦）
1. 使用 `requirements.txt` 和 `Procfile`
2. Render 會自動使用 Gunicorn 啟動 Flask 應用程式

### 方案 2: 轉換為 FastAPI
1. 使用 `app_fastapi.py` 替換 `app_supabase.py`
2. 保持使用 uvicorn 啟動

## 部署步驟

### 使用方案 1（Gunicorn + Flask）
1. 將 `requirements.txt` 和 `Procfile` 上傳到 Render
2. 重新部署
3. Render 會自動使用 Gunicorn

### 使用方案 2（FastAPI）
1. 將 `app_fastapi.py` 重命名為 `app_supabase.py`
2. 重新部署
3. 保持使用 uvicorn 啟動

## 測試命令
```bash
# 測試 webhook
curl -X POST https://anatomy-quiz-bot.onrender.com/webhook \
  -H "Content-Type: application/json" \
  -d '{"events":[{"type":"message","source":{"userId":"test"},"message":{"type":"text","text":"排行榜"}}]}'
```

## 注意事項
- 方案 1 保持現有 Flask 代碼不變
- 方案 2 需要將 Flask 代碼轉換為 FastAPI
- 建議先嘗試方案 1

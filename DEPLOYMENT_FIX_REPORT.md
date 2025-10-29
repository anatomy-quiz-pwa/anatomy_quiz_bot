# LINE Bot 部署問題解決方案

## 問題描述
Render 部署時出現以下錯誤：
- `ERROR: Could not open requirements file: [Errno 2] No such file or directory: 'requirements.txt'`
- 系統同時嘗試使用 Python 和 Node.js，導致配置混亂

## 解決方案

### 1. 重新啟用必要的配置文件
以下文件被重新啟用：
- `requirements.txt` (從 `requirements.txt.disabled`)
- `Procfile` (從 `Procfile.disabled`) 
- `render.yaml` (從 `render.yaml.disabled`)

### 2. 更新 Python 依賴
`requirements.txt` 已更新，包含所有必要的依賴：
```
flask==3.1.2
requests==2.32.5
supabase==2.6.0
line-bot-sdk==3.12.0
python-dotenv==1.0.1
gunicorn==23.0.0
uvicorn[standard]>=0.30
cryptography>=3.4.8
PyJWT==2.8.0
```

### 3. 統一應用程序配置
- `Procfile`: 指向 `app_supabase:app`
- `render.yaml`: 指向 `app_supabase:app`
- 健康檢查端點: `/__health`

### 4. 環境變數配置
`render.yaml` 中配置的環境變數：
- `LINE_CHANNEL_SECRET`
- `LINE_CHANNEL_ACCESS_TOKEN`
- `SUPABASE_URL`
- `SUPABASE_KEY` (注意：不是 SUPABASE_ANON_KEY)
- `LINE_LOGIN_CHANNEL_ID`
- `LINE_LOGIN_CHANNEL_SECRET`
- `LINE_LOGIN_REDIRECT_URI`
- `PAGE_ACCESS_TOKEN`
- `VERIFY_TOKEN`
- `FLASK_SECRET_KEY`

## 部署步驟

### 1. 確保環境變數設置
在 Render 控制台中設置所有必要的環境變數。

### 2. 推送代碼
```bash
git add .
git commit -m "Fix deployment configuration"
git push origin main
```

### 3. 觸發重新部署
在 Render 控制台中手動觸發重新部署。

## 驗證
運行驗證腳本檢查配置：
```bash
python verify_deployment.py
```

## 技術細節

### 應用程序架構
- 主要應用：`app_supabase.py` (包含健康檢查端點)
- 安全模組：`secure_token_manager.py`, `secure_session_manager.py`
- Web 應用：`web_app.py` (用於網站功能)

### 部署配置
- 使用 Gunicorn 作為 WSGI 服務器
- 2 個 worker 進程，4 個線程
- 120 秒超時
- 健康檢查路徑：`/__health`

### 依賴管理
- 使用 `requirements.txt` 管理 Python 依賴
- 包含 JWT 支持用於安全會話管理
- 支持 LINE Bot SDK v3

## 注意事項
1. 確保所有環境變數在 Render 中正確設置
2. `SUPABASE_KEY` 變數名稱與其他應用可能不同
3. 健康檢查端點必須存在於 `app_supabase.py` 中
4. 部署後檢查日誌確保應用正常啟動

## 故障排除
如果部署仍然失敗：
1. 檢查 Render 日誌中的具體錯誤信息
2. 確認環境變數是否正確設置
3. 驗證 GitHub 倉庫中的文件是否正確推送
4. 檢查 `app_supabase.py` 中的導入是否正確

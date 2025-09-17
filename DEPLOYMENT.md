# 🚀 Vercel 部署指南

## 快速部署

### 1. 自動部署 (推薦)
1. 前往 [vercel.com](https://vercel.com)
2. 使用 GitHub 帳號登入
3. 點擊 "New Project"
4. 選擇 `anatomy-quiz-pwa/anatomy_admin_panel` 倉庫
5. 點擊 "Deploy"

### 2. 手動部署
```bash
# 安裝 Vercel CLI
npm i -g vercel

# 登入 Vercel
vercel login

# 部署
vercel --prod
```

## 環境變數設置

在 Vercel 項目設置中添加以下環境變數：

| 變數名 | 值 | 說明 |
|--------|-----|------|
| `NEXT_PUBLIC_API_BASE_URL` | `https://your-flask-app.onrender.com` | 您的 Flask 後端 API 地址 |
| `NODE_ENV` | `production` | 環境模式 |

## 部署後檢查

1. **檢查構建日誌**：確保沒有錯誤
2. **測試頁面**：訪問部署的 URL
3. **檢查 API 連接**：確認能正常調用後端

## 自定義域名

在 Vercel 項目設置中可以：
- 添加自定義域名
- 設置 HTTPS 重定向
- 配置 DNS 記錄

## 故障排除

### 常見問題
- **構建失敗**：檢查 `package.json` 和依賴
- **API 錯誤**：確認環境變數設置正確
- **路由問題**：檢查 `vercel.json` 配置

### 支持
如有問題，請檢查：
1. Vercel 構建日誌
2. 瀏覽器控制台錯誤
3. 網絡請求狀態


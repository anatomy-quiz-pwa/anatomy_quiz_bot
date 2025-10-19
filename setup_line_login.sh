#!/bin/bash

echo "🚀 LINE Login A/B 兩條路徑設定腳本"
echo "=================================="

# 檢查必要的環境變數
check_env_var() {
    if [ -z "${!1}" ]; then
        echo "❌ 錯誤: 環境變數 $1 未設定"
        echo "請在 Vercel Dashboard 中設定此環境變數"
        exit 1
    else
        echo "✅ $1 已設定"
    fi
}

echo ""
echo "📋 檢查環境變數..."
check_env_var "LINE_LOGIN_CHANNEL_ID"
check_env_var "LINE_LOGIN_CHANNEL_SECRET"
check_env_var "LIFF_ID"
check_env_var "APP_SESSION_SECRET"
check_env_var "SUPABASE_URL"
check_env_var "SUPABASE_SERVICE_KEY"
check_env_var "NEXT_PUBLIC_LIFF_ID"

echo ""
echo "🔧 檢查 Supabase 資料表結構..."

# 這裡可以加入 Supabase 資料表檢查邏輯
echo "請確保 users 表有 line_user_id 欄位："
echo "ALTER TABLE users ADD COLUMN IF NOT EXISTS line_user_id text UNIQUE;"

echo ""
echo "📱 檢查 LINE Console 設定..."
echo "1. LINE Login Channel Callback URL: https://YOUR-APP.vercel.app/api/auth/line/callback"
echo "2. LIFF App Endpoint URL: https://YOUR-APP.vercel.app/game-new"
echo "3. Scopes: openid profile"

echo ""
echo "🧪 測試路徑："
echo "情境 A (LIFF): 在 LINE 中開啟 https://YOUR-APP.vercel.app/game-new"
echo "情境 B (OIDC): 在瀏覽器開啟 https://YOUR-APP.vercel.app/test-login"

echo ""
echo "✅ 設定完成！"
echo "現在可以部署到 Vercel 並測試登入功能了。"

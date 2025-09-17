#!/bin/bash
# 完整的環境變量設置腳本

echo "🚀 開始設置解剖問答機器人完整環境變量..."

# 設置 Supabase 環境變量
export SUPABASE_URL="https://ciqlfqfgzqqgdrogedxg.supabase.co"
export SUPABASE_ANON_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA"

echo "✅ 已設置 Supabase 環境變量"

# 檢查 LINE Bot 環境變量
if [ -z "$LINE_CHANNEL_ACCESS_TOKEN" ]; then
    echo "⚠️ LINE_CHANNEL_ACCESS_TOKEN 未設置"
    echo "請設置您的 LINE Bot 訪問令牌:"
    echo "export LINE_CHANNEL_ACCESS_TOKEN='your_actual_token_here'"
    echo ""
    echo "💡 獲取方法:"
    echo "1. 前往 https://developers.line.biz/console/"
    echo "2. 登入您的 LINE 帳號"
    echo "3. 創建或選擇 Provider"
    echo "4. 創建 Messaging API Channel"
    echo "5. 在 Channel 設定中複製 'Channel access token'"
else
    echo "✅ LINE_CHANNEL_ACCESS_TOKEN 已設置"
fi

if [ -z "$LINE_CHANNEL_SECRET" ]; then
    echo "⚠️ LINE_CHANNEL_SECRET 未設置"
    echo "請設置您的 LINE Bot 密鑰:"
    echo "export LINE_CHANNEL_SECRET='your_actual_secret_here'"
    echo ""
    echo "💡 獲取方法:"
    echo "1. 在 LINE Developers Console 中"
    echo "2. 在 Channel 設定中複製 'Channel secret'"
else
    echo "✅ LINE_CHANNEL_SECRET 已設置"
fi

# 檢查 Facebook Messenger 環境變量 (可選)
if [ -z "$PAGE_ACCESS_TOKEN" ]; then
    echo "⚠️ PAGE_ACCESS_TOKEN 未設置 (Facebook Messenger 可選)"
    echo "如需使用 Facebook Messenger，請設置:"
    echo "export PAGE_ACCESS_TOKEN='your_actual_page_token_here'"
else
    echo "✅ PAGE_ACCESS_TOKEN 已設置"
fi

if [ -z "$VERIFY_TOKEN" ]; then
    echo "⚠️ VERIFY_TOKEN 未設置 (Facebook Messenger 可選)"
    echo "如需使用 Facebook Messenger，請設置:"
    echo "export VERIFY_TOKEN='your_actual_verify_token_here'"
else
    echo "✅ VERIFY_TOKEN 已設置"
fi

echo ""
echo "📋 當前環境變量狀態:"
echo "  SUPABASE_URL: $SUPABASE_URL"
echo "  SUPABASE_ANON_KEY: ${SUPABASE_ANON_KEY:0:20}..."
echo "  LINE_CHANNEL_ACCESS_TOKEN: ${LINE_CHANNEL_ACCESS_TOKEN:+已設置}"
echo "  LINE_CHANNEL_SECRET: ${LINE_CHANNEL_SECRET:+已設置}"
echo "  PAGE_ACCESS_TOKEN: ${PAGE_ACCESS_TOKEN:+已設置}"
echo "  VERIFY_TOKEN: ${VERIFY_TOKEN:+已設置}"

echo ""
echo "🧪 測試環境變量設置..."
python test_env_setup.py

echo ""
echo "💡 要永久設置環境變量，請將以下內容添加到 ~/.bashrc 或 ~/.zshrc:"
echo ""
echo "# 解剖問答機器人環境變量"
echo "export SUPABASE_URL=\"https://ciqlfqfgzqqgdrogedxg.supabase.co\""
echo "export SUPABASE_ANON_KEY=\"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA\""
echo "export LINE_CHANNEL_ACCESS_TOKEN=\"your_actual_token_here\""
echo "export LINE_CHANNEL_SECRET=\"your_actual_secret_here\""
echo "export PAGE_ACCESS_TOKEN=\"your_actual_page_token_here\""
echo "export VERIFY_TOKEN=\"your_actual_verify_token_here\""
echo ""
echo "然後執行: source ~/.bashrc  # 或 source ~/.zshrc"

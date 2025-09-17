#!/bin/bash
# 解剖問答機器人環境變量設置腳本

echo "🔧 設置解剖問答機器人環境變量..."

# 檢查是否已設置
if [ -n "$LINE_CHANNEL_ACCESS_TOKEN" ]; then
    echo "✅ LINE_CHANNEL_ACCESS_TOKEN 已設置"
else
    echo "⚠️ LINE_CHANNEL_ACCESS_TOKEN 未設置"
    echo "請設置 LINE_CHANNEL_ACCESS_TOKEN 環境變量"
    echo "例如: export LINE_CHANNEL_ACCESS_TOKEN='your_token_here'"
fi

if [ -n "$LINE_CHANNEL_SECRET" ]; then
    echo "✅ LINE_CHANNEL_SECRET 已設置"
else
    echo "⚠️ LINE_CHANNEL_SECRET 未設置"
    echo "請設置 LINE_CHANNEL_SECRET 環境變量"
    echo "例如: export LINE_CHANNEL_SECRET='your_secret_here'"
fi

if [ -n "$PAGE_ACCESS_TOKEN" ]; then
    echo "✅ PAGE_ACCESS_TOKEN 已設置"
else
    echo "⚠️ PAGE_ACCESS_TOKEN 未設置 (Facebook Messenger 可選)"
fi

# 設置 Supabase 環境變量 (如果未設置)
if [ -z "$SUPABASE_URL" ]; then
    export SUPABASE_URL="https://ciqlfqfgzqqgdrogedxg.supabase.co"
    echo "✅ 設置 SUPABASE_URL"
fi

if [ -z "$SUPABASE_ANON_KEY" ]; then
    export SUPABASE_ANON_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA"
    echo "✅ 設置 SUPABASE_ANON_KEY"
fi

echo ""
echo "📋 當前環境變量狀態:"
echo "  SUPABASE_URL: $SUPABASE_URL"
echo "  SUPABASE_ANON_KEY: ${SUPABASE_ANON_KEY:0:20}..."
echo "  LINE_CHANNEL_ACCESS_TOKEN: ${LINE_CHANNEL_ACCESS_TOKEN:+已設置}"
echo "  LINE_CHANNEL_SECRET: ${LINE_CHANNEL_SECRET:+已設置}"
echo "  PAGE_ACCESS_TOKEN: ${PAGE_ACCESS_TOKEN:+已設置}"

echo ""
echo "💡 要永久設置環境變量，請將以下內容添加到 ~/.bashrc 或 ~/.zshrc:"
echo "export LINE_CHANNEL_ACCESS_TOKEN='your_line_channel_access_token_here'"
echo "export LINE_CHANNEL_SECRET='your_line_channel_secret_here'"
echo "export PAGE_ACCESS_TOKEN='your_page_access_token_here'"
echo "export VERIFY_TOKEN='your_verify_token_here'"

#!/bin/bash
# 快速設置示例 - 請替換為您的實際憑證

echo "🚀 快速設置環境變量示例"
echo "請將以下命令中的 'your_actual_*' 替換為您的實際憑證"
echo ""

echo "# 1. 設置 Supabase (已包含)"
echo "export SUPABASE_URL=\"https://ciqlfqfgzqqgdrogedxg.supabase.co\""
echo "export SUPABASE_ANON_KEY=\"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA\""
echo ""

echo "# 2. 設置 LINE Bot (需要您提供)"
echo "export LINE_CHANNEL_ACCESS_TOKEN=\"your_actual_line_token_here\""
echo "export LINE_CHANNEL_SECRET=\"your_actual_line_secret_here\""
echo ""

echo "# 3. 設置 Facebook Messenger (可選)"
echo "export PAGE_ACCESS_TOKEN=\"your_actual_page_token_here\""
echo "export VERIFY_TOKEN=\"your_actual_verify_token_here\""
echo ""

echo "💡 設置完成後，運行以下命令測試:"
echo "python test_env_setup.py"
echo ""

echo "📋 獲取 LINE Bot 憑證的步驟:"
echo "1. 前往 https://developers.line.biz/console/"
echo "2. 登入您的 LINE 帳號"
echo "3. 創建或選擇 Provider"
echo "4. 創建 Messaging API Channel"
echo "5. 在 Channel 設定中複製:"
echo "   - Channel access token → LINE_CHANNEL_ACCESS_TOKEN"
echo "   - Channel secret → LINE_CHANNEL_SECRET"
echo ""

echo "🔧 如果您已經有 LINE Bot 憑證，請直接運行:"
echo "export LINE_CHANNEL_ACCESS_TOKEN=\"您的實際令牌\""
echo "export LINE_CHANNEL_SECRET=\"您的實際密鑰\""
echo "python test_env_setup.py"

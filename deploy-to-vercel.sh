#!/bin/bash

echo "🚀 解剖學測驗 - 快速部署到 Vercel"
echo "=================================="
echo ""

# 檢查是否安裝 vercel CLI
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI 未安裝"
    echo "📦 正在安裝 Vercel CLI..."
    npm install -g vercel
    
    if [ $? -ne 0 ]; then
        echo "❌ 安裝失敗，請手動安裝："
        echo "   npm install -g vercel"
        exit 1
    fi
    
    echo "✅ Vercel CLI 安裝成功！"
    echo ""
fi

echo "📁 準備部署文件..."
cd "$(dirname "$0")/public"

if [ ! -f "index.html" ]; then
    echo "❌ 找不到 index.html 文件"
    echo "   請確保在正確的目錄中運行此腳本"
    exit 1
fi

echo "✅ 文件檢查完成"
echo ""

echo "🔐 請先登入 Vercel（如果還沒登入）"
echo "   會在瀏覽器中打開登入頁面..."
vercel login

echo ""
echo "🚀 開始部署到 Vercel..."
echo "=================================="
echo ""

vercel --prod

if [ $? -eq 0 ]; then
    echo ""
    echo "=================================="
    echo "🎉 部署成功！"
    echo ""
    echo "你的遊戲已經上線了！"
    echo "可以通過 Vercel 提供的 URL 訪問"
    echo ""
    echo "📝 下一步："
    echo "1. 在瀏覽器中打開提供的 URL"
    echo "2. 測試遊戲功能"
    echo "3. 分享給你的朋友！"
    echo ""
    echo "💡 提示："
    echo "- 可以在 Vercel Dashboard 查看部署詳情"
    echo "- 每次更新後重新運行此腳本即可更新網站"
    echo ""
else
    echo ""
    echo "❌ 部署失敗"
    echo "請檢查錯誤信息並重試"
    echo ""
    echo "常見問題："
    echo "1. 網絡連接問題 - 檢查網絡"
    echo "2. 登入過期 - 運行 'vercel login'"
    echo "3. 權限問題 - 確保有足夠權限"
    echo ""
fi


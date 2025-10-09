#!/bin/bash

echo "🚀 解剖學測驗 - 快速部署到 Vercel"
echo "📌 強制從 Supabase 抓取題目（不使用緩存）"
echo "=========================================="
echo ""

# 切換到 public 目錄
cd "$(dirname "$0")/public"

if [ ! -f "index.html" ]; then
    echo "❌ 找不到 index.html"
    exit 1
fi

echo "✅ 找到遊戲文件"
echo "📁 準備部署以下文件："
echo "   - index.html"
echo "   - game.js (強制從 Supabase 抓取)"
echo "   - vercel.json"
echo ""

# 檢查是否有 vercel CLI
if command -v vercel &> /dev/null; then
    echo "✅ 找到 Vercel CLI"
    echo ""
    echo "🚀 開始部署..."
    echo "=========================================="
    vercel --prod
    
elif command -v npx &> /dev/null; then
    echo "✅ 找到 npx，將使用 npx vercel"
    echo ""
    echo "🚀 開始部署..."
    echo "=========================================="
    npx vercel --prod
    
else
    echo "❌ 未找到 Vercel CLI 或 npx"
    echo ""
    echo "請先安裝 Vercel CLI："
    echo "   npm install -g vercel"
    echo ""
    echo "或使用瀏覽器部署："
    echo "   1. 訪問 https://vercel.com"
    echo "   2. 拖放 public 文件夾"
    echo "   3. 完成部署！"
    exit 1
fi

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "🎉 部署成功！"
    echo ""
    echo "✅ 你的遊戲已上線"
    echo "✅ 強制從 Supabase 抓取題目"
    echo "✅ 全球 CDN 加速"
    echo ""
    echo "📝 重要提醒："
    echo "   - 確保 Supabase 題庫有題目"
    echo "   - 檢查 questions 表權限設置"
    echo "   - 測試遊戲功能是否正常"
    echo ""
else
    echo ""
    echo "❌ 部署失敗"
    echo "請查看上方錯誤信息"
    echo ""
fi


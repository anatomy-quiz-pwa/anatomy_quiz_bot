#!/bin/bash

# 🚀 Vercel 自動部署腳本

set -e

echo "🚀 開始 Vercel 部署..."

# 檢查是否安裝了 Vercel CLI
if ! command -v vercel &> /dev/null; then
    echo "📦 安裝 Vercel CLI..."
    npm install -g vercel
fi

# 檢查是否已登入
if ! vercel whoami &> /dev/null; then
    echo "🔐 請先登入 Vercel..."
    vercel login
fi

# 構建項目
echo "🔨 構建項目..."
npm run build

# 部署到 Vercel
echo "🚀 部署到 Vercel..."
vercel --prod

echo "✅ 部署完成！"
echo "�� 您的 admin 面板已經上線！"


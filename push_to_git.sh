#!/bin/bash
set -e

echo "=== Git 推送腳本 ==="

# 檢查是否提供了倉庫 URL
if [ -z "$1" ]; then
    echo "❌ 請提供 Git 倉庫 URL"
    echo "用法: ./push_to_git.sh <倉庫URL>"
    echo "例如: ./push_to_git.sh https://github.com/username/anatomy_quiz_bot.git"
    exit 1
fi

REPO_URL="$1"

echo "🔗 設置遠端倉庫: $REPO_URL"
git remote add origin "$REPO_URL" 2>/dev/null || {
    echo "ℹ️  遠端倉庫已存在，更新 URL"
    git remote set-url origin "$REPO_URL"
}

echo "📤 推送到遠端倉庫..."
git push -u origin main

echo "✅ 推送完成！"
echo "🌐 你現在可以在 Render 使用 Blueprint 部署了"

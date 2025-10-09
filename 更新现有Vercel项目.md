# 🔄 更新现有 Vercel 项目

## 📊 当前状态

- **现有项目**: anatomy-quiz-bot
- **URL**: https://anatomy-quiz-bot.vercel.app
- **状态**: 404 错误（需要更新）
- **环境变量**: 已设置好

## 🎯 解决方案

### 方法一：通过 Vercel Dashboard 重新部署

1. **访问你的 Vercel Dashboard**
   ```
   https://vercel.com/dashboard
   ```

2. **找到 "anatomy-quiz-bot" 项目**
   - 点击项目名称

3. **重新部署**
   - 点击 "Deployments" 标签
   - 点击 "Redeploy" 或 "Deploy"
   - 或者点击 "Settings" → "Git" → "Redeploy"

### 方法二：推送新代码到 GitHub

如果项目连接到 GitHub：

```bash
# 1. 确保在正确的目录
cd "/Users/baobaoc/Downloads/anatomy_quiz_bot 2/anatomy_quiz_bot"

# 2. 添加新文件到 Git
git add public/
git commit -m "添加游戏化问答系统 - 强制从 Supabase 抓取"

# 3. 推送到 GitHub（会自动触发 Vercel 部署）
git push origin main
```

### 方法三：直接更新项目设置

在 Vercel Dashboard：

1. **进入项目设置**
   - 点击 "anatomy-quiz-bot" 项目
   - 点击 "Settings"

2. **修改构建设置**
   - 点击 "General"
   - **Root Directory**: 改为 `public`
   - **Build Command**: 留空
   - **Output Directory**: 改为 `.`

3. **重新部署**
   - 点击 "Deployments"
   - 点击 "Redeploy"

## 🔧 环境变量检查

确保以下环境变量已设置：

### Supabase 设置
```
SUPABASE_URL=https://ciqlfqfgzqqgdrogedxg.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 其他设置（如果需要）
```
LINE_CHANNEL_ACCESS_TOKEN=你的token
LINE_CHANNEL_SECRET=你的secret
FLASK_SECRET_KEY=你的secret
```

## 🎮 测试部署

部署完成后：

1. **访问**: https://anatomy-quiz-bot.vercel.app
2. **测试游戏功能**
3. **检查控制台日志**（F12）

成功的话应该看到：
```
🔄 正在從 Supabase 載入題目...
✅ 成功從 Supabase 載入 XX 道題目
```

## 📋 部署检查清单

- [ ] 访问 Vercel Dashboard
- [ ] 找到 anatomy-quiz-bot 项目
- [ ] 检查 Root Directory 设置为 `public`
- [ ] 重新部署项目
- [ ] 测试 https://anatomy-quiz-bot.vercel.app
- [ ] 确认游戏能加载题目
- [ ] 检查环境变量是否正确

## 🐛 如果还是 404

可能的原因：
1. **Root Directory 设置错误** - 应该设为 `public`
2. **缺少 index.html** - 确保 `public/index.html` 存在
3. **构建失败** - 检查部署日志

## 📞 需要帮助？

告诉我你看到的具体情况，我会帮你解决！

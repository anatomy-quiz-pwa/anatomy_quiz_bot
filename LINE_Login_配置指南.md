# LINE Login 配置指南

## 🎯 概述

本指南将帮助您配置 LINE Login 功能，让用户可以使用 LINE 账号登录游戏。

## 📋 配置步骤

### 1. 创建 LINE Login Channel

1. 访问 [LINE Developers Console](https://developers.line.biz/console/)
2. 登录您的 LINE 开发者账号
3. 点击 "Create" 创建新的 Provider
4. 选择 "LINE Login" 创建新的 Channel
5. 填写 Channel 信息：
   - **Channel name**: `解剖學問答遊戲`
   - **Channel description**: `醫學學習遊戲平台`
   - **App types**: 选择 `Web app`

### 2. 配置 Callback URL

在 Channel 设置中，添加以下 Callback URL：
```
https://anatomy-quiz-bot.vercel.app
```

### 3. 获取 Channel ID

在 Channel 的 "Basic settings" 页面，复制 **Channel ID**。

### 4. 更新代码配置

在 `public/game.js` 文件中，找到以下行：
```javascript
const channelId = 'YOUR_CHANNEL_ID'; // 需要替换为实际的 Channel ID
```

将 `YOUR_CHANNEL_ID` 替换为您在第3步获取的 Channel ID。

### 5. 配置环境变量（可选）

如果您想使用环境变量，可以在 Vercel 项目设置中添加：
- `LINE_CHANNEL_ID`: 您的 LINE Channel ID

然后更新代码：
```javascript
const channelId = process.env.LINE_CHANNEL_ID || 'YOUR_CHANNEL_ID';
```

## 🔧 功能说明

### 登录流程

1. 用户点击 "使用 LINE 登入" 按钮
2. 跳转到 LINE 登录页面
3. 用户授权后，LINE 重定向回游戏页面
4. 游戏获取用户信息并保存到 Supabase
5. 显示用户信息并允许开始游戏

### 用户信息存储

用户信息会保存到 Supabase 的 `users` 表中，包含：
- `user_id`: LINE 用户 ID
- `nickname`: LINE 显示名称
- `line_id`: LINE 用户 ID（与 user_id 相同）
- `last_login`: 最后登录时间
- `created_at`: 创建时间

### 备用登录方式

如果 LINE 登录失败，用户仍可以使用手动输入昵称的方式登录。

## 🚀 部署说明

1. 确保已配置正确的 Channel ID
2. 确保 Callback URL 指向正确的域名
3. 推送代码到 GitHub
4. Vercel 会自动部署更新

## 🔍 测试步骤

1. 访问游戏网站
2. 点击 "使用 LINE 登入" 按钮
3. 在 LINE 登录页面输入账号密码
4. 授权后应该重定向回游戏页面
5. 检查是否显示用户信息
6. 点击 "開始遊戲" 开始游戏

## ⚠️ 注意事项

1. **Channel ID 保密**: 不要将 Channel ID 提交到公开的代码仓库
2. **HTTPS 要求**: LINE Login 要求使用 HTTPS
3. **域名匹配**: Callback URL 必须与部署域名完全匹配
4. **测试环境**: 建议先在测试环境验证功能

## 🛠️ 故障排除

### 常见问题

1. **登录失败**: 检查 Channel ID 和 Callback URL 是否正确
2. **重定向错误**: 确保域名配置正确
3. **用户信息获取失败**: 检查权限设置

### 调试方法

1. 打开浏览器开发者工具
2. 查看 Console 日志
3. 检查 Network 请求
4. 验证 Supabase 连接

## 📞 技术支持

如果遇到问题，请检查：
1. LINE Developers Console 配置
2. Vercel 部署状态
3. Supabase 连接状态
4. 浏览器控制台错误信息

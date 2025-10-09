# LINE Login 真实配置指南

## 🎯 基于现有 LINE Bot 配置

根据项目中的真实配置信息，我们已经找到了以下关键信息：

### 📋 现有配置信息

- **LINE Bot Webhook URL**: `https://anatomy-quiz-bot.onrender.com/webhook`
- **LINE Login Channel ID**: `2004874394`
- **部署域名**: `anatomy-quiz-bot.onrender.com`

## 🔧 LINE Developers Console 配置

### 1. 访问 LINE Developers Console

1. 打开 [LINE Developers Console](https://developers.line.biz/console/)
2. 登录您的 LINE 开发者账号
3. 找到 Channel ID `2004874394` 对应的 LINE Login Channel

### 2. 配置回调 URL

在 Channel 的 "LINE Login" 设置页面：

1. 找到 "Callback URL" 设置
2. 添加以下回调 URL：
   ```
   https://anatomy-quiz-bot.onrender.com/auth/callback
   ```
3. 点击 "Save" 保存设置

### 3. 验证现有配置

确保以下设置正确：

- **Channel ID**: `2004874394` ✅
- **Callback URL**: `https://anatomy-quiz-bot.onrender.com/auth/callback` ⏳ (需要添加)
- **Scope**: `profile`, `openid` ✅
- **Webhook URL**: `https://anatomy-quiz-bot.onrender.com/webhook` ✅ (已存在)

## 🚀 部署说明

### 当前部署状态

- **Vercel 游戏网站**: `https://anatomy-quiz-bot.vercel.app`
- **Render LINE Bot**: `https://anatomy-quiz-bot.onrender.com`
- **LINE Login 回调**: 需要指向 Render 服务器

### 为什么使用 Render 作为回调？

1. **现有基础设施**: LINE Bot 已经在 Render 上运行
2. **统一管理**: 所有 LINE 相关功能都在同一个服务器
3. **已验证配置**: Render 服务器已经通过 LINE 验证

## 📋 配置检查清单

- [ ] LINE Login Channel ID: `2004874394` ✅
- [ ] 添加 Callback URL: `https://anatomy-quiz-bot.onrender.com/auth/callback` ⏳
- [ ] 权限范围: `profile`, `openid` ✅
- [ ] Render 服务器运行正常 ✅
- [ ] Vercel 游戏网站运行正常 ✅

## 🧪 测试流程

### 1. 配置完成后测试

1. 访问游戏网站：https://anatomy-quiz-bot.vercel.app
2. 点击 "使用 LINE 登入" 按钮
3. 应该跳转到 LINE 登录页面（不再出现 400 错误）
4. 输入 LINE 账号密码
5. 授权后重定向到 Render 服务器处理
6. 最终重定向回 Vercel 游戏页面显示用户信息

### 2. 预期结果

- ✅ LINE 登录页面正常显示
- ✅ 用户授权后正常回调
- ✅ 用户信息正确显示
- ✅ 游戏功能正常启动

## 🔍 故障排除

### 如果仍然出现 400 错误：

1. **检查回调 URL 格式**
   - 确保完全匹配：`https://anatomy-quiz-bot.onrender.com/auth/callback`
   - 注意大小写和斜杠

2. **检查 Render 服务器状态**
   - 访问：https://anatomy-quiz-bot.onrender.com
   - 确保服务器正常运行

3. **检查 LINE Console 配置**
   - 确认回调 URL 已保存
   - 检查 Channel 状态是否为 "Active"

## 📞 技术支持

如果问题仍然存在，请提供：

1. LINE Developers Console 配置截图
2. 浏览器控制台错误信息
3. Render 服务器日志
4. Vercel 部署状态

## 🎯 配置完成后

配置完成后，LINE Login 功能将：

1. ✅ 使用真实的 LINE 用户信息
2. ✅ 与现有 LINE Bot 数据兼容
3. ✅ 支持用户数据同步
4. ✅ 提供完整的游戏体验

---

**重要提醒**: 确保在 LINE Developers Console 中添加回调 URL `https://anatomy-quiz-bot.onrender.com/auth/callback` 后，LINE Login 功能才能正常工作。

# LINE Login 回调 URL 配置指南

## 🚨 当前问题

LINE Login 出现 `Invalid redirect_uri` 错误，需要在 LINE Developers Console 中配置正确的回调 URL。

## 🔧 解决步骤

### 1. 访问 LINE Developers Console

1. 打开 [LINE Developers Console](https://developers.line.biz/console/)
2. 登录您的 LINE 开发者账号
3. 找到 Channel ID `2004874394` 对应的 LINE Login Channel

### 2. 配置回调 URL

在 Channel 的 "LINE Login" 设置页面：

1. 找到 "Callback URL" 设置
2. 添加以下回调 URL：
   ```
   https://anatomy-quiz-bot.vercel.app/auth/callback
   ```
3. 点击 "Save" 保存设置

### 3. 验证配置

确保以下设置正确：

- **Channel ID**: `2004874394`
- **Callback URL**: `https://anatomy-quiz-bot.vercel.app/auth/callback`
- **Scope**: `profile`, `openid`

## 📋 配置检查清单

- [ ] LINE Login Channel 已创建
- [ ] Channel ID 为 `2004874394`
- [ ] 回调 URL 已添加：`https://anatomy-quiz-bot.vercel.app/auth/callback`
- [ ] 权限范围包含 `profile` 和 `openid`
- [ ] 设置已保存

## 🧪 测试步骤

1. 访问游戏网站：https://anatomy-quiz-bot.vercel.app
2. 点击 "使用 LINE 登入" 按钮
3. 应该跳转到 LINE 登录页面（不再出现 400 错误）
4. 输入 LINE 账号密码
5. 授权后应该重定向回游戏页面

## 🔍 故障排除

### 如果仍然出现 400 错误：

1. **检查回调 URL 格式**
   - 确保 URL 完全匹配：`https://anatomy-quiz-bot.vercel.app/auth/callback`
   - 注意大小写和斜杠

2. **检查 Channel 状态**
   - 确保 Channel 处于 "Active" 状态
   - 检查是否有任何限制或暂停

3. **清除浏览器缓存**
   - 清除浏览器缓存和 cookies
   - 尝试无痕模式

4. **检查域名**
   - 确保 `anatomy-quiz-bot.vercel.app` 是正确的域名
   - 如果域名有变化，需要更新回调 URL

## 📞 技术支持

如果问题仍然存在，请检查：

1. LINE Developers Console 中的配置截图
2. 浏览器控制台的错误信息
3. Vercel 部署日志

## 🎯 预期结果

配置完成后，LINE Login 流程应该：

1. ✅ 点击登录按钮跳转到 LINE 登录页面
2. ✅ 输入账号密码后正常授权
3. ✅ 重定向回游戏页面并显示用户信息
4. ✅ 可以正常开始游戏

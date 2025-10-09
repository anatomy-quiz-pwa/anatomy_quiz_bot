# 🔧 解决 Supabase 题目加载问题

## 🔍 问题分析

错误信息：**"載入題目時發生錯誤!請重新整理頁面或聯繫管理員。"**

可能原因：
1. Supabase 的 `questions` 表为空
2. Supabase 连接配置错误
3. 权限设置问题

## 🎯 解决步骤

### 步骤 1：检查 Supabase 题目

1. **访问 Supabase Dashboard**
   ```
   https://supabase.com/dashboard
   ```

2. **选择你的项目**
   - 项目名：ciqlfqfgzqqgdrogedxg

3. **进入 Table Editor**
   - 点击左侧 "Table Editor"
   - 找到 `questions` 表

4. **检查是否有题目**
   - 如果表为空，需要添加题目
   - 如果有题目，检查格式是否正确

### 步骤 2：添加题目（如果表为空）

在 Supabase SQL Editor 中执行：

```sql
-- 创建 questions 表（如果不存在）
CREATE TABLE IF NOT EXISTS questions (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    options JSONB NOT NULL,
    correct_answer INTEGER NOT NULL,
    explanation TEXT,
    level INTEGER NOT NULL CHECK (level BETWEEN 1 AND 14),
    category TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 添加示例题目
INSERT INTO questions (question, options, correct_answer, explanation, level, category)
VALUES 
('心臟的主要功能是什麼？', 
 '["輸送血液", "過濾血液", "儲存血液", "製造血液"]', 
 0, 
 '心臟是循環系統的核心，主要功能是泵血輸送到全身各個器官和組織。', 
 1, 
 '循環系統'),

('人體最大的器官是什麼？', 
 '["心臟", "肝臟", "皮膚", "肺"]', 
 2, 
 '皮膚是人體最大的器官，覆蓋整個身體表面，具有保護、調節體溫等功能。', 
 1, 
 '器官系統'),

('心臟有幾個腔室？', 
 '["2個", "3個", "4個", "5個"]', 
 2, 
 '心臟有4個腔室：左心房、左心室、右心房、右心室。左側負責體循環，右側負責肺循環。', 
 2, 
 '循環系統'),

('人體有多少塊骨頭？', 
 '["186塊", "206塊", "226塊", "246塊"]', 
 1, 
 '成年人體有206塊骨頭，嬰兒出生時約有270塊，隨著生長部分骨頭會融合。', 
 2, 
 '骨骼系統'),

('大腦的主要能量來源是？', 
 '["蛋白質", "脂肪", "葡萄糖", "氧氣"]', 
 2, 
 '大腦主要使用葡萄糖作為能量來源，約消耗人體20%的能量。', 
 3, 
 '神經系統'),

('肝臟位於人體的哪個位置？', 
 '["左上腹", "右上腹", "左下腹", "右下腹"]', 
 1, 
 '肝臟位於右上腹，是人體最大的內臟器官，具有代謝、解毒等多種功能。', 
 3, 
 '消化系統'),

('肺的主要功能是什麼？', 
 '["消化食物", "過濾血液", "氣體交換", "製造血液"]', 
 2, 
 '肺的主要功能是進行氣體交換，吸入氧氣，排出二氧化碳。', 
 4, 
 '呼吸系統'),

('腎臟的主要功能是什麼？', 
 '["過濾血液", "製造血液", "消化食物", "調節體溫"]', 
 0, 
 '腎臟的主要功能是過濾血液，排除廢物和多餘的水分，形成尿液。', 
 4, 
 '泌尿系統'),

('胃的主要功能是什麼？', 
 '["過濾血液", "消化食物", "製造血液", "氣體交換"]', 
 1, 
 '胃的主要功能是初步消化食物，分泌胃酸和消化酶。', 
 5, 
 '消化系統'),

('小腸的主要功能是什麼？', 
 '["過濾血液", "吸收營養", "製造血液", "氣體交換"]', 
 1, 
 '小腸的主要功能是吸收營養物質，是消化系統中最重要的吸收器官。', 
 5, 
 '消化系統');

-- 檢查插入結果
SELECT count(*) FROM questions;
SELECT level, count(*) FROM questions GROUP BY level ORDER BY level;
```

### 步骤 3：设置权限

在 Supabase Dashboard：

1. **进入 Authentication → Policies**
2. **为 `questions` 表添加政策**：

```sql
-- 允许所有人读取题目
CREATE POLICY "Enable read access for all users" 
ON questions 
FOR SELECT 
USING (true);
```

### 步骤 4：测试连接

1. **刷新游戏页面**
2. **打开浏览器控制台 (F12)**
3. **查看 Console 标签**
4. **应该看到**：
   ```
   🔄 正在從 Supabase 載入題目...
   ✅ 成功從 Supabase 載入 XX 道題目
   ```

## 🐛 如果还是有问题

### 检查 Supabase 配置

在 `public/game.js` 中确认：

```javascript
const SUPABASE_URL = 'https://ciqlfqfgzqqgdrogedxg.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA';
```

### 检查网络连接

在浏览器控制台执行：

```javascript
// 测试 Supabase 连接
console.log('Testing Supabase connection...');
```

## 📞 需要帮助？

完成上述步骤后，告诉我：
1. Supabase 的 `questions` 表有多少题目？
2. 权限设置是否正确？
3. 刷新页面后还显示错误吗？

我会继续帮你解决！

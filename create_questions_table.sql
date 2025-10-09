-- 創建 questions 表格
-- 請在 Supabase SQL Editor 中執行

CREATE TABLE IF NOT EXISTS public.questions (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    options JSONB NOT NULL,
    correct_answer INTEGER NOT NULL,
    explanation TEXT DEFAULT '',
    level INTEGER NOT NULL DEFAULT 1,
    category VARCHAR(100) DEFAULT '',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 創建索引
CREATE INDEX IF NOT EXISTS idx_questions_level ON public.questions(level);
CREATE INDEX IF NOT EXISTS idx_questions_category ON public.questions(category);

-- 插入示例題目
INSERT INTO public.questions (question, options, correct_answer, explanation, level, category) VALUES
(
    '心臟的主要功能是什麼？',
    '["輸送血液", "過濾血液", "儲存血液", "製造血液"]',
    0,
    '心臟是循環系統的核心，主要功能是泵血輸送到全身。',
    1,
    '循環系統'
),
(
    '人體最大的器官是什麼？',
    '["心臟", "肝臟", "皮膚", "肺"]',
    2,
    '皮膚是人體最大的器官，覆蓋整個身體表面。',
    1,
    '器官系統'
),
(
    '心臟有幾個腔室？',
    '["2個", "3個", "4個", "5個"]',
    2,
    '心臟有4個腔室：左心房、左心室、右心房、右心室。',
    2,
    '循環系統'
),
(
    '肺的主要功能是什麼？',
    '["消化食物", "過濾血液", "氣體交換", "儲存能量"]',
    2,
    '肺的主要功能是進行氣體交換，吸入氧氣，呼出二氧化碳。',
    2,
    '呼吸系統'
),
(
    '肝臟的主要功能是什麼？',
    '["呼吸", "消化", "代謝和解毒", "循環"]',
    2,
    '肝臟是重要的代謝器官，負責解毒、代謝和儲存等功能。',
    3,
    '消化系統'
),
(
    '腎臟的主要功能是什麼？',
    '["呼吸", "消化", "過濾血液和排泄", "循環"]',
    2,
    '腎臟負責過濾血液中的廢物和多餘水分，形成尿液排出體外。',
    3,
    '泌尿系統'
),
(
    '大腦的主要組成部分不包括？',
    '["大腦皮質", "小腦", "肝臟", "腦幹"]',
    2,
    '肝臟不是大腦的組成部分，而是消化系統的器官。',
    4,
    '神經系統'
),
(
    '骨骼系統的主要功能是什麼？',
    '["呼吸", "支持身體和保護器官", "消化", "循環"]',
    1,
    '骨骼系統提供身體結構支持，保護內部器官，並協助運動。',
    4,
    '骨骼系統'
),
(
    '肌肉系統中，心肌的特點是什麼？',
    '["可以隨意控制", "不疲勞", "有橫紋", "以上都是"]',
    2,
    '心肌是有橫紋的不隨意肌，具有不疲勞的特點。',
    5,
    '肌肉系統'
),
(
    '消化系統中，胃的主要功能是？',
    '["吸收營養", "機械性消化和初步化學消化", "製造膽汁", "過濾血液"]',
    1,
    '胃主要進行機械性消化和初步的化學消化，為後續吸收做準備。',
    5,
    '消化系統'
);

-- 確認表格創建成功
SELECT 'questions表格創建成功' as status;

-- 查看插入的題目
SELECT id, question, level, category FROM public.questions ORDER BY level, id;


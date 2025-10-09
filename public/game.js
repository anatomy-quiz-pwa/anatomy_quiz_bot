// Supabase 配置
const SUPABASE_URL = 'https://ciqlfqfgzqqgdrogedxg.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA';

// 初始化 Supabase 客戶端
const supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// 等級稱號對應
const LEVEL_TITLES = {
    1: "新手解剖師",
    2: "初級解剖師", 3: "初級解剖師",
    4: "中級解剖師", 5: "中級解剖師", 6: "中級解剖師", 7: "中級解剖師",
    8: "高級解剖師", 9: "高級解剖師", 10: "高級解剖師", 11: "高級解剖師",
    12: "專家解剖師", 13: "專家解剖師",
    14: "終極解剖師"
};

// 遊戲狀態
let gameState = {
    userId: null,
    nickname: '遊客',
    currentLevel: 1,
    score: 0,
    correctAnswers: 0,
    totalAnswers: 0,
    streak: 0,
    currentQuestion: null,
    selectedAnswer: null,
    allQuestions: [],
    usedQuestionIds: []
};

// 開始遊戲
async function startGame() {
    const nicknameInput = document.getElementById('nickname-input');
    const nickname = nicknameInput.value.trim() || '遊客';
    gameState.nickname = nickname;
    
    // 生成臨時用戶 ID
    gameState.userId = 'web_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    
    // 隱藏開始畫面，顯示載入中
    document.getElementById('start-screen').style.display = 'none';
    document.getElementById('loading-screen').style.display = 'block';
    
    try {
        // 載入題目（強制從 Supabase）
        await loadQuestions();
        
        // 顯示統計欄和遊戲畫面
        document.getElementById('stats-bar').style.display = 'flex';
        document.getElementById('loading-screen').style.display = 'none';
        document.getElementById('game-screen').style.display = 'block';
        
        // 更新統計
        updateStats();
        
        // 載入第一題
        await nextQuestion();
        
    } catch (error) {
        // 載入失敗，返回開始畫面
        console.error('❌ 遊戲啟動失敗:', error);
        document.getElementById('loading-screen').style.display = 'none';
        document.getElementById('start-screen').style.display = 'block';
    }
}

// 載入題目（強制從 Supabase 抓取）
async function loadQuestions() {
    try {
        console.log('🔄 正在從 Supabase 載入題目...');
        
        const { data, error } = await supabase
            .from('anatomy_questions_v2')
            .select('*')
            .order('level', { ascending: true });
        
        if (error) {
            console.error('❌ 載入題目失敗:', error);
            alert('無法連接到題庫！請檢查網路連接或聯繫管理員。\n錯誤: ' + error.message);
            throw new Error('無法載入題目');
        }
        
        if (!data || data.length === 0) {
            console.error('❌ 題庫為空');
            alert('題庫目前沒有題目！請聯繫管理員添加題目。');
            throw new Error('題庫為空');
        }
        
        // 轉換數據格式以符合遊戲系統
        const convertedQuestions = data.map(item => ({
            id: item.id,
            question: item.question,
            options: [
                item.option_1 || '',
                item.option_2 || '',
                item.option_3 || '',
                item.option_4 || ''
            ].filter(opt => opt.trim() !== ''), // 過濾空選項
            correct_answer: (item.correct_option || 1) - 1, // 轉換為 0-based 索引
            explanation: item.explanation || '',
            level: item.level || 1,
            category: item.category || '解剖學',
            image_url: item.image_url || '',
            qimage_url: item.qimage_url || ''
        }));
        
        gameState.allQuestions = convertedQuestions;
        console.log(`✅ 成功從 Supabase 載入 ${convertedQuestions.length} 道題目`);
        console.log('📊 題目分佈:', getQuestionDistribution(convertedQuestions));
        console.log('🔍 示例題目:', convertedQuestions[0]);
        
    } catch (err) {
        console.error('❌ 載入題目錯誤:', err);
        // 不使用預設題目，直接報錯
        alert('載入題目時發生錯誤！請重新整理頁面或聯繫管理員。');
        throw err;
    }
}

// 獲取題目分佈統計
function getQuestionDistribution(questions) {
    const distribution = {};
    questions.forEach(q => {
        distribution[q.level] = (distribution[q.level] || 0) + 1;
    });
    return distribution;
}

// 注意：本系統不使用預設題目，所有題目必須從 Supabase 即時獲取
// 這確保了題庫的即時性和準確性

// 載入下一題
async function nextQuestion() {
    // 隱藏上一題的結果
    document.getElementById('explanation-area').style.display = 'none';
    document.getElementById('submit-btn').style.display = 'inline-block';
    document.getElementById('next-btn').style.display = 'none';
    document.getElementById('submit-btn').disabled = true;
    
    // 重置選擇
    gameState.selectedAnswer = null;
    
    // 獲取當前等級的題目
    const availableQuestions = gameState.allQuestions.filter(q => 
        q.level === gameState.currentLevel && 
        !gameState.usedQuestionIds.includes(q.id)
    );
    
    // 如果當前等級沒有題目了，嘗試其他等級
    if (availableQuestions.length === 0) {
        const allAvailable = gameState.allQuestions.filter(q => 
            !gameState.usedQuestionIds.includes(q.id)
        );
        
        if (allAvailable.length === 0) {
            // 所有題目都答過了，重置已使用題目
            gameState.usedQuestionIds = [];
            return nextQuestion();
        }
        
        // 隨機選擇一題
        gameState.currentQuestion = allAvailable[Math.floor(Math.random() * allAvailable.length)];
    } else {
        // 從當前等級隨機選擇一題
        gameState.currentQuestion = availableQuestions[Math.floor(Math.random() * availableQuestions.length)];
    }
    
    // 標記為已使用
    gameState.usedQuestionIds.push(gameState.currentQuestion.id);
    
    // 顯示題目
    displayQuestion();
    
    // 更新進度條
    updateProgress();
}

// 顯示題目
function displayQuestion() {
    const question = gameState.currentQuestion;
    
    document.getElementById('question-level').textContent = 
        `等級 ${question.level} - ${LEVEL_TITLES[question.level]}`;
    document.getElementById('question-category').textContent = question.category;
    document.getElementById('question-text').textContent = question.question;
    
    // 顯示題目圖片（如果有）
    const questionCard = document.querySelector('.question-card .card-body');
    let imageHtml = '';
    
    if (question.qimage_url) {
        imageHtml = `
            <div class="question-image mb-3">
                <img src="${question.qimage_url}" 
                     alt="題目圖片" 
                     class="img-fluid rounded"
                     style="max-width: 100%; height: auto; max-height: 300px;"
                     onerror="this.style.display='none'">
            </div>
        `;
    }
    
    // 插入圖片到題目文字後面
    const questionTextElement = document.getElementById('question-text');
    questionTextElement.insertAdjacentHTML('afterend', imageHtml);
    
    // 顯示選項
    const optionsContainer = document.getElementById('options-container');
    optionsContainer.innerHTML = '';
    
    question.options.forEach((option, index) => {
        const button = document.createElement('button');
        button.className = 'option-btn';
        button.textContent = `${String.fromCharCode(65 + index)}. ${option}`;
        button.onclick = () => selectAnswer(index);
        button.id = `option-${index}`;
        optionsContainer.appendChild(button);
    });
}

// 選擇答案
function selectAnswer(index) {
    // 移除所有選中狀態
    document.querySelectorAll('.option-btn').forEach(btn => {
        btn.classList.remove('selected');
    });
    
    // 添加選中狀態
    document.getElementById(`option-${index}`).classList.add('selected');
    gameState.selectedAnswer = index;
    
    // 啟用提交按鈕
    document.getElementById('submit-btn').disabled = false;
}

// 提交答案
async function submitAnswer() {
    if (gameState.selectedAnswer === null) return;
    
    const question = gameState.currentQuestion;
    const isCorrect = gameState.selectedAnswer === question.correct_answer;
    
    // 禁用所有選項
    document.querySelectorAll('.option-btn').forEach(btn => {
        btn.disabled = true;
    });
    
    // 顯示正確/錯誤狀態
    document.querySelectorAll('.option-btn').forEach((btn, index) => {
        if (index === question.correct_answer) {
            btn.classList.add('correct');
        } else if (index === gameState.selectedAnswer && !isCorrect) {
            btn.classList.add('wrong');
        }
    });
    
    // 更新統計
    gameState.totalAnswers++;
    if (isCorrect) {
        gameState.correctAnswers++;
        gameState.score += 10;
        gameState.streak++;
        
        // 檢查是否升級（每5題正確答案升一級）
        if (gameState.correctAnswers % 5 === 0 && gameState.currentLevel < 14) {
            gameState.currentLevel++;
            showLevelUpAnimation();
        }
    } else {
        gameState.streak = 0;
    }
    
    updateStats();
    
    // 顯示解釋
    if (question.explanation) {
        document.getElementById('explanation-text').textContent = question.explanation;
        document.getElementById('explanation-area').style.display = 'block';
    }
    
    // 顯示答案圖片（如果有）
    if (question.image_url) {
        const explanationArea = document.getElementById('explanation-area');
        const imageHtml = `
            <div class="answer-image mt-3">
                <h5 class="mb-3"><i class="fas fa-image text-info"></i> 答案圖片：</h5>
                <img src="${question.image_url}" 
                     alt="答案圖片" 
                     class="img-fluid rounded"
                     style="max-width: 100%; height: auto; max-height: 400px;"
                     onerror="this.style.display='none'">
            </div>
        `;
        explanationArea.insertAdjacentHTML('beforeend', imageHtml);
    }
    
    // 顯示結果動畫
    showResultAnimation(isCorrect);
    
    // 隱藏提交按鈕，顯示下一題按鈕
    document.getElementById('submit-btn').style.display = 'none';
    document.getElementById('next-btn').style.display = 'inline-block';
    
    // 保存到資料庫（可選）
    await saveProgress();
}

// 顯示結果動畫
function showResultAnimation(isCorrect) {
    const modal = document.getElementById('result-modal');
    const icon = document.getElementById('result-icon');
    const title = document.getElementById('result-title');
    const message = document.getElementById('result-message');
    
    if (isCorrect) {
        icon.innerHTML = '<i class="fas fa-check-circle fa-5x text-success"></i>';
        title.textContent = '答對了！🎉';
        title.className = 'text-success';
        message.textContent = '太棒了！你答對了這道題！';
    } else {
        icon.innerHTML = '<i class="fas fa-times-circle fa-5x text-danger"></i>';
        title.textContent = '答錯了 😢';
        title.className = 'text-danger';
        message.textContent = '別灰心，繼續加油！';
    }
    
    modal.style.display = 'flex';
    
    setTimeout(() => {
        modal.style.display = 'none';
    }, 1500);
}

// 顯示升級動畫
function showLevelUpAnimation() {
    const modal = document.getElementById('result-modal');
    const icon = document.getElementById('result-icon');
    const title = document.getElementById('result-title');
    const message = document.getElementById('result-message');
    const stats = document.getElementById('result-stats');
    
    icon.innerHTML = '<i class="fas fa-trophy fa-5x text-warning"></i>';
    title.textContent = '恭喜升級！🎊';
    title.className = 'text-warning';
    message.textContent = `你已晉升為 ${LEVEL_TITLES[gameState.currentLevel]}！`;
    stats.innerHTML = `<h3 class="mt-3">等級 ${gameState.currentLevel}</h3>`;
    
    modal.style.display = 'flex';
    
    setTimeout(() => {
        modal.style.display = 'none';
        stats.innerHTML = '';
    }, 2500);
}

// 更新統計
function updateStats() {
    document.getElementById('stat-score').textContent = gameState.score;
    document.getElementById('stat-level').textContent = gameState.currentLevel;
    
    const accuracy = gameState.totalAnswers > 0 
        ? Math.round((gameState.correctAnswers / gameState.totalAnswers) * 100)
        : 0;
    document.getElementById('stat-correct').textContent = 
        `${gameState.correctAnswers}/${gameState.totalAnswers} (${accuracy}%)`;
    
    document.getElementById('stat-streak').textContent = gameState.streak;
}

// 更新進度條
function updateProgress() {
    const progress = gameState.totalAnswers > 0 
        ? Math.min((gameState.correctAnswers / (gameState.currentLevel * 5)) * 100, 100)
        : 0;
    
    document.getElementById('progress-bar').style.width = `${progress}%`;
    document.getElementById('progress-text').textContent = `${Math.round(progress)}%`;
}

// 保存進度到資料庫
async function saveProgress() {
    try {
        const { data, error } = await supabase
            .from('web_game_stats')
            .upsert({
                user_id: gameState.userId,
                nickname: gameState.nickname,
                level: gameState.currentLevel,
                score: gameState.score,
                correct: gameState.correctAnswers,
                total: gameState.totalAnswers,
                streak: gameState.streak,
                last_played: new Date().toISOString()
            }, {
                onConflict: 'user_id'
            });
        
        if (error) {
            console.log('保存進度失敗（資料庫可能未設置）:', error.message);
        } else {
            console.log('✅ 進度已保存');
        }
    } catch (err) {
        console.log('保存進度錯誤:', err);
    }
}

// 頁面載入完成
document.addEventListener('DOMContentLoaded', () => {
    console.log('🎮 解剖學測驗遊戲已就緒！');
    console.log('✅ Supabase 連接已建立');
});


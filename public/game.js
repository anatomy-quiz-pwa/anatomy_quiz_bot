// Supabase 配置
const SUPABASE_URL = 'https://ciqlfqfgzqqgdrogedxg.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA';

// 初始化 Supabase 客戶端
const supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// 等級稱號對應（與 LINE Bot 保持一致）
const LEVEL_TITLES = {
    1: "解剖新手村",
    2: "胚體學長",
    3: "肌肉拆解師",
    4: "神經探路員",
    5: "解剖影武者",
    6: "組織細胞使者",
    7: "血管引導員",
    8: "解剖研究員",
    9: "解剖操盤手",
    10: "解剖副教授",
    11: "腦神經導師",
    12: "人體地圖管理",
    13: "解剖大魔導",
    14: "解剖學傳說"
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
    usedQuestionIds: [],
    user: null, // LINE 用户信息
    isLoggedIn: false
};

// LINE 登录功能
async function initLineLogin() {
    try {
        // 检查是否有 LINE 用户信息参数
        const urlParams = new URLSearchParams(window.location.search);
        const lineUser = urlParams.get('line_user');
        
        if (lineUser) {
            // 处理 LINE 登录回调
            await handleLineCallback(lineUser);
        } else {
            // 检查本地存储的登录状态
            const savedUser = localStorage.getItem('lineUser');
            if (savedUser) {
                const user = JSON.parse(savedUser);
                gameState.user = user;
                gameState.isLoggedIn = true;
                gameState.nickname = user.displayName;
                gameState.userId = user.userId;
                
                showUserInfo(user);
            } else {
                showLoginButton();
            }
        }
    } catch (error) {
        console.error('❌ LINE 登录初始化失败:', error);
        showManualLogin();
    }
}

// 处理 LINE 登录回调
async function handleLineCallback(lineUserData) {
    try {
        // 解析用户信息
        const user = JSON.parse(decodeURIComponent(lineUserData));
        
        gameState.user = user;
        gameState.isLoggedIn = true;
        gameState.nickname = user.displayName;
        gameState.userId = user.userId;
        
        // 保存到本地存储
        localStorage.setItem('lineUser', JSON.stringify(user));
        
        showUserInfo(user);
        await saveUserToSupabase(user);
        
        // 清除 URL 参数
        window.history.replaceState({}, document.title, window.location.pathname);
        
        console.log('✅ LINE 登录成功:', user.displayName);
        
    } catch (error) {
        console.error('❌ 处理 LINE 回调失败:', error);
        showManualLogin();
    }
}

// 显示用户信息
function showUserInfo(profile) {
    document.getElementById('login-section').style.display = 'none';
    document.getElementById('manual-login-section').style.display = 'none';
    document.getElementById('user-info').style.display = 'block';
    document.getElementById('start-btn').style.display = 'inline-block';
    
    document.getElementById('user-display-name').textContent = 
        `${profile.displayName} (${profile.userId})`;
}

// 显示登录按钮
function showLoginButton() {
    document.getElementById('login-section').style.display = 'block';
    document.getElementById('manual-login-section').style.display = 'none';
    document.getElementById('user-info').style.display = 'none';
    document.getElementById('start-btn').style.display = 'none';
}

// 显示手动登录选项
function showManualLogin() {
    document.getElementById('login-section').style.display = 'none';
    document.getElementById('manual-login-section').style.display = 'block';
    document.getElementById('user-info').style.display = 'none';
    document.getElementById('start-btn').style.display = 'inline-block';
}

// 显示昵称输入界面
function showUserIdInput() {
    console.log('📝 开始显示昵称输入界面');
    
    document.getElementById('login-section').style.display = 'none';
    document.getElementById('manual-login-section').style.display = 'none';
    document.getElementById('user-info').style.display = 'none';
    document.getElementById('start-btn').style.display = 'none';
    
    // 创建昵称输入 HTML
    const nicknameInputHtml = `
        <div id="line-nickname-input" class="mb-4">
            <div class="alert alert-info">
                <h5><i class="fab fa-line"></i> LINE 昵称登入</h5>
                <p class="mb-3">請輸入您在 LINE Bot 中設置的昵稱來完成登入：</p>
                
                <div class="mb-3">
                    <label for="line-nickname" class="form-label">LINE 昵称：</label>
                    <input type="text" id="line-nickname" class="form-control" 
                           placeholder="例如：小明、阿華、醫學學生" 
                           maxlength="20">
                    <div class="form-text">
                        <i class="fas fa-info-circle"></i>
                        請輸入您在 LINE Bot 中設置的昵稱（2-20 個字符）
                    </div>
                </div>
                
                <div class="mb-3">
                    <button class="btn btn-primary" onclick="sendVerificationCode()">
                        <i class="fas fa-paper-plane"></i> 發送驗證碼
                    </button>
                    <button class="btn btn-outline-secondary ms-2" onclick="showLoginButton()">
                        <i class="fas fa-arrow-left"></i> 返回
                    </button>
                </div>
                
                <div class="text-muted small">
                    <i class="fas fa-question-circle"></i>
                    不知道昵称？請先在 LINE Bot 中設置昵称，或使用手動輸入方式
                </div>
            </div>
        </div>
    `;
    
    // 插入到登录区域
    const loginSection = document.getElementById('login-section');
    if (loginSection) {
        loginSection.insertAdjacentHTML('afterend', nicknameInputHtml);
        console.log('✅ 昵称输入界面已插入到页面');
    } else {
        console.error('❌ 找不到 login-section 元素');
    }
}

// 发送验证码
async function sendVerificationCode() {
    const nickname = document.getElementById('line-nickname').value.trim();
    
    if (!nickname) {
        alert('請輸入 LINE 昵称');
        return;
    }
    
    if (nickname.length < 2 || nickname.length > 20) {
        alert('請輸入正確的昵称格式（2-20 個字符）');
        return;
    }
    
    try {
        // 生成 6 位数字验证码
        const verificationCode = Math.floor(100000 + Math.random() * 900000).toString();
        
        // 保存验证码到本地存储
        localStorage.setItem('pendingVerificationCode', verificationCode);
        localStorage.setItem('pendingNickname', nickname);
        
        // 调用 API 发送验证码
        const response = await fetch('/api/send-verification-code', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                nickname: nickname,
                verificationCode: verificationCode
            })
        });
        
        if (response.ok) {
            // 显示验证码输入界面
            showVerificationCodeInput(nickname, verificationCode);
        } else {
            const errorData = await response.json();
            if (response.status === 404) {
                alert('找不到該昵称，請確認昵称是否正確，或先在 LINE Bot 中設置昵称');
            } else {
                alert('發送驗證碼失敗，請重試');
            }
        }
        
    } catch (error) {
        console.error('❌ 发送验证码失败:', error);
        alert('發送驗證碼時發生錯誤，請重試');
    }
}

// 显示验证码输入界面
function showVerificationCodeInput(nickname, verificationCode) {
    // 移除昵称输入界面
    const nicknameInput = document.getElementById('line-nickname-input');
    if (nicknameInput) {
        nicknameInput.remove();
    }
    
    // 创建验证码输入 HTML
    const verificationInputHtml = `
        <div id="verification-code-input" class="mb-4">
            <div class="alert alert-success">
                <h5><i class="fas fa-key"></i> 輸入驗證碼</h5>
                <p class="mb-3">我們已向昵称「<strong>${nickname}</strong>」的 LINE 發送驗證碼，請輸入收到的 6 位數字：</p>
                
                <div class="mb-3">
                    <label for="verification-code" class="form-label">驗證碼：</label>
                    <input type="text" id="verification-code" class="form-control text-center" 
                           placeholder="000000" maxlength="6" style="font-size: 1.5rem; letter-spacing: 0.5rem;">
                </div>
                
                <div class="mb-3">
                    <button class="btn btn-success" onclick="verifyCode()">
                        <i class="fas fa-check"></i> 驗證登入
                    </button>
                    <button class="btn btn-outline-secondary ms-2" onclick="resendVerificationCode()">
                        <i class="fas fa-redo"></i> 重新發送
                    </button>
                </div>
                
                <div class="text-muted small">
                    <i class="fas fa-info-circle"></i>
                    昵称：<code>${nickname}</code> | 
                    驗證碼：<code>${verificationCode}</code>（僅供測試）
                </div>
            </div>
        </div>
    `;
    
    // 插入到登录区域
    const loginSection = document.getElementById('login-section');
    loginSection.insertAdjacentHTML('afterend', verificationInputHtml);
    
    // 自动聚焦到验证码输入框
    document.getElementById('verification-code').focus();
}

// 重新发送验证码
async function resendVerificationCode() {
    const nickname = localStorage.getItem('pendingNickname');
    if (nickname) {
        // 设置昵称到输入框
        document.getElementById('line-nickname').value = nickname;
        await sendVerificationCode();
    }
}

// 验证验证码
async function verifyCode() {
    const inputCode = document.getElementById('verification-code').value.trim();
    const expectedCode = localStorage.getItem('pendingVerificationCode');
    const nickname = localStorage.getItem('pendingNickname');
    
    if (!inputCode) {
        alert('請輸入驗證碼');
        return;
    }
    
    if (inputCode !== expectedCode) {
        alert('驗證碼錯誤，請重新輸入');
        return;
    }
    
    try {
        // 验证成功，通过昵称获取用户信息
        const { data: userData, error: userError } = await supabase
            .from('users')
            .select('*')
            .eq('nickname', nickname)
            .single();
        
        if (userError || !userData) {
            alert('找不到該昵称的用戶信息，請確認昵称是否正確');
            return;
        }
        
        // 完成登录
        const user = {
            userId: userData.user_id,
            displayName: userData.nickname,
            pictureUrl: userData.picture_url || 'https://via.placeholder.com/100'
        };
        
        gameState.user = user;
        gameState.isLoggedIn = true;
        gameState.nickname = user.displayName;
        gameState.userId = user.userId;
        
        // 保存到本地存储
        localStorage.setItem('lineUser', JSON.stringify(user));
        
        // 清除验证码输入界面
        const verificationInput = document.getElementById('verification-code-input');
        if (verificationInput) {
            verificationInput.remove();
        }
        
        showUserInfo(user);
        
        // 清除临时数据
        localStorage.removeItem('pendingVerificationCode');
        localStorage.removeItem('pendingNickname');
        
        console.log('✅ LINE Bot 验证码登录成功:', user.displayName);
        
    } catch (error) {
        console.error('❌ 验证码验证失败:', error);
        alert('驗證碼驗證時發生錯誤，請重試');
    }
}

// LINE 登录（通过 LINE Bot 验证码）
async function lineLogin() {
    try {
        console.log('🔑 点击了 LINE 登录按钮');
        // 直接显示昵称输入界面
        showUserIdInput();
        console.log('✅ 已显示昵称输入界面');
        
    } catch (error) {
        console.error('❌ LINE 登录失败:', error);
        alert('LINE 登录失败，请使用手动输入方式。');
        showManualLogin();
    }
}

// 确保 lineLogin 函数是全局可访问的
window.lineLogin = lineLogin;

// 添加一个简单的测试函数
window.testLineLogin = function() {
    console.log('🧪 测试 LINE 登录函数');
    try {
        lineLogin();
    } catch (error) {
        console.error('❌ 测试失败:', error);
    }
};

// 添加一个简单的测试函数来检查元素
window.testElements = function() {
    console.log('🔍 检查页面元素');
    const loginSection = document.getElementById('login-section');
    const lineLoginBtn = document.getElementById('line-login-btn');
    console.log('login-section:', loginSection);
    console.log('line-login-btn:', lineLoginBtn);
    console.log('lineLogin function:', typeof lineLogin);
};

// 登出
function logout() {
    // 清除本地存储
    localStorage.removeItem('lineUser');
    
    // 重置游戏状态
    gameState.user = null;
    gameState.isLoggedIn = false;
    gameState.nickname = '遊客';
    gameState.userId = null;
    
    showLoginButton();
}

// 保存用户信息到 Supabase
async function saveUserToSupabase(profile) {
    try {
        const { error } = await supabase
            .from('users')
            .upsert({
                user_id: profile.userId,
                nickname: profile.displayName,
                line_id: profile.userId,
                last_login: new Date().toISOString(),
                created_at: new Date().toISOString()
            });
        
        if (error) {
            console.error('❌ 保存用户信息失败:', error);
        } else {
            console.log('✅ 用户信息已保存到 Supabase');
        }
    } catch (error) {
        console.error('❌ 保存用户信息错误:', error);
    }
}

// 复制到剪贴板
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        alert('已複製到剪貼板！');
    }).catch(err => {
        console.error('複製失敗:', err);
        // 备用方案
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        alert('已複製到剪貼板！');
    });
}

// 检查登录状态
async function checkLoginStatus(loginToken) {
    try {
        // 检查 Supabase 中是否有对应的登录记录
        const { data, error } = await supabase
            .from('web_login_tokens')
            .select('*')
            .eq('token', loginToken)
            .eq('status', 'completed')
            .single();
        
        if (error || !data) {
            alert('尚未完成登入，請先在 LINE Bot 中回覆登入訊息。');
            return;
        }
        
        // 获取用户信息
        const { data: userData, error: userError } = await supabase
            .from('users')
            .select('*')
            .eq('user_id', data.user_id)
            .single();
        
        if (userError || !userData) {
            alert('找不到用戶信息，請重新登入。');
            return;
        }
        
        // 完成登录
        const user = {
            userId: userData.user_id,
            displayName: userData.nickname,
            pictureUrl: userData.picture_url || 'https://via.placeholder.com/100'
        };
        
        gameState.user = user;
        gameState.isLoggedIn = true;
        gameState.nickname = user.displayName;
        gameState.userId = user.userId;
        
        // 保存到本地存储
        localStorage.setItem('lineUser', JSON.stringify(user));
        
        // 清除登录说明
        const instructionsElement = document.getElementById('line-bot-login-instructions');
        if (instructionsElement) {
            instructionsElement.remove();
        }
        
        showUserInfo(user);
        
        // 清除登录令牌
        localStorage.removeItem('pendingLoginToken');
        
        console.log('✅ LINE Bot 登录成功:', user.displayName);
        
    } catch (error) {
        console.error('❌ 检查登录状态失败:', error);
        alert('檢查登入狀態時發生錯誤，請重試。');
    }
}

// 開始遊戲
async function startGame() {
    // 如果没有 LINE 登录，使用手动输入的昵称
    if (!gameState.isLoggedIn) {
        const nicknameInput = document.getElementById('nickname-input');
        const nickname = nicknameInput.value.trim() || '遊客';
        gameState.nickname = nickname;
        gameState.userId = 'web_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
    
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
    
    // 清除上一題的圖片
    const existingAnswerImage = document.querySelector('.answer-image');
    if (existingAnswerImage) {
        existingAnswerImage.remove();
    }
    
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
    
    // 移除之前可能存在的圖片
    const existingImage = document.querySelector('.question-image');
    if (existingImage) {
        existingImage.remove();
    }
    
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
            const oldLevel = gameState.currentLevel;
            gameState.currentLevel++;
            showLevelUpAnimation(oldLevel, gameState.currentLevel);
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
    
    // 顯示圖片（優先使用 image_url，若無則使用 qimage_url）
    // 根據 Supabase 資料庫欄位：image_url 為答案圖片，qimage_url 為題目圖片
    const imageUrl = question.image_url || question.qimage_url;
    
    if (imageUrl) {
        const explanationArea = document.getElementById('explanation-area');
        const imageHtml = `
            <div class="answer-image mt-3">
                <h5 class="mb-3"><i class="fas fa-image text-info"></i> 補充圖片：</h5>
                <img src="${imageUrl}" 
                     alt="補充圖片" 
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

// 顯示升級動畫（參考 LINE Bot 設計）
function showLevelUpAnimation(oldLevel, newLevel) {
    const modal = document.getElementById('result-modal');
    const icon = document.getElementById('result-icon');
    const title = document.getElementById('result-title');
    const message = document.getElementById('result-message');
    const stats = document.getElementById('result-stats');
    
    const oldTitle = LEVEL_TITLES[oldLevel];
    const newTitle = LEVEL_TITLES[newLevel];
    
    // 升級圖片 URL（從 Supabase Storage）
    const levelPosterUrl = `https://ciqlfqfgzqqgdrogedxg.supabase.co/storage/v1/object/public/linebot/level_${newLevel}_poster.png`;
    
    // 設置升級圖片
    icon.innerHTML = `
        <div class="level-up-image-container">
            <img src="${levelPosterUrl}" 
                 alt="等級 ${newLevel} 海報" 
                 class="level-up-poster"
                 onerror="this.style.display='none'; this.nextElementSibling.style.display='block';">
            <div class="level-up-fallback" style="display: none;">
                <i class="fas fa-trophy fa-5x text-warning"></i>
            </div>
        </div>
    `;
    
    title.innerHTML = '🎉 恭喜升級！';
    title.className = 'text-warning';
    
    // 參考 LINE Bot 的訊息內容
    message.innerHTML = `
        <div class="level-up-details">
            <p class="level-transition">🏆 從 <strong>${oldTitle}</strong></p>
            <p class="level-transition">晉升為 <strong class="text-warning">${newTitle}</strong>！</p>
            <hr style="margin: 20px 0; border-color: #ffd700;">
            <p class="level-description">你已經掌握了等級 ${oldLevel} 的知識，</p>
            <p class="level-description">現在開始挑戰等級 ${newLevel} 的更高難度！</p>
            <p class="level-encouragement"><strong>繼續加油，朝著終極解剖師的目標前進！</strong></p>
        </div>
    `;
    
    stats.innerHTML = `<h3 class="mt-3" style="color: #ffd700;">等級 ${newLevel}</h3>`;
    
    modal.style.display = 'flex';
    
    setTimeout(() => {
        modal.style.display = 'none';
        stats.innerHTML = '';
    }, 4000); // 延長顯示時間讓用戶欣賞升級圖片
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
    
    // 初始化 LINE 登录
    initLineLogin();
    
    // 添加事件监听器（只添加 logout 按钮，LINE 登录按钮使用 onclick）
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', logout);
    }
    
    console.log('✅ 页面初始化完成');
    
    // 测试：3秒后自动显示昵称输入界面
    setTimeout(() => {
        console.log('🧪 3秒后自动测试显示昵称输入界面');
        showUserIdInput();
    }, 3000);
});


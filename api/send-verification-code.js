// Vercel API 函数：发送验证码到 LINE Bot
export default async function handler(req, res) {
    // 设置 CORS 头
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    
    if (req.method === 'OPTIONS') {
        res.status(200).end();
        return;
    }
    
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }
    
    const { userId, verificationCode } = req.body;
    
    if (!userId || !verificationCode) {
        return res.status(400).json({ error: 'Missing userId or verificationCode' });
    }
    
    try {
        // LINE Bot 配置
        const LINE_CHANNEL_ACCESS_TOKEN = process.env.LINE_CHANNEL_ACCESS_TOKEN || 
            "AhZFgYWfEMeFSDxJJhzcvJoKx78lVrfRH3cqqusfiZhug/f5wRhQTkDD9fW7+IJLA3xpoQtunFWoVKnHtaE9p+U1QVFUz1o8CQ5AnNpPicjK32KAD5Z1ouF1HNKATv/BhUHIS3OjcndnUGpOqPDYKAdB04t89/1O/w1cDnyilFU=";
        
        // 发送验证码消息到 LINE Bot
        const message = {
            text: `🔐 網頁登入驗證碼\n\n您的驗證碼是：${verificationCode}\n\n請在網頁中輸入此驗證碼完成登入。\n\n驗證碼有效期：5 分鐘`
        };
        
        const response = await fetch('https://api.line.me/v2/bot/message/push', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${LINE_CHANNEL_ACCESS_TOKEN}`
            },
            body: JSON.stringify({
                to: userId,
                messages: [message]
            })
        });
        
        if (!response.ok) {
            console.error('LINE API 错误:', await response.text());
            return res.status(500).json({ error: 'Failed to send verification code' });
        }
        
        console.log(`✅ 验证码已发送到用户 ${userId}: ${verificationCode}`);
        
        res.status(200).json({ 
            success: true, 
            message: 'Verification code sent successfully' 
        });
        
    } catch (error) {
        console.error('❌ 发送验证码错误:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
}

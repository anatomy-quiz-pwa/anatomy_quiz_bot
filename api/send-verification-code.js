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
    
    const { nickname, verificationCode } = req.body;
    
    if (!nickname || !verificationCode) {
        return res.status(400).json({ error: 'Missing nickname or verificationCode' });
    }
    
    try {
        // Supabase 配置
        const SUPABASE_URL = process.env.SUPABASE_URL || 'https://ciqlfqfgzqqgdrogedxg.supabase.co';
        const SUPABASE_KEY = process.env.SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA';
        
        // 通过昵称查找用户
        const { createClient } = await import('@supabase/supabase-js');
        const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);
        
        const { data: userData, error: userError } = await supabase
            .from('users')
            .select('line_user_id, game_nickname')
            .eq('game_nickname', nickname)
            .single();
        
        if (userError || !userData) {
            console.log(`❌ 找不到昵称: ${nickname}`);
            return res.status(404).json({ error: 'User not found' });
        }
        
        // LINE Bot 配置
        const LINE_CHANNEL_ACCESS_TOKEN = process.env.LINE_CHANNEL_ACCESS_TOKEN || 
            "AhZFgYWfEMeFSDxJJhzcvJoKx78lVrfRH3cqqusfiZhug/f5wRhQTkDD9fW7+IJLA3xpoQtunFWoVKnHtaE9p+U1QVFUz1o8CQ5AnNpPicjK32KAD5Z1ouF1HNKATv/BhUHIS3OjcndnUGpOqPDYKAdB04t89/1O/w1cDnyilFU=";
        
        // 发送验证码消息到 LINE Bot
        const message = {
            text: `🔐 網頁登入驗證碼\n\n親愛的 ${nickname}，\n\n您的驗證碼是：${verificationCode}\n\n請在網頁中輸入此驗證碼完成登入。\n\n驗證碼有效期：5 分鐘`
        };
        
        const response = await fetch('https://api.line.me/v2/bot/message/push', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${LINE_CHANNEL_ACCESS_TOKEN}`
            },
            body: JSON.stringify({
                to: userData.line_user_id,
                messages: [message]
            })
        });
        
        if (!response.ok) {
            console.error('LINE API 错误:', await response.text());
            return res.status(500).json({ error: 'Failed to send verification code' });
        }
        
        console.log(`✅ 验证码已发送到昵称 ${nickname} (${userData.line_user_id}): ${verificationCode}`);
        
        res.status(200).json({ 
            success: true, 
            message: 'Verification code sent successfully',
            userId: userData.line_user_id
        });
        
    } catch (error) {
        console.error('❌ 发送验证码错误:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
}

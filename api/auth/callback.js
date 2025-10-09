// Vercel API 函数：处理 LINE Login 回调
export default async function handler(req, res) {
    // 设置 CORS 头
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    
    if (req.method === 'OPTIONS') {
        res.status(200).end();
        return;
    }
    
    if (req.method !== 'GET') {
        return res.status(405).json({ error: 'Method not allowed' });
    }
    
    const { code, state } = req.query;
    
    if (!code) {
        return res.status(400).json({ error: 'Missing authorization code' });
    }
    
    try {
        // 暂时使用模拟数据来测试流程
        // TODO: 配置真实的 LINE Login Channel Secret 后启用真实 API 调用
        
        console.log('LINE Login callback received:', { code, state });
        
        // 模拟用户信息（用于测试）
        const mockProfile = {
            userId: 'U' + Math.random().toString(36).substr(2, 32),
            displayName: 'LINE 测试用户',
            pictureUrl: 'https://via.placeholder.com/100'
        };
        
        // 重定向到前端，携带用户信息
        const userData = encodeURIComponent(JSON.stringify(mockProfile));
        const redirectUrl = `${req.headers.origin || 'https://anatomy-quiz-bot.vercel.app'}?line_user=${userData}`;
        
        console.log('Redirecting to:', redirectUrl);
        res.redirect(302, redirectUrl);
        
    } catch (error) {
        console.error('LINE Login error:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
}

import type { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  try {
    // 模擬 callback 的處理流程
    const code = req.query.code as string | undefined;
    const state = req.query.state as string | undefined;
    
    console.log('Debug callback - code:', code ? 'present' : 'missing');
    console.log('Debug callback - state:', state ? 'present' : 'missing');
    console.log('Debug callback - cookies:', req.cookies);
    
    // 檢查環境變數
    const envCheck = {
      LINE_LOGIN_CHANNEL_ID: !!process.env.LINE_LOGIN_CHANNEL_ID,
      LINE_LOGIN_CHANNEL_SECRET: !!process.env.LINE_LOGIN_CHANNEL_SECRET,
      APP_SESSION_SECRET: !!process.env.APP_SESSION_SECRET,
      SUPABASE_URL: !!process.env.SUPABASE_URL,
      SUPABASE_SERVICE_KEY: !!process.env.SUPABASE_SERVICE_KEY,
    };

    // 測試 Supabase 連線
    let supabaseTest: { success: boolean; error: string | undefined } | null = null;
    try {
      const { createClient } = await import('@supabase/supabase-js');
      const sbAdmin = createClient(
        process.env.SUPABASE_URL!,
        process.env.SUPABASE_SERVICE_KEY!,
        { auth: { persistSession: false }}
      );
      
      const { data, error } = await sbAdmin.from('users').select('count').limit(1);
      supabaseTest = { success: !error, error: error?.message };
    } catch (e: any) {
      supabaseTest = { success: false, error: e.message };
    }

    // 測試 LINE token 交換
    let tokenTest = null;
    if (code) {
      try {
        const host = req.headers['x-forwarded-host'] || req.headers.host;
        const redirect_uri = `https://${host}/api/auth/line/callback`;
        
        const tokenRes = await fetch('https://api.line.me/oauth2/v2.1/token', {
          method: 'POST',
          headers: {'Content-Type':'application/x-www-form-urlencoded'},
          body: new URLSearchParams({
            grant_type: 'authorization_code',
            code, 
            redirect_uri,
            client_id: process.env.LINE_LOGIN_CHANNEL_ID!,
            client_secret: process.env.LINE_LOGIN_CHANNEL_SECRET!,
            code_verifier: 'test_verifier', // 這會失敗，但我們可以看到錯誤
          }),
        });
        
        const tokenJson = await tokenRes.json();
        tokenTest = { 
          success: tokenRes.ok, 
          status: tokenRes.status,
          error: tokenJson 
        };
      } catch (e: any) {
        tokenTest = { success: false, error: e.message };
      }
    }

    res.status(200).json({
      query: req.query,
      cookies: req.cookies,
      envCheck,
      supabaseTest,
      tokenTest,
      timestamp: new Date().toISOString()
    });
  } catch (e: any) {
    res.status(500).json({ error: e.message, stack: e.stack });
  }
}

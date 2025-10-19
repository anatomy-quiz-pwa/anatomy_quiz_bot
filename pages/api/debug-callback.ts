import type { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  try {
    console.log('=== DEBUG CALLBACK START ===');
    console.log('Query:', req.query);
    console.log('Cookies:', req.cookies);
    console.log('Headers:', req.headers);
    
    const code = req.query.code as string | undefined;
    const state = req.query.state as string | undefined;
    
    console.log('Code present:', !!code);
    console.log('State present:', !!state);
    
    const cookieState = req.cookies?.oidc_state;
    const code_verifier = req.cookies?.oidc_cv;
    
    console.log('Cookie state present:', !!cookieState);
    console.log('Code verifier present:', !!code_verifier);
    console.log('State match:', cookieState === state);
    
    // 測試環境變數
    const envCheck = {
      LINE_LOGIN_CHANNEL_ID: !!process.env.LINE_LOGIN_CHANNEL_ID,
      LINE_LOGIN_CHANNEL_SECRET: !!process.env.LINE_LOGIN_CHANNEL_SECRET,
      APP_SESSION_SECRET: !!process.env.APP_SESSION_SECRET,
      SUPABASE_URL: !!process.env.SUPABASE_URL,
      SUPABASE_SERVICE_KEY: !!process.env.SUPABASE_SERVICE_KEY,
    };
    
    console.log('Environment check:', envCheck);

    res.status(200).json({
      query: req.query,
      cookies: req.cookies,
      headers: {
        host: req.headers.host,
        'x-forwarded-host': req.headers['x-forwarded-host'],
        'user-agent': req.headers['user-agent']
      },
      envCheck,
      debug: {
        code: !!code,
        state: !!state,
        cookieState: !!cookieState,
        codeVerifier: !!code_verifier,
        stateMatch: cookieState === state
      },
      timestamp: new Date().toISOString()
    });
  } catch (e: any) {
    console.error('Debug callback error:', e);
    res.status(500).json({ 
      error: e.message, 
      stack: e.stack,
      timestamp: new Date().toISOString()
    });
  }
}

import type { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  try {
    // 檢查環境變數
    const envCheck = {
      LINE_LOGIN_CHANNEL_ID: !!process.env.LINE_LOGIN_CHANNEL_ID,
      LINE_LOGIN_CHANNEL_SECRET: !!process.env.LINE_LOGIN_CHANNEL_SECRET,
      APP_SESSION_SECRET: !!process.env.APP_SESSION_SECRET,
      SUPABASE_URL: !!process.env.SUPABASE_URL,
      SUPABASE_SERVICE_KEY: !!process.env.SUPABASE_SERVICE_KEY,
    };

    // 測試 Supabase 連線
    let supabaseTest = null;
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

    res.status(200).json({
      envCheck,
      supabaseTest,
      timestamp: new Date().toISOString()
    });
  } catch (e: any) {
    res.status(500).json({ error: e.message });
  }
}

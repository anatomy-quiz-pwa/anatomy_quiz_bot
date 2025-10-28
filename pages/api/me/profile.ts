import type { NextApiRequest, NextApiResponse } from 'next';
import { jwtVerify } from 'jose';
import { createClient } from '@supabase/supabase-js';

const sbAdmin = createClient(process.env.SUPABASE_URL!, process.env.SUPABASE_SERVICE_KEY!, { auth: { persistSession: false }});
const SESSION_NAME = 'app_session';
const secret = new TextEncoder().encode(process.env.APP_SESSION_SECRET!);

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const raw = req.cookies?.[SESSION_NAME];
  if (!raw) return res.status(401).json({ error: 'unauthorized' });

  try {
    const { payload } = await jwtVerify(raw, secret);
    const userId = String(payload.sub);

    // 獲取用戶基本信息
    const { data: user, error: userError } = await sbAdmin
      .from('users')
      .select('id, line_user_id, display_name, picture, nickname')
      .eq('id', userId)
      .maybeSingle();
    
    if (userError) return res.status(500).json({ error: 'db_error' });
    if (!user) return res.status(404).json({ error: 'user_not_found' });

    // 獲取用戶統計信息
    const { data: stats } = await sbAdmin
      .from('user_stats')
      .select('*')
      .eq('user_id', userId)
      .maybeSingle();

    res.status(200).json({ 
      userId: user.id,
      lineUserId: user.line_user_id,
      displayName: user.display_name || user.nickname || '解剖學員',
      picture: user.picture,
      nickname: user.nickname,
      stats: stats || { 
        level: 1, 
        streak: 0, 
        total_correct: 0,
        correct_answers: 0,
        total_answers: 0
      }
    });
  } catch (e) {
    console.error('Profile API error:', e);
    res.status(401).json({ error: 'unauthorized' });
  }
}


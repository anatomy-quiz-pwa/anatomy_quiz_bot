import type { VercelRequest, VercelResponse } from '@vercel/node';
import { jwtVerify } from 'jose';
import { createClient } from '@supabase/supabase-js';

const sbAdmin = createClient(process.env.SUPABASE_URL!, process.env.SUPABASE_SERVICE_KEY!, { auth: { persistSession: false }});
const SESSION_NAME = 'app_session';
const secret = new TextEncoder().encode(process.env.APP_SESSION_SECRET!);

export default async function handler(req: VercelRequest, res: VercelResponse) {
  const raw = req.cookies?.[SESSION_NAME];
  if (!raw) return res.status(401).json({ error: 'unauthorized' });

  try {
    const { payload } = await jwtVerify(raw, secret);
    const userId = String(payload.sub);

    const { data, error } = await sbAdmin.from('user_stats').select('*').eq('user_id', userId).maybeSingle();
    if (error) return res.status(500).json({ error: 'db_error' });

    res.status(200).json({ user_id: userId, stats: data ?? { level: 1, streak: 0, total_correct: 0 } });
  } catch {
    res.status(401).json({ error: 'unauthorized' });
  }
}

// app/api/me/stats/route.ts
import { cookies } from 'next/headers';
import { NextResponse } from 'next/server';
import { getSessionUserId } from '@/lib/session';
import { sbAdmin } from '@/lib/supabase';

export const runtime = 'edge';

export async function GET() {
  const userId = await getSessionUserId(cookies());
  if (!userId) return NextResponse.json({ error:'unauthorized' }, { status: 401 });

  // 讀你的統計（這裡示範 user_stats，也可 join / 重算）
  const { data: stats, error } = await sbAdmin
    .from('user_stats')
    .select('*')
    .eq('user_id', userId)
    .maybeSingle();

  if (error) return NextResponse.json({ error: 'db_error' }, { status: 500 });

  return NextResponse.json({
    user_id: userId,
    stats: stats ?? { total_correct: 0, streak: 0, level: 1 }
  });
}

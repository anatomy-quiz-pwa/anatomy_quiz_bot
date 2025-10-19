// lib/users.ts
import { sbAdmin } from './supabase';

export async function findOrCreateUserByLineSub(lineSub: string, profile?: {displayName?:string, pictureUrl?:string}) {
  // 先找
  const { data: existing, error: e1 } = await sbAdmin
    .from('users')
    .select('id')
    .eq('line_user_id', lineSub)
    .maybeSingle();
  if (e1) throw e1;
  if (existing) return existing.id as string;

  // 沒有就建
  const { data: created, error: e2 } = await sbAdmin
    .from('users')
    .insert([{
      line_user_id: lineSub,
      display_name: profile?.displayName ?? null,
      picture: profile?.pictureUrl ?? null
    }])
    .select('id')
    .single();
  if (e2) throw e2;
  return created.id as string;
}

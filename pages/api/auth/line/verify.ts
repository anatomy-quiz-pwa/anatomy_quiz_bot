import type { NextApiRequest, NextApiResponse } from 'next';
import { createRemoteJWKSet, jwtVerify, SignJWT } from 'jose';
import { createClient } from '@supabase/supabase-js';

const sbAdmin = createClient(process.env.SUPABASE_URL!, process.env.SUPABASE_SERVICE_KEY!, {
  auth: { persistSession: false },
});
const JWKS = createRemoteJWKSet(new URL('https://api.line.me/oauth2/v2.1/certs'));
const LINE_ISS = 'https://access.line.me';
const LINE_AUD = process.env.LINE_LOGIN_CHANNEL_ID!;
const SESSION_NAME = 'app_session';
const secret = new TextEncoder().encode(process.env.APP_SESSION_SECRET!);

async function findOrCreateUserByLineSub(sub: string, profile?: {name?:string, picture?:string}) {
  const { data: exist, error: e1 } = await sbAdmin.from('users').select('id').eq('line_user_id', sub).maybeSingle();
  if (e1) throw e1;
  if (exist) return exist.id as string;
  const { data: created, error: e2 } = await sbAdmin.from('users').insert([{
    line_user_id: sub,
    display_name: profile?.name ?? null,
    picture: profile?.picture ?? null,
  }]).select('id').single();
  if (e2) throw e2;
  return created.id as string;
}

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') return res.status(405).end();
  try {
    const { idToken } = req.body || {};
    if (!idToken) return res.status(400).json({ error: 'missing_idToken' });

    const { payload } = await jwtVerify(idToken, JWKS, { issuer: LINE_ISS, audience: LINE_AUD });
    const sub = String(payload.sub);
    const profile = { name: (payload as any).name, picture: (payload as any).picture };

    const userId = await findOrCreateUserByLineSub(sub, profile);

    const session = await new SignJWT({ sub: userId })
      .setProtectedHeader({ alg: 'HS256' })
      .setIssuedAt().setExpirationTime('7d').sign(secret);

    res.setHeader('Set-Cookie',
      `${SESSION_NAME}=${session}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=${7*24*60*60}`);
    res.status(200).json({ ok: true });
  } catch {
    res.status(401).json({ error: 'verify_failed' });
  }
}

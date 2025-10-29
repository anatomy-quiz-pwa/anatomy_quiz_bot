import type { NextApiRequest, NextApiResponse } from 'next';
import { createRemoteJWKSet, jwtVerify, SignJWT } from 'jose';
import { createClient } from '@supabase/supabase-js';

const sbAdmin = createClient(process.env.SUPABASE_URL!, process.env.SUPABASE_SERVICE_KEY!, { auth: { persistSession: false }});
const JWKS = createRemoteJWKSet(new URL('https://api.line.me/oauth2/v2.1/certs'));
const LINE_ISS = 'https://access.line.me';
const LINE_AUD = process.env.LINE_LOGIN_CHANNEL_ID!;
const SESSION_NAME = 'app_session';
const secret = new TextEncoder().encode(process.env.APP_SESSION_SECRET!);

async function findOrCreateUserByLineSub(sub: string, profile?: {name?:string, picture?:string}) {
  const { data: exist, error: e1 } = await sbAdmin.from('users').select('id').eq('line_user_id', sub).maybeSingle();
  if (e1) throw e1;
  if (exist) return exist.id as string;
  const { data: created, error: e2 } = await sbAdmin.from('users').insert([{ line_user_id: sub, display_name: profile?.name ?? null, picture: profile?.picture ?? null }]).select('id').single();
  if (e2) throw e2;
  return created.id as string;
}

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'GET') return res.status(405).end();
  try {
    const code = req.query.code as string | undefined;
    const state = req.query.state as string | undefined;
    if (!code || !state) return res.status(400).json({ error: 'missing' });

    console.log('[LINE Callback] received state:', state);
    console.log('[LINE Callback] received code:', code ? 'present' : 'missing');
    console.log('[LINE Callback] cookies:', req.cookies);
    console.log('[LINE Callback] timestamp:', new Date().toISOString());

    const cookieState = req.cookies?.oidc_state;
    const code_verifier = req.cookies?.oidc_cv;
    
    console.log('[LINE Callback] cookie state:', cookieState);
    console.log('[LINE Callback] code verifier:', code_verifier ? 'present' : 'missing');
    console.log('[LINE Callback] state match:', cookieState === state);
    console.log('[LINE Callback] state lengths:', { 
      received: state?.length, 
      cookie: cookieState?.length 
    });
    
    if (!cookieState || !code_verifier || cookieState !== state) {
      console.log('[LINE Callback] state validation failed');
      return res.status(400).json({ error: 'bad_state' });
    }

    const host = req.headers['x-forwarded-host'] || req.headers.host;
    const redirect_uri = `https://${host}/api/auth/line/callback`;

    const tokenRes = await fetch('https://api.line.me/oauth2/v2.1/token', {
      method: 'POST',
      headers: {'Content-Type':'application/x-www-form-urlencoded'},
      body: new URLSearchParams({
        grant_type: 'authorization_code',
        code, redirect_uri,
        client_id: process.env.LINE_LOGIN_CHANNEL_ID!,
        client_secret: process.env.LINE_LOGIN_CHANNEL_SECRET!,
        code_verifier,
      }),
    });
    const tokenJson: any = await tokenRes.json();
    if (!tokenRes.ok) return res.status(401).json({ error: 'token_exchange_failed', detail: tokenJson });

    const idToken = tokenJson.id_token as string;
    
    // 驗證 LINE ID Token - 修復 JWT 算法問題
    console.log('開始驗證 LINE ID Token...');
    const { payload } = await jwtVerify(idToken, JWKS, { 
      issuer: LINE_ISS, 
      audience: LINE_AUD,
      algorithms: ['RS256']  // LINE 只使用 RS256 算法
    });
    console.log('JWT 驗證成功');
    
    const sub = String(payload.sub);
    const profile = { name: (payload as any).name, picture: (payload as any).picture };
    
    const userId = await findOrCreateUserByLineSub(sub, profile);
    
    const session = await new SignJWT({ sub: userId })
      .setProtectedHeader({ alg: 'HS256' }).setIssuedAt().setExpirationTime('7d').sign(secret);
    
    res.setHeader('Set-Cookie', [
      `${SESSION_NAME}=${session}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=${7*24*60*60}`,
      `oidc_state=; Path=/; Max-Age=0`, `oidc_cv=; Path=/; Max-Age=0`,
    ]);
    
    // 重定向到遊戲頁面
    res.writeHead(302, { Location: '/game-play' });
    res.end();
  } catch (e) {
    console.error('LINE callback error:', e);
    res.status(500).json({ 
      error: 'callback_failed', 
      message: e instanceof Error ? e.message : String(e),
      stack: process.env.NODE_ENV === 'development' ? (e instanceof Error ? e.stack : undefined) : undefined
    });
  }
}

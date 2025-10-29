import { NextApiRequest, NextApiResponse } from 'next';
import { jwtVerify, createRemoteJWKSet, SignJWT } from 'jose';
import { createClient } from '@supabase/supabase-js';

const LINE_JWKS = createRemoteJWKSet(new URL('https://api.line.me/oauth2/v2.1/certs'));
const LINE_ISSUER = 'https://access.line.me';
const SESSION_NAME = 'app_session';
const secret = new TextEncoder().encode(process.env.APP_SESSION_SECRET!);

const sbAdmin = createClient(process.env.SUPABASE_URL!, process.env.SUPABASE_SERVICE_KEY!, { 
  auth: { persistSession: false }
});

// base64url 解碼函數，對應 login.ts 中的 b64url
const b64urlDecode = (str: string): string => {
  const base64 = str.replace(/-/g, '+').replace(/_/g, '/');
  return Buffer.from(base64, 'base64').toString('utf-8');
};

async function findOrCreateUserByLineSub(sub: string, profile?: {name?:string, picture?:string}) {
  const { data: exist, error: e1 } = await sbAdmin.from('users').select('id').eq('line_user_id', sub).maybeSingle();
  if (e1) throw e1;
  if (exist) return exist.id as string;
  const { data: created, error: e2 } = await sbAdmin.from('users').insert([{ 
    line_user_id: sub, 
    display_name: profile?.name ?? null, 
    picture: profile?.picture ?? null 
  }]).select('id').single();
  if (e2) throw e2;
  return created.id as string;
}

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'GET') return res.status(405).end();
  
  try {
    const { code, state } = req.query;

    if (!code) return res.status(400).json({ error: 'missing_code' });
    if (!state) return res.status(400).json({ error: 'missing_state' });

    // 解碼 state（包含 state 和 code_verifier）
    let code_verifier: string | undefined;
    try {
      const decoded = b64urlDecode(String(state));
      const stateData = JSON.parse(decoded);
      code_verifier = stateData.cv;
      console.log('[LINE Callback] PKCE code_verifier:', code_verifier ? 'present' : 'missing');
    } catch (e) {
      console.warn('[LINE Callback] Failed to decode state for PKCE, continuing without code_verifier');
    }

    // 1️⃣ 用 code 換取 access_token + id_token
    const preferredBaseUrl = process.env.PUBLIC_BASE_URL;
    const host = req.headers['x-forwarded-host'] || req.headers.host;
    const baseUrl = preferredBaseUrl || `https://${host}`;
    const redirect_uri = `${baseUrl}/api/auth/line/callback`;

    const body = new URLSearchParams({
      grant_type: 'authorization_code',
      code: String(code),
      redirect_uri,
      client_id: process.env.LINE_LOGIN_CHANNEL_ID!,
      client_secret: process.env.LINE_LOGIN_CHANNEL_SECRET!,
    });

    // 如果有 code_verifier（PKCE），添加到請求中
    if (code_verifier) {
      body.append('code_verifier', code_verifier);
    }

    const tokenRes = await fetch('https://api.line.me/oauth2/v2.1/token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body,
    });

    const tokens = await tokenRes.json();
    if (!tokenRes.ok) {
      console.error('LINE token exchange failed:', tokens);
      return res.status(400).json({ error: 'token_exchange_failed', detail: tokens });
    }

    const idToken = tokens.id_token as string;
    if (!idToken) {
      return res.status(400).json({ error: 'missing_id_token' });
    }

    // 2️⃣ 驗證 id_token (RS256) - 修復 JWT 算法問題
    console.log('[LINE Callback] 開始驗證 LINE ID Token (RS256)...');
    let payload;
    try {
      const result = await jwtVerify(idToken, LINE_JWKS, {
        algorithms: ['RS256'],
        issuer: LINE_ISSUER,
        audience: process.env.LINE_LOGIN_CHANNEL_ID!,
      });
      payload = result.payload;
      console.log('[LINE Callback] JWT 驗證成功');
    } catch (jwtError) {
      console.error('[LINE Callback] JWT 驗證失敗:', jwtError);
      return res.status(400).json({ 
        error: 'jwt_verification_failed', 
        message: jwtError instanceof Error ? jwtError.message : String(jwtError)
      });
    }

    // 3️⃣ 建立或查找用戶，創建 session
    const sub = String(payload.sub);
    const profile = { 
      name: (payload as any).name, 
      picture: (payload as any).picture 
    };
    
    const userId = await findOrCreateUserByLineSub(sub, profile);
    
    // 創建 session token
    const session = await new SignJWT({ sub: userId })
      .setProtectedHeader({ alg: 'HS256' })
      .setIssuedAt()
      .setExpirationTime('7d')
      .sign(secret);
    
    // 設置 session cookie
    res.setHeader('Set-Cookie', [
      `${SESSION_NAME}=${session}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=${7*24*60*60}`,
      `oidc_state=; Path=/; Max-Age=0`,
      `oidc_cv=; Path=/; Max-Age=0`,
    ]);
    
    // 重定向到遊戲頁面
    res.writeHead(302, { Location: '/game-play' });
    res.end();
    
  } catch (err: any) {
    console.error('[LINE Callback] 錯誤:', err);
    return res.status(400).json({ 
      error: 'callback_failed', 
      message: String(err?.message || err) 
    });
  }
}

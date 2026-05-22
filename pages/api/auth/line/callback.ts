// /api/auth/line/callback.ts
import type { NextApiRequest, NextApiResponse } from 'next';
import { SignJWT } from 'jose';
import { verifyLineIdToken } from '../../../../lib/line_oidc';

const TOK_URL = 'https://api.line.me/oauth2/v2.1/token';
const SESSION_NAME = 'app_session';
const SESSION_MAX_AGE_SEC = 60 * 60 * 24 * 30; // 30 days

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  try {
    const code = String(req.query.code || '');
    const stateParam = String(req.query.state || '');
    if (!code) return res.status(400).json({ error: 'missing_code' });

    // 從 state 取出 PKCE code_verifier (state = base64url(JSON.stringify({s, cv})))
    let codeVerifier = '';
    try {
      const b64 = stateParam.replace(/-/g, '+').replace(/_/g, '/');
      const json = Buffer.from(b64, 'base64').toString();
      const parsed = JSON.parse(json);
      codeVerifier = parsed.cv || '';
    } catch (e) {
      console.error('[LINE Callback] state parse failed', e);
    }

    // 以環境變數為優先，避免不同網域造成 redirect_uri 不匹配
    const preferredBaseUrl = process.env.PUBLIC_BASE_URL;
    const host = req.headers['x-forwarded-host'] || req.headers.host;
    const baseUrl = preferredBaseUrl || `https://${host}`;
    const redirectUri = `${baseUrl}/api/auth/line/callback`;

    // 優先使用 LINE_CHANNEL_ID，如果不存在則使用 LINE_LOGIN_CHANNEL_ID
    const clientId = process.env.LINE_CHANNEL_ID || process.env.LINE_LOGIN_CHANNEL_ID || '';
    const clientSecret = process.env.LINE_CHANNEL_SECRET || process.env.LINE_LOGIN_CHANNEL_SECRET || '';
    if (!clientId || !clientSecret) {
      console.error('[LINE Callback] Error: Missing client_id or client_secret');
      return res.status(500).json({ error: 'misconfigured_credentials' });
    }

    const sessionSecret = process.env.APP_SESSION_SECRET;
    if (!sessionSecret) {
      console.error('[LINE Callback] Error: Missing APP_SESSION_SECRET');
      return res.status(500).json({ error: 'misconfigured_session_secret' });
    }

    // 1) 用 code 換 token
    const body = new URLSearchParams({
      grant_type: 'authorization_code',
      code,
      redirect_uri: redirectUri,
      client_id: clientId,
      client_secret: clientSecret,
    });
    if (codeVerifier) body.set('code_verifier', codeVerifier);

    const r = await fetch(TOK_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body,
    });
    const tok = await r.json();
    if (!r.ok) {
      return res.status(400).json({ error: 'token_exchange_failed', detail: tok });
    }
    const idToken = tok.id_token as string;
    if (!idToken) return res.status(400).json({ error: 'missing_id_token' });

    // 2) 驗證 id_token（RS256 + 本地 JWKS）
    const { payload } = await verifyLineIdToken(idToken, clientId);

    // 3) 簽 app_session JWT，sub = LINE user id（與舊 quiz_logs.user_id 對應）
    const secret = new TextEncoder().encode(sessionSecret);
    const sessionJwt = await new SignJWT({
      name: payload.name,
      picture: payload.picture,
    })
      .setProtectedHeader({ alg: 'HS256' })
      .setSubject(String(payload.sub))
      .setIssuedAt()
      .setExpirationTime(`${SESSION_MAX_AGE_SEC}s`)
      .sign(secret);

    // 4) 寫 HttpOnly cookie
    const cookie = [
      `${SESSION_NAME}=${sessionJwt}`,
      'HttpOnly',
      'Secure',
      'SameSite=Lax',
      'Path=/',
      `Max-Age=${SESSION_MAX_AGE_SEC}`,
    ].join('; ');
    res.setHeader('Set-Cookie', cookie);

    // 5) Redirect 到遊戲頁
    res.writeHead(302, { Location: '/game-play' });
    res.end();
  } catch (err: any) {
    console.error('[LINE Callback] error:', err);
    return res.status(400).json({
      error: 'jwt_verification_failed',
      message: String(err?.message || err),
    });
  }
}

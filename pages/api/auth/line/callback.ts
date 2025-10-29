// /api/auth/line/callback.ts
import type { NextApiRequest, NextApiResponse } from 'next';
import { verifyLineIdToken } from '../../../../lib/line_oidc';

const TOK_URL = 'https://api.line.me/oauth2/v2.1/token';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  try {
    const code = String(req.query.code || '');
    const state = String(req.query.state || '');
    if (!code) return res.status(400).json({ error: 'missing_code' });

    // TODO: 如有實作 state/nonce/PKCE，這裡取出並比對
    // if (state !== expected) return res.status(400).json({ error: 'bad_state' });

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

    // 1) 用 code 換 token
    const body = new URLSearchParams({
      grant_type: 'authorization_code',
      code,
      redirect_uri: redirectUri,
      client_id: clientId,
      client_secret: clientSecret,
      // 如有 PKCE：body.set('code_verifier', codeVerifierFromCookieOrStore)
    });

    const r = await fetch(TOK_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body
    });
    const tok = await r.json();
    if (!r.ok) {
      return res.status(400).json({ error: 'token_exchange_failed', detail: tok });
    }
    const idToken = tok.id_token as string;
    if (!idToken) return res.status(400).json({ error: 'missing_id_token' });

    // 2) 驗證 id_token（RS256 + 本地 JWKS）
    const { payload } = await verifyLineIdToken(
      idToken,
      clientId
    );

    // 3) TODO: 建立你的 session / JWT / cookie；這裡先回應 JSON，方便雲端 log 驗證
    return res.status(200).json({
      ok: true,
      sub: payload.sub,
      name: payload.name,
      picture: payload.picture,
      aud: payload.aud,
      iss: payload.iss,
    });
  } catch (err: any) {
    return res.status(400).json({
      error: 'jwt_verification_failed',
      message: String(err?.message || err)
    });
  }
}

// /api/auth/line/callback.ts
import type { NextApiRequest, NextApiResponse } from 'next';
import { verifyLineIdToken } from '../../../../lib/line_oidc';

const TOK_URL = 'https://api.line.me/oauth2/v2.1/token';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  console.log('[LINE Callback] Version: 628a5135-debug-v2');
  console.log('[LINE Callback] Env check - LINE_CHANNEL_ID:', process.env.LINE_CHANNEL_ID ? 'SET' : 'NOT SET');
  console.log('[LINE Callback] Env check - PUBLIC_BASE_URL:', process.env.PUBLIC_BASE_URL || 'NOT SET');
  
  try {
    const code = String(req.query.code || '');
    const state = String(req.query.state || '');
    if (!code) return res.status(400).json({ error: 'missing_code' });

    // TODO: 如有實作 state/nonce/PKCE，這裡取出並比對
    // if (state !== expected) return res.status(400).json({ error: 'bad_state' });

    const redirectUri = `${process.env.PUBLIC_BASE_URL}/api/auth/line/callback`;

    // 1) 用 code 換 token
    const body = new URLSearchParams({
      grant_type: 'authorization_code',
      code,
      redirect_uri: redirectUri,
      client_id: process.env.LINE_CHANNEL_ID || '',
      client_secret: process.env.LINE_CHANNEL_SECRET || '',
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
    const { payload, protectedHeader } = await verifyLineIdToken(
      idToken,
      process.env.LINE_CHANNEL_ID as string
    );

    // 3) TODO: 建立你的 session / JWT / cookie；這裡先回應 JSON，方便雲端 log 驗證
    return res.status(200).json({
      ok: true,
      sub: payload.sub,
      name: payload.name,
      picture: payload.picture,
      header: protectedHeader,
      aud: payload.aud,
      iss: payload.iss,
    });
  } catch (err: any) {
    return res.status(400).json({
      error: 'callback_failed',
      message: String(err?.message || err)
    });
  }
}

import type { NextApiRequest, NextApiResponse } from 'next';
import crypto from 'crypto';

const b64url = (buf: Buffer) => buf.toString('base64').replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'');

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'GET') return res.status(405).end();

  const state = b64url(crypto.randomBytes(16));
  const code_verifier = b64url(crypto.randomBytes(32));
  const code_challenge = b64url(crypto.createHash('sha256').update(code_verifier).digest());

  // 將 state 和 code_verifier 編碼到 URL 中，避免 cookie 問題
  const encodedState = encodeURIComponent(state);
  const encodedVerifier = encodeURIComponent(code_verifier);

  // 以環境變數為優先，避免不同網域造成 redirect_uri 不匹配
  const preferredBaseUrl = process.env.PUBLIC_BASE_URL; // 例如 https://anatomy-quiz-bot.vercel.app
  const host = req.headers['x-forwarded-host'] || req.headers.host;
  const baseUrl = preferredBaseUrl || `https://${host}`;
  const redirect_uri = `${baseUrl}/api/auth/line/callback`;

  // 調試資訊（僅輸出到伺服器日誌）
  console.log('[LINE Login] client_id:', process.env.LINE_LOGIN_CHANNEL_ID);
  console.log('[LINE Login] redirect_uri:', redirect_uri);
  console.log('[LINE Login] state:', state);

  const params = new URLSearchParams({
    response_type: 'code',
    client_id: process.env.LINE_LOGIN_CHANNEL_ID!,
    redirect_uri,
    state: encodedState, // 使用編碼的 state
    scope: 'openid profile',
    code_challenge,
    code_challenge_method: 'S256',
  });

  const authorizeUrl = `https://access.line.me/oauth2/v2.1/authorize?${params}`;
  console.log('[LINE Login] authorize URL:', authorizeUrl);
  
  // 將 code_verifier 存儲在 sessionStorage 中（通過前端處理）
  res.writeHead(302, { 
    Location: authorizeUrl,
    'Set-Cookie': `oidc_cv=${code_verifier}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=600`
  });
  res.end();
}

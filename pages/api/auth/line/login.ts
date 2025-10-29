import type { NextApiRequest, NextApiResponse } from 'next';
import crypto from 'crypto';

const b64url = (buf: Buffer) => buf.toString('base64').replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'');

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'GET') return res.status(405).end();

  const state = b64url(crypto.randomBytes(16));
  const code_verifier = b64url(crypto.randomBytes(32));
  const code_challenge = b64url(crypto.createHash('sha256').update(code_verifier).digest());

  // 設置 OAuth state 和 code_verifier 到 cookie
  const cookieOptions = [
    'Path=/',
    'HttpOnly',
    'Secure',
    'SameSite=Lax',  // 改為 Lax 避免跨站問題
    'Max-Age=600'
  ].join('; ');
  
  res.setHeader('Set-Cookie', [
    `oidc_state=${state}; ${cookieOptions}`,
    `oidc_cv=${code_verifier}; ${cookieOptions}`,
  ]);
  
  console.log('[LINE Login] state:', state);
  console.log('[LINE Login] cookies set:', ['oidc_state', 'oidc_cv']);

  // 以環境變數為優先，避免不同網域造成 redirect_uri 不匹配
  const preferredBaseUrl = process.env.PUBLIC_BASE_URL; // 例如 https://anatomy-quiz-bot.vercel.app
  const host = req.headers['x-forwarded-host'] || req.headers.host;
  const baseUrl = preferredBaseUrl || `https://${host}`;
  const redirect_uri = `${baseUrl}/api/auth/line/callback`;

  // 調試資訊（僅輸出到伺服器日誌）
  console.log('[LINE Login] client_id:', process.env.LINE_LOGIN_CHANNEL_ID);
  console.log('[LINE Login] redirect_uri:', redirect_uri);

  const params = new URLSearchParams({
    response_type: 'code',
    client_id: process.env.LINE_LOGIN_CHANNEL_ID!,
    redirect_uri,
    state,
    scope: 'openid profile',
    code_challenge,
    code_challenge_method: 'S256',
  });

  const authorizeUrl = `https://access.line.me/oauth2/v2.1/authorize?${params}`;
  console.log('[LINE Login] authorize URL:', authorizeUrl);
  res.writeHead(302, { Location: authorizeUrl });
  res.end();
}

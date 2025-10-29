import type { NextApiRequest, NextApiResponse } from 'next';
import crypto from 'crypto';

const b64url = (buf: Buffer) => buf.toString('base64').replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'');

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'GET') return res.status(405).end();

  const randomState = b64url(crypto.randomBytes(16));
  const code_verifier = b64url(crypto.randomBytes(32));
  const code_challenge = b64url(crypto.createHash('sha256').update(code_verifier).digest());

  // 將 state 和 code_verifier 組合成一個 JSON，然後 base64url 編碼
  // 這樣可以在 callback 中完全恢復，避免 cookie 依賴
  const stateData = JSON.stringify({ s: randomState, cv: code_verifier });
  const encodedState = b64url(Buffer.from(stateData));

  // 以環境變數為優先，避免不同網域造成 redirect_uri 不匹配
  const preferredBaseUrl = process.env.PUBLIC_BASE_URL; // 例如 https://anatomy-quiz-bot.vercel.app
  const host = req.headers['x-forwarded-host'] || req.headers.host;
  const baseUrl = preferredBaseUrl || `https://${host}`;
  const redirect_uri = `${baseUrl}/api/auth/line/callback`;

  // 優先使用 LINE_CHANNEL_ID，如果不存在則使用 LINE_LOGIN_CHANNEL_ID
  const clientId = process.env.LINE_CHANNEL_ID || process.env.LINE_LOGIN_CHANNEL_ID;
  if (!clientId) {
    console.error('[LINE Login] Error: LINE_CHANNEL_ID and LINE_LOGIN_CHANNEL_ID are both undefined');
    return res.status(500).json({ error: 'misconfigured_client_id' });
  }

  // 調試資訊（僅輸出到伺服器日誌）
  console.log('[LINE Login] client_id:', clientId);
  console.log('[LINE Login] redirect_uri:', redirect_uri);
  console.log('[LINE Login] random state:', randomState);
  console.log('[LINE Login] code_verifier present:', !!code_verifier);

  const params = new URLSearchParams({
    response_type: 'code',
    client_id: clientId,
    redirect_uri,
    state: encodedState, // 使用編碼的 state
    scope: 'openid profile',
    code_challenge,
    code_challenge_method: 'S256',
  });

  const authorizeUrl = `https://access.line.me/oauth2/v2.1/authorize?${params}`;
  console.log('[LINE Login] authorize URL:', authorizeUrl);
  console.log('[LINE Login] encoded state contains both state and code_verifier');
  
  res.writeHead(302, { Location: authorizeUrl });
  res.end();
}

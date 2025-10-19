import type { NextApiRequest, NextApiResponse } from 'next';
import crypto from 'crypto';

const b64url = (buf: Buffer) => buf.toString('base64').replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'');

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'GET') return res.status(405).end();

  const state = b64url(crypto.randomBytes(16));
  const code_verifier = b64url(crypto.randomBytes(32));
  const code_challenge = b64url(crypto.createHash('sha256').update(code_verifier).digest());

  // 存在 HttpOnly cookie，callback 要用
  res.setHeader('Set-Cookie', [
    `oidc_state=${state}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=600`,
    `oidc_cv=${code_verifier}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=600`,
  ]);

  const host = req.headers['x-forwarded-host'] || req.headers.host;
  const redirect_uri = `https://${host}/api/auth/line/callback`;

  const params = new URLSearchParams({
    response_type: 'code',
    client_id: process.env.LINE_LOGIN_CHANNEL_ID!,
    redirect_uri,
    state,
    scope: 'openid profile',
    code_challenge,
    code_challenge_method: 'S256',
  });

  res.writeHead(302, { Location: `https://access.line.me/oauth2/v2.1/authorize?${params}` });
  res.end();
}

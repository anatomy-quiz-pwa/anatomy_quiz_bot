// app/api/auth/line/login/route.ts
import { NextRequest, NextResponse } from 'next/server';
import crypto from 'crypto';

export const runtime = 'edge';

function b64url(input: ArrayBuffer) {
  return Buffer.from(input).toString('base64')
    .replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'');
}

export async function GET(req: NextRequest) {
  const state = b64url(crypto.randomBytes(16));
  const code_verifier = b64url(crypto.randomBytes(32));
  const code_challenge = b64url(crypto.createHash('sha256').update(code_verifier).digest());

  // 存在 cookie（HttpOnly），callback 用得到
  const headers = new Headers();
  headers.append('Set-Cookie', `oidc_state=${state}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=600`);
  headers.append('Set-Cookie', `oidc_cv=${code_verifier}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=600`);

  const params = new URLSearchParams({
    response_type: 'code',
    client_id: process.env.LINE_LOGIN_CHANNEL_ID!,
    redirect_uri: `https://${req.headers.get('host')}/api/auth/line/callback`,
    state,
    scope: 'openid profile',
    code_challenge,
    code_challenge_method: 'S256',
  });

  return NextResponse.redirect(`https://access.line.me/oauth2/v2.1/authorize?${params.toString()}`, { headers });
}

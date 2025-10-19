// lib/line_oidc.ts
import { createRemoteJWKSet, jwtVerify } from 'jose';

// LINE 的 JWKS
const JWKS = createRemoteJWKSet(new URL('https://api.line.me/oauth2/v2.1/certs'));
const LINE_ISS = 'https://access.line.me';
const LINE_AUD = process.env.LINE_LOGIN_CHANNEL_ID!;

// 驗證 LIFF 或 OIDC 取得的 id_token
export async function verifyLineIdToken(idToken: string) {
  const { payload } = await jwtVerify(idToken, JWKS, {
    issuer: LINE_ISS,
    audience: LINE_AUD,
  });
  // payload.sub 就是唯一識別（line_user_id）
  return payload as any; // { sub, name?, picture?, ... }
}

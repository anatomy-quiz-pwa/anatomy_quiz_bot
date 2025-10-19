// lib/session.ts
import { SignJWT, jwtVerify } from 'jose';
const SESSION_NAME = 'app_session';
const secret = new TextEncoder().encode(process.env.APP_SESSION_SECRET!);

export async function setSessionCookie(userId: string, headers: Headers) {
  const token = await new SignJWT({ sub: userId })
    .setProtectedHeader({ alg: 'HS256' })
    .setIssuedAt()
    .setExpirationTime('7d')                // 你的網站 Session 期限（可改）
    .sign(secret);

  headers.append('Set-Cookie',
    `${SESSION_NAME}=${token}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=${7*24*60*60}`);
}

export async function getSessionUserId(cookies: { get: (k:string)=>{value?:string}|undefined }) {
  const raw = cookies.get(SESSION_NAME)?.value;
  if (!raw) return null;
  try {
    const { payload } = await jwtVerify(raw, secret);
    return String(payload.sub);
  } catch {
    return null;
  }
}


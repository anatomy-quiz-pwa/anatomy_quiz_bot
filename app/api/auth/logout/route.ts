// app/api/auth/logout/route.ts
import { NextResponse } from 'next/server';

export const runtime = 'edge';

export async function POST() {
  const headers = new Headers();
  // 清除 session cookie
  headers.append('Set-Cookie', 'app_session=; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=0');
  
  return new NextResponse(JSON.stringify({ ok: true }), { 
    status: 200,
    headers 
  });
}

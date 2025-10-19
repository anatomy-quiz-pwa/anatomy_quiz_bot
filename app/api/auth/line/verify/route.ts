// app/api/auth/line/verify/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { verifyLineIdToken } from '@/lib/line_oidc';
import { findOrCreateUserByLineSub } from '@/lib/users';
import { setSessionCookie } from '@/lib/session';

export const runtime = 'edge';

export async function POST(req: NextRequest) {
  try {
    const { idToken } = await req.json();
    if (!idToken) return NextResponse.json({error:'missing idToken'}, {status:400});

    const payload = await verifyLineIdToken(idToken);
    const sub = String(payload.sub);
    const profile = {
      displayName: (payload as any).name,
      pictureUrl: (payload as any).picture
    };

    const userId = await findOrCreateUserByLineSub(sub, profile);

    const headers = new Headers();
    await setSessionCookie(userId, headers);
    return new NextResponse(JSON.stringify({ ok:true }), { headers });
  } catch (e) {
    return NextResponse.json({ error:'verify_failed' }, { status:401 });
  }
}

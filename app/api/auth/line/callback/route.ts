// app/api/auth/line/callback/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { verifyLineIdToken } from '@/lib/line_oidc';
import { findOrCreateUserByLineSub } from '@/lib/users';
import { setSessionCookie } from '@/lib/session';

export const runtime = 'edge';

export async function GET(req: NextRequest) {
  try {
    const url = new URL(req.url);
    const code = url.searchParams.get('code');
    const state = url.searchParams.get('state');
    if (!code || !state) return NextResponse.json({error:'missing'}, {status:400});

    const cookieState = req.cookies.get('oidc_state')?.value;
    const code_verifier = req.cookies.get('oidc_cv')?.value;
    if (!cookieState || !code_verifier || cookieState !== state) {
      return NextResponse.json({error:'bad_state'}, {status:400});
    }

    // 用 code + code_verifier 向 LINE 換 token
    const tokenRes = await fetch('https://api.line.me/oauth2/v2.1/token', {
      method: 'POST',
      headers: {'Content-Type':'application/x-www-form-urlencoded'},
      body: new URLSearchParams({
        grant_type: 'authorization_code',
        code,
        redirect_uri: `https://${req.headers.get('host')}/api/auth/line/callback`,
        client_id: process.env.LINE_LOGIN_CHANNEL_ID!,
        client_secret: process.env.LINE_LOGIN_CHANNEL_SECRET!,
        code_verifier
      })
    });
    const tokenJson = await tokenRes.json() as any;
    if (!tokenRes.ok) return NextResponse.json({error:'token_exchange_failed', detail: tokenJson}, {status:401});

    const idToken = tokenJson.id_token as string;
    const payload = await verifyLineIdToken(idToken);
    const sub = String(payload.sub);

    const userId = await findOrCreateUserByLineSub(sub, {
      displayName: (payload as any).name,
      pictureUrl: (payload as any).picture
    });

    // 設網站 Session；並清掉 OIDC 暫存 cookie
    const headers = new Headers();
    await setSessionCookie(userId, headers);
    headers.append('Set-Cookie', `oidc_state=; Path=/; Max-Age=0`);
    headers.append('Set-Cookie', `oidc_cv=; Path=/; Max-Age=0`);

    // 導回你的遊戲頁
    headers.append('Location', '/game');
    return new NextResponse(null, { status: 302, headers });
  } catch (e) {
    return NextResponse.json({ error:'callback_failed' }, { status:500 });
  }
}

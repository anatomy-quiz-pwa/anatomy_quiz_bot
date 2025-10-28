import type { NextApiRequest, NextApiResponse } from 'next';
import { jwtVerify } from 'jose';

const SESSION_NAME = 'app_session';
const secret = new TextEncoder().encode(process.env.APP_SESSION_SECRET!);

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'GET') return res.status(405).end();

  try {
    const sessionToken = req.cookies?.[SESSION_NAME];
    
    if (!sessionToken) {
      return res.status(200).json({ authenticated: false });
    }

    // 驗證 session token
    const { payload } = await jwtVerify(sessionToken, secret);
    const userId = String(payload.sub);

    return res.status(200).json({ 
      authenticated: true,
      userId: userId
    });
  } catch (e) {
    console.error('Session verification error:', e);
    return res.status(200).json({ authenticated: false });
  }
}


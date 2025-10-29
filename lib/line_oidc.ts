// lib/line_oidc.ts
import { createLocalJWKSet, jwtVerify } from 'jose';

const LINE_JWKS_URL = 'https://api.line.me/oauth2/v2.1/certs';
const LINE_ISSUER = 'https://access.line.me';
const TTL = 1000 * 60 * 60; // 1h

// 定義 JWKSet 類型
interface JWKSet {
  keys: Array<{
    kid?: string;
    kty?: string;
    alg?: string;
    use?: string;
    [key: string]: any;
  }>;
}

let cache: { exp: number; set: ReturnType<typeof createLocalJWKSet> } | null = null;

async function fetchJWKS(): Promise<JWKSet> {
  const res = await fetch(LINE_JWKS_URL, { cache: 'no-store' });
  if (!res.ok) throw new Error(`[LINE OIDC] Fetch JWKS failed: ${res.status} ${res.statusText}`);
  const jwks = await res.json();
  // 調試：列出 key 清單
  try {
    const list = (jwks.keys || []).map((k: any) => ({ kid: k.kid, kty: k.kty, alg: k.alg, use: k.use }));
    console.log('[LINE OIDC] JWKS keys:', JSON.stringify(list));
  } catch {}
  return jwks;
}

function filterRS256(jwks: JWKSet): JWKSet {
  const keys = (jwks.keys || []).filter((k: any) => k?.kty === 'RSA' && (!k.alg || k.alg === 'RS256'));
  if (!keys.length) throw new Error('No RS256 RSA keys found in LINE JWKS');
  // 有些 key 可能沒帶 alg，強制標記為 RS256，避免 jose 報 Unsupported "alg"
  for (const k of keys) if (!k.alg) (k as any).alg = 'RS256';
  return { keys };
}

async function getLocalJWKSet() {
  const now = Date.now();
  if (cache && cache.exp > now) return cache.set;
  // 抓取並過濾
  const raw = await fetchJWKS();
  const filtered = filterRS256(raw);
  const local = createLocalJWKSet(filtered);
  cache = { exp: now + TTL, set: local };
  return local;
}

export async function verifyLineIdToken(idToken: string, audience: string) {
  try {
    const jwks = await getLocalJWKSet();
    const { payload, protectedHeader } = await jwtVerify(idToken, jwks, {
      algorithms: ['RS256'],
      issuer: LINE_ISSUER,
      audience, // 必須等於你的 LINE_CHANNEL_ID
    });
    console.log('[LINE OIDC] jwtVerify ok:', { kid: protectedHeader.kid, alg: protectedHeader.alg });
    return { payload, protectedHeader };
  } catch (e: any) {
    console.error('[LINE OIDC] jwtVerify error:', e?.message || e);
    throw new Error('jwt_verification_failed');
  }
}

// lib/line_oidc.ts
import { createLocalJWKSet, jwtVerify, JWKSet } from 'jose';

const LINE_JWKS_URL = 'https://api.line.me/oauth2/v2.1/certs';
const LINE_ISSUER = 'https://access.line.me';

let _jwksCache: { set: ReturnType<typeof createLocalJWKSet>, exp: number } | null = null;
const JWKS_TTL_MS = 60 * 60 * 1000; // 1 小時

async function fetchLINEJwks(): Promise<JWKSet> {
  const res = await fetch(LINE_JWKS_URL, { cache: 'no-store' });
  if (!res.ok) throw new Error(`Fetch LINE JWKS failed: ${res.status} ${res.statusText}`);
  return await res.json();
}

function filterRS256(jwks: JWKSet): JWKSet {
  const keys = (jwks.keys || []).filter((k: any) => {
    // 只接受 RSA / RS256；若 alg 缺省但 kty=RSA 也保留
    const isRSA = k.kty === 'RSA';
    const algOK = !k.alg || k.alg === 'RS256';
    return isRSA && algOK;
  });
  if (!keys.length) throw new Error('No RS256 RSA keys found in LINE JWKS');
  
  // 強制標示 alg=RS256，避免某些 key 未帶 alg
  // 並且確保每個 key 都是獨立的對象（避免修改原始對象）
  const processedKeys = keys.map((k: any) => {
    const newKey = { ...k };
    if (!newKey.alg) newKey.alg = 'RS256';
    return newKey;
  });
  
  return { keys: processedKeys };
}

async function getLocalJwkSet() {
  const now = Date.now();
  if (_jwksCache && _jwksCache.exp > now) return _jwksCache.set;
  
  console.log('[LINE OIDC] Fetching JWKS from LINE...');
  const raw = await fetchLINEJwks();
  console.log('[LINE OIDC] Received JWKS with', raw.keys?.length || 0, 'keys');
  
  const filtered = filterRS256(raw);
  console.log('[LINE OIDC] Filtered to', filtered.keys.length, 'RS256 keys');
  
  // 詳細記錄每個 key 的屬性
  filtered.keys.forEach((k: any, i: number) => {
    console.log(`[LINE OIDC] Key ${i}: kty=${k.kty}, alg=${k.alg}, kid=${k.kid}`);
  });
  
  const local = createLocalJWKSet(filtered);
  _jwksCache = { set: local, exp: now + JWKS_TTL_MS };
  console.log('[LINE OIDC] Created local JWKS successfully');
  return local;
}

export async function verifyLineIdToken(idToken: string, audience: string) {
  console.log('[LINE OIDC] Verifying token with audience:', audience);
  
  try {
    const jwks = await getLocalJwkSet();
    
    // 檢查 JWT header 中的算法
    try {
      const [headerPart] = idToken.split('.');
      const header = JSON.parse(Buffer.from(headerPart, 'base64url').toString('utf-8'));
      console.log('[LINE OIDC] JWT header alg:', header.alg, 'kid:', header.kid);
    } catch (e) {
      console.warn('[LINE OIDC] Could not parse JWT header:', e);
    }
    
    const { payload, protectedHeader } = await jwtVerify(idToken, jwks, {
      algorithms: ['RS256'],
      issuer: LINE_ISSUER,
      audience, // 必須等於 LINE_CHANNEL_ID
    });
    
    console.log('[LINE OIDC] Token verified successfully');
    return { payload, protectedHeader };
  } catch (error) {
    console.error('[LINE OIDC] Verification failed:', error);
    console.error('[LINE OIDC] Error details:', {
      message: error instanceof Error ? error.message : String(error),
      name: error instanceof Error ? error.name : undefined,
      code: (error as any).code,
    });
    throw error;
  }
}

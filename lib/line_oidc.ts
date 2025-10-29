import { createLocalJWKSet, jwtVerify, JWKSet } from 'jose';

const LINE_JWKS_URL = 'https://api.line.me/oauth2/v2.1/certs';
const LINE_ISSUER = 'https://access.line.me';
let cache: { exp: number; set: ReturnType<typeof createLocalJWKSet> } | null = null;
const TTL = 1000 * 60 * 60; // 1h

async function fetchJWKS(): Promise<JWKSet> {
  const res = await fetch(LINE_JWKS_URL, { cache: 'no-store' });
  const jwks = await res.json();
  console.log('[LINE OIDC] JWKS keys:', (jwks.keys || []).map((k: any) => ({
    kid: k.kid, kty: k.kty, alg: k.alg
  })));
  const filtered = { keys: (jwks.keys || []).filter((k: any) => k.kty === 'RSA' && (!k.alg || k.alg === 'RS256')) };
  if (!filtered.keys.length) throw new Error('No RS256 RSA keys found in LINE JWKS');
  for (const k of filtered.keys) if (!k.alg) k.alg = 'RS256';
  return filtered;
}

async function getLocalJWKSet() {
  const now = Date.now();
  if (cache && cache.exp > now) return cache.set;
  const jwks = await fetchJWKS();
  const local = createLocalJWKSet(jwks);
  cache = { exp: now + TTL, set: local };
  return local;
}

export async function verifyLineIdToken(idToken: string, aud: string) {
  const jwks = await getLocalJWKSet();
  const { payload, protectedHeader } = await jwtVerify(idToken, jwks, {
    algorithms: ['RS256'],
    issuer: LINE_ISSUER,
    audience: aud,
  });
  return { payload, protectedHeader };
}

// lib/line_oidc.ts
import { jwtVerify, importJWK, createLocalJWKSet } from 'jose';

const LINE_ISS = 'https://access.line.me';
const LINE_AUD = process.env.LINE_LOGIN_CHANNEL_ID!;
const LINE_JWKS_URL = 'https://api.line.me/oauth2/v2.1/certs';

// 緩存 JWKS
let cachedJWKS: ReturnType<typeof createLocalJWKSet> | null = null;
let jwksFetchTime = 0;
const JWKS_CACHE_TTL = 3600000; // 1 小時

// 獲取並過濾 JWKS，只保留 RS256 的 key
async function getLineJWKS() {
  const now = Date.now();
  
  // 如果緩存有效，直接返回
  if (cachedJWKS && (now - jwksFetchTime) < JWKS_CACHE_TTL) {
    return cachedJWKS;
  }

  try {
    // 獲取 LINE 的 JWKS
    const response = await fetch(LINE_JWKS_URL);
    const jwks = await response.json();
    
    // 過濾出 RS256 的 key（RSA key 通常使用 RS256）
    const rs256Keys = jwks.keys.filter((key: any) => 
      key.alg === 'RS256' || (key.kty === 'RSA' && !key.alg)
    );
    
    if (rs256Keys.length === 0) {
      throw new Error('No RS256 keys found in LINE JWKS');
    }

    // 為每個 key 確保 alg 設為 RS256
    const processedKeys = rs256Keys.map((key: any) => ({
      ...key,
      alg: 'RS256'
    }));
    
    // 創建本地 JWKS
    cachedJWKS = createLocalJWKSet({ keys: processedKeys });
    jwksFetchTime = now;
    
    return cachedJWKS;
  } catch (error) {
    console.error('Failed to fetch/process LINE JWKS:', error);
    throw error;
  }
}

// 驗證 LIFF 或 OIDC 取得的 id_token
export async function verifyLineIdToken(idToken: string) {
  const JWKS = await getLineJWKS();
  const { payload } = await jwtVerify(idToken, JWKS, {
    issuer: LINE_ISS,
    audience: LINE_AUD,
    algorithms: ['RS256'], // 明確指定 RS256
  });
  // payload.sub 就是唯一識別（line_user_id）
  return payload as any; // { sub, name?, picture?, ... }
}

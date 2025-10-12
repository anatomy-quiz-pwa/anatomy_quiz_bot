// lib/session.ts
import { jwtVerify } from "jose";

const secret = new TextEncoder().encode(process.env.SESSION_SECRET || "default-secret-key-please-change-in-production");

/**
 * 從 Cookie 中解析並驗證 JWT session，返回 line_user_id
 * @param cookieHeader Cookie header 字串
 * @returns line_user_id 或 null
 */
export async function getSessionLineUserId(cookieHeader?: string): Promise<string | null> {
  const cookie = cookieHeader ?? "";
  const match = /(?:^|;\s*)session=([^;]+)/.exec(cookie);
  
  if (!match) {
    return null;
  }
  
  try {
    const { payload } = await jwtVerify(match[1], secret);
    return (payload as any).line_user_id as string;
  } catch (error) {
    console.error("JWT 驗證失敗:", error);
    return null;
  }
}


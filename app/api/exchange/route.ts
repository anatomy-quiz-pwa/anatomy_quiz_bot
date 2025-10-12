// app/api/exchange/route.ts
import { cookies } from "next/headers";
import { NextResponse } from "next/server";
import { SignJWT } from "jose";
import { createClient } from "@supabase/supabase-js";

const secret = new TextEncoder().encode(process.env.SESSION_SECRET || "default-secret-key-please-change-in-production");

// 使用 Service Role Key 以繞過 RLS
const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE || process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

export async function POST(req: Request) {
  try {
    const { token } = await req.json();

    if (!token) {
      return NextResponse.json({ ok: false, reason: "missing_token" }, { status: 400 });
    }

    // 查詢 token
    const { data, error } = await supabase
      .from("link_tokens")
      .select("line_user_id, expires_at, used")
      .eq("token", token)
      .single();

    if (error || !data) {
      console.error("Token 查詢失敗:", error);
      return NextResponse.json({ ok: false, reason: "invalid_token" }, { status: 400 });
    }

    // 檢查是否已使用
    if (data.used) {
      return NextResponse.json({ ok: false, reason: "token_already_used" }, { status: 400 });
    }

    // 檢查是否過期
    if (new Date(data.expires_at) < new Date()) {
      return NextResponse.json({ ok: false, reason: "token_expired" }, { status: 400 });
    }

    // 標記 token 為已使用
    await supabase
      .from("link_tokens")
      .update({ used: true })
      .eq("token", token);

    // 創建 JWT session
    const jwt = await new SignJWT({ line_user_id: data.line_user_id })
      .setProtectedHeader({ alg: "HS256" })
      .setIssuedAt()
      .setExpirationTime("30d")
      .sign(secret);

    // 設置 HttpOnly Cookie
    cookies().set("session", jwt, {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "lax",
      path: "/",
      maxAge: 30 * 24 * 60 * 60, // 30 days
    });

    console.log("✅ Token 交換成功，用戶:", data.line_user_id);

    return NextResponse.json({ ok: true, line_user_id: data.line_user_id });
  } catch (error) {
    console.error("Token 交換失敗:", error);
    return NextResponse.json({ ok: false, reason: "server_error" }, { status: 500 });
  }
}


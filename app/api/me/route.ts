// app/api/me/route.ts
import { NextResponse } from "next/server";
import { getSessionLineUserId } from "@/lib/session";
import { createClient } from "@supabase/supabase-js";

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE || process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

export async function GET(req: Request) {
  try {
    // 從 Cookie 中取得 line_user_id
    const line_user_id = await getSessionLineUserId(req.headers.get("cookie") ?? "");
    
    if (!line_user_id) {
      return NextResponse.json({ ok: false, reason: "unauthorized" }, { status: 401 });
    }

    // 查詢用戶統計資料
    const { data: stats, error: statsError } = await supabase
      .from("user_stats")
      .select("*")
      .eq("line_user_id", line_user_id)
      .single();

    if (statsError && statsError.code !== "PGRST116") {
      console.error("查詢用戶統計失敗:", statsError);
    }

    // 查詢用戶基本資料
    const { data: user, error: userError } = await supabase
      .from("users")
      .select("*")
      .eq("line_user_id", line_user_id)
      .single();

    if (userError && userError.code !== "PGRST116") {
      console.error("查詢用戶資料失敗:", userError);
    }

    return NextResponse.json({
      ok: true,
      line_user_id,
      stats: stats ?? null,
      user: user ?? null,
    });
  } catch (error) {
    console.error("API /me 錯誤:", error);
    return NextResponse.json({ ok: false, reason: "server_error" }, { status: 500 });
  }
}


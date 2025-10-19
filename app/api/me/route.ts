// app/api/me/route.ts
import { cookies } from 'next/headers';
import { NextResponse } from 'next/server';
import { getSessionUserId } from '@/lib/session';
import { sbAdmin } from '@/lib/supabase';

export const runtime = 'edge';

export async function GET() {
  try {
    const userId = await getSessionUserId(cookies());
    if (!userId) {
      return NextResponse.json({ ok: false, reason: "unauthorized" }, { status: 401 });
    }

    // 查詢用戶基本資料
    const { data: user, error: userError } = await sbAdmin
      .from("users")
      .select("*")
      .eq("id", userId)
      .single();

    if (userError && userError.code !== "PGRST116") {
      console.error("查詢用戶資料失敗:", userError);
    }

    // 查詢用戶統計資料
    const { data: stats, error: statsError } = await sbAdmin
      .from("user_stats")
      .select("*")
      .eq("user_id", userId)
      .single();

    if (statsError && statsError.code !== "PGRST116") {
      console.error("查詢用戶統計失敗:", statsError);
    }

    return NextResponse.json({
      ok: true,
      user_id: userId,
      stats: stats ?? null,
      user: user ?? null,
    });
  } catch (error) {
    console.error("API /me 錯誤:", error);
    return NextResponse.json({ ok: false, reason: "server_error" }, { status: 500 });
  }
}


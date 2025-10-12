// app/api/answer/route.ts
import { NextResponse } from "next/server";
import { getSessionLineUserId } from "@/lib/session";
import { createClient } from "@supabase/supabase-js";

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE || process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

export async function POST(req: Request) {
  try {
    // 從 Cookie 中取得 line_user_id
    const line_user_id = await getSessionLineUserId(req.headers.get("cookie") ?? "");
    
    if (!line_user_id) {
      return NextResponse.json({ ok: false, reason: "unauthorized" }, { status: 401 });
    }

    const { question_id, answer, is_correct } = await req.json();

    if (!question_id || typeof is_correct !== "boolean") {
      return NextResponse.json({ ok: false, reason: "invalid_data" }, { status: 400 });
    }

    // 記錄答題
    const { error: logError } = await supabase
      .from("quiz_logs")
      .insert({
        line_user_id,
        question_id,
        user_answer: answer,
        is_correct,
        answered_at: new Date().toISOString(),
      });

    if (logError) {
      console.error("記錄答題失敗:", logError);
    }

    // 更新用戶統計
    const { data: currentStats } = await supabase
      .from("user_stats")
      .select("*")
      .eq("line_user_id", line_user_id)
      .single();

    const newCorrect = (currentStats?.correct || 0) + (is_correct ? 1 : 0);
    const newWrong = (currentStats?.wrong || 0) + (is_correct ? 0 : 1);
    const newTotal = newCorrect + newWrong;

    const { error: statsError } = await supabase
      .from("user_stats")
      .upsert({
        line_user_id,
        correct: newCorrect,
        wrong: newWrong,
        total: newTotal,
        updated_at: new Date().toISOString(),
      });

    if (statsError) {
      console.error("更新統計失敗:", statsError);
    }

    return NextResponse.json({
      ok: true,
      stats: {
        correct: newCorrect,
        wrong: newWrong,
        total: newTotal,
      },
    });
  } catch (error) {
    console.error("API /answer 錯誤:", error);
    return NextResponse.json({ ok: false, reason: "server_error" }, { status: 500 });
  }
}


import { NextRequest, NextResponse } from "next/server";
import { createClient } from "@supabase/supabase-js";

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const serviceRoleKey = process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;
const supabase = createClient(supabaseUrl, serviceRoleKey);

export async function POST(req: NextRequest) {
  try {
    const { line_user_id, question_id, chosen_option, is_correct, source } = await req.json();
    if (!line_user_id || typeof question_id !== "number" || typeof chosen_option !== "number") {
      return NextResponse.json({ error: "missing fields" }, { status: 400 });
    }

    // 找/建 user
    const { data: userFound } = await supabase
      .from("users")
      .select("id")
      .eq("line_user_id", line_user_id)
      .single();

    let user_id = userFound?.id;
    if (!user_id) {
      const { data: created, error: cerr } = await supabase
        .from("users")
        .insert({ line_user_id })
        .select("id")
        .single();
      if (cerr) throw cerr;
      user_id = created.id;
    }

    // 寫 quiz_logs
    const { error: qerr } = await supabase.from("quiz_logs").insert({
      user_id,
      question_id,
      chosen_option,
      is_correct: !!is_correct,
      source: source || "web",
    });
    if (qerr) throw qerr;

    // 更新/建立 user_stats
    const incField = !!is_correct ? "correct" : "wrong";
    const { error: serr } = await supabase.rpc("inc_user_stat", {
      p_user_id: user_id,
      p_field: incField
    });
    if (serr) throw serr;

    return NextResponse.json({ ok: true });
  } catch (e: any) {
    return NextResponse.json({ error: e.message }, { status: 500 });
  }
}


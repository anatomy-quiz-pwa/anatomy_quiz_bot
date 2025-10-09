import { NextRequest, NextResponse } from "next/server";
import { createClient } from "@supabase/supabase-js";

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const serviceRoleKey = process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;
const supabase = createClient(supabaseUrl, serviceRoleKey);

export async function GET(req: NextRequest) {
  try {
    const { searchParams } = new URL(req.url);
    const line_user_id = searchParams.get("line_user_id");
    if (!line_user_id) return NextResponse.json({ error: "line_user_id required" }, { status: 400 });

    // 找 user
    const { data: userRow, error: uerr } = await supabase
      .from("users")
      .select("id")
      .eq("line_user_id", line_user_id)
      .single();
    if (uerr || !userRow) return NextResponse.json({ error: "user not found" }, { status: 404 });

    // 取進度
    const { data: stats, error } = await supabase
      .from("user_stats")
      .select("correct, wrong, last_update")
      .eq("user_id", userRow.id)
      .single();

    if (error && error.code !== "PGRST116") throw error; // PGRST116: row not found

    return NextResponse.json({
      progress: stats || { correct: 0, wrong: 0, last_update: null },
    });
  } catch (e: any) {
    return NextResponse.json({ error: e.message }, { status: 500 });
  }
}


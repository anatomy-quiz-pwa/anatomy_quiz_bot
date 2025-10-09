import { NextRequest, NextResponse } from "next/server";
import { createClient } from "@supabase/supabase-js";

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const serviceRoleKey = process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;
const supabase = createClient(supabaseUrl, serviceRoleKey);

export async function POST(req: NextRequest) {
  try {
    const { line_user_id, display_name, picture_url } = await req.json();

    if (!line_user_id) {
      return NextResponse.json({ error: "line_user_id required" }, { status: 400 });
    }

    // upsert users
    const { data, error } = await supabase
      .from("users")
      .upsert(
        { line_user_id, display_name, picture_url },
        { onConflict: "line_user_id" }
      )
      .select("id, line_user_id, display_name");

    if (error) throw error;

    return NextResponse.json({ user: data?.[0] ?? null });
  } catch (e: any) {
    return NextResponse.json({ error: e.message }, { status: 500 });
  }
}


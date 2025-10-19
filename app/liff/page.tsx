"use client";
import { useEffect, useState } from "react";
import { sbAdmin } from "@/lib/supabase";

declare global {
  interface Window { liff: any }
}

export default function LiffPage() {
  const [status, setStatus] = useState("initial");
  const [profile, setProfile] = useState<any>(null);
  const [progress, setProgress] = useState<any>(null);
  const LIFF_ID = process.env.NEXT_PUBLIC_LIFF_ID!;

  useEffect(() => {
    (async () => {
      try {
        setStatus("init LIFF...");
        if (!window.liff) {
          // LIFF SDK 將通過 script 標籤載入
          setStatus("LIFF SDK not loaded");
          return;
        }
        await window.liff.init({ liffId: LIFF_ID });

        if (!window.liff.isLoggedIn()) {
          window.liff.login();
          return;
        }
        setStatus("getProfile...");
        const prof = await window.liff.getProfile();
        setProfile(prof);

        // 綁定/建立 user
        await fetch("/api/link-line", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            line_user_id: prof.userId,
            display_name: prof.displayName,
            picture_url: prof.pictureUrl
          })
        });

        // 拉進度
        const res = await fetch(`/api/progress?line_user_id=${prof.userId}`);
        const json = await res.json();
        setProgress(json.progress);
        setStatus("ready");
      } catch (e: any) {
        setStatus("error: " + e.message);
      }
    })();
  }, []);

  async function answerDemo(isCorrect: boolean) {
    if (!profile) return;
    await fetch("/api/answer", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        line_user_id: profile.userId,
        question_id: 123,
        chosen_option: isCorrect ? 1 : 2,
        is_correct: isCorrect,
        source: "web"
      })
    });
    const res = await fetch(`/api/progress?line_user_id=${profile.userId}`);
    const json = await res.json();
    setProgress(json.progress);
  }

  return (
    <main className="mx-auto max-w-md p-6">
      <h1 className="text-2xl font-bold mb-4">解剖咬一口 · LIFF 登入</h1>
      <p className="mb-2">狀態：{status}</p>
      {profile && (
        <div className="mb-4 flex items-center gap-3">
          {profile.pictureUrl && <img src={profile.pictureUrl} alt="avatar" className="w-12 h-12 rounded-full" />}
          <div>
            <div className="font-semibold">{profile.displayName}</div>
            <div className="text-xs text-gray-500 break-all">{profile.userId}</div>
          </div>
        </div>
      )}

      {progress && (
        <div className="mb-4 p-3 border rounded">
          <div>今日進度</div>
          <div className="text-sm text-gray-600">答對：{progress.correct ?? 0}｜答錯：{progress.wrong ?? 0}</div>
          <div className="text-xs text-gray-500">last_update：{progress.last_update ?? "—"}</div>
        </div>
      )}

      <div className="flex gap-3">
        <button onClick={() => answerDemo(true)} className="px-3 py-2 rounded bg-black text-white">答對示範</button>
        <button onClick={() => answerDemo(false)} className="px-3 py-2 rounded border">答錯示範</button>
      </div>
    </main>
  );
}


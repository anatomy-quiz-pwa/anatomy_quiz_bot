// app/link/page.tsx
"use client";
import { useEffect, useState } from "react";
import Link from "next/link";

type LinkState = "loading" | "ok" | "fail";

export default function LinkPage() {
  const [state, setState] = useState<LinkState>("loading");
  const [errorMessage, setErrorMessage] = useState<string>("");

  useEffect(() => {
    const token = new URLSearchParams(window.location.search).get("token");
    
    if (!token) {
      setState("fail");
      setErrorMessage("缺少連結 token");
      return;
    }

    // 呼叫 API 交換 token
    fetch("/api/exchange", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ token }),
    })
      .then((r) => r.json())
      .then((data) => {
        if (data.ok) {
          setState("ok");
        } else {
          setState("fail");
          setErrorMessage(getErrorMessage(data.reason));
        }
      })
      .catch((error) => {
        console.error("連結失敗:", error);
        setState("fail");
        setErrorMessage("網路錯誤，請稍後再試");
      });
  }, []);

  const getErrorMessage = (reason: string) => {
    switch (reason) {
      case "invalid_token":
        return "無效的連結 token";
      case "token_already_used":
        return "此連結已經使用過";
      case "token_expired":
        return "連結已過期（有效期 10 分鐘）";
      default:
        return "連結失敗，請稍後再試";
    }
  };

  return (
    <main className="min-h-screen flex flex-col items-center justify-center p-8" style={{
      background: "linear-gradient(135deg, #fffaf5 0%, #fff5eb 100%)",
      fontFamily: "ui-sans-serif, system-ui, -apple-system"
    }}>
      <div className="max-w-md w-full bg-white rounded-2xl shadow-xl p-8 border-2 border-gray-800">
        {state === "loading" && (
          <div className="text-center">
            <div className="animate-spin rounded-full h-16 w-16 border-4 border-gray-200 border-t-[#C57B57] mx-auto mb-4"></div>
            <h1 className="text-2xl font-bold text-gray-800 mb-2">連結中...</h1>
            <p className="text-gray-600">正在綁定你的 LINE 帳號</p>
          </div>
        )}

        {state === "ok" && (
          <div className="text-center">
            <div className="mb-6">
              <svg className="w-20 h-20 mx-auto text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h1 className="text-3xl font-bold text-gray-800 mb-4">🎉 連結成功！</h1>
            <div className="bg-green-50 border-2 border-green-200 rounded-xl p-4 mb-6">
              <p className="text-green-800 font-medium mb-2">✓ LINE 帳號已與網站登入綁定</p>
              <p className="text-green-700 text-sm">等級與紀錄將自動同步</p>
            </div>
            <Link 
              href="/"
              className="inline-block w-full bg-[#C57B57] hover:bg-[#A66847] text-white font-bold py-4 px-6 rounded-xl transition-all duration-200 transform hover:scale-105 shadow-lg"
            >
              🎮 開始遊戲
            </Link>
          </div>
        )}

        {state === "fail" && (
          <div className="text-center">
            <div className="mb-6">
              <svg className="w-20 h-20 mx-auto text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h1 className="text-3xl font-bold text-gray-800 mb-4">❌ 連結失敗</h1>
            <div className="bg-red-50 border-2 border-red-200 rounded-xl p-4 mb-6">
              <p className="text-red-800 font-medium">{errorMessage}</p>
            </div>
            <div className="space-y-3">
              <p className="text-gray-600 text-sm mb-4">
                請回到 LINE 再次輸入「網站」以取得新的連結。
              </p>
              <Link 
                href="/"
                className="inline-block w-full bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-3 px-6 rounded-xl transition-all duration-200"
              >
                回到首頁
              </Link>
            </div>
          </div>
        )}
      </div>

      {/* 品牌標誌 */}
      <div className="mt-8 text-center">
        <p className="text-gray-600 text-sm">解剖咬一口 Anatomy Bite</p>
        <p className="text-gray-400 text-xs mt-1">遊戲化解剖學習系統</p>
      </div>
    </main>
  );
}


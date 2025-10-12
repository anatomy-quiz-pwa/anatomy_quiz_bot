"use client";
import { useEffect } from "react";

export default function HomePage() {
  useEffect(() => {
    // 直接重定向到根目錄（會被 next.config.mjs 重寫為 public/index.html）
    window.location.href = "/";
  }, []);

  return (
    <main style={{
      minHeight: "100vh",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      padding: "24px",
      fontFamily: "ui-sans-serif",
      background: "linear-gradient(135deg, #fffaf5 0%, #fff5eb 100%)"
    }}>
      <div style={{
        textAlign: "center",
        maxWidth: "600px"
      }}>
        <h1 style={{
          fontSize: "2.5rem",
          fontWeight: "bold",
          color: "#1C1C1C",
          marginBottom: "1rem"
        }}>
          解剖咬一口 Anatomy Bite
        </h1>
        <p style={{
          fontSize: "1.25rem",
          color: "#666",
          marginBottom: "2rem"
        }}>
          正在載入遊戲...
        </p>
        <div style={{
          display: "inline-block",
          width: "50px",
          height: "50px",
          border: "4px solid #f3f3f3",
          borderTop: "4px solid #C57B57",
          borderRadius: "50%",
          animation: "spin 1s linear infinite"
        }}></div>
        <p style={{
          marginTop: "2rem",
          fontSize: "0.875rem",
          color: "#999"
        }}>
          如果頁面沒有自動跳轉，請點擊 <a href="/" style={{ color: "#C57B57", textDecoration: "underline" }}>這裡</a>
        </p>
      </div>
      <style jsx>{`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
    </main>
  );
}
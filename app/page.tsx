"use client";
import { useEffect, useState } from "react";

export default function HomePage() {
  const [checking, setChecking] = useState(true);
  const [authenticated, setAuthenticated] = useState(false);

  useEffect(() => {
    checkAuth();
  }, []);

  async function checkAuth() {
    try {
      const response = await fetch('/api/auth/me');
      const data = await response.json();
      
      if (data.authenticated) {
        // 已登入，直接進入遊戲
        window.location.href = "/game-play";
      } else {
        // 未登入，顯示登入頁面
        setAuthenticated(false);
        setChecking(false);
      }
    } catch (error) {
      console.error('檢查登入狀態失敗:', error);
      setAuthenticated(false);
      setChecking(false);
    }
  }

  function handleLineLogin() {
    window.location.href = "/api/auth/line/login";
  }

  function handleGuestPlay() {
    window.location.href = "/game-play";
  }

  // 檢查中
  if (checking) {
    return (
      <main style={{
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        background: "#F4E8D8",
        fontFamily: "Noto Sans TC, sans-serif"
      }}>
        <div style={{ textAlign: "center" }}>
          <h1 style={{ fontSize: "2rem", marginBottom: "1rem", color: "#1C1C1C" }}>
            🧠 解剖咬一口
          </h1>
          <p style={{ color: "#666" }}>檢查登入狀態...</p>
        </div>
      </main>
    );
  }

  // 登入頁面
  return (
    <main style={{
      minHeight: "100vh",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      padding: "24px",
      background: "#F4E8D8",
      fontFamily: "Noto Sans TC, sans-serif"
    }}>
      <div style={{
        background: "white",
        borderRadius: "16px",
        padding: "40px",
        maxWidth: "500px",
        width: "100%",
        boxShadow: "0 4px 20px rgba(0,0,0,0.1)",
        textAlign: "center"
      }}>
        {/* Logo/標題 */}
        <div style={{ marginBottom: "30px" }}>
          <h1 style={{
            fontSize: "2.5rem",
            fontWeight: "bold",
            color: "#1C1C1C",
            marginBottom: "0.5rem"
          }}>
            🧠 解剖咬一口
          </h1>
          <p style={{
            fontSize: "1.1rem",
            color: "#666",
            margin: 0
          }}>
            Anatomy Bite
          </p>
        </div>

        {/* 描述 */}
        <p style={{
          fontSize: "1rem",
          color: "#666",
          marginBottom: "30px",
          lineHeight: "1.6"
        }}>
          每天學一點解剖、咬一口文獻！<br />
          遊戲化學習，14個等級等你挑戰
        </p>

        {/* 登入按鈕 */}
        <div style={{ marginBottom: "20px" }}>
          <button
            onClick={handleLineLogin}
            style={{
              width: "100%",
              padding: "15px 30px",
              background: "linear-gradient(135deg, #00C300, #00A000)",
              color: "white",
              border: "none",
              borderRadius: "12px",
              fontSize: "1.1rem",
              fontWeight: "bold",
              cursor: "pointer",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              gap: "10px",
              transition: "transform 0.2s"
            }}
            onMouseOver={(e) => e.currentTarget.style.transform = "translateY(-2px)"}
            onMouseOut={(e) => e.currentTarget.style.transform = "translateY(0)"}
          >
            <span style={{ fontSize: "1.3rem" }}>📱</span>
            使用 LINE 登入
          </button>
        </div>

        {/* 分隔線 */}
        <div style={{
          display: "flex",
          alignItems: "center",
          margin: "20px 0",
          color: "#999"
        }}>
          <div style={{ flex: 1, height: "1px", background: "#ddd" }}></div>
          <span style={{ padding: "0 15px", fontSize: "0.9rem" }}>或</span>
          <div style={{ flex: 1, height: "1px", background: "#ddd" }}></div>
        </div>

        {/* 訪客按鈕 */}
        <button
          onClick={handleGuestPlay}
          style={{
            width: "100%",
            padding: "15px 30px",
            background: "#C57B57",
            color: "white",
            border: "none",
            borderRadius: "12px",
            fontSize: "1.1rem",
            fontWeight: "bold",
            cursor: "pointer",
            transition: "all 0.2s"
          }}
          onMouseOver={(e) => {
            e.currentTarget.style.background = "#B85C38";
            e.currentTarget.style.transform = "translateY(-2px)";
          }}
          onMouseOut={(e) => {
            e.currentTarget.style.background = "#C57B57";
            e.currentTarget.style.transform = "translateY(0)";
          }}
        >
          🎮 訪客遊玩（不保存進度）
        </button>

        {/* 功能介紹 */}
        <div style={{
          marginTop: "30px",
          display: "grid",
          gridTemplateColumns: "repeat(3, 1fr)",
          gap: "20px",
          textAlign: "center"
        }}>
          <div>
            <div style={{ fontSize: "2rem", marginBottom: "5px" }}>⚡</div>
            <div style={{ fontSize: "0.85rem", color: "#666" }}>即時回饋</div>
          </div>
          <div>
            <div style={{ fontSize: "2rem", marginBottom: "5px" }}>🏆</div>
            <div style={{ fontSize: "0.85rem", color: "#666" }}>遊戲化學習</div>
          </div>
          <div>
            <div style={{ fontSize: "2rem", marginBottom: "5px" }}>📊</div>
            <div style={{ fontSize: "0.85rem", color: "#666" }}>進度追蹤</div>
          </div>
        </div>
      </div>
    </main>
  );
}
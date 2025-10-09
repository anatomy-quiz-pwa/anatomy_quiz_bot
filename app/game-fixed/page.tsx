"use client";
import { useEffect, useState } from "react";

export default function GameFixedPage() {
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    setIsLoaded(true);
  }, []);

  if (!isLoaded) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '100vh',
        fontFamily: 'ui-sans-serif'
      }}>
        <h2>正在載入遊戲...</h2>
      </div>
    );
  }

  return (
    <div>
      {/* 內嵌 HTML 內容，確保 LINE 登入按鈕可以正常工作 */}
      <iframe
        src="/public/index.html"
        style={{
          width: "100%",
          height: "100vh",
          border: "none",
          display: "block"
        }}
        title="解剖咬一口遊戲"
      />
      
      {/* 備用方案：如果 iframe 不工作，顯示直接連結 */}
      <div style={{
        position: "fixed",
        top: "10px",
        right: "10px",
        zIndex: 1000,
        backgroundColor: "rgba(0,0,0,0.8)",
        color: "white",
        padding: "10px",
        borderRadius: "5px"
      }}>
        <p>如果遊戲無法載入，請點擊：</p>
        <a 
          href="/public/index.html" 
          target="_blank"
          style={{ color: "#00C300", textDecoration: "underline" }}
        >
          在新視窗中開啟
        </a>
      </div>
    </div>
  );
}

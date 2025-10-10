"use client";
import { useEffect } from "react";

export default function GamePage() {
  useEffect(() => {
    // 重定向到靜態 HTML 文件
    window.location.href = '/index.html';
  }, []);

  return (
    <div style={{ 
      display: 'flex', 
      justifyContent: 'center', 
      alignItems: 'center', 
      height: '100vh',
      fontFamily: 'ui-sans-serif',
      backgroundColor: '#F4E8D8'
    }}>
      <div style={{
        textAlign: 'center',
        padding: '40px',
        backgroundColor: '#fffaf5',
        border: '3px solid #1C1C1C',
        borderRadius: '16px',
        boxShadow: '8px 8px 0 #1C1C1C'
      }}>
        <h2 style={{ color: '#1C1C1C', marginBottom: '20px' }}>🎮 正在載入遊戲...</h2>
        <p style={{ color: '#666', marginBottom: '20px' }}>如果沒有自動跳轉，請點擊：</p>
        <a 
          href="/index.html" 
          style={{
            display: 'inline-block',
            padding: '15px 30px',
            backgroundColor: '#C57B57',
            color: 'white',
            textDecoration: 'none',
            borderRadius: '8px',
            fontWeight: 'bold',
            border: '2px solid #1C1C1C',
            boxShadow: '3px 3px 0 #1C1C1C'
          }}
        >
          🚀 手動進入遊戲
        </a>
      </div>
    </div>
  );
}

"use client";
import { useEffect } from "react";

export default function GamePage() {
  useEffect(() => {
    // 重定向到靜態 HTML 文件
    window.location.href = '/public/index.html';
  }, []);

  return (
    <div style={{ 
      display: 'flex', 
      justifyContent: 'center', 
      alignItems: 'center', 
      height: '100vh',
      fontFamily: 'ui-sans-serif'
    }}>
      <div>
        <h2>正在載入遊戲...</h2>
        <p>如果沒有自動跳轉，請點擊：</p>
        <a 
          href="/public/index.html" 
          style={{
            display: 'inline-block',
            padding: '10px 20px',
            backgroundColor: '#C57B57',
            color: 'white',
            textDecoration: 'none',
            borderRadius: '8px'
          }}
        >
          手動進入遊戲
        </a>
      </div>
    </div>
  );
}

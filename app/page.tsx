"use client";
import { useEffect, useState } from "react";

export default function Page() {
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);
  }, []);

  if (!isClient) {
    return (
      <main style={{padding:24, fontFamily:"ui-sans-serif"}}>
        <h1>載入中...</h1>
      </main>
    );
  }

  return (
    <main style={{padding:24, fontFamily:"ui-sans-serif"}}>
      <div style={{maxWidth: "800px", margin: "0 auto"}}>
        <h1>解剖咬一口 Anatomy Bite</h1>
        <p>遊戲化問答系統</p>
        
        <div style={{margin: "20px 0", padding: "20px", border: "2px solid #1C1C1C", borderRadius: "12px", backgroundColor: "#fffaf5"}}>
          <h3>🎮 開始遊戲</h3>
          <p>請選擇登入方式：</p>
          
          <div style={{margin: "20px 0"}}>
            <a 
              href="/liff" 
              style={{
                display: "inline-block",
                padding: "15px 30px",
                backgroundColor: "#00C300",
                color: "white",
                textDecoration: "none",
                borderRadius: "8px",
                fontWeight: "bold",
                marginRight: "10px"
              }}
            >
              🔗 使用 LINE 登入 (LIFF)
            </a>
            
            <a 
              href="/game-direct" 
              style={{
                display: "inline-block",
                padding: "15px 30px",
                backgroundColor: "#C57B57",
                color: "white",
                textDecoration: "none",
                borderRadius: "8px",
                fontWeight: "bold",
                marginRight: "10px"
              }}
            >
              🎯 修復版遊戲
            </a>
            
            <a 
              href="/game-fixed" 
              style={{
                display: "inline-block",
                padding: "15px 30px",
                backgroundColor: "#28a745",
                color: "white",
                textDecoration: "none",
                borderRadius: "8px",
                fontWeight: "bold",
                marginRight: "10px"
              }}
            >
              🔧 備用版本
            </a>
            
            <a 
              href="/game-redesign" 
              style={{
                display: "inline-block",
                padding: "15px 30px",
                backgroundColor: "#8B4513",
                color: "white",
                textDecoration: "none",
                borderRadius: "8px",
                fontWeight: "bold",
                marginRight: "10px"
              }}
            >
              🎨 新設計版本
            </a>
            
            <a 
              href="/game-complete" 
              style={{
                display: "inline-block",
                padding: "15px 30px",
                backgroundColor: "#DC143C",
                color: "white",
                textDecoration: "none",
                borderRadius: "8px",
                fontWeight: "bold",
                marginRight: "10px"
              }}
            >
              🚀 完整功能版本
            </a>
            
            <a 
              href="/game-simple" 
              style={{
                display: "inline-block",
                padding: "15px 30px",
                backgroundColor: "#FF6B35",
                color: "white",
                textDecoration: "none",
                borderRadius: "8px",
                fontWeight: "bold",
                marginRight: "10px"
              }}
            >
              🎯 簡化版本 (直接顯示題目)
            </a>
            
            <a 
              href="/game-test" 
              style={{
                display: "inline-block",
                padding: "15px 30px",
                backgroundColor: "#9B59B6",
                color: "white",
                textDecoration: "none",
                borderRadius: "8px",
                fontWeight: "bold"
              }}
            >
              🧪 測試版本 (無組件依賴)
            </a>
          </div>
        </div>

        <div style={{margin: "20px 0", padding: "20px", border: "2px solid #1C1C1C", borderRadius: "12px", backgroundColor: "#f8f9fa"}}>
          <h3>📋 功能說明</h3>
          <ul>
            <li><strong>LINE LIFF 登入：</strong> 使用 LINE 帳號登入，數據會與 LINE Bot 同步</li>
            <li><strong>直接遊戲：</strong> 無需登入即可開始遊戲，適合快速體驗</li>
            <li><strong>14 個等級：</strong> 從解剖新手到解剖學傳說</li>
            <li><strong>即時回饋：</strong> 答題後立即查看詳細解釋</li>
          </ul>
        </div>
      </div>
    </main>
  );
}

"use client";
import { useEffect, useState } from "react";

declare global {
  interface Window {
    supabase: any;
    lineLogin: () => void;
    testLineLogin: () => void;
  }
}

export default function GameDirectPage() {
  const [gameState, setGameState] = useState({
    userId: null,
    nickname: '遊客',
    currentLevel: 1,
    score: 0,
    correctAnswers: 0,
    totalAnswers: 0,
    streak: 0,
    isLoggedIn: false
  });

  const [status, setStatus] = useState("載入中...");

  useEffect(() => {
    // 動態載入 Supabase 和遊戲腳本
    const loadScripts = async () => {
      try {
        // 載入 Supabase
        if (!window.supabase) {
          const supabaseScript = document.createElement('script');
          supabaseScript.src = 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2';
          document.head.appendChild(supabaseScript);
          
          await new Promise((resolve) => {
            supabaseScript.onload = resolve;
          });
        }

        // 初始化 LINE 登入函數
        window.lineLogin = () => {
          console.log('🖱️ LINE 登入按鈕被點擊');
          setStatus("LINE 登入功能已觸發");
          alert("LINE 登入功能已觸發！請檢查控制台日誌。");
        };

        window.testLineLogin = () => {
          console.log('🧪 測試 LINE 登入');
          setStatus("測試功能已觸發");
          alert("測試功能已觸發！");
        };

        setStatus("準備就緒");
      } catch (error) {
        console.error('載入腳本失敗:', error);
        setStatus("載入失敗");
      }
    };

    loadScripts();
  }, []);

  return (
    <div style={{
      fontFamily: "'Noto Sans TC', sans-serif",
      backgroundColor: "#F4E8D8",
      minHeight: "100vh",
      padding: "20px"
    }}>
      <div style={{
        maxWidth: "900px",
        margin: "0 auto",
        backgroundColor: "#fffaf5",
        border: "3px solid #1C1C1C",
        boxShadow: "8px 8px 0 #1C1C1C",
        borderRadius: "16px",
        overflow: "hidden"
      }}>
        {/* 標題區 */}
        <div style={{
          background: "#C57B57",
          color: "#fffaf5",
          borderBottom: "3px solid #1C1C1C",
          padding: "30px",
          textAlign: "center"
        }}>
          <h1 style={{
            color: "#fffaf5",
            textShadow: "2px 2px 0 #1C1C1C",
            fontWeight: "700",
            margin: "0",
            fontSize: "2.5rem"
          }}>
            🧠 解剖咬一口 Anatomy Bite
          </h1>
          <p style={{ color: "#fffaf5", opacity: 0.95 }}>
            每天學一點解剖、咬一口文獻！
          </p>
        </div>

        {/* 統計欄 */}
        <div style={{
          display: "flex",
          justifyContent: "space-around",
          background: "#B85C38",
          color: "#fffaf5",
          borderBottom: "3px solid #1C1C1C",
          padding: "20px",
          margin: "0"
        }}>
          <div style={{ textAlign: "center" }}>
            <span style={{ fontSize: "2rem", fontWeight: "bold", color: "#fffaf5", display: "block" }}>
              {gameState.score}
            </span>
            <span style={{ color: "#fffaf5", fontSize: "0.9rem", opacity: 0.9 }}>總分</span>
          </div>
          <div style={{ textAlign: "center" }}>
            <span style={{ fontSize: "2rem", fontWeight: "bold", color: "#fffaf5", display: "block" }}>
              {gameState.currentLevel}
            </span>
            <span style={{ color: "#fffaf5", fontSize: "0.9rem", opacity: 0.9 }}>等級</span>
          </div>
          <div style={{ textAlign: "center" }}>
            <span style={{ fontSize: "2rem", fontWeight: "bold", color: "#fffaf5", display: "block" }}>
              {gameState.correctAnswers}/{gameState.totalAnswers}
            </span>
            <span style={{ color: "#fffaf5", fontSize: "0.9rem", opacity: 0.9 }}>答對率</span>
          </div>
          <div style={{ textAlign: "center" }}>
            <span style={{ fontSize: "2rem", fontWeight: "bold", color: "#fffaf5", display: "block" }}>
              {gameState.streak}
            </span>
            <span style={{ color: "#fffaf5", fontSize: "0.9rem", opacity: 0.9 }}>連續答對</span>
          </div>
        </div>

        {/* 遊戲內容 */}
        <div style={{ padding: "40px" }}>
          <div style={{
            textAlign: "center",
            padding: "60px 40px"
          }}>
            <div style={{
              background: "#fffaf5",
              border: "2px solid #1C1C1C",
              boxShadow: "4px 4px 0 #1C1C1C",
              borderRadius: "12px",
              padding: "2rem",
              margin: "20px 0"
            }}>
              <div style={{ marginBottom: "20px" }}>
                <img 
                  src="https://ciqlfqfgzqqgdrogedxg.supabase.co/storage/v1/object/public/linebot/opening.png" 
                  alt="解剖咬一口開場圖片" 
                  style={{
                    maxWidth: "300px",
                    height: "auto",
                    borderRadius: "15px",
                    boxShadow: "0 10px 30px rgba(0,0,0,0.2)"
                  }}
                />
              </div>
              
              <div style={{ display: "flex", justifyContent: "space-around", marginBottom: "20px" }}>
                <div style={{ textAlign: "center" }}>
                  <div style={{ fontSize: "3rem", color: "#ffc107", marginBottom: "10px" }}>⚡</div>
                  <h5>即時回饋</h5>
                  <p style={{ color: "#6c757d" }}>答題後立即知道結果</p>
                </div>
                <div style={{ textAlign: "center" }}>
                  <div style={{ fontSize: "3rem", color: "#28a745", marginBottom: "10px" }}>🏆</div>
                  <h5>遊戲化學習</h5>
                  <p style={{ color: "#6c757d" }}>14個等級等你挑戰</p>
                </div>
                <div style={{ textAlign: "center" }}>
                  <div style={{ fontSize: "3rem", color: "#007bff", marginBottom: "10px" }}>📈</div>
                  <h5>進度追蹤</h5>
                  <p style={{ color: "#6c757d" }}>實時查看你的學習成果</p>
                </div>
              </div>

              {/* LINE 登入區域 */}
              <div style={{ marginBottom: "20px" }}>
                <div style={{ marginBottom: "10px" }}>
                  <button
                    onClick={() => window.lineLogin?.()}
                    style={{
                      background: "linear-gradient(135deg, #00C300, #00A000)",
                      color: "white",
                      border: "2px solid #1C1C1C",
                      borderRadius: "8px",
                      fontWeight: "bold",
                      padding: "15px 40px",
                      fontSize: "1.2rem",
                      cursor: "pointer",
                      pointerEvents: "auto",
                      transition: "all 0.2s ease",
                      boxShadow: "3px 3px 0 #1C1C1C",
                      fontFamily: "'Noto Sans TC', sans-serif"
                    }}
                    onMouseOver={(e) => {
                      e.currentTarget.style.background = "linear-gradient(135deg, #00A000, #008000)";
                      e.currentTarget.style.transform = "translate(-2px, -2px)";
                      e.currentTarget.style.boxShadow = "5px 5px 0 #1C1C1C";
                    }}
                    onMouseOut={(e) => {
                      e.currentTarget.style.background = "linear-gradient(135deg, #00C300, #00A000)";
                      e.currentTarget.style.transform = "translate(0px, 0px)";
                      e.currentTarget.style.boxShadow = "3px 3px 0 #1C1C1C";
                    }}
                  >
                    📱 使用 LINE 登入
                  </button>
                  
                  {/* 測試按鈕 */}
                  <button
                    onClick={() => window.testLineLogin?.()}
                    style={{
                      background: "#17a2b8",
                      color: "white",
                      border: "1px solid #1C1C1C",
                      borderRadius: "4px",
                      padding: "5px 10px",
                      marginLeft: "10px",
                      cursor: "pointer",
                      fontSize: "0.8rem"
                    }}
                  >
                    🧪 測試
                  </button>
                </div>
                <p style={{ color: "#6c757d", fontSize: "0.9rem" }}>或</p>
              </div>

              <div style={{ marginBottom: "20px" }}>
                <input
                  type="text"
                  placeholder="請輸入你的暱稱（選填）"
                  maxLength={20}
                  style={{
                    width: "100%",
                    padding: "15px",
                    border: "2px solid #1C1C1C",
                    borderRadius: "8px",
                    backgroundColor: "#fffaf5",
                    color: "#1C1C1C",
                    fontSize: "1rem",
                    fontFamily: "'Noto Sans TC', sans-serif"
                  }}
                />
              </div>

              <button
                onClick={() => alert("開始遊戲功能")}
                style={{
                  backgroundColor: "#C57B57",
                  color: "#fffaf5",
                  border: "2px solid #1C1C1C",
                  borderRadius: "8px",
                  fontWeight: "bold",
                  padding: "15px 40px",
                  fontSize: "1.2rem",
                  cursor: "pointer",
                  transition: "all 0.2s ease",
                  boxShadow: "3px 3px 0 #1C1C1C",
                  fontFamily: "'Noto Sans TC', sans-serif"
                }}
                onMouseOver={(e) => {
                  e.currentTarget.style.backgroundColor = "#B85C38";
                  e.currentTarget.style.transform = "translate(-2px, -2px)";
                  e.currentTarget.style.boxShadow = "5px 5px 0 #1C1C1C";
                }}
                onMouseOut={(e) => {
                  e.currentTarget.style.backgroundColor = "#C57B57";
                  e.currentTarget.style.transform = "translate(0px, 0px)";
                  e.currentTarget.style.boxShadow = "3px 3px 0 #1C1C1C";
                }}
              >
                🎮 開始遊戲
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* 狀態顯示 */}
      <div style={{
        position: "fixed",
        bottom: "20px",
        left: "20px",
        backgroundColor: "rgba(0,0,0,0.8)",
        color: "white",
        padding: "10px 15px",
        borderRadius: "5px",
        fontSize: "0.9rem"
      }}>
        狀態: {status}
      </div>
    </div>
  );
}

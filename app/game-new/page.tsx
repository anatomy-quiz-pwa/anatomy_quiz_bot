"use client";
import { useEffect, useState } from "react";

interface UserStats {
  total_correct: number;
  streak: number;
  level: number;
}

interface UserData {
  user_id: string;
  stats: UserStats;
}

export default function GameNewPage() {
  const [userData, setUserData] = useState<UserData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isInLine, setIsInLine] = useState(false);

  useEffect(() => {
    // 檢測是否在 LINE 內
    const userAgent = navigator.userAgent.toLowerCase();
    const isLineApp = userAgent.includes('line/');
    setIsInLine(isLineApp);

    if (isLineApp) {
      // 情境 A：在 LINE 內，使用 LIFF
      initLiff();
    } else {
      // 情境 B：一般瀏覽器，檢查現有 session
      checkSession();
    }
  }, []);

  const initLiff = async () => {
    try {
      // 動態載入 LIFF SDK
      const script = document.createElement('script');
      script.src = 'https://static.line-scdn.net/liff/edge/2/sdk.js';
      script.async = true;
      document.head.appendChild(script);

      script.onload = async () => {
        try {
          // @ts-ignore
          await window.liff.init({ liffId: process.env.NEXT_PUBLIC_LIFF_ID || '填你的 LIFF_ID' });

          // @ts-ignore
          if (!window.liff.isLoggedIn()) {
            // @ts-ignore
            window.liff.login();
            return;
          }

          // @ts-ignore
          const idToken = window.liff.getIDToken();
          if (!idToken) {
            setError('無法取得 LINE 登入憑證');
            setLoading(false);
            return;
          }

          // 送給後端驗簽 + 建/查 user + 設網站 Session Cookie
          const res = await fetch('/api/auth/line/verify', {
            method: 'POST',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify({ idToken })
          });

          if (res.ok) {
            // 現在網站已有 HttpOnly Session Cookie，取得用戶資料
            await loadUserData();
          } else {
            setError('LINE 登入失敗，請重試');
            setLoading(false);
          }
        } catch (error) {
          console.error('LIFF 初始化失敗:', error);
          setError('LINE 登入失敗');
          setLoading(false);
        }
      };
    } catch (error) {
      console.error('載入 LIFF SDK 失敗:', error);
      setError('載入 LINE 登入功能失敗');
      setLoading(false);
    }
  };

  const checkSession = async () => {
    await loadUserData();
  };

  const loadUserData = async () => {
    try {
      const res = await fetch('/api/me/stats', { 
        credentials: 'include' 
      });
      
      if (res.ok) {
        const data = await res.json();
        setUserData(data);
      } else if (res.status === 401) {
        // 未登入，顯示登入按鈕
        setUserData(null);
      } else {
        setError('載入用戶資料失敗');
      }
    } catch (error) {
      console.error('載入用戶資料失敗:', error);
      setError('載入用戶資料失敗');
    } finally {
      setLoading(false);
    }
  };

  const handleLineLogin = () => {
    window.location.href = '/api/auth/line/login';
  };

  if (loading) {
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
          <h2 style={{ color: '#1C1C1C', marginBottom: '20px' }}>
            {isInLine ? '🔐 LINE 登入中...' : '⏳ 載入中...'}
          </h2>
          <p style={{ color: '#666' }}>請稍候</p>
        </div>
      </div>
    );
  }

  if (error) {
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
          <h2 style={{ color: '#dc2626', marginBottom: '20px' }}>❌ 錯誤</h2>
          <p style={{ color: '#666', marginBottom: '20px' }}>{error}</p>
          <button 
            onClick={() => window.location.reload()}
            style={{
              padding: '15px 30px',
              backgroundColor: '#C57B57',
              color: 'white',
              border: '2px solid #1C1C1C',
              borderRadius: '8px',
              fontWeight: 'bold',
              boxShadow: '3px 3px 0 #1C1C1C',
              cursor: 'pointer'
            }}
          >
            🔄 重新載入
          </button>
        </div>
      </div>
    );
  }

  if (!userData) {
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
          <h2 style={{ color: '#1C1C1C', marginBottom: '20px' }}>🎮 歡迎來到解剖學問答</h2>
          <p style={{ color: '#666', marginBottom: '30px' }}>
            請使用 LINE 登入以開始遊戲
          </p>
          <button 
            onClick={handleLineLogin}
            style={{
              padding: '15px 30px',
              backgroundColor: '#00B900',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              fontWeight: 'bold',
              border: '2px solid #1C1C1C',
              boxShadow: '3px 3px 0 #1C1C1C',
              cursor: 'pointer',
              fontSize: '16px'
            }}
          >
            📱 用 LINE 登入
          </button>
        </div>
      </div>
    );
  }

  return (
    <div style={{ 
      minHeight: '100vh',
      fontFamily: 'ui-sans-serif',
      backgroundColor: '#F4E8D8',
      padding: '20px'
    }}>
      <div style={{
        maxWidth: '800px',
        margin: '0 auto',
        backgroundColor: '#fffaf5',
        border: '3px solid #1C1C1C',
        borderRadius: '16px',
        boxShadow: '8px 8px 0 #1C1C1C',
        padding: '30px'
      }}>
        <h1 style={{ 
          color: '#1C1C1C', 
          textAlign: 'center', 
          marginBottom: '30px',
          fontSize: '2rem'
        }}>
          🎮 解剖學問答遊戲
        </h1>

        <div style={{
          backgroundColor: '#f0f9ff',
          border: '2px solid #1C1C1C',
          borderRadius: '12px',
          padding: '20px',
          marginBottom: '30px'
        }}>
          <h2 style={{ color: '#1C1C1C', marginBottom: '15px' }}>📊 你的進度</h2>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '15px' }}>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#C57B57' }}>
                {userData.stats.total_correct}
              </div>
              <div style={{ color: '#666' }}>總答對題數</div>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#C57B57' }}>
                {userData.stats.streak}
              </div>
              <div style={{ color: '#666' }}>連續答對</div>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#C57B57' }}>
                {userData.stats.level}
              </div>
              <div style={{ color: '#666' }}>目前等級</div>
            </div>
          </div>
        </div>

        <div style={{ textAlign: 'center' }}>
          <button 
            onClick={() => window.location.href = '/index.html'}
            style={{
              padding: '20px 40px',
              backgroundColor: '#C57B57',
              color: 'white',
              border: 'none',
              borderRadius: '12px',
              fontWeight: 'bold',
              border: '3px solid #1C1C1C',
              boxShadow: '5px 5px 0 #1C1C1C',
              cursor: 'pointer',
              fontSize: '18px',
              marginRight: '15px'
            }}
          >
            🚀 開始遊戲
          </button>
          <button 
            onClick={() => window.location.href = '/leaderboard'}
            style={{
              padding: '20px 40px',
              backgroundColor: '#3B82F6',
              color: 'white',
              border: 'none',
              borderRadius: '12px',
              fontWeight: 'bold',
              border: '3px solid #1C1C1C',
              boxShadow: '5px 5px 0 #1C1C1C',
              cursor: 'pointer',
              fontSize: '18px'
            }}
          >
            🏆 排行榜
          </button>
        </div>

        <div style={{ 
          textAlign: 'center', 
          marginTop: '30px',
          padding: '15px',
          backgroundColor: '#fef3c7',
          border: '2px solid #1C1C1C',
          borderRadius: '8px'
        }}>
          <p style={{ color: '#666', margin: 0 }}>
            💡 提示：你的進度會自動同步到 LINE Bot
          </p>
        </div>
      </div>
    </div>
  );
}

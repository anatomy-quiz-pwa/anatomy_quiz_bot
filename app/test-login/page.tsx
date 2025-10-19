"use client";
import { useEffect, useState } from "react";

interface UserData {
  user_id: string;
  stats: {
    total_correct: number;
    streak: number;
    level: number;
  };
}

export default function TestLoginPage() {
  const [userData, setUserData] = useState<UserData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const checkSession = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const res = await fetch('/api/me/stats', { 
        credentials: 'include' 
      });
      
      if (res.ok) {
        const data = await res.json();
        setUserData(data);
      } else if (res.status === 401) {
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

  const handleLogout = async () => {
    try {
      await fetch('/api/auth/logout', { 
        method: 'POST',
        credentials: 'include'
      });
      setUserData(null);
    } catch (error) {
      console.error('登出失敗:', error);
    }
  };

  useEffect(() => {
    checkSession();
  }, []);

  return (
    <div style={{ 
      minHeight: '100vh',
      fontFamily: 'ui-sans-serif',
      backgroundColor: '#F4E8D8',
      padding: '20px'
    }}>
      <div style={{
        maxWidth: '600px',
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
          marginBottom: '30px'
        }}>
          🔐 登入測試頁面
        </h1>

        <div style={{ textAlign: 'center', marginBottom: '30px' }}>
          <button 
            onClick={checkSession}
            disabled={loading}
            style={{
              padding: '15px 30px',
              backgroundColor: loading ? '#ccc' : '#3B82F6',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              fontWeight: 'bold',
              border: '2px solid #1C1C1C',
              boxShadow: '3px 3px 0 #1C1C1C',
              cursor: loading ? 'not-allowed' : 'pointer',
              marginRight: '15px'
            }}
          >
            {loading ? '⏳ 檢查中...' : '🔍 檢查登入狀態'}
          </button>
        </div>

        {error && (
          <div style={{
            backgroundColor: '#fee2e2',
            border: '2px solid #dc2626',
            borderRadius: '8px',
            padding: '15px',
            marginBottom: '20px',
            color: '#dc2626'
          }}>
            ❌ {error}
          </div>
        )}

        {userData ? (
          <div style={{
            backgroundColor: '#f0f9ff',
            border: '2px solid #1C1C1C',
            borderRadius: '12px',
            padding: '20px',
            marginBottom: '20px'
          }}>
            <h2 style={{ color: '#1C1C1C', marginBottom: '15px' }}>✅ 已登入</h2>
            <p><strong>用戶 ID:</strong> {userData.user_id}</p>
            <p><strong>總答對題數:</strong> {userData.stats.total_correct}</p>
            <p><strong>連續答對:</strong> {userData.stats.streak}</p>
            <p><strong>目前等級:</strong> {userData.stats.level}</p>
            
            <div style={{ textAlign: 'center', marginTop: '20px' }}>
              <button 
                onClick={handleLogout}
                style={{
                  padding: '15px 30px',
                  backgroundColor: '#dc2626',
                  color: 'white',
                  border: 'none',
                  borderRadius: '8px',
                  fontWeight: 'bold',
                  border: '2px solid #1C1C1C',
                  boxShadow: '3px 3px 0 #1C1C1C',
                  cursor: 'pointer',
                  marginRight: '15px'
                }}
              >
                🚪 登出
              </button>
              <button 
                onClick={() => window.location.href = '/game-new'}
                style={{
                  padding: '15px 30px',
                  backgroundColor: '#C57B57',
                  color: 'white',
                  border: 'none',
                  borderRadius: '8px',
                  fontWeight: 'bold',
                  border: '2px solid #1C1C1C',
                  boxShadow: '3px 3px 0 #1C1C1C',
                  cursor: 'pointer'
                }}
              >
                🎮 進入遊戲
              </button>
            </div>
          </div>
        ) : (
          <div style={{
            backgroundColor: '#fef3c7',
            border: '2px solid #1C1C1C',
            borderRadius: '12px',
            padding: '20px',
            marginBottom: '20px'
          }}>
            <h2 style={{ color: '#1C1C1C', marginBottom: '15px' }}>❌ 未登入</h2>
            <p style={{ marginBottom: '20px' }}>請使用 LINE 登入以開始使用</p>
            
            <div style={{ textAlign: 'center' }}>
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
        )}

        <div style={{ 
          backgroundColor: '#f3f4f6',
          border: '2px solid #1C1C1C',
          borderRadius: '8px',
          padding: '15px',
          fontSize: '14px',
          color: '#666'
        }}>
          <h3 style={{ margin: '0 0 10px 0', color: '#1C1C1C' }}>測試說明：</h3>
          <ul style={{ margin: 0, paddingLeft: '20px' }}>
            <li>點擊「檢查登入狀態」查看當前登入狀態</li>
            <li>點擊「用 LINE 登入」進行 OIDC 登入流程</li>
            <li>登入成功後會顯示用戶資料和統計</li>
            <li>可以點擊「登出」清除登入狀態</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

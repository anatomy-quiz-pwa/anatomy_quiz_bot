"use client";
import { useEffect, useState } from 'react';

// Supabase 配置
const SUPABASE_URL = 'https://ciqlfqfgzqqgdrogedxg.supabase.co';
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA';

interface Question {
  id: number;
  question: string;
  options: string[];
  correct_answer: number;
  explanation: string;
  level: number;
  category: string;
  image_url: string;
  qimage_url: string;
}

export default function GamePlayPage() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [currentQuestion, setCurrentQuestion] = useState<Question | null>(null);
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null);
  const [showExplanation, setShowExplanation] = useState(false);
  const [score, setScore] = useState(0);
  const [totalAnswered, setTotalAnswered] = useState(0);
  const [correctAnswers, setCorrectAnswers] = useState(0);
  const [allQuestions, setAllQuestions] = useState<Question[]>([]);

  // 初始化並載入題目
  useEffect(() => {
    loadQuestions();
  }, []);

  async function loadQuestions() {
    try {
      setLoading(true);
      setError(null);
      
      // 動態載入 Supabase SDK
      const { createClient } = await import('@supabase/supabase-js');
      const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

      const { data, error: fetchError } = await supabase
        .from('anatomy_questions_v2')
        .select('*')
        .limit(50);

      if (fetchError) {
        throw new Error('載入題目失敗: ' + fetchError.message);
      }

      if (!data || data.length === 0) {
        throw new Error('題庫為空');
      }

      // 轉換數據格式
      const questions: Question[] = data.map(item => ({
        id: item.id,
        question: item.question,
        options: [
          item.option_1,
          item.option_2,
          item.option_3,
          item.option_4
        ].filter(opt => opt && opt.trim()),
        correct_answer: (item.correct_option || 1) - 1,
        explanation: item.explanation || '',
        level: item.level || 1,
        category: '解剖學',
        image_url: item.image_url || '',
        qimage_url: item.qimage_url || ''
      }));

      setAllQuestions(questions);
      // 隨機選擇第一題
      const randomIndex = Math.floor(Math.random() * questions.length);
      setCurrentQuestion(questions[randomIndex]);
      setLoading(false);
    } catch (err) {
      console.error('載入題目錯誤:', err);
      setError(err instanceof Error ? err.message : '載入失敗');
      setLoading(false);
    }
  }

  function selectAnswer(index: number) {
    if (showExplanation) return;
    setSelectedAnswer(index);
  }

  function submitAnswer() {
    if (selectedAnswer === null || !currentQuestion) return;

    const isCorrect = selectedAnswer === currentQuestion.correct_answer;
    
    setTotalAnswered(prev => prev + 1);
    if (isCorrect) {
      setCorrectAnswers(prev => prev + 1);
      setScore(prev => prev + 10);
    }
    
    setShowExplanation(true);
  }

  function nextQuestion() {
    if (allQuestions.length === 0) return;
    
    const randomIndex = Math.floor(Math.random() * allQuestions.length);
    setCurrentQuestion(allQuestions[randomIndex]);
    setSelectedAnswer(null);
    setShowExplanation(false);
  }

  // 載入中
  if (loading) {
    return (
      <div style={{ 
        minHeight: '100vh', 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'center',
        background: '#F4E8D8',
        fontFamily: 'Noto Sans TC, sans-serif'
      }}>
        <div style={{ textAlign: 'center' }}>
          <h1 style={{ fontSize: '2rem', marginBottom: '1rem' }}>🧠 解剖咬一口</h1>
          <p>正在載入題目...</p>
          <div style={{
            margin: '20px auto',
            width: '40px',
            height: '40px',
            border: '4px solid #f3f3f3',
            borderTop: '4px solid #C57B57',
            borderRadius: '50%',
            animation: 'spin 1s linear infinite'
          }}></div>
          <style jsx>{`
            @keyframes spin {
              0% { transform: rotate(0deg); }
              100% { transform: rotate(360deg); }
            }
          `}</style>
        </div>
      </div>
    );
  }

  // 錯誤狀態
  if (error) {
    return (
      <div style={{ 
        minHeight: '100vh', 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'center',
        background: '#F4E8D8',
        fontFamily: 'Noto Sans TC, sans-serif'
      }}>
        <div style={{ 
          textAlign: 'center',
          background: 'white',
          padding: '2rem',
          borderRadius: '12px',
          maxWidth: '500px'
        }}>
          <h2 style={{ color: '#DC3545' }}>⚠️ 載入失敗</h2>
          <p>{error}</p>
          <button 
            onClick={loadQuestions}
            style={{
              marginTop: '1rem',
              padding: '10px 20px',
              background: '#C57B57',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer'
            }}
          >
            重新載入
          </button>
        </div>
      </div>
    );
  }

  // 遊戲畫面
  if (!currentQuestion) {
    return <div>沒有題目</div>;
  }

  const accuracy = totalAnswered > 0 
    ? Math.round((correctAnswers / totalAnswered) * 100) 
    : 0;

  return (
    <div style={{
      minHeight: '100vh',
      background: '#F4E8D8',
      padding: '20px',
      fontFamily: 'Noto Sans TC, sans-serif'
    }}>
      {/* 頭部 */}
      <div style={{
        maxWidth: '900px',
        margin: '0 auto 20px',
        background: '#C57B57',
        color: 'white',
        padding: '20px',
        borderRadius: '12px',
        textAlign: 'center'
      }}>
        <h1 style={{ margin: 0, fontSize: '1.8rem' }}>🧠 解剖咬一口</h1>
      </div>

      {/* 統計欄 */}
      <div style={{
        maxWidth: '900px',
        margin: '0 auto 20px',
        background: '#B85C38',
        color: 'white',
        padding: '15px',
        borderRadius: '12px',
        display: 'flex',
        justifyContent: 'space-around',
        textAlign: 'center'
      }}>
        <div>
          <div style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>{score}</div>
          <div style={{ fontSize: '0.9rem' }}>總分</div>
        </div>
        <div>
          <div style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>{correctAnswers}/{totalAnswered}</div>
          <div style={{ fontSize: '0.9rem' }}>答對率 {accuracy}%</div>
        </div>
      </div>

      {/* 題目卡片 */}
      <div style={{
        maxWidth: '900px',
        margin: '0 auto',
        background: 'white',
        padding: '30px',
        borderRadius: '12px',
        boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
      }}>
        <div style={{ marginBottom: '20px' }}>
          <span style={{
            background: '#8B4513',
            color: 'white',
            padding: '5px 15px',
            borderRadius: '15px',
            fontSize: '0.9rem'
          }}>
            等級 {currentQuestion.level} • {currentQuestion.category}
          </span>
        </div>

        {/* 題目圖片 */}
        {currentQuestion.qimage_url && (
          <img 
            src={currentQuestion.qimage_url} 
            alt="題目圖片"
            style={{
              width: '100%',
              maxHeight: '400px',
              objectFit: 'cover',
              borderRadius: '8px',
              marginBottom: '20px'
            }}
          />
        )}

        {/* 題目文字 */}
        <h2 style={{
          fontSize: '1.5rem',
          marginBottom: '25px',
          lineHeight: '1.6'
        }}>
          {currentQuestion.question}
        </h2>

        {/* 選項 */}
        <div style={{ marginBottom: '20px' }}>
          {currentQuestion.options.map((option, index) => {
            const isSelected = selectedAnswer === index;
            const isCorrect = index === currentQuestion.correct_answer;
            const showResult = showExplanation;
            
            let backgroundColor = '#fffaf5';
            let color = '#1C1C1C';
            
            if (showResult) {
              if (isCorrect) {
                backgroundColor = '#4caf50';
                color = 'white';
              } else if (isSelected && !isCorrect) {
                backgroundColor = '#f44336';
                color = 'white';
              }
            } else if (isSelected) {
              backgroundColor = '#C57B57';
              color = 'white';
            }

            return (
              <button
                key={index}
                onClick={() => selectAnswer(index)}
                disabled={showExplanation}
                style={{
                  width: '100%',
                  padding: '18px',
                  margin: '10px 0',
                  background: backgroundColor,
                  color: color,
                  border: '2px solid #1C1C1C',
                  borderRadius: '10px',
                  fontSize: '1.1rem',
                  textAlign: 'left',
                  cursor: showExplanation ? 'default' : 'pointer',
                  transition: 'all 0.3s'
                }}
              >
                {String.fromCharCode(65 + index)}. {option}
              </button>
            );
          })}
        </div>

        {/* 解釋區域 */}
        {showExplanation && (
          <div style={{
            background: '#F4E8D8',
            padding: '20px',
            borderRadius: '10px',
            marginTop: '20px',
            borderLeft: '5px solid #B85C38'
          }}>
            <h3 style={{ marginTop: 0 }}>💡 詳細解釋</h3>
            {currentQuestion.image_url && (
              <img 
                src={currentQuestion.image_url} 
                alt="解釋圖片"
                style={{
                  width: '100%',
                  maxHeight: '300px',
                  objectFit: 'cover',
                  borderRadius: '8px',
                  marginBottom: '15px'
                }}
              />
            )}
            <p style={{ lineHeight: '1.6', margin: 0 }}>
              {currentQuestion.explanation}
            </p>
          </div>
        )}

        {/* 按鈕區 */}
        <div style={{ marginTop: '25px', textAlign: 'center' }}>
          {!showExplanation ? (
            <button
              onClick={submitAnswer}
              disabled={selectedAnswer === null}
              style={{
                padding: '15px 40px',
                background: selectedAnswer !== null ? '#C57B57' : '#ccc',
                color: 'white',
                border: 'none',
                borderRadius: '8px',
                fontSize: '1.1rem',
                cursor: selectedAnswer !== null ? 'pointer' : 'not-allowed',
                fontWeight: 'bold'
              }}
            >
              ✓ 提交答案
            </button>
          ) : (
            <button
              onClick={nextQuestion}
              style={{
                padding: '15px 40px',
                background: '#C57B57',
                color: 'white',
                border: 'none',
                borderRadius: '8px',
                fontSize: '1.1rem',
                cursor: 'pointer',
                fontWeight: 'bold'
              }}
            >
              ➡️ 下一題
            </button>
          )}
        </div>
      </div>
    </div>
  );
}


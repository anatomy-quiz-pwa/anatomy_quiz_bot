"use client";
import { useState, useEffect } from "react";
import ProgressSection from "../components/ProgressSection";
import QuestionCard from "../components/QuestionCard";
import UserProfile from "../components/UserProfile";
import Leaderboard from "../components/Leaderboard";
import LearningStats from "../components/LearningStats";

interface Question {
  id: number;
  category: string;
  question: string;
  imageUrl?: string;
  options: string[];
  correctAnswer: number;
  explanation: string;
  level: number;
}

export default function GameSimplePage() {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [totalQuestions] = useState(3);
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null);
  const [timeLeft, setTimeLeft] = useState(300); // 5 minutes
  const [userLevel, setUserLevel] = useState(15);
  const [consecutiveDays, setConsecutiveDays] = useState(47);
  const [totalScore, setTotalScore] = useState(1234);
  const [showExplanation, setShowExplanation] = useState(false);
  const [isCorrect, setIsCorrect] = useState<boolean | null>(null);
  const [score, setScore] = useState(0);
  const [correctAnswers, setCorrectAnswers] = useState(0);

  // 模擬題目數據庫
  const questions: Question[] = [
    {
      id: 1,
      category: "骨骼系統",
      question: "圖中標示的骨骼結構是人體頭骨的哪一個部分？",
      imageUrl: "https://via.placeholder.com/400x300/cccccc/666666?text=頭骨解剖圖",
      options: [
        "額骨 (Frontal bone)",
        "頂骨 (Parietal bone)", 
        "顳骨 (Temporal bone)",
        "枕骨 (Occipital bone)"
      ],
      correctAnswer: 0,
      explanation: "額骨位於頭骨的前部，形成前額和眼眶的上緣。它是顱骨的重要組成部分，保護大腦前葉。",
      level: 1
    },
    {
      id: 2,
      category: "循環系統",
      question: "人體心臟有多少個心腔？",
      options: [
        "2個",
        "3個", 
        "4個",
        "5個"
      ],
      correctAnswer: 2,
      explanation: "人體心臟有4個心腔：左心房、右心房、左心室、右心室。心房負責接收血液，心室負責泵出血液。",
      level: 1
    },
    {
      id: 3,
      category: "神經系統",
      question: "人體最大的神經是什麼？",
      options: [
        "視神經",
        "聽神經", 
        "坐骨神經",
        "迷走神經"
      ],
      correctAnswer: 2,
      explanation: "坐骨神經是人體最大的神經，從腰椎和骶椎發出，延伸至下肢，負責下肢的感覺和運動功能。",
      level: 2
    }
  ];

  const currentQuestion = questions[currentQuestionIndex] || questions[0];

  // 排行榜數據
  const leaderboardData = [
    { rank: 1, name: "李醫師", score: 2456, avatar: "https://via.placeholder.com/40x40/cccccc/666666?text=李" },
    { rank: 2, name: "王護士", score: 2103, avatar: "https://via.placeholder.com/40x40/cccccc/666666?text=王" },
    { rank: 3, name: "陳醫師 (你)", score: totalScore, avatar: "https://via.placeholder.com/40x40/cccccc/666666?text=陳", isCurrentUser: true }
  ];

  // 計時器效果
  useEffect(() => {
    const timer = setInterval(() => {
      setTimeLeft(prev => {
        if (prev <= 0) {
          clearInterval(timer);
          handleTimeUp();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const handleAnswerSelect = (index: number) => {
    if (showExplanation) return;
    setSelectedAnswer(index);
  };

  const handleSubmitAnswer = () => {
    if (selectedAnswer === null) return;
    
    const correct = selectedAnswer === currentQuestion.correctAnswer;
    setIsCorrect(correct);
    setShowExplanation(true);
    
    if (correct) {
      setScore(prev => prev + 10);
      setCorrectAnswers(prev => prev + 1);
    }
  };

  const handleNextQuestion = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(prev => prev + 1);
      setSelectedAnswer(null);
      setShowExplanation(false);
      setIsCorrect(null);
      setTimeLeft(300); // 重置計時器
    } else {
      // 遊戲結束
      alert(`遊戲結束！\n總分：${score}\n答對：${correctAnswers}/${questions.length}`);
    }
  };

  const handleTimeUp = () => {
    setShowExplanation(true);
    setIsCorrect(false);
    alert("時間到！");
  };

  const handleViewFullLeaderboard = () => {
    console.log("查看完整排行榜");
  };

  return (
    <div className="min-h-screen bg-[#F4E8D8] p-5">
      <div className="max-w-7xl mx-auto">
        {/* 頭部導航 */}
        <header className="bg-[#C57B57] text-white p-4 rounded-t-lg border-2 border-[#1C1C1C] border-b-0">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-white rounded-full flex items-center justify-center">
                <span className="text-[#C57B57] text-lg">🦷</span>
              </div>
              <h1 className="text-2xl font-bold">解剖咬一口</h1>
            </div>
            <nav className="flex items-center space-x-6">
              <div className="flex items-center space-x-2 cursor-pointer hover:bg-[#B85C38] px-3 py-2 rounded">
                <span className="text-lg">❓</span>
                <span>練習</span>
              </div>
              <div className="flex items-center space-x-2 cursor-pointer hover:bg-[#B85C38] px-3 py-2 rounded">
                <span className="text-lg">🏆</span>
                <span>排行榜</span>
              </div>
              <div className="flex items-center space-x-2 cursor-pointer hover:bg-[#B85C38] px-3 py-2 rounded">
                <span className="text-lg">👤</span>
                <span>個人檔案</span>
              </div>
            </nav>
          </div>
        </header>

        <div className="flex flex-col lg:flex-row gap-5">
          {/* 主內容區域 */}
          <div className="flex-1 bg-[#fffaf5] border-2 border-[#1C1C1C] border-t-0 rounded-b-lg p-6">
            {/* 今日進度區域 */}
            <ProgressSection 
              currentQuestion={currentQuestionIndex + 1} 
              totalQuestions={questions.length} 
            />

            {/* 題目區域 */}
            <QuestionCard
              questionId={currentQuestion.id}
              category={currentQuestion.category}
              question={currentQuestion.question}
              imageUrl={currentQuestion.imageUrl}
              options={currentQuestion.options}
              selectedAnswer={selectedAnswer}
              onAnswerSelect={handleAnswerSelect}
              timeLeft={timeLeft}
            />

            {/* 解釋區域 */}
            {showExplanation && (
              <div className="mt-6 bg-[#F4E8D8] border-2 border-[#1C1C1C] rounded-lg p-6">
                <div className="flex items-center space-x-2 mb-4">
                  <span className="text-2xl">{isCorrect ? "🎉" : "😢"}</span>
                  <h3 className="text-xl font-bold">
                    {isCorrect ? "答對了！" : "答錯了！"}
                  </h3>
                </div>
                <div className="mb-4">
                  <p className="text-lg font-semibold mb-2">正確答案：</p>
                  <p className="text-[#C57B57] font-bold">
                    {String.fromCharCode(65 + currentQuestion.correctAnswer)}. {currentQuestion.options[currentQuestion.correctAnswer]}
                  </p>
                </div>
                <div>
                  <p className="text-lg font-semibold mb-2">詳細解釋：</p>
                  <p className="text-gray-700">{currentQuestion.explanation}</p>
                </div>
              </div>
            )}

            {/* 按鈕區域 */}
            <div className="mt-6 flex justify-center space-x-4">
              {!showExplanation ? (
                <button 
                  onClick={handleSubmitAnswer}
                  disabled={selectedAnswer === null}
                  className={`btn-retro ${selectedAnswer === null ? 'opacity-50 cursor-not-allowed' : ''}`}
                >
                  ✓ 提交答案
                </button>
              ) : (
                <button 
                  onClick={handleNextQuestion}
                  className="btn-retro"
                >
                  ➡️ 下一題
                </button>
              )}
            </div>
          </div>

          {/* 右側邊欄 */}
          <div className="w-full lg:w-80 space-y-5">
            {/* 用戶資料卡片 */}
            <UserProfile
              name="陳醫師"
              level={userLevel}
              title="解剖學愛好者"
              consecutiveDays={consecutiveDays}
              totalScore={totalScore + score}
            />

            {/* 本週排行榜 */}
            <Leaderboard
              users={leaderboardData}
              onViewFullLeaderboard={handleViewFullLeaderboard}
            />

            {/* 學習統計 */}
            <LearningStats
              weeklyQuestions={156}
              totalQuestions={1234 + currentQuestionIndex + 1}
              accuracy={correctAnswers > 0 ? Math.round((correctAnswers / (currentQuestionIndex + 1)) * 100) : 0}
              streak={correctAnswers}
            />

            {/* 當前遊戲統計 */}
            <div className="bg-[#fffaf5] border-2 border-[#1C1C1C] rounded-lg p-6">
              <h3 className="text-lg font-bold mb-4">本局統計</h3>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">當前分數</span>
                  <span className="font-bold text-[#C57B57]">{score}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">答對題數</span>
                  <span className="font-bold text-[#C57B57]">{correctAnswers}/{currentQuestionIndex + 1}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">剩餘時間</span>
                  <span className="font-bold text-[#C57B57]">
                    {Math.floor(timeLeft / 60)}:{(timeLeft % 60).toString().padStart(2, '0')}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* 底部按鈕 */}
        <footer className="mt-5 flex justify-between">
          <button className="btn-retro">
            <span>🏠</span>
            <span>主頁</span>
          </button>
          <div className="flex space-x-3">
            <button className="btn-retro">
              <span>💡</span>
              <span>提示</span>
            </button>
            <button className="btn-retro">
              <span>📊</span>
              <span>統計</span>
            </button>
          </div>
        </footer>
      </div>
    </div>
  );
}

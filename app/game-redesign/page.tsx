"use client";
import { useState, useEffect } from "react";
import ProgressSection from "../components/ProgressSection";
import QuestionCard from "../components/QuestionCard";
import UserProfile from "../components/UserProfile";
import Leaderboard from "../components/Leaderboard";
import LearningStats from "../components/LearningStats";

export default function GameRedesignPage() {
  const [currentQuestion, setCurrentQuestion] = useState(12);
  const [totalQuestions] = useState(20);
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null);
  const [timeLeft, setTimeLeft] = useState(165); // 2:45 in seconds
  const [userLevel, setUserLevel] = useState(15);
  const [consecutiveDays, setConsecutiveDays] = useState(47);
  const [totalScore, setTotalScore] = useState(1234);

  // 模擬題目數據
  const questionData = {
    id: 13,
    category: "骨骼系統",
    question: "圖中標示的骨骼結構是人體頭骨的哪一個部分？",
    image: "/api/placeholder/400/300", // 頭骨圖片
    options: [
      "額骨 (Frontal bone)",
      "頂骨 (Parietal bone)", 
      "顳骨 (Temporal bone)",
      "枕骨 (Occipital bone)"
    ]
  };

  // 排行榜數據
  const leaderboardData = [
    { rank: 1, name: "李醫師", score: 2456, avatar: "/api/placeholder/40/40" },
    { rank: 2, name: "王護士", score: 2103, avatar: "/api/placeholder/40/40" },
    { rank: 3, name: "陳醫師 (你)", score: 1234, avatar: "/api/placeholder/40/40", isCurrentUser: true }
  ];

  // 計時器效果
  useEffect(() => {
    const timer = setInterval(() => {
      setTimeLeft(prev => {
        if (prev <= 0) {
          clearInterval(timer);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const handleAnswerSelect = (index: number) => {
    setSelectedAnswer(index);
  };

  const handleViewFullLeaderboard = () => {
    // 處理查看完整排行榜的邏輯
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
              currentQuestion={currentQuestion} 
              totalQuestions={totalQuestions} 
            />

            {/* 題目區域 */}
            <QuestionCard
              questionId={questionData.id}
              category={questionData.category}
              question={questionData.question}
              imageUrl={questionData.image}
              options={questionData.options}
              selectedAnswer={selectedAnswer}
              onAnswerSelect={handleAnswerSelect}
              timeLeft={timeLeft}
            />
          </div>

          {/* 右側邊欄 */}
          <div className="w-full lg:w-80 space-y-5">
            {/* 用戶資料卡片 */}
            <UserProfile
              name="陳醫師"
              level={userLevel}
              title="解剖學愛好者"
              consecutiveDays={consecutiveDays}
              totalScore={totalScore}
            />

            {/* 本週排行榜 */}
            <Leaderboard
              users={leaderboardData}
              onViewFullLeaderboard={handleViewFullLeaderboard}
            />

            {/* 學習統計 */}
            <LearningStats
              weeklyQuestions={156}
              totalQuestions={1234}
              accuracy={85}
              streak={12}
            />
          </div>
        </div>

        {/* 底部按鈕 */}
        <footer className="mt-5 flex justify-between">
          <button className="bg-[#C57B57] text-white border-2 border-[#1C1C1C] rounded-lg px-6 py-3 font-semibold hover:bg-[#B85C38] transition-colors flex items-center space-x-2">
            <span>🏠</span>
            <span>主頁</span>
          </button>
          <div className="flex space-x-3">
            <button className="bg-[#C57B57] text-white border-2 border-[#1C1C1C] rounded-lg px-6 py-3 font-semibold hover:bg-[#B85C38] transition-colors flex items-center space-x-2">
              <span>💡</span>
              <span>提示</span>
            </button>
            <button className="bg-[#C57B57] text-white border-2 border-[#1C1C1C] rounded-lg px-6 py-3 font-semibold hover:bg-[#B85C38] transition-colors flex items-center space-x-2">
              <span>提交答案</span>
              <span>→</span>
            </button>
          </div>
        </footer>
      </div>
    </div>
  );
}

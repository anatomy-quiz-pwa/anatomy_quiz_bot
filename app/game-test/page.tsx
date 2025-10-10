"use client";
import { useState, useEffect } from "react";

export default function GameTestPage() {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null);
  const [timeLeft, setTimeLeft] = useState(300);
  const [showExplanation, setShowExplanation] = useState(false);
  const [isCorrect, setIsCorrect] = useState<boolean | null>(null);

  // 模擬題目數據庫
  const questions = [
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
    }
  ];

  const currentQuestion = questions[currentQuestionIndex];

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

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const handleAnswerSelect = (index: number) => {
    if (showExplanation) return;
    setSelectedAnswer(index);
  };

  const handleSubmitAnswer = () => {
    if (selectedAnswer === null) return;
    
    const correct = selectedAnswer === currentQuestion.correctAnswer;
    setIsCorrect(correct);
    setShowExplanation(true);
  };

  const handleNextQuestion = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(prev => prev + 1);
      setSelectedAnswer(null);
      setShowExplanation(false);
      setIsCorrect(null);
      setTimeLeft(300);
    } else {
      alert("遊戲結束！");
    }
  };

  return (
    <div className="min-h-screen bg-[#F4E8D8] p-5">
      <div className="max-w-4xl mx-auto">
        {/* 頭部 */}
        <header className="bg-[#C57B57] text-white p-4 rounded-t-lg border-2 border-[#1C1C1C] border-b-0">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-white rounded-full flex items-center justify-center">
                <span className="text-[#C57B57] text-lg">🦷</span>
              </div>
              <h1 className="text-2xl font-bold">解剖咬一口 - 測試版本</h1>
            </div>
            <div className="flex items-center space-x-2">
              <span className="text-lg">⏰</span>
              <span className="text-lg font-mono">{formatTime(timeLeft)}</span>
            </div>
          </div>
        </header>

        {/* 主內容 */}
        <div className="bg-[#fffaf5] border-2 border-[#1C1C1C] border-t-0 rounded-b-lg p-6">
          {/* 進度顯示 */}
          <div className="mb-6">
            <div className="flex items-center justify-between mb-3">
              <span className="text-lg font-semibold">
                第 {currentQuestionIndex + 1} 題 / 共 {questions.length} 題
              </span>
              <span className="text-sm text-gray-600">
                已完成 {Math.round(((currentQuestionIndex + 1) / questions.length) * 100)}%
              </span>
            </div>
            <div className="w-full bg-[#F4E8D8] border-2 border-[#1C1C1C] rounded-full h-6 overflow-hidden">
              <div 
                className="h-full bg-gradient-to-r from-[#B85C38] to-[#C57B57] transition-all duration-500 flex items-center justify-end pr-2"
                style={{ width: `${((currentQuestionIndex + 1) / questions.length) * 100}%` }}
              >
                <span className="text-white text-sm font-semibold">
                  {Math.round(((currentQuestionIndex + 1) / questions.length) * 100)}%
                </span>
              </div>
            </div>
          </div>

          {/* 題目區域 */}
          <div className="bg-[#fffaf5] border-2 border-[#1C1C1C] rounded-lg p-6 mb-6">
            <div className="flex items-center space-x-3 mb-4">
              <span className="bg-[#C57B57] text-white px-3 py-1 rounded-full text-sm font-bold">
                {currentQuestion.id}
              </span>
              <span className="text-lg font-semibold">{currentQuestion.category}</span>
            </div>

            {/* 題目圖片 */}
            <div className="mb-6 text-center">
              <div className="w-full max-w-md mx-auto bg-white border-2 border-[#1C1C1C] rounded-lg overflow-hidden">
                <img 
                  src={currentQuestion.imageUrl} 
                  alt="題目圖片" 
                  className="w-full aspect-square object-cover"
                />
              </div>
            </div>

            {/* 題目文字 */}
            <div className="mb-6">
              <p className="text-lg mb-2">{currentQuestion.question}</p>
              <p className="text-gray-600">請選擇最正確的答案:</p>
            </div>

            {/* 選項 */}
            <div className="space-y-3">
              {currentQuestion.options.map((option, index) => (
                <button
                  key={index}
                  onClick={() => handleAnswerSelect(index)}
                  className={`w-full p-4 text-left border-2 border-[#1C1C1C] rounded-lg transition-all duration-200 ${
                    selectedAnswer === index
                      ? 'bg-[#C57B57] text-white transform -translate-x-1 -translate-y-1 shadow-[4px_4px_0_#1C1C1C]'
                      : 'bg-[#fffaf5] hover:bg-[#F4E8D8] hover:transform hover:-translate-x-1 hover:-translate-y-1 hover:shadow-[4px_4px_0_#1C1C1C]'
                  }`}
                >
                  <span className="font-semibold">{String.fromCharCode(65 + index)}</span> {option}
                </button>
              ))}
            </div>
          </div>

          {/* 解釋區域 */}
          {showExplanation && (
            <div className="mb-6 bg-[#F4E8D8] border-2 border-[#1C1C1C] rounded-lg p-6">
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
          <div className="flex justify-center space-x-4">
            {!showExplanation ? (
              <button 
                onClick={handleSubmitAnswer}
                disabled={selectedAnswer === null}
                className={`bg-[#C57B57] text-white border-2 border-[#1C1C1C] rounded-lg px-6 py-3 font-semibold hover:bg-[#B85C38] transition-colors ${
                  selectedAnswer === null ? 'opacity-50 cursor-not-allowed' : ''
                }`}
              >
                ✓ 提交答案
              </button>
            ) : (
              <button 
                onClick={handleNextQuestion}
                className="bg-[#C57B57] text-white border-2 border-[#1C1C1C] rounded-lg px-6 py-3 font-semibold hover:bg-[#B85C38] transition-colors"
              >
                ➡️ 下一題
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

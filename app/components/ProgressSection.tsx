"use client";

interface ProgressSectionProps {
  currentQuestion: number;
  totalQuestions: number;
}

export default function ProgressSection({ currentQuestion, totalQuestions }: ProgressSectionProps) {
  const progressPercentage = (currentQuestion / totalQuestions) * 100;
  const remainingQuestions = totalQuestions - currentQuestion;

  return (
    <div className="mb-8">
      <h2 className="text-xl font-bold mb-4 text-[#1C1C1C]">今日進度</h2>
      <div className="bg-[#fffaf5] border-2 border-[#1C1C1C] rounded-lg p-4">
        <div className="flex items-center justify-between mb-3">
          <span className="text-lg font-semibold">{currentQuestion} / {totalQuestions} 題</span>
          <div className="flex items-center space-x-2">
            <span className="text-sm">已完成 {Math.round(progressPercentage)}%</span>
            <span className="text-sm text-gray-600">還需 {remainingQuestions} 題達成目標</span>
          </div>
        </div>
        <div className="w-full bg-[#F4E8D8] border-2 border-[#1C1C1C] rounded-full h-6 overflow-hidden">
          <div 
            className="h-full bg-gradient-to-r from-[#B85C38] to-[#C57B57] transition-all duration-500 flex items-center justify-end pr-2"
            style={{ width: `${progressPercentage}%` }}
          >
            <span className="text-white text-sm font-semibold">{Math.round(progressPercentage)}%</span>
          </div>
        </div>
      </div>
    </div>
  );
}

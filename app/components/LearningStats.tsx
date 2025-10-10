"use client";

interface LearningStatsProps {
  weeklyQuestions: number;
  totalQuestions?: number;
  accuracy?: number;
  streak?: number;
}

export default function LearningStats({ 
  weeklyQuestions, 
  totalQuestions, 
  accuracy, 
  streak 
}: LearningStatsProps) {
  return (
    <div className="bg-[#fffaf5] border-2 border-[#1C1C1C] rounded-lg p-6">
      <h3 className="text-lg font-bold mb-4">學習統計</h3>
      <div className="space-y-3">
        <div className="flex justify-between items-center">
          <span className="text-gray-600">本週答題</span>
          <span className="font-bold text-[#C57B57]">{weeklyQuestions} 題</span>
        </div>
        
        {totalQuestions && (
          <div className="flex justify-between items-center">
            <span className="text-gray-600">總答題數</span>
            <span className="font-bold text-[#C57B57]">{totalQuestions} 題</span>
          </div>
        )}
        
        {accuracy !== undefined && (
          <div className="flex justify-between items-center">
            <span className="text-gray-600">正確率</span>
            <span className="font-bold text-[#C57B57]">{accuracy}%</span>
          </div>
        )}
        
        {streak !== undefined && (
          <div className="flex justify-between items-center">
            <span className="text-gray-600">連續答對</span>
            <span className="font-bold text-[#C57B57]">{streak} 題</span>
          </div>
        )}
      </div>
    </div>
  );
}

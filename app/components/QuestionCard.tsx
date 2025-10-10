"use client";

interface QuestionCardProps {
  questionId: number;
  category: string;
  question: string;
  imageUrl?: string;
  options: string[];
  selectedAnswer: number | null;
  onAnswerSelect: (index: number) => void;
  timeLeft: number;
}

export default function QuestionCard({
  questionId,
  category,
  question,
  imageUrl,
  options,
  selectedAnswer,
  onAnswerSelect,
  timeLeft
}: QuestionCardProps) {
  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="bg-[#fffaf5] border-2 border-[#1C1C1C] rounded-lg p-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-3">
          <span className="bg-[#C57B57] text-white px-3 py-1 rounded-full text-sm font-bold">
            {questionId}
          </span>
          <span className="text-lg font-semibold">{category}</span>
        </div>
        <div className="flex items-center space-x-2">
          <span className="text-lg">⏰</span>
          <span className="text-lg font-mono">{formatTime(timeLeft)}</span>
        </div>
      </div>

      {/* 題目圖片 */}
      <div className="mb-6 text-center">
        <div className="w-full max-w-md mx-auto bg-white border-2 border-[#1C1C1C] rounded-lg overflow-hidden">
          {imageUrl ? (
            <img 
              src={imageUrl} 
              alt="題目圖片" 
              className="w-full aspect-square object-cover"
            />
          ) : (
            <div className="aspect-square bg-gray-100 flex items-center justify-center">
              <span className="text-gray-500 text-lg">頭骨解剖圖</span>
            </div>
          )}
        </div>
      </div>

      {/* 題目文字 */}
      <div className="mb-6">
        <p className="text-lg mb-2">{question}</p>
        <p className="text-gray-600">請選擇最正確的答案:</p>
      </div>

      {/* 選項 */}
      <div className="space-y-3">
        {options.map((option, index) => (
          <button
            key={index}
            onClick={() => onAnswerSelect(index)}
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
  );
}

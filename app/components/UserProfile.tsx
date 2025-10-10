"use client";

interface UserProfileProps {
  name: string;
  level: number;
  title: string;
  consecutiveDays: number;
  totalScore: number;
  avatar?: string;
}

export default function UserProfile({
  name,
  level,
  title,
  consecutiveDays,
  totalScore,
  avatar
}: UserProfileProps) {
  return (
    <div className="bg-[#fffaf5] border-2 border-[#1C1C1C] rounded-lg p-6">
      <div className="text-center mb-4">
        <div className="w-16 h-16 bg-gray-300 rounded-full mx-auto mb-3 flex items-center justify-center">
          {avatar ? (
            <img src={avatar} alt={name} className="w-full h-full rounded-full object-cover" />
          ) : (
            <span className="text-2xl">👨‍⚕️</span>
          )}
        </div>
        <h3 className="text-lg font-bold">{name}</h3>
        <p className="text-sm text-gray-600">等級 {level} • {title}</p>
      </div>
      
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-[#fffaf5] border-2 border-[#1C1C1C] rounded-lg p-3 text-center">
          <div className="text-2xl font-bold text-[#C57B57]">{consecutiveDays}</div>
          <div className="text-sm text-gray-600">連續天數</div>
        </div>
        <div className="bg-[#fffaf5] border-2 border-[#1C1C1C] rounded-lg p-3 text-center">
          <div className="text-2xl font-bold text-[#C57B57]">{totalScore.toLocaleString()}</div>
          <div className="text-sm text-gray-600">總分數</div>
        </div>
      </div>
    </div>
  );
}

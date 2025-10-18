"use client";

interface UserProfileProps {
  name: string;
  level: number;
  title: string;
  consecutiveDays: number;
  totalScore: number;
  avatar?: string;
  levelProgress?: number; // 當前等級的進度 (0-2)
}

// 等級稱號對應表
const getLevelTitle = (level: number): string => {
  const levelTitles: { [key: number]: string } = {
    1: "解剖新手村",
    2: "胚體學長", 
    3: "肌肉拆解師",
    4: "神經探路員",
    5: "解剖影武者",
    6: "組織細胞使者",
    7: "血管引導員",
    8: "解剖研究員",
    9: "解剖操盤手",
    10: "解剖副教授",
    11: "腦神經導師",
    12: "人體地圖管理",
    13: "解剖大魔導",
    14: "解剖學傳說"
  };
  return levelTitles[level] || "未知等級";
};

// 計算距離升級還差幾題
const getQuestionsToNextLevel = (levelProgress: number = 0): number => {
  return 3 - levelProgress;
};

export default function UserProfile({
  name,
  level,
  title,
  consecutiveDays,
  totalScore,
  avatar,
  levelProgress = 0
}: UserProfileProps) {
  const levelTitle = getLevelTitle(level);
  const toNextLevel = getQuestionsToNextLevel(levelProgress);

  return (
    <div className="bg-[#fffaf5] border-2 border-[#1C1C1C] rounded-lg p-6">
      <div className="flex flex-col items-center text-center">
        {/* 等級對應海報圖片（從 Supabase 載入） */}
        <img
          src={`https://ciqlfqfgzqqgdrogedxg.supabase.co/storage/v1/object/public/linebot/level_${level}_poster.png`}
          alt={`等級 ${level} 海報`}
          className="w-40 h-40 md:w-52 md:h-52 rounded-xl object-cover shadow-md border-2 border-[#b96e3a]/40 bg-[#fff9f3]"
        />

        {/* 狀態文字 */}
        <div className="mt-4 flex flex-col items-center text-stone-800">
          <p className="font-semibold text-lg">
            👤 {name}｜等級 {level} {levelTitle}
          </p>
          <p className="text-sm text-stone-600">
            🔥 連續答題 {consecutiveDays} 天｜距離升級還差 {toNextLevel} 題！
          </p>
        </div>
      </div>
      
      <div className="grid grid-cols-2 gap-4 mt-6">
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

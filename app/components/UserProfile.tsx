"use client";

import { useState } from 'react';

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

// 獲取等級海報圖片 URL（與 LINE Bot 邏輯一致）
const getLevelPosterUrl = (level: number): string => {
  // 確保等級在有效範圍內 (1-14)
  const validLevel = Math.max(1, Math.min(14, level));
  return `https://ciqlfqfgzqqgdrogedxg.supabase.co/storage/v1/object/public/linebot/level_${validLevel}_poster.png`;
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
  const [imageError, setImageError] = useState(false);
  const levelTitle = getLevelTitle(level);
  const toNextLevel = getQuestionsToNextLevel(levelProgress);

  const handleImageError = () => {
    setImageError(true);
  };

  return (
    <div className="bg-[#fffaf5] border-2 border-[#1C1C1C] rounded-lg p-6">
      <div className="flex flex-col items-center text-center">
        {/* 等級對應海報圖片（從 Supabase 載入） */}
        {imageError ? (
          <div className="w-40 h-40 md:w-52 md:h-52 rounded-xl bg-gray-200 flex items-center justify-center shadow-md border-2 border-[#b96e3a]/40">
            <span className="text-4xl">🏆</span>
          </div>
        ) : (
          <img
            src={getLevelPosterUrl(level)}
            alt={`等級 ${level} 海報`}
            className="w-40 h-40 md:w-52 md:h-52 rounded-xl object-cover shadow-md border-2 border-[#b96e3a]/40 bg-[#fff9f3]"
            onError={handleImageError}
          />
        )}

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

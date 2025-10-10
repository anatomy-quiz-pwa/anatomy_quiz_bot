"use client";

interface LeaderboardUser {
  rank: number;
  name: string;
  score: number;
  avatar?: string;
  isCurrentUser?: boolean;
}

interface LeaderboardProps {
  users: LeaderboardUser[];
  onViewFullLeaderboard?: () => void;
}

export default function Leaderboard({ users, onViewFullLeaderboard }: LeaderboardProps) {
  const getRankColor = (rank: number) => {
    switch (rank) {
      case 1: return 'bg-yellow-500';
      case 2: return 'bg-gray-400';
      case 3: return 'bg-amber-600';
      default: return 'bg-gray-300';
    }
  };

  return (
    <div className="bg-[#fffaf5] border-2 border-[#1C1C1C] rounded-lg p-6">
      <div className="flex items-center space-x-2 mb-4">
        <span className="text-lg">🏆</span>
        <h3 className="text-lg font-bold">本週排行榜</h3>
      </div>
      
      <div className="space-y-3">
        {users.map((user, index) => (
          <div key={index} className={`flex items-center space-x-3 p-2 rounded ${
            user.isCurrentUser ? 'bg-[#F4E8D8]' : ''
          }`}>
            <div className={`w-8 h-8 rounded-full flex items-center justify-center text-white font-bold ${
              getRankColor(user.rank)
            }`}>
              {user.rank}
            </div>
            <div className="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center">
              {user.avatar ? (
                <img src={user.avatar} alt={user.name} className="w-full h-full rounded-full object-cover" />
              ) : (
                <span className="text-sm">👤</span>
              )}
            </div>
            <div className="flex-1">
              <div className="font-semibold text-sm">{user.name}</div>
            </div>
            <div className="font-bold text-[#C57B57]">{user.score.toLocaleString()}</div>
          </div>
        ))}
      </div>
      
      <button 
        onClick={onViewFullLeaderboard}
        className="w-full mt-4 bg-[#C57B57] text-white border-2 border-[#1C1C1C] rounded-lg py-2 font-semibold hover:bg-[#B85C38] transition-colors"
      >
        查看完整排行榜
      </button>
    </div>
  );
}

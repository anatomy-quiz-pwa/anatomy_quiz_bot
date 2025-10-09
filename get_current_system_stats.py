import os
from supabase import create_client, Client
from datetime import datetime, timedelta
from collections import defaultdict

# Supabase configuration
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://ciqlfqfgzqqgdrogedxg.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA')

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_current_system_stats():
    """獲取當前系統使用統計數據"""
    
    print("=" * 80)
    print(f"🤖 LINE Bot 系統使用統計報告")
    print(f"📅 報告生成時間：{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
    print("=" * 80)
    print()
    
    # 1. 總用戶數
    try:
        all_user_stats = supabase.table('user_stats').select('*').execute()
        all_users = supabase.table('users').select('*').execute()
        
        total_users = len(all_user_stats.data) if all_user_stats.data else 0
        total_registered = len(all_users.data) if all_users.data else 0
        
        print(f"👥 總註冊用戶數：{total_users} 人")
        print(f"📋 系統記錄用戶：{total_registered} 人")
    except Exception as e:
        print(f"❌ 查詢總用戶數錯誤：{e}")
        total_users = 0
        all_user_stats = None
    
    print()
    
    # 2. 今日活躍用戶（從最後更新時間判斷）
    try:
        today = datetime.now().date().isoformat()
        
        # 查詢今日有活動的用戶（根據 last_update 欄位）
        today_users = supabase.table('user_stats').select('*').eq('last_update', today).execute()
        
        if today_users.data:
            today_active_users = len(today_users.data)
            # 計算今日答題數（從 daily_quota 或根據更新時間推算）
            today_total_answers = sum(u.get('correct', 0) + u.get('wrong', 0) for u in today_users.data)
        else:
            today_active_users = 0
            today_total_answers = 0
            
        print(f"📊 今日活躍用戶：{today_active_users} 人")
        
        if today_active_users > 0:
            avg_answers_today = today_total_answers / today_active_users if today_active_users > 0 else 0
            print(f"📈 今日平均每人答題：{avg_answers_today:.1f} 題")
    except Exception as e:
        print(f"❌ 查詢今日數據錯誤：{e}")
        today_active_users = 0
    
    print()
    
    # 3. 本週活躍用戶（過去7天）
    try:
        week_ago = (datetime.now() - timedelta(days=7)).date()
        week_dates = [(week_ago + timedelta(days=i)).isoformat() for i in range(8)]
        
        week_users = []
        for date in week_dates:
            date_users = supabase.table('user_stats').select('*').eq('last_update', date).execute()
            if date_users.data:
                week_users.extend(date_users.data)
        
        # 去重（根據 user_id）
        unique_user_ids = set(u['user_id'] for u in week_users)
        week_active_users = len(unique_user_ids)
            
        print(f"📅 本週活躍用戶（7天）：{week_active_users} 人")
    except Exception as e:
        print(f"❌ 查詢本週數據錯誤：{e}")
        week_active_users = 0
    
    print()
    
    # 4. 總體答題統計（從 user_stats 彙總）
    try:
        if all_user_stats and all_user_stats.data:
            total_correct = sum(u.get('correct', 0) for u in all_user_stats.data)
            total_wrong = sum(u.get('wrong', 0) for u in all_user_stats.data)
            total_answers = total_correct + total_wrong
            accuracy_rate = (total_correct / total_answers * 100) if total_answers > 0 else 0
            
            print(f"📊 總體答題統計")
            print(f"   • 總答題次數：{total_answers} 次")
            print(f"   • 正確答案：{total_correct} 次")
            print(f"   • 錯誤答案：{total_wrong} 次")
            print(f"   • 平均準確率：{accuracy_rate:.1f}%")
            
            if total_users > 0:
                avg_per_user = total_answers / total_users
                print(f"   • 平均每人答題：{avg_per_user:.1f} 題")
        else:
            print(f"📊 總體答題統計：無數據")
    except Exception as e:
        print(f"❌ 查詢答題統計錯誤：{e}")
    
    print()
    
    # 5. 用戶等級分布
    try:
        if all_user_stats and all_user_stats.data:
            level_distribution = defaultdict(int)
            for user in all_user_stats.data:
                level = user.get('level', 1)
                level_distribution[level] += 1
            
            print(f"🏆 用戶等級分布")
            for level in sorted(level_distribution.keys()):
                count = level_distribution[level]
                percentage = (count / total_users * 100) if total_users > 0 else 0
                print(f"   • 等級 {level}：{count} 人（{percentage:.1f}%）")
        else:
            print(f"🏆 用戶等級分布：無數據")
    except Exception as e:
        print(f"❌ 查詢等級分布錯誤：{e}")
    
    print()
    
    # 6. Top 10 活躍用戶（按總答題數）
    try:
        if all_user_stats and all_user_stats.data:
            # 計算總答題數並排序
            users_with_answers = []
            for user in all_user_stats.data:
                total = user.get('correct', 0) + user.get('wrong', 0)
                if total > 0:  # 只顯示有答題記錄的用戶
                    users_with_answers.append({
                        'user_id': user.get('user_id'),
                        'total': total,
                        'correct': user.get('correct', 0),
                        'wrong': user.get('wrong', 0),
                        'level': user.get('level', 1)
                    })
            
            # 排序
            sorted_users = sorted(users_with_answers, key=lambda x: x['total'], reverse=True)[:10]
            
            if sorted_users:
                print(f"🔥 Top 10 最活躍用戶（按總答題數）")
                
                # 獲取用戶暱稱
                for idx, user in enumerate(sorted_users, 1):
                    user_id = user['user_id']
                    total = user['total']
                    correct = user['correct']
                    accuracy = (correct / total * 100) if total > 0 else 0
                    level = user['level']
                    
                    # 從 users 表獲取暱稱
                    try:
                        user_info = supabase.table('users').select('game_nickname, display_name').eq('line_user_id', user_id).execute()
                        if user_info.data and len(user_info.data) > 0:
                            nickname = user_info.data[0].get('game_nickname') or user_info.data[0].get('display_name', '未設定')
                        else:
                            nickname = '未設定'
                    except:
                        nickname = '未設定'
                    
                    print(f"   {idx}. {nickname} - 等級{level}，答題{total}題，準確率{accuracy:.1f}%")
            else:
                print(f"🔥 Top 10 最活躍用戶：暫無答題記錄")
        else:
            print(f"🔥 Top 10 最活躍用戶：無數據")
    except Exception as e:
        print(f"❌ 查詢活躍用戶錯誤：{e}")
    
    print()
    
    # 7. 用戶活躍度分析
    print(f"📈 用戶活躍度分析")
    if total_users > 0:
        today_active_rate = (today_active_users / total_users * 100) if total_users > 0 else 0
        week_active_rate = (week_active_users / total_users * 100) if total_users > 0 else 0
        
        print(f"   • 今日活躍率：{today_active_rate:.1f}%")
        print(f"   • 本週活躍率：{week_active_rate:.1f}%")
        
        # 統計有答題記錄的用戶比例
        if all_user_stats and all_user_stats.data:
            users_with_activity = sum(1 for u in all_user_stats.data if (u.get('correct', 0) + u.get('wrong', 0)) > 0)
            activity_rate = (users_with_activity / total_users * 100) if total_users > 0 else 0
            print(f"   • 有答題記錄的用戶：{users_with_activity} 人（{activity_rate:.1f}%）")
    else:
        print(f"   • 無數據")
    
    print()
    
    # 8. 連續登入統計
    try:
        if all_user_stats and all_user_stats.data:
            streak_distribution = defaultdict(int)
            for user in all_user_stats.data:
                streak = user.get('streak_days', 0)
                if streak >= 7:
                    streak_distribution['7天以上'] += 1
                elif streak >= 3:
                    streak_distribution['3-6天'] += 1
                elif streak >= 2:
                    streak_distribution['2天'] += 1
                else:
                    streak_distribution['0-1天'] += 1
            
            print(f"🔥 連續登入統計")
            for category, count in sorted(streak_distribution.items(), reverse=True):
                percentage = (count / total_users * 100) if total_users > 0 else 0
                print(f"   • {category}：{count} 人（{percentage:.1f}%）")
    except Exception as e:
        print(f"❌ 查詢連續登入錯誤：{e}")
    
    print()
    print("=" * 80)
    print("✅ 報告生成完成")
    print("=" * 80)

if __name__ == "__main__":
    get_current_system_stats()

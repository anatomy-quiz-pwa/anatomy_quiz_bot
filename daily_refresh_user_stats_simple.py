import os
from supabase import create_client, Client
from typing import Optional

# Get environment variables with proper error handling
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://ciqlfqfgzqqgdrogedxg.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA')

# Validate environment variables
if not SUPABASE_URL:
    raise ValueError("SUPABASE_URL environment variable is required but not set")
if not SUPABASE_KEY:
    raise ValueError("SUPABASE_ANON_KEY environment variable is required but not set")

# Create Supabase client
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    print(f"Failed to create Supabase client: {e}")
    raise

def get_user_stats(user_id: str) -> Optional[dict]:
    """Get user statistics from Supabase"""
    try:
        response = supabase.table('user_stats').select('*').eq('user_id', user_id).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Error getting user stats: {e}")
        return None

def update_user_stats(user_id: str, stats: dict) -> bool:
    """Update user statistics in Supabase"""
    try:
        supabase.table('user_stats').upsert({
            'user_id': user_id,
            **stats
        }).execute()
        return True
    except Exception as e:
        print(f"Error updating user stats: {e}")
        return False

def add_correct_answer(user_id: str) -> bool:
    """Add a correct answer to user stats"""
    try:
        # Get current stats
        current_stats = get_user_stats(user_id)
        if current_stats:
            correct_answers = current_stats.get('correct_answers', 0) + 1
            total_answers = current_stats.get('total_answers', 0) + 1
        else:
            correct_answers = 1
            total_answers = 1
        
        # Update stats
        return update_user_stats(user_id, {
            'correct_answers': correct_answers,
            'total_answers': total_answers
        })
    except Exception as e:
        print(f"Error adding correct answer: {e}")
        return False

def add_wrong_answer(user_id: str) -> bool:
    """Add a wrong answer to user stats"""
    try:
        # Get current stats
        current_stats = get_user_stats(user_id)
        if current_stats:
            wrong_answers = current_stats.get('wrong_answers', 0) + 1
            total_answers = current_stats.get('total_answers', 0) + 1
        else:
            wrong_answers = 1
            total_answers = 1
        
        # Update stats
        return update_user_stats(user_id, {
            'wrong_answers': wrong_answers,
            'total_answers': total_answers
        })
    except Exception as e:
        print(f"Error adding wrong answer: {e}")
        return False

def get_or_create_user_stats(user_id: str) -> dict:
    """Get or create user statistics"""
    try:
        stats = get_user_stats(user_id)
        if stats is None:
            # Create new user stats
            from datetime import datetime
            today = datetime.today().date().isoformat()
            
            new_stats = {
                'user_id': user_id,
                'correct': 0,
                'wrong': 0,
                'correct_qids': [],
                'daily_quota': 3,
                'streak_days': 1,
                'correct_in_level': 0,
                'level': 1,
                'last_updated': today
            }
            
            supabase.table('user_stats').insert(new_stats).execute()
            return new_stats
        return stats
    except Exception as e:
        print(f"Error getting or creating user stats: {e}")
        return {}

def calculate_streak_days(user_id: str, current_stats: dict, current_date=None) -> int:
    """Calculate consecutive days based on last_updated date
    
    Args:
        user_id: 用戶ID
        current_stats: 當前用戶統計數據
        current_date: 當前日期（用於測試，默認為今天）
    """
    try:
        from datetime import datetime, timedelta
        
        # 使用提供的日期或今天的日期
        if current_date:
            import datetime as dt
            if isinstance(current_date, dt.date):
                today = current_date
            elif isinstance(current_date, str):
                today = datetime.fromisoformat(current_date).date()
            else:
                today = current_date
        else:
            today = datetime.today().date()
            
        last_updated_str = current_stats.get('last_updated', None)
        current_streak = current_stats.get('streak_days', 1)
        
        if not last_updated_str:
            # First time user, start with day 1
            print(f"用戶 {user_id} 首次答題，連續天數設為 1")
            return 1
        
        try:
            last_updated = datetime.fromisoformat(last_updated_str).date()
        except:
            # Invalid date format, reset to day 1
            print(f"用戶 {user_id} 日期格式錯誤，重置連續天數為 1")
            return 1
        
        # Calculate days difference
        days_diff = (today - last_updated).days
        
        print(f"用戶 {user_id}: 今天={today}, 上次更新={last_updated}, 天數差異={days_diff}")
        
        if days_diff == 0:
            # Same day, keep current streak
            print(f"用戶 {user_id} 同一天內答題，保持連續天數 {current_streak}")
            return current_streak
        elif days_diff == 1:
            # Next day, increment streak
            new_streak = current_streak + 1
            print(f"用戶 {user_id} 連續答題，連續天數從 {current_streak} 增加到 {new_streak}")
            return new_streak
        else:
            # Gap in days, reset to day 1
            print(f"用戶 {user_id} 中斷 {days_diff} 天，重置連續天數為 1")
            return 1
            
    except Exception as e:
        print(f"計算連續天數失敗: {e}")
        return 1

def update_user_after_answer(user_id: str, is_correct: bool, question_id: str = None) -> bool:
    """Update user stats after answering a question"""
    try:
        stats = get_or_create_user_stats(user_id)
        
        # 🔥 計算連續天數（在更新其他數據之前）
        new_streak_days = calculate_streak_days(user_id, stats)
        stats['streak_days'] = new_streak_days
        
        if is_correct:
            stats['correct'] = stats.get('correct', 0) + 1
            stats['correct_in_level'] = stats.get('correct_in_level', 0) + 1
            if question_id:
                correct_qids = stats.get('correct_qids', [])
                if question_id not in correct_qids:
                    correct_qids.append(question_id)
                stats['correct_qids'] = correct_qids
        else:
            stats['wrong'] = stats.get('wrong', 0) + 1
        
        # Update daily quota
        stats['daily_quota'] = max(0, stats.get('daily_quota', 3) - 1)
        
        # Update last_updated
        from datetime import datetime
        stats['last_updated'] = datetime.today().date().isoformat()
        
        print(f"✅ 用戶 {user_id} 統計更新完成 - 連續天數: {new_streak_days}")
        return update_user_stats(user_id, stats)
    except Exception as e:
        print(f"Error updating user after answer: {e}")
        return False

def get_progress_message(user_id: str) -> str:
    """Get user progress message"""
    try:
        stats = get_user_stats(user_id)
        if not stats:
            return "尚未開始答題"
        
        correct = stats.get('correct', 0)
        wrong = stats.get('wrong', 0)
        level = stats.get('level', 1)
        daily_quota = stats.get('daily_quota', 3)
        
        total = correct + wrong
        accuracy = (correct / total * 100) if total > 0 else 0
        
        return f"等級: {level} | 正確: {correct} | 錯誤: {wrong} | 正確率: {accuracy:.1f}% | 今日剩餘: {daily_quota}"
    except Exception as e:
        print(f"Error getting progress message: {e}")
        return "無法獲取進度信息"

def get_user_streak_info(user_id: str) -> dict:
    """Get user streak information with enhanced details"""
    try:
        stats = get_user_stats(user_id)
        if not stats:
            return {
                'streak_days': 0, 
                'last_active': None,
                'streak_message': '還沒開始答題喔！',
                'has_bonus': False
            }
        
        streak_days = stats.get('streak_days', 0)
        last_active = stats.get('last_updated', None)
        
        # Create streak message
        if streak_days == 1:
            streak_message = f"🔥 連續學習第 {streak_days} 天！"
            has_bonus = False
        elif streak_days >= 7:
            streak_message = f"🔥🔥🔥 哇！連續學習 {streak_days} 天！你是學習達人！"
            has_bonus = True
        elif streak_days >= 3:
            streak_message = f"🔥🔥 太棒了！連續學習 {streak_days} 天！"
            has_bonus = True
        else:
            streak_message = f"🔥 連續學習第 {streak_days} 天！"
            has_bonus = False
        
        return {
            'streak_days': streak_days,
            'last_active': last_active,
            'streak_message': streak_message,
            'has_bonus': has_bonus
        }
    except Exception as e:
        print(f"Error getting user streak info: {e}")
        return {
            'streak_days': 0, 
            'last_active': None,
            'streak_message': '無法獲取連續天數信息',
            'has_bonus': False
        }

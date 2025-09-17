#!/usr/bin/env python3
"""
測試 users 表格中的 game_nickname 欄位
"""

from supabase import create_client, Client

# Supabase 配置
SUPABASE_URL = "https://ciqlfqfgzqqgdrogedxg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA"

def test_users_table():
    """測試 users 表格結構"""
    print("🔍 測試 users 表格結構...")
    
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # 檢查 users 表格結構
        response = supabase.table('users').select('*').limit(3).execute()
        
        if response.data:
            print("✅ 成功獲取 users 表格數據")
            print(f"📋 字段：{list(response.data[0].keys())}")
            
            # 檢查是否包含 game_nickname 欄位
            if 'game_nickname' in response.data[0]:
                print("✅ game_nickname 欄位存在！")
                
                # 顯示樣本數據
                print("\n📊 用戶暱稱樣本：")
                for i, user in enumerate(response.data, 1):
                    line_user_id = user.get('line_user_id', 'N/A')
                    game_nickname = user.get('game_nickname', '無暱稱')
                    display_name = user.get('display_name', '無顯示名')
                    print(f"  {i}. {line_user_id} -> 暱稱: {game_nickname}, 顯示名: {display_name}")
                
                return True
            else:
                print("❌ game_nickname 欄位不存在")
                return False
        else:
            print("⚠️ users 表格為空或無法獲取數據")
            return False
            
    except Exception as e:
        print(f"❌ 測試失敗：{e}")
        return False

def test_user_nicknames():
    """測試用戶暱稱數據"""
    print("\n📊 測試用戶暱稱數據...")
    
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # 獲取所有用戶的暱稱
        response = supabase.table('users').select('line_user_id, game_nickname, display_name').execute()
        
        if response.data:
            print(f"📈 找到 {len(response.data)} 個用戶")
            
            # 顯示有暱稱的用戶
            users_with_nickname = [user for user in response.data if user.get('game_nickname')]
            print(f"✅ 有暱稱的用戶：{len(users_with_nickname)} 個")
            
            for user in users_with_nickname[:5]:  # 顯示前5個
                print(f"  {user['line_user_id']} -> {user['game_nickname']}")
            
            return True
        else:
            print("❌ 無法獲取用戶數據")
            return False
            
    except Exception as e:
        print(f"❌ 測試失敗：{e}")
        return False

def test_leaderboard_with_nicknames():
    """測試排行榜暱稱顯示"""
    print("\n🏆 測試排行榜暱稱顯示...")
    
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # 獲取排行榜數據
        stats_response = supabase.table('user_stats').select('user_id, level, correct, wrong').order('correct', desc=True).limit(10).execute()
        
        if stats_response.data:
            print("📊 排行榜數據（包含暱稱）：")
            for i, stats in enumerate(stats_response.data, 1):
                user_id = stats.get('user_id', '')
                level = stats.get('level', 1)
                correct = stats.get('correct', 0)
                wrong = stats.get('wrong', 0)
                total = correct + wrong
                score = correct * 10
                accuracy = (correct / total * 100) if total > 0 else 0
                
                # 獲取暱稱
                try:
                    user_response = supabase.table('users').select('game_nickname').eq('line_user_id', user_id).execute()
                    if user_response.data and user_response.data[0].get('game_nickname'):
                        nickname = user_response.data[0]['game_nickname']
                    else:
                        nickname = generate_default_nickname(user_id)
                except:
                    nickname = generate_default_nickname(user_id)
                
                print(f"  {i:2d}. {nickname:20s} | 等級{level} | {score:3d}分 | {correct:2d}/{total:2d}題 | {accuracy:5.1f}%")
        else:
            print("❌ 無法獲取排行榜數據")
            
    except Exception as e:
        print(f"❌ 測試失敗：{e}")

def generate_default_nickname(user_id):
    """生成默認暱稱"""
    if user_id.startswith('U') and len(user_id) > 10:
        # LINE 用戶ID，使用後8位
        return f"用戶_{user_id[2:10]}"
    elif user_id.startswith('test'):
        # 測試用戶，使用 test 後的部分
        return f"測試用戶_{user_id[5:]}"
    else:
        # 其他用戶ID
        return f"用戶_{user_id}"

def test_application_integration():
    """測試應用程序整合"""
    print("\n🌐 測試應用程序整合...")
    
    try:
        import requests
        
        # 測試排行榜
        response = requests.get('http://localhost:5003/leaderboard')
        if response.status_code == 200:
            content = response.text
            
            # 檢查是否包含暱稱相關內容
            if "用戶_" in content or "測試用戶_" in content:
                print("✅ 排行榜正在顯示暱稱")
            else:
                print("⚠️ 排行榜可能未顯示暱稱")
        else:
            print(f"❌ 排行榜請求失敗：{response.status_code}")
            
        # 測試儀表板
        response = requests.get('http://localhost:5003/dashboard')
        if response.status_code == 200:
            content = response.text
            
            if "用戶_" in content or "測試用戶_" in content:
                print("✅ 儀表板正在顯示暱稱")
            else:
                print("⚠️ 儀表板可能未顯示暱稱")
        else:
            print(f"❌ 儀表板請求失敗：{response.status_code}")
            
    except Exception as e:
        print(f"❌ 應用程序測試失敗：{e}")

if __name__ == "__main__":
    print("🚀 測試 users 表格中的 game_nickname 欄位")
    print("=" * 50)
    
    # 1. 測試 users 表格結構
    has_users_table = test_users_table()
    
    if has_users_table:
        print("\n✅ users 表格結構正常！")
        
        # 2. 測試用戶暱稱數據
        has_nicknames = test_user_nicknames()
        
        if has_nicknames:
            # 3. 測試排行榜暱稱顯示
            test_leaderboard_with_nicknames()
            
            # 4. 測試應用程序整合
            test_application_integration()
            
            print("\n🎉 暱稱功能測試完成！")
            print("\n📝 下一步：")
            print("1. 重新啟動應用程序")
            print("2. 訪問 http://localhost:5003/leaderboard 查看效果")
        else:
            print("\n❌ 用戶暱稱數據測試失敗")
    else:
        print("\n❌ users 表格結構測試失敗")


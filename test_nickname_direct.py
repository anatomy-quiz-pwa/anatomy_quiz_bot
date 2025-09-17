#!/usr/bin/env python3
"""
直接測試 Supabase 暱稱欄位
"""

from supabase import create_client, Client

# Supabase 配置
SUPABASE_URL = "https://ciqlfqfgzqqgdrogedxg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA"

def test_nickname_column_directly():
    """直接測試暱稱欄位"""
    print("🔍 直接測試 Supabase 暱稱欄位...")
    
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # 嘗試獲取包含暱稱的數據
        print("📊 嘗試獲取包含暱稱的數據...")
        response = supabase.table('user_stats').select('user_id, nickname, level, correct').limit(5).execute()
        
        if response.data:
            print("✅ 成功獲取數據！")
            print(f"📋 字段：{list(response.data[0].keys())}")
            
            # 檢查是否包含暱稱欄位
            if 'nickname' in response.data[0]:
                print("✅ 暱稱欄位存在！")
                
                # 顯示數據
                print("\n📊 用戶數據（包含暱稱）：")
                for i, user in enumerate(response.data, 1):
                    nickname = user.get('nickname', '無暱稱')
                    level = user.get('level', 1)
                    correct = user.get('correct', 0)
                    score = correct * 10
                    print(f"  {i}. {nickname} - 等級{level} - {score}分 ({correct}題正確)")
                
                return True
            else:
                print("❌ 暱稱欄位不存在")
                return False
        else:
            print("❌ 無法獲取數據")
            return False
            
    except Exception as e:
        print(f"❌ 測試失敗：{e}")
        return False

def update_nicknames_if_needed():
    """如果需要，更新暱稱"""
    print("\n🔄 檢查並更新暱稱...")
    
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # 獲取所有用戶
        response = supabase.table('user_stats').select('user_id, nickname').execute()
        users = response.data
        
        print(f"📊 找到 {len(users)} 條用戶記錄")
        
        updated_count = 0
        for user in users:
            user_id = user.get('user_id', '')
            current_nickname = user.get('nickname')
            
            # 如果沒有暱稱，生成一個
            if not current_nickname:
                nickname = generate_nickname(user_id)
                
                try:
                    update_response = supabase.table('user_stats').update({
                        'nickname': nickname
                    }).eq('user_id', user_id).execute()
                    
                    if update_response.data:
                        updated_count += 1
                        print(f"✅ 更新用戶 {user_id} 暱稱為：{nickname}")
                    else:
                        print(f"⚠️ 用戶 {user_id} 更新失敗")
                        
                except Exception as e:
                    print(f"❌ 更新用戶 {user_id} 失敗：{e}")
            else:
                print(f"ℹ️ 用戶 {user_id} 已有暱稱：{current_nickname}")
        
        print(f"\n📈 更新完成！成功更新 {updated_count} 條記錄")
        return True
        
    except Exception as e:
        print(f"❌ 更新失敗：{e}")
        return False

def generate_nickname(user_id):
    """根據 user_id 生成暱稱"""
    if user_id.startswith('U') and len(user_id) > 10:
        # LINE 用戶ID，使用後8位
        return f"用戶_{user_id[2:10]}"
    elif user_id.startswith('test'):
        # 測試用戶，使用 test 後的部分
        return f"測試用戶_{user_id[5:]}"
    else:
        # 其他用戶ID
        return f"用戶_{user_id}"

def test_leaderboard_with_nicknames():
    """測試排行榜暱稱顯示"""
    print("\n🏆 測試排行榜暱稱顯示...")
    
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # 獲取排行榜數據
        response = supabase.table('user_stats').select('user_id, nickname, level, correct, wrong').order('correct', desc=True).limit(10).execute()
        
        if response.data:
            print("📊 排行榜數據（包含暱稱）：")
            for i, user in enumerate(response.data, 1):
                nickname = user.get('nickname', '未知')
                level = user.get('level', 1)
                correct = user.get('correct', 0)
                wrong = user.get('wrong', 0)
                total = correct + wrong
                score = correct * 10
                accuracy = (correct / total * 100) if total > 0 else 0
                
                print(f"  {i:2d}. {nickname:20s} | 等級{level} | {score:3d}分 | {correct:2d}/{total:2d}題 | {accuracy:5.1f}%")
        else:
            print("❌ 無法獲取數據")
            
    except Exception as e:
        print(f"❌ 測試失敗：{e}")

if __name__ == "__main__":
    print("🚀 直接測試 Supabase 暱稱欄位")
    print("=" * 50)
    
    # 1. 直接測試暱稱欄位
    has_nickname = test_nickname_column_directly()
    
    if has_nickname:
        print("\n✅ 暱稱欄位已存在！")
        
        # 2. 更新暱稱（如果需要）
        update_success = update_nicknames_if_needed()
        
        if update_success:
            # 3. 測試排行榜顯示
            test_leaderboard_with_nicknames()
            
            print("\n🎉 暱稱功能測試完成！")
            print("\n📝 下一步：")
            print("1. 重新啟動應用程序以檢測新欄位")
            print("2. 訪問 http://localhost:5003/leaderboard 查看效果")
        else:
            print("\n❌ 暱稱更新失敗")
    else:
        print("\n❌ 暱稱欄位不存在或無法訪問")
        print("📖 請確認已在 Supabase Dashboard 中成功添加 nickname 欄位")


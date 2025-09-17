#!/usr/bin/env python3
"""
測試暱稱欄位是否已添加並更新數據
"""

import os
from supabase import create_client, Client

# Supabase 配置
SUPABASE_URL = "https://ciqlfqfgzqqgdrogedxg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA"

def check_nickname_column():
    """檢查暱稱欄位是否存在"""
    print("🔍 檢查暱稱欄位是否存在...")
    
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # 獲取一條記錄來檢查欄位
        response = supabase.table('user_stats').select('*').limit(1).execute()
        
        if response.data:
            fields = list(response.data[0].keys())
            print(f"📋 當前字段：{', '.join(fields)}")
            
            if 'nickname' in fields:
                print("✅ 暱稱欄位已存在！")
                return True
            else:
                print("❌ 暱稱欄位不存在")
                return False
        else:
            print("⚠️ 無法獲取數據")
            return False
            
    except Exception as e:
        print(f"❌ 檢查失敗：{e}")
        return False

def update_nicknames():
    """為現有記錄更新暱稱"""
    print("\n🔄 開始更新暱稱...")
    
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

def test_nickname_display():
    """測試暱稱顯示"""
    print("\n🧪 測試暱稱顯示...")
    
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # 獲取帶暱稱的排行榜數據
        response = supabase.table('user_stats').select('user_id, nickname, level, correct, wrong').order('correct', desc=True).limit(10).execute()
        
        if response.data:
            print("🏆 排行榜（包含暱稱）：")
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

def test_application_with_nicknames():
    """測試應用程序是否正確使用暱稱"""
    print("\n🌐 測試應用程序暱稱顯示...")
    
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
    print("🚀 暱稱欄位測試和更新")
    print("=" * 50)
    
    # 1. 檢查暱稱欄位是否存在
    has_nickname = check_nickname_column()
    
    if has_nickname:
        print("\n✅ 暱稱欄位已存在，開始更新數據...")
        
        # 2. 更新暱稱
        update_success = update_nicknames()
        
        if update_success:
            # 3. 測試暱稱顯示
            test_nickname_display()
            
            # 4. 測試應用程序
            test_application_with_nicknames()
            
            print("\n🎉 暱稱功能測試完成！")
        else:
            print("\n❌ 暱稱更新失敗")
    else:
        print("\n❌ 請先在 Supabase Dashboard 中添加 nickname 欄位")
        print("📖 請參考 'Supabase_添加暱稱欄位指南.md' 文件")


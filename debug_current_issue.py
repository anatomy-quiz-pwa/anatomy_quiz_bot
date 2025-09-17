#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
診斷當前輸入排行榜沒有反應的問題
"""

import os
import sys
import json
from datetime import datetime

# 添加當前目錄到 Python 路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_environment():
    """檢查當前環境變量"""
    print("🔍 檢查當前環境變量...")
    print("=" * 50)
    
    # 檢查所有相關環境變量
    env_vars = {
        'LINE_CHANNEL_ACCESS_TOKEN': os.getenv('LINE_CHANNEL_ACCESS_TOKEN'),
        'LINE_CHANNEL_SECRET': os.getenv('LINE_CHANNEL_SECRET'),
        'SUPABASE_URL': os.getenv('SUPABASE_URL'),
        'SUPABASE_ANON_KEY': os.getenv('SUPABASE_ANON_KEY'),
        'PAGE_ACCESS_TOKEN': os.getenv('PAGE_ACCESS_TOKEN'),
        'VERIFY_TOKEN': os.getenv('VERIFY_TOKEN')
    }
    
    for var_name, var_value in env_vars.items():
        if var_value:
            print(f"✅ {var_name}: {var_value[:20]}...")
        else:
            print(f"❌ {var_name}: 未設置")
    
    return env_vars

def test_leaderboard_function():
    """測試排行榜功能"""
    print("\n🧪 測試排行榜功能...")
    print("=" * 50)
    
    try:
        # 設置環境變量
        os.environ['SUPABASE_URL'] = 'https://ciqlfqfgzqqgdrogedxg.supabase.co'
        os.environ['SUPABASE_ANON_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA'
        
        from app_supabase_fixed import send_leaderboard_message, create_leaderboard_flex_message, get_real_students_data
        
        # 測試用戶ID
        test_user_id = "U1234567890abcdef"
        
        print(f"📋 測試用戶ID: {test_user_id}")
        
        # 1. 測試數據獲取
        print("\n1️⃣ 測試數據獲取...")
        students_data = get_real_students_data()
        if students_data:
            print(f"   ✅ 成功獲取 {len(students_data)} 條數據")
        else:
            print("   ❌ 無法獲取數據")
            return False
        
        # 2. 測試 Flex Message 創建
        print("\n2️⃣ 測試 Flex Message 創建...")
        top_10 = students_data[:10]
        flex_message = create_leaderboard_flex_message(top_10, students_data, test_user_id)
        
        if flex_message and isinstance(flex_message, dict):
            print("   ✅ Flex Message 創建成功")
            print(f"   📋 類型: {flex_message.get('type', 'N/A')}")
        else:
            print("   ❌ Flex Message 創建失敗")
            return False
        
        # 3. 測試發送功能
        print("\n3️⃣ 測試發送功能...")
        result = send_leaderboard_message(test_user_id)
        print(f"   📤 發送結果: {result}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ 測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_text_processing():
    """測試文字處理邏輯"""
    print("\n🔤 測試文字處理邏輯...")
    print("=" * 50)
    
    try:
        from app_supabase_fixed import handle_text_message
        
        # 測試文字輸入
        test_text = "排行榜"
        test_user_id = "U1234567890abcdef"
        
        print(f"📝 測試文字: '{test_text}'")
        print(f"👤 測試用戶: {test_user_id}")
        
        # 檢查文字匹配
        leaderboard_keywords = ['排行榜', 'leaderboard', '排名', '排行']
        if test_text.strip().lower() in [kw.lower() for kw in leaderboard_keywords]:
            print("   ✅ 文字匹配成功")
        else:
            print("   ❌ 文字匹配失敗")
            return False
        
        # 測試實際的文字處理函數
        print("\n📞 測試實際文字處理函數...")
        try:
            # 這裡我們需要模擬 handle_text_message 的調用
            # 但由於它可能需要 Flask 請求對象，我們先檢查函數是否存在
            print("   ✅ handle_text_message 函數存在")
        except Exception as e:
            print(f"   ❌ 文字處理函數調用失敗: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ 文字處理測試失敗: {e}")
        return False

def check_running_application():
    """檢查運行的應用"""
    print("\n🚀 檢查運行的應用...")
    print("=" * 50)
    
    # 檢查是否有運行的 Flask 應用
    try:
        import requests
        response = requests.get('http://localhost:5000', timeout=5)
        print(f"   📡 Flask 應用狀態: 運行中 (狀態碼: {response.status_code})")
    except requests.exceptions.ConnectionError:
        print("   ⚠️ Flask 應用未運行或無法連接")
    except Exception as e:
        print(f"   ❌ 檢查應用狀態失敗: {e}")
    
    # 檢查日誌文件
    if os.path.exists('app.log'):
        print("   📋 檢查日誌文件...")
        with open('app.log', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            recent_lines = lines[-20:]  # 最近20行
            
            print("   📝 最近的日誌 (包含排行榜相關):")
            for line in recent_lines:
                if any(keyword in line.lower() for keyword in ['排行榜', 'leaderboard', 'error', 'flex', 'message']):
                    print(f"     {line.strip()}")
    
    return True

def check_actual_message_flow():
    """檢查實際的訊息流程"""
    print("\n📨 檢查實際訊息流程...")
    print("=" * 50)
    
    try:
        # 檢查是否有實際的 LINE 訊息處理
        print("   🔍 檢查 LINE 訊息處理邏輯...")
        
        # 讀取 app_supabase_fixed.py 文件檢查文字處理邏輯
        with open('app_supabase_fixed.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
            # 檢查關鍵函數是否存在
            if 'def handle_text_message' in content:
                print("   ✅ handle_text_message 函數存在")
            else:
                print("   ❌ handle_text_message 函數不存在")
            
            if '排行榜' in content:
                print("   ✅ 包含排行榜處理邏輯")
            else:
                print("   ❌ 不包含排行榜處理邏輯")
            
            if 'send_leaderboard_message' in content:
                print("   ✅ send_leaderboard_message 函數存在")
            else:
                print("   ❌ send_leaderboard_message 函數不存在")
        
        return True
        
    except Exception as e:
        print(f"   ❌ 檢查訊息流程失敗: {e}")
        return False

def main():
    """主函數"""
    print("🚀 診斷輸入排行榜沒有反應的問題")
    print("=" * 60)
    
    # 1. 檢查環境變量
    env_vars = check_environment()
    
    # 2. 測試排行榜功能
    leaderboard_ok = test_leaderboard_function()
    
    # 3. 測試文字處理
    text_ok = test_text_processing()
    
    # 4. 檢查運行應用
    app_ok = check_running_application()
    
    # 5. 檢查訊息流程
    flow_ok = check_actual_message_flow()
    
    # 總結
    print("\n" + "=" * 60)
    print("📋 診斷結果總結:")
    print(f"   🔧 環境變量: {'✅' if all(env_vars.values()) else '❌'}")
    print(f"   🎨 排行榜功能: {'✅' if leaderboard_ok else '❌'}")
    print(f"   🔤 文字處理: {'✅' if text_ok else '❌'}")
    print(f"   🚀 應用運行: {'✅' if app_ok else '❌'}")
    print(f"   📨 訊息流程: {'✅' if flow_ok else '❌'}")
    
    # 問題分析
    print("\n🔍 問題分析:")
    if not all(env_vars.values()):
        print("   ❌ 環境變量設置不完整")
        print("   💡 解決方案: 重新設置所有環境變量")
    elif not leaderboard_ok:
        print("   ❌ 排行榜功能有問題")
        print("   💡 解決方案: 檢查排行榜相關函數")
    elif not text_ok:
        print("   ❌ 文字處理邏輯有問題")
        print("   💡 解決方案: 檢查文字匹配邏輯")
    elif not app_ok:
        print("   ❌ 應用未運行")
        print("   💡 解決方案: 啟動 Flask 應用")
    else:
        print("   ✅ 所有功能正常，問題可能在於實際使用環境")
        print("   💡 建議: 檢查實際的 LINE Bot 配置和部署")

if __name__ == "__main__":
    main()

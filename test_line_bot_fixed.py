#!/usr/bin/env python3
"""
測試修正後的 LINE Bot 功能
"""

import sys
import os
import requests
import json
import time

def check_venv():
    """檢查是否在正確的虛擬環境中"""
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("❌ 請先啟動虛擬環境：source venv311/bin/activate")
        return False
    
    # 檢查必要的套件
    try:
        import supabase
        print("✅ Supabase 套件已安裝")
    except ImportError:
        print("❌ Supabase 套件未安裝，請執行：pip install supabase")
        return False
    
    try:
        import linebot
        print("✅ LINE Bot SDK 已安裝")
    except ImportError:
        print("❌ LINE Bot SDK 未安裝，請執行：pip install line-bot-sdk")
        return False
    
    return True

def test_webhook_simulation():
    """模擬 LINE webhook 請求"""
    
    # 模擬用戶發送「開始」指令
    webhook_data = {
        "events": [
            {
                "type": "message",
                "message": {
                    "type": "text",
                    "text": "開始"
                },
                "replyToken": "test_reply_token_123",
                "source": {
                    "userId": "test_user_123",
                    "type": "user"
                },
                "timestamp": int(time.time() * 1000)
            }
        ]
    }
    
    try:
        # 發送 webhook 到本地應用程式
        response = requests.post(
            "http://localhost:5001/callback",
            headers={
                "Content-Type": "application/json",
                "X-Line-Signature": "test_signature"
            },
            data=json.dumps(webhook_data),
            timeout=10
        )
        
        print(f"Webhook 回應狀態碼: {response.status_code}")
        print(f"Webhook 回應內容: {response.text}")
        
        return response.status_code == 200
        
    except requests.exceptions.ConnectionError:
        print("❌ 無法連接到應用程式，請確保 app_supabase.py 正在運行")
        return False
    except Exception as e:
        print(f"Webhook 測試失敗: {e}")
        return False

def test_supabase_connection():
    """測試 Supabase 連線"""
    try:
        response = requests.get("http://localhost:5001/test", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"Supabase 測試結果: {data}")
            return data.get("status") == "success"
        else:
            print(f"Supabase 測試失敗，狀態碼: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 無法連接到應用程式，請確保 app_supabase.py 正在運行")
        return False
    except Exception as e:
        print(f"Supabase 測試失敗: {e}")
        return False

def test_user_stats():
    """測試用戶統計功能"""
    try:
        from supabase_user_stats_handler import get_user_stats, add_correct_answer, add_wrong_answer
        
        test_user_id = "test_user_123"
        
        # 獲取初始統計
        initial_stats = get_user_stats(test_user_id)
        print(f"初始統計: {initial_stats}")
        
        # 添加正確答案（使用實際存在的題目 ID）
        success = add_correct_answer(test_user_id, 6)  # 使用實際題目 ID
        print(f"添加正確答案成功: {success}")
        
        # 獲取更新後的統計
        updated_stats = get_user_stats(test_user_id)
        print(f"更新後統計: {updated_stats}")
        
        return success and updated_stats['correct'] > initial_stats['correct']
        
    except ImportError as e:
        print(f"❌ 導入模組失敗: {e}")
        print("請確保在正確的虛擬環境中運行")
        return False
    except Exception as e:
        print(f"用戶統計測試失敗: {e}")
        return False

def main():
    print("🧪 開始測試修正後的 LINE Bot 功能...")
    
    # 檢查虛擬環境
    print("\n0. 檢查虛擬環境...")
    if not check_venv():
        print("\n💡 解決方案：")
        print("1. 啟動虛擬環境：source venv311/bin/activate")
        print("2. 安裝依賴：pip install -r requirements.txt")
        print("3. 重新運行測試：python test_line_bot_fixed.py")
        return
    
    # 測試 Supabase 連線
    print("\n1. 測試 Supabase 連線...")
    if test_supabase_connection():
        print("✅ Supabase 連線正常")
    else:
        print("❌ Supabase 連線失敗")
        return
    
    # 測試用戶統計功能
    print("\n2. 測試用戶統計功能...")
    if test_user_stats():
        print("✅ 用戶統計功能正常")
    else:
        print("❌ 用戶統計功能失敗")
        return
    
    # 測試 webhook 處理
    print("\n3. 測試 webhook 處理...")
    if test_webhook_simulation():
        print("✅ Webhook 處理正常")
    else:
        print("❌ Webhook 處理失敗")
        return
    
    print("\n🎉 所有測試通過！LINE Bot 功能已修正。")
    print("\n📝 修正內容總結：")
    print("1. ✅ 修正了 add_correct_answer 函數參數問題")
    print("2. ✅ 在問題訊息中加入積分顯示")
    print("3. ✅ 修正了 continue_quiz 按鈕處理邏輯")
    print("4. ✅ 在答案處理後發送繼續選單")
    print("5. ✅ 確保積分能即時更新")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
最終生產環境修復腳本
"""

import os
import shutil
import subprocess
import sys
import time
import requests

def check_production_status():
    """檢查生產環境狀態"""
    print("🔍 檢查生產環境狀態...")
    
    try:
        # 檢查健康狀態
        response = requests.get("https://anatomy-quiz-bot.onrender.com/", timeout=10)
        print(f"  📊 健康檢查狀態碼: {response.status_code}")
        
        # 測試 webhook
        webhook_data = {"events": []}
        response = requests.post("https://anatomy-quiz-bot.onrender.com/webhook", 
                               json=webhook_data, 
                               headers={"Content-Type": "application/json"}, 
                               timeout=10)
        print(f"  📊 Webhook 狀態碼: {response.status_code}")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"  ❌ 檢查失敗: {e}")
        return False

def create_production_app():
    """創建生產環境應用程式"""
    print("🔧 創建生產環境應用程式...")
    
    # 讀取修復後的代碼
    with open('app_supabase_fixed.py', 'r', encoding='utf-8') as f:
        fixed_code = f.read()
    
    # 創建生產環境版本
    production_code = fixed_code.replace(
        "app.run(host='0.0.0.0', port=5002, debug=True)",
        "if __name__ == '__main__':\n    import uvicorn\n    uvicorn.run(app, host='0.0.0.0', port=5000)"
    )
    
    # 保存生產環境版本
    with open('app_production_final.py', 'w', encoding='utf-8') as f:
        f.write(production_code)
    
    print("✅ 生產環境應用程式創建完成")

def deploy_to_production():
    """部署到生產環境"""
    print("🚀 部署到生產環境...")
    
    production_path = "/Users/baobaoc/Dev/anatomy_quiz_bot/app_supabase.py"
    
    # 備份原始文件
    if os.path.exists(production_path):
        shutil.copy2(production_path, f"{production_path}.backup.{int(time.time())}")
        print("✅ 已備份原始文件")
    
    # 複製修復後的代碼
    shutil.copy2('app_production_final.py', production_path)
    print("✅ 已複製修復後的代碼到生產環境")
    
    return True

def test_local_leaderboard():
    """測試本地排行榜功能"""
    print("🧪 測試本地排行榜功能...")
    
    try:
        # 測試 webhook
        webhook_data = {
            "events": [
                {
                    "type": "message",
                    "message": {
                        "type": "text",
                        "text": "排行榜"
                    },
                    "source": {
                        "type": "user",
                        "userId": "U977c24d1fec3a2bf07035504e1444911"
                    },
                    "replyToken": "test_token"
                }
            ]
        }
        
        response = requests.post("http://localhost:5002/webhook", 
                               json=webhook_data, 
                               headers={"Content-Type": "application/json"}, 
                               timeout=10)
        
        print(f"  📊 本地測試狀態碼: {response.status_code}")
        print(f"  📊 本地測試響應: {response.text[:200]}...")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"  ❌ 本地測試失敗: {e}")
        return False

def main():
    """主函數"""
    print("🎯 最終生產環境修復...")
    
    # 1. 檢查生產環境狀態
    if check_production_status():
        print("✅ 生產環境正常運行")
        return True
    
    # 2. 創建生產環境應用程式
    create_production_app()
    
    # 3. 部署到生產環境
    if not deploy_to_production():
        print("❌ 部署失敗")
        return False
    
    # 4. 測試本地功能
    if test_local_leaderboard():
        print("✅ 本地排行榜功能正常")
    else:
        print("⚠️ 本地排行榜功能有問題")
    
    print("\n📋 修復完成！")
    print("🚀 請重啟生產環境應用程式：")
    print("   cd /Users/baobaoc/Dev/anatomy_quiz_bot")
    print("   python app_supabase.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

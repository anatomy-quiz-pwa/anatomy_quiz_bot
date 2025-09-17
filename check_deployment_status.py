#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
檢查部署狀態
"""

import requests
import json

def check_deployment_status():
    """檢查部署狀態"""
    print("🔍 檢查部署狀態...")
    
    base_url = "https://anatomy-quiz-bot.onrender.com"
    
    # 檢查根路徑
    try:
        response = requests.get(base_url, timeout=10)
        print(f"📤 根路徑狀態碼: {response.status_code}")
        print(f"📤 根路徑響應: {response.text}")
        
        if response.status_code == 200:
            print("✅ 應用程式正在運行")
        else:
            print(f"❌ 應用程式異常: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 無法連接到應用程式: {e}")
        return False
    
    # 檢查 webhook
    webhook_url = f"{base_url}/webhook"
    
    # 測試 GET 請求
    try:
        response = requests.get(webhook_url, timeout=10)
        print(f"📤 Webhook GET 狀態碼: {response.status_code}")
        print(f"📤 Webhook GET 響應: {response.text}")
        
        if response.status_code == 405:
            print("✅ Webhook 端點存在（405 是預期的）")
        else:
            print(f"⚠️ Webhook GET 返回意外狀態碼: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Webhook GET 測試失敗: {e}")
    
    # 測試 POST 請求
    test_data = {
        "events": [
            {
                "type": "message",
                "source": {
                    "userId": "test_user"
                },
                "message": {
                    "type": "text",
                    "text": "排行榜"
                }
            }
        ]
    }
    
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(webhook_url, json=test_data, headers=headers, timeout=10)
        print(f"📤 Webhook POST 狀態碼: {response.status_code}")
        print(f"📤 Webhook POST 響應: {response.text}")
        
        if response.status_code == 200:
            print("✅ Webhook 修復成功！")
            return True
        elif response.status_code == 500:
            print("❌ Webhook 仍然返回 500 錯誤")
            return False
        else:
            print(f"⚠️ Webhook POST 返回狀態碼: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Webhook POST 測試失敗: {e}")
        return False

def check_server_type():
    """檢查服務器類型"""
    print("\n🔍 檢查服務器類型...")
    
    base_url = "https://anatomy-quiz-bot.onrender.com"
    
    try:
        # 測試一個不存在的端點
        response = requests.get(f"{base_url}/nonexistent", timeout=10)
        print(f"📤 404 響應狀態碼: {response.status_code}")
        print(f"📤 404 響應內容: {response.text}")
        
        # 檢查響應格式
        if '"detail"' in response.text:
            print("⚠️ 響應格式像 FastAPI (包含 'detail' 字段)")
            print("💡 這表示可能仍在使用 uvicorn")
        elif '"error"' in response.text or '"message"' in response.text:
            print("✅ 響應格式像 Flask (包含 'error' 或 'message' 字段)")
            print("💡 這表示可能已切換到 gunicorn")
        else:
            print("❓ 無法確定服務器類型")
            
    except Exception as e:
        print(f"❌ 檢查服務器類型失敗: {e}")

def provide_next_steps():
    """提供下一步建議"""
    print("\n💡 下一步建議:")
    print("1. 確認已將 Procfile 和 requirements.txt 上傳到 Render")
    print("2. 在 Render Dashboard 中手動觸發重新部署")
    print("3. 等待部署完成（通常需要 2-5 分鐘）")
    print("4. 重新運行此腳本檢查狀態")
    
    print("\n📋 如果問題持續存在:")
    print("1. 檢查 Render 部署日誌")
    print("2. 確認 Procfile 格式正確")
    print("3. 確認 requirements.txt 包含 gunicorn")
    print("4. 考慮使用 FastAPI 版本")

def main():
    """主函數"""
    print("🚀 檢查部署狀態")
    print("=" * 50)
    
    # 檢查部署狀態
    status_ok = check_deployment_status()
    
    # 檢查服務器類型
    check_server_type()
    
    # 提供建議
    provide_next_steps()
    
    print("\n" + "=" * 50)
    if status_ok:
        print("🎉 部署狀態正常，排行榜功能應該可以正常運作")
    else:
        print("⚠️ 部署狀態異常，需要進一步檢查")

if __name__ == "__main__":
    main()

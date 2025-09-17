#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
調試生產環境 500 錯誤
"""

import requests
import json
import time

def test_webhook_with_detailed_logging():
    """測試 webhook 並記錄詳細信息"""
    print("🔍 測試 webhook 並記錄詳細信息...")
    
    webhook_url = "https://anatomy-quiz-bot.onrender.com/webhook"
    
    # 測試數據
    test_data = {
        "events": [
            {
                "type": "message",
                "source": {
                    "userId": "U977c24d1fec3a2bf07035504e1444911"
                },
                "message": {
                    "type": "text",
                    "text": "排行榜"
                },
                "replyToken": "test_reply_token_123"
            }
        ]
    }
    
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'LINE Bot SDK'
    }
    
    try:
        print(f"📤 發送請求到: {webhook_url}")
        print(f"📤 請求數據: {json.dumps(test_data, ensure_ascii=False, indent=2)}")
        print(f"📤 請求 headers: {headers}")
        
        response = requests.post(
            webhook_url, 
            json=test_data, 
            headers=headers, 
            timeout=30
        )
        
        print(f"📤 響應狀態碼: {response.status_code}")
        print(f"📤 響應 headers: {dict(response.headers)}")
        print(f"📤 響應內容: {response.text}")
        
        if response.status_code == 200:
            print("✅ 請求成功")
            return True
        else:
            print(f"❌ 請求失敗: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ 請求超時")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ 連接錯誤")
        return False
    except Exception as e:
        print(f"❌ 請求異常: {e}")
        return False

def test_basic_endpoints():
    """測試基本端點"""
    print("\n🔍 測試基本端點...")
    
    base_url = "https://anatomy-quiz-bot.onrender.com"
    
    endpoints = [
        "/",
        "/webhook",
        "/health",
        "/status"
    ]
    
    for endpoint in endpoints:
        url = base_url + endpoint
        try:
            print(f"\n📤 測試端點: {endpoint}")
            
            # 測試 GET
            response = requests.get(url, timeout=10)
            print(f"  GET 狀態碼: {response.status_code}")
            print(f"  GET 響應: {response.text[:100]}...")
            
            # 測試 POST
            response = requests.post(url, json={}, timeout=10)
            print(f"  POST 狀態碼: {response.status_code}")
            print(f"  POST 響應: {response.text[:100]}...")
            
        except Exception as e:
            print(f"  ❌ 測試失敗: {e}")

def test_with_curl_command():
    """生成 curl 命令進行測試"""
    print("\n🔍 生成 curl 命令進行測試...")
    
    webhook_url = "https://anatomy-quiz-bot.onrender.com/webhook"
    
    test_data = {
        "events": [
            {
                "type": "message",
                "source": {
                    "userId": "U977c24d1fec3a2bf07035504e1444911"
                },
                "message": {
                    "type": "text",
                    "text": "排行榜"
                }
            }
        ]
    }
    
    curl_command = f'''curl -X POST {webhook_url} \\
  -H "Content-Type: application/json" \\
  -H "User-Agent: LINE Bot SDK" \\
  -d '{json.dumps(test_data, ensure_ascii=False)}' \\
  -v'''
    
    print("📋 請在終端中執行以下 curl 命令:")
    print(curl_command)
    
    # 也提供簡化版本
    simple_curl = f'''curl -X POST {webhook_url} \\
  -H "Content-Type: application/json" \\
  -d '{{"events":[{{"type":"message","source":{{"userId":"test"}},"message":{{"type":"text","text":"排行榜"}}}}]}}' \\
  -v'''
    
    print("\n📋 簡化版本:")
    print(simple_curl)

def check_render_logs_suggestion():
    """提供檢查 Render 日誌的建議"""
    print("\n🔍 檢查 Render 日誌的建議...")
    
    print("📋 請按照以下步驟檢查 Render 日誌:")
    print("1. 登入 Render Dashboard (https://dashboard.render.com)")
    print("2. 找到您的 anatomy-quiz-bot 服務")
    print("3. 點擊 'Logs' 標籤")
    print("4. 查看最新的日誌，尋找以下內容:")
    print("   - 錯誤訊息 (ERROR)")
    print("   - 異常堆疊 (Traceback)")
    print("   - 應用程式啟動訊息")
    print("   - 數據庫連接狀態")
    
    print("\n📋 常見的 500 錯誤原因:")
    print("1. 環境變數未設置或設置錯誤")
    print("2. 數據庫連接失敗")
    print("3. 依賴項缺失")
    print("4. 代碼語法錯誤")
    print("5. 記憶體不足")
    print("6. 超時錯誤")

def create_minimal_test():
    """創建最小化測試"""
    print("\n🔍 創建最小化測試...")
    
    minimal_code = '''
from flask import Flask, request, jsonify
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        logger.info("📨 收到 webhook 請求")
        data = request.get_json()
        logger.info(f"📊 請求數據: {data}")
        
        if data and 'events' in data:
            for event in data['events']:
                if event.get('type') == 'message':
                    message = event.get('message', {})
                    if message.get('type') == 'text':
                        text = message.get('text', '')
                        logger.info(f"📨 收到文字訊息: {text}")
                        
                        if text.lower() in ['排行榜', 'leaderboard', '排名', '排行']:
                            logger.info("📊 排行榜請求已識別")
                            return jsonify({"status": "success", "message": "排行榜請求已處理"}), 200
        
        return 'OK', 200
        
    except Exception as e:
        logger.error(f"❌ 錯誤: {e}")
        return 'Error', 500

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "ok", "message": "Webhook service is running"})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
'''
    
    with open('minimal_webhook_debug.py', 'w', encoding='utf-8') as f:
        f.write(minimal_code)
    
    print("✅ 最小化測試代碼已創建: minimal_webhook_debug.py")
    print("💡 建議使用此代碼替換當前版本進行測試")

def main():
    """主函數"""
    print("🚀 開始調試生產環境 500 錯誤")
    print("=" * 60)
    
    # 1. 測試 webhook 並記錄詳細信息
    test_webhook_with_detailed_logging()
    
    # 2. 測試基本端點
    test_basic_endpoints()
    
    # 3. 生成 curl 命令
    test_with_curl_command()
    
    # 4. 提供檢查日誌的建議
    check_render_logs_suggestion()
    
    # 5. 創建最小化測試
    create_minimal_test()
    
    print("\n" + "=" * 60)
    print("🏁 調試完成")
    
    print("\n💡 下一步建議:")
    print("1. 檢查 Render 部署日誌")
    print("2. 使用 curl 命令測試")
    print("3. 考慮使用最小化版本")
    print("4. 檢查環境變數設置")

if __name__ == "__main__":
    main()

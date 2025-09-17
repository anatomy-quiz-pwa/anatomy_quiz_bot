#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修復 uvicorn + Flask 兼容性問題
"""

import os

def create_requirements_txt():
    """創建正確的 requirements.txt"""
    print("🔍 創建正確的 requirements.txt...")
    
    requirements = '''flask==3.0.3
requests==2.32.5
supabase==2.6.0
line-bot-sdk==3.12.0
python-dotenv==1.0.1
gunicorn==22.0.0
'''
    
    with open('requirements.txt', 'w', encoding='utf-8') as f:
        f.write(requirements)
    
    print("✅ requirements.txt 已創建")

def create_procfile():
    """創建 Procfile 用於正確的部署"""
    print("🔍 創建 Procfile...")
    
    procfile_content = '''web: gunicorn app_supabase:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120
'''
    
    with open('Procfile', 'w', encoding='utf-8') as f:
        f.write(procfile_content)
    
    print("✅ Procfile 已創建")

def create_fastapi_version():
    """創建 FastAPI 版本的應用程式"""
    print("🔍 創建 FastAPI 版本的應用程式...")
    
    fastapi_code = '''from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import requests
import json
import os
import logging
from supabase import create_client, Client
from typing import Optional
import datetime

app = FastAPI(title="Anatomy Quiz Bot API")

# 設置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 環境變數
PAGE_ACCESS_TOKEN = os.getenv('PAGE_ACCESS_TOKEN')
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# LINE 環境變數
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')

# 如果 LINE 環境變數未設置，使用預設值進行測試
if not LINE_CHANNEL_ACCESS_TOKEN:
    LINE_CHANNEL_ACCESS_TOKEN = "AhZFgYWfEMeFSDxJJhzcvJoKx78lVrfRH3cqqusfiZhug/f5wRhQTkDD9fW7+IJLA3xpoQtunFWoVKnHtaE9p+U1QVFUz1o8CQ5AnNpPicjK32KAD5Z1ouF1HNKATv/BhUHIS3OjcndnUGpOqPDYKAdB04t89/1O/w1cDnyilFU="
    logger.info("🔧 使用預設 LINE_CHANNEL_ACCESS_TOKEN 進行測試")

if not LINE_CHANNEL_SECRET:
    LINE_CHANNEL_SECRET = "c025320a9328abc76bf61f36c1039756"
    logger.info("🔧 使用預設 LINE_CHANNEL_SECRET 進行測試")

# 如果環境變數未設置，使用已知的 Supabase 配置進行測試
if not SUPABASE_URL:
    SUPABASE_URL = "https://ciqlfqfgzqqgdrogedxg.supabase.co"
    logger.info("🔧 使用預設 SUPABASE_URL 進行測試")

if not SUPABASE_KEY:
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA"
    logger.info("🔧 使用預設 SUPABASE_KEY 進行測試")

# 創建 Supabase 客戶端
try:
    logger.info(f"🔗 正在連接 Supabase: {SUPABASE_URL}")
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # 測試連接
    logger.info("🧪 正在測試數據庫連接...")
    test_response = supabase.table('user_stats').select('count', count='exact').limit(1).execute()
    logger.info(f"✅ Supabase 連接成功！數據庫中有 {test_response.count} 條記錄")
    
except Exception as e:
    logger.error(f"❌ Supabase 連接失敗: {e}")
    supabase = None

@app.get("/")
async def root():
    """根路徑"""
    return {"message": "Anatomy Quiz Bot API is running!"}

@app.get("/webhook")
async def verify_webhook(mode: str = None, token: str = None, challenge: str = None):
    """驗證 webhook"""
    if mode and token:
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            return challenge
        else:
            raise HTTPException(status_code=403, detail="Forbidden")
    
    raise HTTPException(status_code=400, detail="Bad Request")

@app.post("/webhook")
async def webhook(request: Request):
    """處理 webhook 訊息"""
    try:
        data = await request.json()
        logger.info(f"📨 收到 webhook 請求: {data}")
        
        # 處理 LINE Bot 訊息
        if 'events' in data:
            for event in data['events']:
                if event['type'] == 'message':
                    sender_id = event['source']['userId']
                    message = event['message']
                    
                    if message['type'] == 'text':
                        message_text = message.get('text', '').strip()
                        logger.info(f"📨 收到來自用戶 {sender_id} 的訊息: {message_text}")
                        
                        # 檢查是否為排行榜請求
                        if message_text.lower() in ['排行榜', 'leaderboard', '排名', '排行']:
                            logger.info(f"📊 用戶 {sender_id} 請求查看排行榜")
                            # 這裡應該發送排行榜，但先只記錄日誌
                            logger.info("✅ 排行榜請求已識別")
                            
                            # 發送簡單的回應
                            await send_line_message(sender_id, {"text": "🏆 排行榜功能正在處理中..."})
        
        return {"status": "success"}
        
    except Exception as e:
        logger.error(f"❌ Webhook 處理失敗: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

async def send_line_message(user_id: str, message_data: dict):
    """發送訊息到 LINE"""
    if not LINE_CHANNEL_ACCESS_TOKEN:
        logger.error("❌ LINE_CHANNEL_ACCESS_TOKEN 未設置")
        return {"error": "LINE_CHANNEL_ACCESS_TOKEN not set"}
    
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {LINE_CHANNEL_ACCESS_TOKEN}'
    }
    
    data = {
        "to": user_id,
        "messages": [message_data]
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        logger.info(f"📤 LINE 訊息發送結果: {response.status_code}")
        
        if response.status_code != 200:
            logger.error(f"❌ LINE 訊息發送失敗 - 狀態碼: {response.status_code}")
            logger.error(f"❌ 響應內容: {response.text}")
        
        return response.json()
    except Exception as e:
        logger.error(f"❌ LINE 訊息發送失敗: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get('PORT', 5000))
    uvicorn.run(app, host="0.0.0.0", port=port)
'''
    
    with open('app_fastapi.py', 'w', encoding='utf-8') as f:
        f.write(fastapi_code)
    
    print("✅ FastAPI 版本的應用程式已創建: app_fastapi.py")

def create_deployment_instructions():
    """創建部署說明"""
    print("🔍 創建部署說明...")
    
    instructions = '''# 修復 uvicorn + Flask 兼容性問題

## 問題分析
生產環境使用 `uvicorn app_supabase:app` 啟動 Flask 應用程式，但 uvicorn 是為 FastAPI 設計的 ASGI 服務器，與 Flask（WSGI）存在兼容性問題。

## 解決方案

### 方案 1: 使用 Gunicorn（推薦）
1. 使用 `requirements.txt` 和 `Procfile`
2. Render 會自動使用 Gunicorn 啟動 Flask 應用程式

### 方案 2: 轉換為 FastAPI
1. 使用 `app_fastapi.py` 替換 `app_supabase.py`
2. 保持使用 uvicorn 啟動

## 部署步驟

### 使用方案 1（Gunicorn + Flask）
1. 將 `requirements.txt` 和 `Procfile` 上傳到 Render
2. 重新部署
3. Render 會自動使用 Gunicorn

### 使用方案 2（FastAPI）
1. 將 `app_fastapi.py` 重命名為 `app_supabase.py`
2. 重新部署
3. 保持使用 uvicorn 啟動

## 測試命令
```bash
# 測試 webhook
curl -X POST https://anatomy-quiz-bot.onrender.com/webhook \\
  -H "Content-Type: application/json" \\
  -d '{"events":[{"type":"message","source":{"userId":"test"},"message":{"type":"text","text":"排行榜"}}]}'
```

## 注意事項
- 方案 1 保持現有 Flask 代碼不變
- 方案 2 需要將 Flask 代碼轉換為 FastAPI
- 建議先嘗試方案 1
'''
    
    with open('DEPLOYMENT_FIX_INSTRUCTIONS.md', 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print("✅ 部署說明已創建: DEPLOYMENT_FIX_INSTRUCTIONS.md")

def main():
    """主函數"""
    print("🚀 開始修復 uvicorn + Flask 兼容性問題")
    print("=" * 60)
    
    # 1. 創建 requirements.txt
    create_requirements_txt()
    
    # 2. 創建 Procfile
    create_procfile()
    
    # 3. 創建 FastAPI 版本
    create_fastapi_version()
    
    # 4. 創建部署說明
    create_deployment_instructions()
    
    print("\n" + "=" * 60)
    print("🏁 修復準備完成")
    
    print("\n📋 已創建的文件:")
    print("  - requirements.txt (正確的依賴項)")
    print("  - Procfile (使用 Gunicorn)")
    print("  - app_fastapi.py (FastAPI 版本)")
    print("  - DEPLOYMENT_FIX_INSTRUCTIONS.md (部署說明)")
    
    print("\n💡 建議的修復步驟:")
    print("1. 上傳 requirements.txt 和 Procfile 到 Render")
    print("2. 重新部署應用程式")
    print("3. 測試 webhook 功能")
    print("4. 如果仍有問題，考慮使用 FastAPI 版本")

if __name__ == "__main__":
    main()

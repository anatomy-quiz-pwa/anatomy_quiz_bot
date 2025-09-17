#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
創建超級簡單版本
"""

def create_super_simple():
    """創建超級簡單版本"""
    print("🔍 創建超級簡單版本...")
    
    # 創建一個超級簡單的 FastAPI 應用程式
    super_simple_content = '''from fastapi import FastAPI, Request
import json
import logging

app = FastAPI(title="Anatomy Quiz Bot API")

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/")
async def root():
    """根路徑"""
    return {"message": "Anatomy Quiz Bot API is running!", "version": "super_simple_v1"}

@app.post("/webhook")
async def webhook(request: Request):
    """處理 webhook 訊息"""
    try:
        logger.info("📨 收到 webhook 請求")
        
        # 獲取請求數據
        data = await request.json()
        logger.info(f"📨 請求數據: {data}")
        
        # 檢查是否為排行榜請求
        if 'events' in data:
            for event in data['events']:
                if event['type'] == 'message':
                    message = event['message']
                    if message['type'] == 'text':
                        message_text = message.get('text', '').strip()
                        if message_text.lower() in ['排行榜', 'leaderboard', '排名', '排行']:
                            logger.info(f"📊 收到排行榜請求: {message_text}")
                            return {"status": "success", "message": "排行榜請求已收到", "version": "super_simple_v1"}
        
        # 簡單回應
        return {"status": "success", "message": "webhook 正常運作", "version": "super_simple_v1"}
        
    except Exception as e:
        logger.error(f"❌ Webhook 處理失敗: {e}")
        return {"status": "error", "message": str(e), "version": "super_simple_v1"}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get('PORT', 5000))
    uvicorn.run(app, host="0.0.0.0", port=port)
'''
    
    target_file = "/Users/baobaoc/Dev/anatomy_quiz_bot/app_supabase.py"
    
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(super_simple_content)
    
    print(f"✅ 超級簡單版本已創建: {target_file}")

def update_requirements_super_simple():
    """更新 requirements.txt 為超級簡單版本"""
    print("🔍 更新 requirements.txt 為超級簡單版本...")
    
    super_simple_requirements = """fastapi==0.115.14
uvicorn==0.30.1
"""
    
    requirements_file = "/Users/baobaoc/Dev/anatomy_quiz_bot/requirements.txt"
    
    with open(requirements_file, 'w', encoding='utf-8') as f:
        f.write(super_simple_requirements)
    
    print("✅ requirements.txt 已更新為超級簡單版本")

def main():
    """主函數"""
    print("🚀 創建超級簡單版本")
    print("=" * 50)
    
    # 1. 創建超級簡單版本
    create_super_simple()
    
    # 2. 更新 requirements.txt
    update_requirements_super_simple()
    
    print("\n" + "=" * 50)
    print("🎉 超級簡單版本完成！")
    print("\n📋 下一步:")
    print("1. 將 app_supabase.py、requirements.txt 上傳到 Render")
    print("2. 重新部署應用程式")
    print("3. 測試 webhook 基本功能")
    print("\n💡 這個版本:")
    print("- 包含版本標識符 'super_simple_v1'")
    print("- 可以識別排行榜請求")
    print("- 只返回 JSON 響應")
    print("- 應該能夠在 uvicorn 下正常運作")

if __name__ == "__main__":
    main()

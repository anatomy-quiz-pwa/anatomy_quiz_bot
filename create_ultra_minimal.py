#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
創建極簡版本
"""

def create_ultra_minimal():
    """創建極簡版本"""
    print("🔍 創建極簡版本...")
    
    # 創建一個極簡的 FastAPI 應用程式
    ultra_minimal_content = '''from fastapi import FastAPI, Request
import json
import logging

app = FastAPI(title="Anatomy Quiz Bot API")

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/")
async def root():
    """根路徑"""
    return {"message": "Anatomy Quiz Bot API is running!"}

@app.post("/webhook")
async def webhook(request: Request):
    """處理 webhook 訊息"""
    try:
        logger.info("📨 收到 webhook 請求")
        
        # 獲取請求數據
        data = await request.json()
        logger.info(f"📨 請求數據: {data}")
        
        # 簡單回應
        return {"status": "success", "message": "webhook 正常運作"}
        
    except Exception as e:
        logger.error(f"❌ Webhook 處理失敗: {e}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get('PORT', 5000))
    uvicorn.run(app, host="0.0.0.0", port=port)
'''
    
    target_file = "/Users/baobaoc/Dev/anatomy_quiz_bot/app_supabase.py"
    
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(ultra_minimal_content)
    
    print(f"✅ 極簡版本已創建: {target_file}")

def update_requirements_minimal():
    """更新 requirements.txt 為極簡版本"""
    print("🔍 更新 requirements.txt 為極簡版本...")
    
    minimal_requirements = """fastapi==0.115.14
uvicorn==0.30.1
"""
    
    requirements_file = "/Users/baobaoc/Dev/anatomy_quiz_bot/requirements.txt"
    
    with open(requirements_file, 'w', encoding='utf-8') as f:
        f.write(minimal_requirements)
    
    print("✅ requirements.txt 已更新為極簡版本")

def main():
    """主函數"""
    print("🚀 創建極簡版本")
    print("=" * 50)
    
    # 1. 創建極簡版本
    create_ultra_minimal()
    
    # 2. 更新 requirements.txt
    update_requirements_minimal()
    
    print("\n" + "=" * 50)
    print("🎉 極簡版本完成！")
    print("\n📋 下一步:")
    print("1. 將 app_supabase.py、requirements.txt 上傳到 Render")
    print("2. 重新部署應用程式")
    print("3. 測試 webhook 基本功能")
    print("\n💡 這個版本:")
    print("- 只包含最基本的 FastAPI 功能")
    print("- 沒有任何外部依賴項")
    print("- 只返回 JSON 響應")
    print("- 應該能夠在 uvicorn 下正常運作")

if __name__ == "__main__":
    main()

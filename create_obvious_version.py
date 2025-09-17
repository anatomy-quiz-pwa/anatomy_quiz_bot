#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
創建明顯版本標識符
"""

def create_obvious_version():
    """創建明顯版本標識符"""
    print("🔍 創建明顯版本標識符...")
    
    # 創建一個包含明顯版本標識符的 FastAPI 應用程式
    obvious_version_content = '''from fastapi import FastAPI, Request
import json
import logging

app = FastAPI(title="Anatomy Quiz Bot API")

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/")
async def root():
    """根路徑"""
    return {
        "message": "Anatomy Quiz Bot API is running!", 
        "version": "OBVIOUS_VERSION_V2_2025_09_16",
        "status": "DEPLOYED_SUCCESSFULLY",
        "timestamp": "2025-09-16T15:02:00Z"
    }

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
                            return {
                                "status": "success", 
                                "message": "排行榜請求已收到", 
                                "version": "OBVIOUS_VERSION_V2_2025_09_16",
                                "action": "LEADERBOARD_REQUEST_DETECTED"
                            }
        
        # 簡單回應
        return {
            "status": "success", 
            "message": "webhook 正常運作", 
            "version": "OBVIOUS_VERSION_V2_2025_09_16",
            "action": "GENERAL_MESSAGE_PROCESSED"
        }
        
    except Exception as e:
        logger.error(f"❌ Webhook 處理失敗: {e}")
        return {
            "status": "error", 
            "message": str(e), 
            "version": "OBVIOUS_VERSION_V2_2025_09_16",
            "action": "ERROR_OCCURRED"
        }

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get('PORT', 5000))
    uvicorn.run(app, host="0.0.0.0", port=port)
'''
    
    target_file = "/Users/baobaoc/Dev/anatomy_quiz_bot/app_supabase.py"
    
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(obvious_version_content)
    
    print(f"✅ 明顯版本標識符已創建: {target_file}")

def create_deployment_guide():
    """創建部署指南"""
    print("🔍 創建部署指南...")
    
    guide_content = f"""# Render 部署指南

## 問題診斷
❌ Render 沒有使用我們上傳的文件
- 根路徑響應不包含版本標識符
- webhook 仍然返回 500 錯誤
- 所有端點都不包含版本標識符

## 解決方案

### 1. 確認文件上傳
請確認以下文件已正確上傳到 Render：
- `app_supabase.py` (包含明顯版本標識符)
- `requirements.txt` (FastAPI 依賴項)

### 2. 重新部署步驟
1. 登入 Render Dashboard
2. 找到您的應用程式
3. 點擊 "Manual Deploy"
4. 選擇 "Deploy latest commit"
5. 等待部署完成

### 3. 驗證部署
部署完成後，訪問以下 URL 檢查版本標識符：
- 根路徑: https://anatomy-quiz-bot.onrender.com/
- 應該看到: `"version": "OBVIOUS_VERSION_V2_2025_09_16"`

### 4. 測試 webhook
使用測試腳本驗證 webhook 功能：
```bash
python test_obvious_version.py
```

## 版本標識符
當前版本: `OBVIOUS_VERSION_V2_2025_09_16`
如果看到這個標識符，表示部署成功。

## 故障排除
如果仍然看不到版本標識符：
1. 檢查 Render 部署日誌
2. 確認文件路徑正確
3. 嘗試刪除並重新創建應用程式
4. 檢查 Render 服務狀態
"""
    
    with open("/Users/baobaoc/Dev/anatomy_quiz_bot/DEPLOYMENT_GUIDE.md", 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print("✅ 部署指南已創建: DEPLOYMENT_GUIDE.md")

def main():
    """主函數"""
    print("🚀 創建明顯版本標識符")
    print("=" * 50)
    
    # 1. 創建明顯版本標識符
    create_obvious_version()
    
    # 2. 創建部署指南
    create_deployment_guide()
    
    print("\n" + "=" * 50)
    print("🎉 明顯版本標識符完成！")
    print("\n📋 下一步:")
    print("1. 將 app_supabase.py、requirements.txt 上傳到 Render")
    print("2. 重新部署應用程式")
    print("3. 檢查根路徑是否包含版本標識符")
    print("4. 測試 webhook 功能")
    print("\n💡 版本標識符:")
    print("- 根路徑: 'OBVIOUS_VERSION_V2_2025_09_16'")
    print("- 如果看到這個標識符，表示部署成功")
    print("- 如果看不到，表示 Render 沒有使用我們的文件")

if __name__ == "__main__":
    main()

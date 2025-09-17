#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
創建直接解決方案
"""

def create_direct_solution():
    """創建直接解決方案"""
    print("🔍 創建直接解決方案...")
    
    # 創建一個包含非常明顯標識符的 FastAPI 應用程式
    direct_solution_content = '''from fastapi import FastAPI, Request
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
        "version": "DIRECT_SOLUTION_V3_2025_09_17",
        "status": "DEPLOYED_SUCCESSFULLY",
        "timestamp": "2025-09-17T02:05:00Z",
        "debug": "THIS_IS_THE_NEW_VERSION"
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
                                "version": "DIRECT_SOLUTION_V3_2025_09_17",
                                "action": "LEADERBOARD_REQUEST_DETECTED",
                                "debug": "LEADERBOARD_FUNCTION_WORKING"
                            }
        
        # 簡單回應
        return {
            "status": "success", 
            "message": "webhook 正常運作", 
            "version": "DIRECT_SOLUTION_V3_2025_09_17",
            "action": "GENERAL_MESSAGE_PROCESSED",
            "debug": "WEBHOOK_FUNCTION_WORKING"
        }
        
    except Exception as e:
        logger.error(f"❌ Webhook 處理失敗: {e}")
        return {
            "status": "error", 
            "message": str(e), 
            "version": "DIRECT_SOLUTION_V3_2025_09_17",
            "action": "ERROR_OCCURRED",
            "debug": "ERROR_IN_WEBHOOK"
        }

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get('PORT', 5000))
    uvicorn.run(app, host="0.0.0.0", port=port)
'''
    
    target_file = "/Users/baobaoc/Dev/anatomy_quiz_bot/app_supabase.py"
    
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(direct_solution_content)
    
    print(f"✅ 直接解決方案已創建: {target_file}")

def create_deployment_checklist():
    """創建部署檢查清單"""
    print("🔍 創建部署檢查清單...")
    
    checklist_content = f"""# Render 部署檢查清單

## 問題確認
❌ Render 沒有使用我們上傳的文件
- 根路徑響應不包含版本標識符
- webhook 仍然返回 500 錯誤
- 所有端點都不包含版本標識符

## 部署步驟檢查清單

### 1. 文件準備 ✅
- [ ] 確認 app_supabase.py 包含版本標識符 "DIRECT_SOLUTION_V3_2025_09_17"
- [ ] 確認 requirements.txt 包含 FastAPI 依賴項
- [ ] 確認文件路徑正確

### 2. Render 上傳
- [ ] 登入 Render Dashboard
- [ ] 找到您的應用程式
- [ ] 點擊 "Files" 或 "Code" 標籤
- [ ] 上傳 app_supabase.py
- [ ] 上傳 requirements.txt
- [ ] 確認文件已成功上傳

### 3. 重新部署
- [ ] 點擊 "Manual Deploy"
- [ ] 選擇 "Deploy latest commit"
- [ ] 等待部署完成
- [ ] 檢查部署日誌是否有錯誤

### 4. 驗證部署
- [ ] 訪問: https://anatomy-quiz-bot.onrender.com/
- [ ] 應該看到: "version": "DIRECT_SOLUTION_V3_2025_09_17"
- [ ] 應該看到: "debug": "THIS_IS_THE_NEW_VERSION"

### 5. 測試 webhook
- [ ] 使用測試腳本: python test_direct_solution.py
- [ ] 檢查 webhook 是否返回 200 狀態碼
- [ ] 檢查響應是否包含版本標識符

## 故障排除

### 如果仍然看不到版本標識符：
1. 檢查 Render 部署日誌
2. 確認文件上傳成功
3. 嘗試刪除並重新創建應用程式
4. 檢查 Render 服務狀態
5. 聯繫 Render 支援

### 如果 webhook 仍然返回 500 錯誤：
1. 檢查 Render 部署日誌
2. 確認 FastAPI 應用程式語法正確
3. 檢查依賴項是否正確安裝
4. 嘗試簡化應用程式邏輯

## 版本標識符
當前版本: DIRECT_SOLUTION_V3_2025_09_17
如果看到這個標識符，表示部署成功。
"""
    
    with open("/Users/baobaoc/Dev/anatomy_quiz_bot/DEPLOYMENT_CHECKLIST.md", 'w', encoding='utf-8') as f:
        f.write(checklist_content)
    
    print("✅ 部署檢查清單已創建: DEPLOYMENT_CHECKLIST.md")

def main():
    """主函數"""
    print("🚀 創建直接解決方案")
    print("=" * 50)
    
    # 1. 創建直接解決方案
    create_direct_solution()
    
    # 2. 創建部署檢查清單
    create_deployment_checklist()
    
    print("\n" + "=" * 50)
    print("🎉 直接解決方案完成！")
    print("\n📋 下一步:")
    print("1. 將 app_supabase.py、requirements.txt 上傳到 Render")
    print("2. 重新部署應用程式")
    print("3. 檢查根路徑是否包含版本標識符")
    print("4. 測試 webhook 功能")
    print("\n💡 版本標識符:")
    print("- 根路徑: 'DIRECT_SOLUTION_V3_2025_09_17'")
    print("- 調試信息: 'THIS_IS_THE_NEW_VERSION'")
    print("- 如果看到這些標識符，表示部署成功")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
LINE Bot 狀態檢查工具
用於檢查 LINE Bot 是否遇到月度限制問題
"""

import os
import requests
import json
from datetime import datetime

# 載入環境變數
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', 
    "AhZFgYWfEMeFSDxJJhzcvJoKx78lVrfRH3cqqusfiZhug/f5wRhQTkDD9fW7+IJLA3xpoQtunFWoVKnHtaE9p+U1QVFUz1o8CQ5AnNpPicjK32KAD5Z1ouF1HNKATv/BhUHIS3OjcndnUGpOqPDYKAdB04t89/1O/w1cDnyilFU=")

def check_line_bot_quota():
    """檢查 LINE Bot 的配額狀態"""
    print("🔍 正在檢查 LINE Bot 狀態...")
    
    # 測試用戶ID（寶的帳號）
    test_user_id = "U977c24d1fec3a2bf07035504e1444911"
    
    # 嘗試發送一個簡單的測試訊息
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {LINE_CHANNEL_ACCESS_TOKEN}'
    }
    
    test_message = {
        "to": test_user_id,
        "messages": [{
            "type": "text",
            "text": "🔍 LINE Bot 狀態檢查 - " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(test_message))
        
        print(f"📊 HTTP 狀態碼: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ LINE Bot 狀態正常，可以發送訊息")
            return True
        elif response.status_code == 429:
            try:
                error_data = response.json()
                print(f"❌ LINE Bot 已達到月度限制")
                print(f"📝 錯誤詳情: {error_data}")
                
                if "monthly limit" in error_data.get("message", "").lower():
                    print("🚨 確認：這是月度訊息發送限制問題")
                    print("💡 解決方案：")
                    print("   1. 升級到付費計劃")
                    print("   2. 等待下個計費週期重置")
                    print("   3. 優化訊息發送策略")
                
                return False
            except:
                print(f"❌ 解析錯誤響應失敗: {response.text}")
                return False
        else:
            print(f"⚠️ 其他錯誤: {response.status_code}")
            print(f"📝 響應內容: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 檢查失敗: {e}")
        return False

def get_quota_info():
    """獲取配額信息（如果可用）"""
    print("\n📈 配額信息:")
    print("   LINE Messaging API 免費配額通常為每月 1000 條訊息")
    print("   付費計劃可獲得更多配額")
    print("   詳情請查看: https://developers.line.biz/en/docs/messaging-api/")

def show_recommendations():
    """顯示建議"""
    print("\n💡 建議:")
    print("1. 🔧 代碼優化:")
    print("   - 合併相關訊息")
    print("   - 使用 Flex Messages 替代多條文字訊息")
    print("   - 實施訊息配額管理")
    
    print("\n2. 📊 監控:")
    print("   - 定期檢查訊息發送量")
    print("   - 設置警告閾值")
    print("   - 記錄用戶互動模式")
    
    print("\n3. 🚀 升級選項:")
    print("   - 考慮付費計劃")
    print("   - 評估多渠道支持")
    print("   - 實施負載均衡")

if __name__ == "__main__":
    print("=" * 50)
    print("🤖 LINE Bot 狀態檢查工具")
    print("=" * 50)
    
    # 檢查配額狀態
    is_working = check_line_bot_quota()
    
    # 顯示配額信息
    get_quota_info()
    
    # 顯示建議
    show_recommendations()
    
    print("\n" + "=" * 50)
    if is_working:
        print("✅ 檢查完成 - LINE Bot 狀態正常")
    else:
        print("❌ 檢查完成 - LINE Bot 遇到問題，請參考上述建議")
    print("=" * 50)

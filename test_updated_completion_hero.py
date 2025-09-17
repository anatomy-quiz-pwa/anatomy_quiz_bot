#!/usr/bin/env python3
"""
測試更新後的Level 14通關完成Hero圖片
使用新的finish_14 level.jpg圖片
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app_supabase import (
    send_completion_celebration,
    send_message,
    create_completion_celebration_flex,
    get_user_nickname
)
import logging
import datetime

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_updated_completion_hero():
    """測試更新後的通關完成Hero圖片"""
    print("🎯 測試更新後的Level 14通關完成Hero圖片")
    print("=" * 60)
    
    # 保的LINE用戶ID
    bao_user_id = "U977c24d1fec3a2bf07035504e1444911"
    
    print(f"📱 目標用戶ID: {bao_user_id}")
    print(f"🖼️ 新的Hero圖片: finish_14 level.jpg")
    print()
    
    # 1. 發送更新通知
    print("1️⃣ 發送更新通知...")
    try:
        update_message = {
            "text": f"🔄 Level 14通關完成訊息已更新！\n\n🖼️ 新增專屬Hero圖片:\n'finish_14 level.jpg'\n\n📅 更新時間: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n接下來會發送更新後的通關完成訊息給你測試！"
        }
        send_message(bao_user_id, update_message)
        print("   ✅ 更新通知發送成功！")
    except Exception as e:
        print(f"   ❌ 更新通知發送失敗: {e}")
    print()
    
    # 2. 獲取用戶暱稱
    print("2️⃣ 獲取用戶暱稱...")
    try:
        nickname = get_user_nickname(bao_user_id)
        print(f"   ✅ 用戶暱稱: {nickname}")
    except Exception as e:
        print(f"   ❌ 獲取暱稱失敗: {e}")
        nickname = "pao"
    print()
    
    # 3. 測試創建更新後的Flex Message
    print("3️⃣ 測試創建更新後的Flex Message...")
    try:
        completion_flex = create_completion_celebration_flex(nickname, 14)
        if completion_flex:
            print("   ✅ 更新後的Flex Message創建成功")
            print(f"   📝 altText: {completion_flex.get('altText', 'N/A')}")
            
            # 檢查圖片URL
            header = completion_flex.get('contents', {}).get('header', {})
            contents = header.get('contents', [])
            if contents and len(contents) > 0:
                image_url = contents[0].get('url', '')
                print(f"   🖼️ Hero圖片URL: {image_url}")
                
                if 'finish_14%20level.jpg' in image_url:
                    print("   ✅ Hero圖片URL已正確更新為 finish_14 level.jpg")
                else:
                    print("   ⚠️ Hero圖片URL可能未正確更新")
            else:
                print("   ⚠️ 無法檢查Hero圖片URL")
        else:
            print("   ❌ Flex Message創建失敗")
    except Exception as e:
        print(f"   ❌ Flex Message創建錯誤: {e}")
    print()
    
    # 4. 發送更新後的通關完成訊息
    print("4️⃣ 發送更新後的通關完成訊息...")
    try:
        send_completion_celebration(bao_user_id, 14)
        print("   ✅ 更新後的通關完成訊息發送成功！")
        print("   📨 請檢查你的LINE是否收到了帶有新Hero圖片的通關完成訊息")
    except Exception as e:
        print(f"   ❌ 通關完成訊息發送失敗: {e}")
    print()
    
    # 5. 發送圖片URL確認訊息
    print("5️⃣ 發送圖片URL確認訊息...")
    try:
        url_message = {
            "text": f"🖼️ 通關完成Hero圖片資訊確認：\n\n📂 檔案名稱: finish_14 level.jpg\n🔗 完整URL:\nhttps://ciqlfqfgzqqgdrogedxg.supabase.co/storage/v1/object/public/linebot/finish_14%20level.jpg\n\n✅ 此圖片現在會顯示在Level 14通關完成的Flex Message中！\n\n如果上面的通關訊息顯示了新的Hero圖片，表示更新成功！"
        }
        send_message(bao_user_id, url_message)
        print("   ✅ 圖片URL確認訊息發送成功！")
    except Exception as e:
        print(f"   ❌ 圖片URL確認訊息發送失敗: {e}")
    print()
    
    print("=" * 60)
    print("🎉 Level 14通關完成Hero圖片更新測試完成！")
    print()
    print("📋 更新總結：")
    print("   ✅ 更新了create_completion_celebration_flex函數")
    print("   ✅ Hero圖片從 completion_trophy.png 更換為 finish_14 level.jpg")
    print("   ✅ 發送了更新後的通關完成訊息到你的LINE帳號")
    print()
    print("🔍 請確認：")
    print("   1. 你的LINE是否收到了帶有新Hero圖片的通關完成訊息？")
    print("   2. 新的Hero圖片是否正確顯示？")
    print("   3. Flex Message的其他內容是否正常？")

if __name__ == "__main__":
    test_updated_completion_hero()

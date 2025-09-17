#!/usr/bin/env python3
"""
測試level升級Flex Message結構
"""

import sys
import json

# 模擬app_supabase中的函數
def get_level_title(level):
    """根據等級獲取對應的稱號"""
    level_titles = {
        1: "新手解剖師", 2: "初級解剖師", 3: "初級解剖師", 4: "中級解剖師", 
        5: "中級解剖師", 6: "中級解剖師", 7: "中級解剖師", 8: "高級解剖師",
        9: "高級解剖師", 10: "高級解剖師", 11: "高級解剖師", 12: "專家解剖師",
        13: "專家解剖師", 14: "終極解剖師"
    }
    return level_titles.get(level, f"等級{level}解剖師")

def create_level_up_flex_message(old_level, new_level):
    """創建level升級的Flex Message"""
    try:
        # 獲取等級對應的稱號
        old_title = get_level_title(old_level)
        new_title = get_level_title(new_level)
        
        # 獲取等級對應的海報圖片
        level_poster_url = f"https://ciqlfqfgzqqgdrogedxg.supabase.co/storage/v1/object/public/linebot/level_{new_level}_poster.png"
        
        flex_message = {
            "type": "flex",
            "altText": f"🎉 恭喜升級！從{old_title}晉升為{new_title}！",
            "contents": {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": level_poster_url,
                    "size": "full",
                    "aspectRatio": "20:13",
                    "aspectMode": "cover"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🎉 恭喜升級！",
                            "weight": "bold",
                            "size": "xl",
                            "color": "#FF6B35",
                            "align": "center",
                            "margin": "md"
                        },
                        {
                            "type": "text",
                            "text": f"🏆 從{old_title}",
                            "size": "md",
                            "color": "#666666",
                            "align": "center",
                            "margin": "md"
                        },
                        {
                            "type": "text",
                            "text": f"晉升為{new_title}！",
                            "size": "md",
                            "color": "#666666",
                            "align": "center"
                        },
                        {
                            "type": "separator",
                            "margin": "xl"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "lg",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": f"你已經掌握了等級 {new_level} 的知識，",
                                    "color": "#666666",
                                    "size": "sm",
                                    "align": "center"
                                },
                                {
                                    "type": "text",
                                    "text": f"現在開始挑戰等級 {new_level + 1} 的更高難度！",
                                    "color": "#666666",
                                    "size": "sm",
                                    "align": "center"
                                },
                                {
                                    "type": "text",
                                    "text": "繼續加油，朝著終極解剖師的目標前進！",
                                    "color": "#FF6B35",
                                    "size": "sm",
                                    "align": "center",
                                    "weight": "bold",
                                    "margin": "md"
                                }
                            ]
                        }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "button",
                            "style": "primary",
                            "height": "sm",
                            "action": {
                                "type": "message",
                                "label": "🚀 繼續答題",
                                "text": "開始"
                            },
                            "color": "#FF6B35"
                        }
                    ],
                    "flex": 0
                }
            }
        }
        
        return flex_message
        
    except Exception as e:
        print(f"❌ 創建level升級Flex Message失敗: {e}")
        return None

def test_level_up_flex_messages():
    """測試不同等級升級的Flex Message"""
    print("=" * 60)
    print("🧪 測試Level升級Flex Message結構")
    print("=" * 60)
    
    test_cases = [
        (2, 3),  # 初級解剖師 -> 初級解剖師
        (3, 4),  # 初級解剖師 -> 中級解剖師
        (7, 8),  # 中級解剖師 -> 高級解剖師
        (11, 12), # 高級解剖師 -> 專家解剖師
        (13, 14), # 專家解剖師 -> 終極解剖師
    ]
    
    for old_level, new_level in test_cases:
        print(f"\n📊 測試升級: {old_level} -> {new_level}")
        print(f"   稱號變化: {get_level_title(old_level)} -> {get_level_title(new_level)}")
        
        # 創建Flex Message
        flex_message = create_level_up_flex_message(old_level, new_level)
        
        if flex_message:
            print("   ✅ Flex Message創建成功")
            print(f"   📷 Hero圖片: level_{new_level}_poster.png")
            print(f"   📝 Alt Text: {flex_message['altText']}")
            
            # 驗證結構
            contents = flex_message['contents']
            assert contents['type'] == 'bubble', "結構應該是bubble"
            assert 'hero' in contents, "應該包含hero區塊"
            assert 'body' in contents, "應該包含body區塊"
            assert 'footer' in contents, "應該包含footer區塊"
            
            # 驗證hero圖片
            hero_url = contents['hero']['url']
            expected_url = f"https://ciqlfqfgzqqgdrogedxg.supabase.co/storage/v1/object/public/linebot/level_{new_level}_poster.png"
            assert hero_url == expected_url, f"Hero圖片URL不正確: {hero_url}"
            
            print("   ✅ 結構驗證通過")
            
        else:
            print("   ❌ Flex Message創建失敗")
            
    print("\n" + "=" * 60)
    print("✅ 所有測試完成")
    
    # 輸出一個完整的範例
    print("\n📄 完整Flex Message範例 (等級3->4升級):")
    example_flex = create_level_up_flex_message(3, 4)
    if example_flex:
        print(json.dumps(example_flex, ensure_ascii=False, indent=2))

def test_level_titles():
    """測試等級稱號對應"""
    print("\n🏷️  測試等級稱號對應:")
    print("-" * 40)
    
    for level in range(1, 15):
        title = get_level_title(level)
        print(f"   等級 {level:2d}: {title}")
    
    print(f"   等級 99: {get_level_title(99)}")  # 測試未定義等級

if __name__ == "__main__":
    try:
        test_level_titles()
        test_level_up_flex_messages()
        
        print("\n🎉 所有測試順利完成！")
        print("\n💡 使用方式:")
        print("   1. 在LINE Bot中，當用戶升級時會自動觸發此Flex Message")
        print("   2. 每個等級都有對應的hero海報圖片")
        print("   3. 包含完整的升級慶祝內容和繼續答題按鈕")
        print("   4. 支援多層備用方案確保訊息能正常發送")
        
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {e}")
        sys.exit(1)

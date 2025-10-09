#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修復暱稱設置完成後自動開始答題的流程
"""

# 這是對 app_supabase.py 的修改建議

def suggested_fix_for_nickname_success():
    """
    修復建議：在暱稱設置成功後自動發送第一道題目
    """
    
    # 在 app_supabase.py 的暱稱設置成功邏輯中，
    # 在發送暱稱成功 Flex Message 之後，添加以下邏輯：
    
    suggested_code = '''
    # 在第265行之後添加：
    
    # 暱稱設置成功後，自動開始第一道題目
    logger.info(f"🎯 暱稱設置完成，準備為用戶 {user_id} 自動發送第一道題目")
    
    try:
        # 檢查用戶是否為管理員
        admin_info = get_user_admin_info(user_id)
        
        if admin_info and admin_info.get('is_admin'):
            # 管理員用戶：自動發送管理員模式的第一道題目
            send_admin_quiz_question(user_id)
            logger.info(f"✅ 已為管理員用戶 {user_id} 自動發送第一道題目")
        else:
            # 普通用戶：檢查每日限制後發送題目
            daily_limit_status = check_daily_question_limit(user_id)
            
            if daily_limit_status['can_answer']:
                # 獲取用戶統計（如果不存在會創建）
                user_stats = get_user_stats(user_id)
                if not user_stats:
                    user_stats = create_initial_user_stats(user_id)
                
                current_level = user_stats.get('level', 1) if user_stats else 1
                send_quiz_question(user_id, level=current_level)
                logger.info(f"✅ 已為普通用戶 {user_id} 自動發送第一道題目 (等級 {current_level})")
            else:
                # 已達每日限制，發送提醒
                nickname = get_user_nickname(user_id) or "朋友"
                send_message(user_id, {
                    "text": f"🎉 {nickname}，歡迎加入！\\n\\n⏰ 今天的答題次數已達上限，明天再來挑戰吧！\\n\\n📊 輸入「積分」查看學習進度\\n🏆 輸入「排行榜」查看排名"
                })
                logger.info(f"ℹ️ 用戶 {user_id} 已達每日答題限制，發送歡迎但不能答題的訊息")
                
    except Exception as auto_quiz_error:
        logger.error(f"❌ 自動發送第一道題目失敗: {auto_quiz_error}")
        # 失敗時發送引導訊息
        nickname = get_user_nickname(user_id) or "朋友"
        send_message(user_id, {
            "text": f"🎉 {nickname}，歡迎加入！\\n\\n🚀 輸入「開始」開始你的解剖學學習之旅！\\n📊 輸入「積分」查看學習進度\\n🏆 輸入「排行榜」查看排名"
        })
        logger.info(f"📝 已為用戶 {user_id} 發送手動開始指引")
    '''
    
    return suggested_code

def create_improved_nickname_success_message():
    """
    改進暱稱成功訊息，讓用戶更容易開始答題
    """
    
    improved_message = '''
    def create_nickname_success_flex_message(nickname):
        """創建暱稱設定成功的 flex 訊息模板（改進版）"""
        return {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": "https://ciqlfqfgzqqgdrogedxg.supabase.co/storage/v1/object/public/linebot/nickname.png",
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
                        "text": "🎉 設定完成！",
                        "weight": "bold",
                        "size": "xl",
                        "color": "#B5651D"
                    },
                    {
                        "type": "text",
                        "text": f"好的，之後就叫你「{nickname}」啦！",
                        "size": "md",
                        "color": "#666666",
                        "margin": "md"
                    },
                    {
                        "type": "separator",
                        "margin": "xl"
                    },
                    {
                        "type": "text",
                        "text": "🚀 準備好開始解剖學學習之旅了嗎？",
                        "size": "md",
                        "color": "#333333",
                        "margin": "xl",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": "第一道題目即將為你準備好！",
                        "size": "sm",
                        "color": "#666666",
                        "margin": "sm"
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
                        "color": "#B5651D",
                        "action": {
                            "type": "message",
                            "label": "🚀 立即開始答題",
                            "text": "開始"
                        }
                    },
                    {
                        "type": "button",
                        "style": "secondary",
                        "action": {
                            "type": "message",
                            "label": "📊 查看學習進度",
                            "text": "積分"
                        }
                    }
                ]
            }
        }
    '''
    
    return improved_message

if __name__ == "__main__":
    print("📋 修復建議：")
    print("=" * 50)
    print("1. 在暱稱設置成功後自動發送第一道題目")
    print("2. 改進暱稱成功訊息的引導性")
    print("3. 為無法答題的用戶提供清楚的說明")
    print("\n詳細修改代碼請查看此文件的函數內容。")

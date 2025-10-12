#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生產環境 LINE Bot 應用程序 - 包含完整排行榜功能
"""

import os
import logging
from flask import Flask, request, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
from supabase import create_client, Client
import json
from typing import Optional
from datetime import datetime, timedelta
import uuid
import requests

app = Flask(__name__)

# 設置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 環境變數
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# 如果環境變數未設置，使用預設值
if not LINE_CHANNEL_ACCESS_TOKEN:
    LINE_CHANNEL_ACCESS_TOKEN = "AhZFgYWfEMeFSDxJJhzcvJoKx78lVrfRH3cqqusfiZhug/f5wRhQTkDD9fW7+IJLA3xpoQtunFWoVKnHtaE9p+U1QVFUz1o8CQ5AnNpPicjK32KAD5Z1ouF1HNKATv/BhUHIS3OjcndnUGpOqPDYKAdB04t89/1O/w1cDnyilFU="
    logger.info("🔧 使用預設 LINE_CHANNEL_ACCESS_TOKEN")

if not LINE_CHANNEL_SECRET:
    LINE_CHANNEL_SECRET = "c025320a9328abc76bf61f36c1039756"
    logger.info("🔧 使用預設 LINE_CHANNEL_SECRET")

if not SUPABASE_URL:
    SUPABASE_URL = "https://ciqlfqfgzqqgdrogedxg.supabase.co"
    logger.info("🔧 使用預設 SUPABASE_URL")

if not SUPABASE_KEY:
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA"
    logger.info("🔧 使用預設 SUPABASE_KEY")

# 創建 LINE Bot API 實例
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 創建 Supabase 客戶端
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    logger.info(f"✅ Supabase 連接成功: {SUPABASE_URL}")
except Exception as e:
    logger.error(f"❌ Supabase 連接失敗: {e}")
    supabase = None

def get_user_nickname(user_id):
    """從 users 表格獲取用戶暱稱"""
    try:
        if supabase is None:
            return f"用戶_{user_id}"
        
        response = supabase.table('users').select('game_nickname').eq('line_user_id', user_id).execute()
        
        if response.data and len(response.data) > 0:
            nickname = response.data[0].get('game_nickname')
            if nickname:
                return nickname
        
        return f"用戶_{user_id[2:10] if user_id.startswith('U') else user_id}"
        
    except Exception as e:
        logger.error(f"❌ 獲取用戶 {user_id} 暱稱失敗: {e}")
        return f"用戶_{user_id}"

def get_real_students_data():
    """獲取真實的 Supabase 數據並轉換為標準格式"""
    logger.info("📊 正在從 Supabase 獲取真實數據...")
    
    if supabase is None:
        logger.error("❌ Supabase 未連接")
        return []
    
    try:
        # 獲取用戶統計數據 - 使用正確的列名: correct, wrong (不是 total)
        response = supabase.table('user_stats').select('*').order('correct', desc=True).execute()
        
        if not response.data:
            logger.error("❌ 無法獲取用戶統計數據")
            return []
        
        logger.info(f"✅ 成功獲取 {len(response.data)} 條真實數據")
        
        # 轉換數據格式
        students_data = []
        for item in response.data:
            user_id = item.get('user_id', '')
            nickname = get_user_nickname(user_id)
            
            correct = item.get('correct', 0)
            wrong = item.get('wrong', 0)
            total = correct + wrong  # 計算總題數
            
            student = {
                'name': nickname,
                'score': correct * 10,  # 分數 = 正確題數 * 10
                'correct': correct,
                'total': total,
                'level': item.get('level', 1),
                'user_id': user_id
            }
            students_data.append(student)
        
        logger.info(f"✅ 數據轉換完成，共 {len(students_data)} 條記錄")
        
        # 記錄前3名
        for i, student in enumerate(students_data[:3]):
            logger.info(f"🏆 第{i+1}名: {student['name']} - {student['score']}分 (正確:{student['correct']}, 總題:{student['total']})")
        
        return students_data
        
    except Exception as e:
        logger.error(f"❌ 獲取真實數據失敗: {e}")
        return []

def create_leaderboard_flex_message(top_10, all_students, user_id):
    """創建排行榜 Flex Message"""
    try:
        logger.info("🎨 正在創建排行榜 Flex Message...")
        
        # 找到用戶在排行榜中的位置
        user_rank = 0
        user_score = 0
        for i, student in enumerate(all_students):
            if student['user_id'] == user_id:
                user_rank = i + 1
                user_score = student['score']
                break
        
        # 創建排行榜內容
        leaderboard_items = []
        for i, student in enumerate(top_10):
            rank_emoji = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"{i+1}."
            
            leaderboard_items.append({
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "text",
                        "text": rank_emoji,
                        "size": "sm",
                        "color": "#666666",
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": student['name'][:10],  # 限制暱稱長度
                        "size": "sm",
                        "color": "#666666",
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": f"{student['score']}分",
                        "size": "sm",
                        "color": "#666666",
                        "align": "end"
                    }
                ]
            })
        
        # 創建 Flex Message 結構
        flex_message = {
            "type": "flex",
            "altText": "🏆 排行榜 - 前10名",
            "contents": {
                "type": "bubble",
                "size": "kilo",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🏆 排行榜",
                            "weight": "bold",
                            "size": "xl",
                            "color": "#0066CC"
                        },
                        {
                            "type": "text",
                            "text": "前10名成績",
                            "size": "sm",
                            "color": "#666666"
                        }
                    ]
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": leaderboard_items
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": f"你的排名: 第{user_rank}名",
                                    "size": "sm",
                                    "color": "#0066CC",
                                    "weight": "bold"
                                },
                                {
                                    "type": "text",
                                    "text": f" ({user_score}分)",
                                    "size": "sm",
                                    "color": "#666666"
                                }
                            ]
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "postback",
                                "label": "重新挑戰",
                                "data": "action=start_quiz"
                            },
                            "style": "primary",
                            "color": "#0066CC"
                        }
                    ]
                }
            }
        }
        
        logger.info("✅ 排行榜 Flex Message 創建成功")
        return flex_message
        
    except Exception as e:
        logger.error(f"❌ 創建排行榜 Flex Message 失敗: {e}")
        return None

def safe_reply_message(reply_token, message):
    """安全發送回覆訊息"""
    try:
        logger.info(f"[DEBUG] safe_reply_message 開始執行")
        logger.info(f"[DEBUG] reply_token: {reply_token}")
        logger.info(f"[DEBUG] message type: {type(message)}")
        logger.info(f"[DEBUG] message content: {message}")
        
        if isinstance(message, dict) and message.get('type') == 'flex':
            logger.info(f"[DEBUG] Flex Message沒有包含hero圖片")
            logger.info(f"[DEBUG] Contents鍵值: {list(message.get('contents', {}).keys())}")
            logger.info(f"[DEBUG] 使用 LINE Messaging API 發送訊息")
            logger.info(f"[DEBUG] 發送 FlexMessage")
            
            # 發送 Flex Message
            line_bot_api.reply_message(reply_token, FlexSendMessage.new_from_json_dict(message))
        else:
            # 發送文字訊息
            line_bot_api.reply_message(reply_token, TextSendMessage(text=str(message)))
        
        logger.info(f"[DEBUG] safe_reply_message 已執行，內容為：FlexMessage")
        return True
        
    except Exception as e:
        logger.error(f"❌ safe_reply_message 失敗: {e}")
        return False

@app.route('/api/create-link-token', methods=['POST'])
def create_link_token():
    """創建一次性連結 token，用於 LINE 帳號與網站登入綁定"""
    try:
        data = request.get_json()
        line_user_id = data.get('line_user_id')
        
        if not line_user_id:
            logger.error("❌ 缺少 line_user_id")
            return jsonify({"ok": False, "reason": "missing_line_user_id"}), 400
        
        # 生成 UUID token
        token = str(uuid.uuid4())
        
        # 設定過期時間（10 分鐘後）
        expires_at = (datetime.utcnow() + timedelta(minutes=10)).isoformat() + 'Z'
        
        # 插入到 Supabase
        if supabase is None:
            logger.error("❌ Supabase 未連接")
            return jsonify({"ok": False, "reason": "database_error"}), 500
        
        response = supabase.table('link_tokens').insert({
            'token': token,
            'line_user_id': line_user_id,
            'expires_at': expires_at,
            'used': False
        }).execute()
        
        logger.info(f"✅ 為用戶 {line_user_id} 創建連結 token: {token}")
        
        return jsonify({"ok": True, "token": token}), 200
        
    except Exception as e:
        logger.error(f"❌ 創建連結 token 失敗: {e}")
        return jsonify({"ok": False, "reason": "server_error", "error": str(e)}), 500

@app.route('/webhook', methods=['POST'])
def webhook():
    """處理 LINE Webhook"""
    try:
        signature = request.headers['X-Line-Signature']
        body = request.get_data(as_text=True)
        logger.info(f"[🔁 收到 LINE Webhook] {body}")
        
        # 處理 webhook
        handler.handle(body, signature)
        logger.info(f"[✅ Webhook 處理成功]")
        return 'OK', 200
        
    except InvalidSignatureError:
        logger.error("❌ 無效的簽名")
        return 'Bad Request', 400
    except Exception as e:
        logger.error(f"❌ Webhook 處理失敗: {e}")
        return 'Internal Server Error', 500

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """處理文字訊息"""
    try:
        user_id = event.source.user_id
        message_text = event.message.text.strip()
        
        logger.info(f"📨 收到來自用戶 {user_id} 的訊息: {message_text}")
        
        # 處理網站連結請求
        if message_text in ['網站', 'website', '網頁', 'web']:
            logger.info(f"🌐 用戶 {user_id} 請求網站連結")
            
            try:
                # 呼叫 API 創建連結 token
                import requests
                api_url = os.getenv('API_BASE_URL', 'http://localhost:5000')
                response = requests.post(
                    f"{api_url}/api/create-link-token",
                    json={"line_user_id": user_id},
                    timeout=5
                )
                
                if response.status_code == 200:
                    token = response.json().get('token')
                    site_base = os.getenv('WEBSITE_URL', 'https://anatomy-quiz-bot.vercel.app')
                    
                    # 創建 Flex Message
                    flex_message = FlexSendMessage(
                        alt_text="在網站中繼續遊戲",
                        contents={
                            "type": "bubble",
                            "body": {
                                "type": "box",
                                "layout": "vertical",
                                "spacing": "md",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "🌐 在網站中繼續遊戲",
                                        "weight": "bold",
                                        "size": "xl",
                                        "color": "#C57B57"
                                    },
                                    {
                                        "type": "text",
                                        "text": "點一下把你的 LINE 帳號與網站登入連結，同步等級與紀錄。",
                                        "size": "sm",
                                        "wrap": True,
                                        "color": "#666666",
                                        "margin": "md"
                                    },
                                    {
                                        "type": "separator",
                                        "margin": "lg"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "margin": "lg",
                                        "spacing": "sm",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": "✨ 網站功能特色",
                                                "weight": "bold",
                                                "size": "sm",
                                                "color": "#1C1C1C"
                                            },
                                            {
                                                "type": "text",
                                                "text": "• 大螢幕更好操作\n• 進度自動同步\n• 隨時隨地學習",
                                                "size": "xs",
                                                "wrap": True,
                                                "color": "#999999",
                                                "margin": "sm"
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
                                        "color": "#C57B57",
                                        "action": {
                                            "type": "uri",
                                            "label": "🔗 一鍵連結並開始",
                                            "uri": f"{site_base}/link?token={token}"
                                        }
                                    },
                                    {
                                        "type": "text",
                                        "text": "連結有效期限：10 分鐘",
                                        "size": "xxs",
                                        "color": "#999999",
                                        "align": "center",
                                        "margin": "sm"
                                    }
                                ]
                            }
                        }
                    )
                    
                    line_bot_api.reply_message(event.reply_token, flex_message)
                    logger.info(f"✅ 已發送網站連結給用戶 {user_id}")
                    return
                else:
                    logger.error(f"❌ 創建連結 token 失敗: {response.status_code}")
                    safe_reply_message(event.reply_token, "抱歉，創建連結失敗，請稍後再試。")
                    return
                    
            except Exception as e:
                logger.error(f"❌ 處理網站連結請求失敗: {e}")
                safe_reply_message(event.reply_token, "抱歉，目前無法生成網站連結，請稍後再試。")
                return
        
        # 處理排行榜請求
        if message_text in ['排行榜', 'leaderboard', '排名', '排行']:
            logger.info(f"📊 用戶 {user_id} 請求查看排行榜")
            
            # 獲取排行榜數據
            students_data = get_real_students_data()
            
            if not students_data:
                logger.warning("⚠️ 無法獲取排行榜數據")
                safe_reply_message(event.reply_token, "抱歉，目前無法獲取排行榜數據，請稍後再試。")
                return
            
            # 創建排行榜 Flex Message
            top_10 = students_data[:10]
            leaderboard_message = create_leaderboard_flex_message(top_10, students_data, user_id)
            
            if leaderboard_message:
                safe_reply_message(event.reply_token, leaderboard_message)
            else:
                safe_reply_message(event.reply_token, "抱歉，創建排行榜時發生錯誤，請稍後再試。")
        
        # 處理其他訊息（保持原有邏輯）
        else:
            # 這裡可以添加其他訊息處理邏輯
            logger.info(f"📝 處理其他訊息: {message_text}")
            # 可以保持原有的遊戲開始邏輯
            safe_reply_message(event.reply_token, "請輸入「排行榜」查看排行榜，或輸入「開始」開始遊戲！")
            
    except Exception as e:
        logger.error(f"❌ 處理訊息失敗: {e}")
        safe_reply_message(event.reply_token, "抱歉，處理您的訊息時發生錯誤，請稍後再試。")

if __name__ == '__main__':
    logger.info("🚀 啟動生產環境 LINE Bot 應用程序")
    app.run(port=int(os.environ.get('PORT', 5000)), debug=False)

from flask import Flask, request, jsonify
import requests
import json
import os
import logging
from supabase import create_client, Client
from typing import Optional
import datetime

app = Flask(__name__)

# 健康檢查端點
@app.route("/__health", methods=["GET"])
def __health():
    build_id = "not_found"
    try:
        if os.path.exists(".build_id"):
            with open(".build_id", "r") as f:
                build_id = f.read().strip()
    except Exception:
        pass
    return jsonify({"ok": True, "buildId": build_id})

# 設置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log', encoding='utf-8')
    ]
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

def get_user_nickname(user_id):
    """從 users 表格獲取用戶暱稱"""
    try:
        # 查詢 users 表格中的 game_nickname
        response = supabase.table('users').select('game_nickname').eq('line_user_id', user_id).execute()
        
        if response.data and len(response.data) > 0:
            nickname = response.data[0].get('game_nickname')
            if nickname:
                logger.info(f"✅ 找到用戶 {user_id} 的暱稱: {nickname}")
                return nickname
        
        # 如果沒有找到暱稱，生成默認名稱
        logger.info(f"⚠️ 用戶 {user_id} 沒有暱稱，使用默認名稱")
        return generate_default_nickname(user_id)
        
    except Exception as e:
        logger.error(f"❌ 獲取用戶 {user_id} 暱稱失敗: {e}")
        return generate_default_nickname(user_id)

def generate_default_nickname(user_id):
    """生成默認暱稱"""
    if user_id.startswith('U') and len(user_id) > 10:
        # LINE 用戶ID，使用後8位
        return f"用戶_{user_id[2:10]}"
    elif user_id.startswith('test'):
        # 測試用戶，使用 test 後的部分
        return f"測試用戶_{user_id[5:]}"
    else:
        # 其他用戶ID
        return f"用戶_{user_id}"

def get_user_admin_permissions(user_id):
    """獲取用戶管理員權限"""
    try:
        if supabase is None:
            logger.error("❌ Supabase 未連接，無法獲取管理員權限")
            return None
        
        # 查詢用戶的管理員權限
        response = supabase.table('users').select(
            'is_admin', 'admin_levels', 'test_mode', 'admin_permissions'
        ).eq('line_user_id', user_id).execute()
        
        if response.data and len(response.data) > 0:
            user_data = response.data[0]
            admin_info = {
                'is_admin': user_data.get('is_admin', False),
                'admin_levels': user_data.get('admin_levels', []),
                'test_mode': user_data.get('test_mode', False),
                'admin_permissions': user_data.get('admin_permissions', {})
            }
            logger.info(f"✅ 獲取用戶 {user_id} 管理員權限: {admin_info}")
            return admin_info
        else:
            logger.info(f"⚠️ 用戶 {user_id} 沒有管理員權限記錄")
            return None
            
    except Exception as e:
        logger.error(f"❌ 獲取用戶 {user_id} 管理員權限失敗: {e}")
        return None

def check_admin_access(user_id, required_level=None):
    """檢查用戶是否有管理員權限訪問指定level"""
    try:
        admin_info = get_user_admin_permissions(user_id)
        if not admin_info:
            return False
        
        # 檢查是否為管理員
        if not admin_info.get('is_admin', False):
            return False
        
        # 檢查測試模式
        if not admin_info.get('test_mode', False):
            return False
        
        # 檢查權限配置
        permissions = admin_info.get('admin_permissions', {})
        if not permissions.get('can_access_all_levels', False):
            return False
        
        # 如果指定了level，檢查是否在允許的level列表中
        if required_level is not None:
            admin_levels = admin_info.get('admin_levels', [])
            if required_level not in admin_levels:
                return False
        
        logger.info(f"✅ 用戶 {user_id} 具有管理員權限，可訪問level {required_level}")
        return True
        
    except Exception as e:
        logger.error(f"❌ 檢查用戶 {user_id} 管理員權限失敗: {e}")
        return False

def is_admin_user(user_id):
    """檢查用戶是否為管理員"""
    try:
        admin_info = get_user_admin_permissions(user_id)
        if not admin_info:
            return False
        
        return admin_info.get('is_admin', False) and admin_info.get('test_mode', False)
        
    except Exception as e:
        logger.error(f"❌ 檢查用戶 {user_id} 是否為管理員失敗: {e}")
        return False

def get_real_students_data():
    """獲取真實的 Supabase 數據並轉換為標準格式"""
    logger.info("📊 正在從 Supabase 獲取真實數據...")
    
    if supabase is None:
        logger.error("❌ Supabase 未連接，無法獲取真實數據")
        return []
    
    try:
        # 獲取所有用戶統計數據，按正確答案數排序
        response = supabase.table('user_stats').select('*').order('correct', desc=True).execute()
        raw_data = response.data
        
        logger.info(f"✅ 成功獲取 {len(raw_data)} 條真實數據")
        
        # 轉換數據格式以適配現有的顯示邏輯
        students_data = []
        for i, record in enumerate(raw_data):
            # 計算分數（基於正確答案數）
            correct_answers = record.get('correct', 0)
            wrong_answers = record.get('wrong', 0)
            total_questions = correct_answers + wrong_answers
            score = correct_answers * 10  # 每題10分
            
            # 獲取用戶暱稱
            user_id = record.get('user_id', f'user_{i+1:03d}')
            nickname = get_user_nickname(user_id)
            
            # 轉換為標準格式
            student_data = {
                "user_id": user_id,
                "name": nickname,
                "level": record.get('level', 1),
                "score": score,
                "questions_answered": total_questions,
                "correct_answers": correct_answers,
                "last_active": record.get('last_update', record.get('last_updated', '未知'))
            }
            
            students_data.append(student_data)
        
        # 按分數重新排序
        students_data = sorted(students_data, key=lambda x: x['score'], reverse=True)
        
        logger.info(f"✅ 數據轉換完成，共 {len(students_data)} 條記錄")
        
        # 記錄前3名數據樣本
        for i, student in enumerate(students_data[:3], 1):
            logger.info(f"🏆 第{i}名: {student['name']} - {student['score']}分 (正確:{student['correct_answers']}, 總題:{student['questions_answered']})")
        
        return students_data
        
    except Exception as e:
        logger.error(f"❌ 獲取真實數據失敗: {e}")
        return []

def send_message(recipient_id, message_data):
    """發送訊息到 LINE 或 Facebook Messenger"""
    # 檢查是否為 LINE 用戶ID（以 U 開頭）
    if recipient_id.startswith('U'):
        return send_line_message(recipient_id, message_data)
    else:
        return send_facebook_message(recipient_id, message_data)

def send_facebook_message(recipient_id, message_data):
    """發送訊息到 Facebook Messenger"""
    url = f"https://graph.facebook.com/v18.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    headers = {'Content-Type': 'application/json'}
    
    data = {
        "recipient": {"id": recipient_id},
        "message": message_data
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

def send_line_message(user_id, message_data):
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
        return response.json()
    except Exception as e:
        logger.error(f"❌ LINE 訊息發送失敗: {e}")
        return {"error": str(e)}

def get_leaderboard_data():
    """獲取排行榜數據"""
    try:
        logger.info("📊 正在從 Supabase 獲取真實數據...")
        
        # 使用 Supabase 查詢獲取排行榜數據
        response = supabase.table('user_stats').select('*').order('score', desc=True).limit(10).execute()
        
        if response.data:
            logger.info(f"✅ 成功獲取 {len(response.data)} 條真實數據")
            return response.data
        else:
            logger.warning("⚠️ 沒有獲取到排行榜數據")
            return []
            
    except Exception as e:
        logger.error(f"❌ 獲取排行榜數據失敗: {e}")
        return []

def send_leaderboard_message(user_id):
    """發送排行榜 Flex Message"""
    try:
        logger.info(f"📊 正在為用戶 {user_id} 準備排行榜 Flex Message...")
        
        # 獲取排行榜數據
        students_data = get_leaderboard_data()
        
        if not students_data:
            logger.warning("⚠️ 無法獲取排行榜數據，發送錯誤訊息")
            send_message(user_id, {"text": "抱歉，目前無法獲取排行榜數據，請稍後再試。"})
            return
        
        # 限制顯示前10名
        top_10 = students_data[:10]
        
        # 創建 Flex Message 排行榜
        flex_message = create_leaderboard_flex_message(top_10, students_data, user_id)
        
        # 發送 Flex Message
        send_message(user_id, flex_message)
        
        logger.info(f"✅ 成功發送排行榜 Flex Message 給用戶 {user_id}")
        
    except Exception as e:
        logger.error(f"❌ 發送排行榜 Flex Message 失敗: {e}")
        send_message(user_id, {"text": "抱歉，發送排行榜時發生錯誤，請稍後再試。"})

def create_leaderboard_flex_message(top_10, all_students, user_id):
    """創建排行榜 Flex Message"""
    try:
        # 找到用戶的排名
        user_rank = None
        user_student = None
        for i, student in enumerate(all_students, 1):
            if student['user_id'] == user_id:
                user_rank = i
                user_student = student
                break
        
        # 創建 Flex Message 內容
        flex_content = {
            "type": "flex",
            "altText": "🏆 排行榜 - 前10名",
            "contents": {
                "type": "bubble",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🏆 排行榜",
                            "weight": "bold",
                            "size": "xl",
                            "color": "#2c1810",
                            "align": "center"
                        },
                        {
                            "type": "text",
                            "text": "前10名",
                            "size": "sm",
                            "color": "#8b4513",
                            "align": "center",
                            "margin": "sm"
                        }
                    ],
                    "backgroundColor": "#d2b48c",
                    "paddingAll": "lg"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": []
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "postback",
                                "label": "🔄 重新挑戰",
                                "data": "RESTART_CHALLENGE"
                            },
                            "style": "primary",
                            "color": "#8b4513"
                        }
                    ],
                    "spacing": "sm"
                }
            }
        }
        
        # 添加排行榜項目
        for i, student in enumerate(top_10, 1):
            # 獲取排名圖示和顏色
            if i == 1:
                rank_icon = "🥇"
                rank_color = "#d4af37"
            elif i == 2:
                rank_icon = "🥈"
                rank_color = "#c0c0c0"
            elif i == 3:
                rank_icon = "🥉"
                rank_color = "#cd7f32"
            else:
                rank_icon = f"{i}"
                rank_color = "#8b4513"
            
            # 計算準確率
            accuracy = (student["correct_answers"] / student["questions_answered"] * 100) if student["questions_answered"] > 0 else 0
            
            # 創建排名項目
            rank_item = {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": rank_icon,
                        "size": "lg",
                        "flex": 0,
                        "margin": "sm"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": student['name'],
                                "weight": "bold",
                                "size": "sm",
                                "color": "#2c1810"
                            },
                            {
                                "type": "text",
                                "text": f"分數: {student['score']} | 等級: {student['level']}",
                                "size": "xs",
                                "color": "#8b4513",
                                "margin": "xs"
                            },
                            {
                                "type": "text",
                                "text": f"答題: {student['questions_answered']} | 正確: {student['correct_answers']} ({accuracy:.1f}%)",
                                "size": "xs",
                                "color": "#8b4513"
                            }
                        ],
                        "flex": 1,
                        "margin": "sm"
                    }
                ],
                "backgroundColor": "#f5f5dc" if i % 2 == 0 else "#ffffff",
                "paddingAll": "sm",
                "margin": "xs",
                "cornerRadius": "sm"
            }
            
            flex_content["contents"]["body"]["contents"].append(rank_item)
        
        # 添加用戶自己的排名信息（如果不在前10名）
        if user_rank and user_rank > 10 and user_student:
            user_accuracy = (user_student["correct_answers"] / user_student["questions_answered"] * 100) if user_student["questions_answered"] > 0 else 0
            
            # 分隔線
            separator = {
                "type": "separator",
                "margin": "md"
            }
            flex_content["contents"]["body"]["contents"].append(separator)
            
            # 用戶排名項目
            user_rank_item = {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": "📍",
                        "size": "lg",
                        "flex": 0,
                        "margin": "sm"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": f"你的排名: 第{user_rank}名",
                                "weight": "bold",
                                "size": "sm",
                                "color": "#2c1810"
                            },
                            {
                                "type": "text",
                                "text": f"分數: {user_student['score']} | 等級: {user_student['level']}",
                                "size": "xs",
                                "color": "#8b4513",
                                "margin": "xs"
                            },
                            {
                                "type": "text",
                                "text": f"答題: {user_student['questions_answered']} | 正確: {user_student['correct_answers']} ({user_accuracy:.1f}%)",
                                "size": "xs",
                                "color": "#8b4513"
                            }
                        ],
                        "flex": 1,
                        "margin": "sm"
                    }
                ],
                "backgroundColor": "#e6f3ff",
                "paddingAll": "sm",
                "margin": "xs",
                "cornerRadius": "sm"
            }
            
            flex_content["contents"]["body"]["contents"].append(user_rank_item)
        
        # 添加鼓勵文字
        encouragement = {
            "type": "text",
            "text": "💡 繼續挑戰，提升你的排名！",
            "size": "sm",
            "color": "#8b4513",
            "align": "center",
            "margin": "md"
        }
        flex_content["contents"]["body"]["contents"].append(encouragement)
        
        return flex_content
        
    except Exception as e:
        logger.error(f"❌ 創建排行榜 Flex Message 失敗: {e}")
        # 如果 Flex Message 創建失敗，返回文字訊息
        return {"text": "抱歉，排行榜顯示出現問題，請稍後再試。"}

def send_level_up_celebration(user_id, old_level, new_level):
    """發送帶有 hero 圖示的升級慶祝訊息 - 修復版本"""
    
    # 檢查是否達到最高等級
    MAX_LEVEL = 14  # 根據實際數據，最高等級是14
    
    if new_level >= MAX_LEVEL:
        # 發送通關完成慶祝訊息
        send_completion_celebration(user_id, new_level)
        return
    
    # 方案1: 使用 Hero 模板（推薦）
    try:
        hero_message = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": "🎉 恭喜升級！",
                            "image_url": "https://ciqlfqfgzqqgdrogedxg.supabase.co/storage/v1/object/public/linebot/levelup.png",
                            "subtitle": f"從{old_level} 晉升為{new_level}！",
                            "buttons": [
                                {
                                    "type": "postback",
                                    "title": "繼續挑戰",
                                    "payload": "CONTINUE_CHALLENGE"
                                }
                            ]
                        }
                    ]
                }
            }
        }
        
        # 發送 Hero 訊息
        send_message(user_id, hero_message)
        
        # 發送詳細文字訊息
        text_message = {
            "text": f"你已經掌握了等級{new_level}的知識, 現在開始挑戰等級{new_level+1}的更高難度！\n繼續加油,朝著終極解剖師的目標前進！"
        }
        send_message(user_id, text_message)
        
    except Exception as e:
        print(f"Hero 模板發送失敗: {e}")
        
        # 方案2: 備用方案 - 先發送圖片，再發送文字
        try:
            # 發送圖片
            image_message = {
                "attachment": {
                    "type": "image",
                    "payload": {
                        "url": "https://ciqlfqfgzqqgdrogedxg.supabase.co/storage/v1/object/public/linebot/levelup.png"
                    }
                }
            }
            send_message(user_id, image_message)
            
            # 發送慶祝文字
            celebration_text = f"🎉 恭喜升級！\n從{old_level} 晉升為{new_level}！\n你已經掌握了等級{new_level}的知識, 現在開始挑戰等級{new_level+1}的更高難度！\n繼續加油,朝著終極解剖師的目標前進！"
            
            text_message = {"text": celebration_text}
            send_message(user_id, text_message)
            
        except Exception as e2:
            print(f"備用方案也失敗: {e2}")
            
            # 方案3: 最後備用 - 只發送文字
            fallback_text = f"🎉 恭喜升級！\n從{old_level} 晉升為{new_level}！\n你已經掌握了等級{new_level}的知識, 現在開始挑戰等級{new_level+1}的更高難度！\n繼續加油,朝著終極解剖師的目標前進！"
            send_message(user_id, {"text": fallback_text})

def send_completion_celebration(user_id, final_level):
    """發送通關完成慶祝訊息"""
    try:
        # 獲取用戶暱稱
        nickname = get_user_nickname(user_id)
        
        # 方案1: 使用 Hero 模板發送通關完成訊息
        try:
            completion_message = {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": [
                            {
                                "title": "🏆 恭喜通關完成！",
                                "image_url": "https://ciqlfqfgzqqgdrogedxg.supabase.co/storage/v1/object/public/linebot/levelup.png",
                                "subtitle": f"🎉 {nickname} 已成功完成所有等級挑戰！",
                                "buttons": [
                                    {
                                        "type": "postback",
                                        "title": "查看排行榜",
                                        "payload": "VIEW_LEADERBOARD"
                                    },
                                    {
                                        "type": "postback",
                                        "title": "重新挑戰",
                                        "payload": "RESTART_CHALLENGE"
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
            
            # 發送通關完成訊息
            send_message(user_id, completion_message)
            
        except Exception as e:
            print(f"通關完成 Hero 模板發送失敗: {e}")
        
        # 發送詳細的通關完成文字訊息
        completion_text = f"""🏆 恭喜 {nickname} 通關完成！

🎉 你已經成功完成了所有 {final_level} 個等級的挑戰！
🌟 你現在是真正的解剖學大師！

📊 通關成就：
✅ 完成了所有等級的學習
✅ 掌握了完整的解剖學知識體系
✅ 成為了終極解剖師

🎯 接下來你可以：
• 查看排行榜，看看自己的排名
• 重新挑戰，鞏固已學知識
• 幫助其他學員學習
• 等待新的挑戰內容更新

感謝你的堅持學習，繼續保持這份熱情！"""
        
        text_message = {"text": completion_text}
        send_message(user_id, text_message)
        
        # 發送特殊成就徽章訊息
        badge_message = {
            "text": "🏅 獲得特殊成就：終極解剖師徽章！\n\n這枚徽章代表你已經掌握了所有解剖學知識，是真正的學習冠軍！"
        }
        send_message(user_id, badge_message)
        
    except Exception as e:
        print(f"通關完成慶祝訊息發送失敗: {e}")
        
        # 備用方案：只發送簡單文字
        fallback_text = f"🏆 恭喜 {nickname}！你已經完成了所有等級的挑戰，成為了終極解剖師！"
        send_message(user_id, {"text": fallback_text})

def get_user_stats(user_id: str) -> Optional[dict]:
    """獲取用戶統計資料"""
    try:
        response = supabase.table('user_stats').select('*').eq('user_id', user_id).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        print(f"獲取用戶統計失敗: {e}")
        return None

def update_user_level(user_id: str, new_level: int) -> bool:
    """更新用戶等級"""
    try:
        supabase.table('user_stats').upsert({
            'user_id': user_id,
            'level': new_level
        }).execute()
        return True
    except Exception as e:
        print(f"更新用戶等級失敗: {e}")
        return False

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    """驗證 webhook"""
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    if mode and token:
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            return challenge
        else:
            return 'Forbidden', 403
    
    return 'Bad Request', 400

@app.route('/webhook', methods=['POST'])
def webhook():
    """處理 webhook 訊息"""
    data = request.get_json()
    
    # 處理 LINE Bot 訊息
    if 'events' in data:
        for event in data['events']:
            if event['type'] == 'message':
                sender_id = event['source']['userId']
                message = event['message']
                
                if message['type'] == 'text':
                    # 處理文字訊息
                    handle_text_message(sender_id, message)
                
            elif event['type'] == 'postback':
                sender_id = event['source']['userId']
                postback = event['postback']
                # 處理按鈕點擊
                handle_postback(sender_id, postback)
    
    # 處理 Facebook Messenger 訊息
    elif 'object' in data and data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                sender_id = messaging_event['sender']['id']
                
                if messaging_event.get('message'):
                    # 處理文字訊息
                    handle_text_message(sender_id, messaging_event['message'])
                
                elif messaging_event.get('postback'):
                    # 處理按鈕點擊
                    handle_postback(sender_id, messaging_event['postback'])
    
    return 'OK', 200

def handle_text_message(sender_id, message):
    """處理文字訊息"""
    try:
        message_text = message.get('text', '').strip()
        logger.info(f"📨 收到來自用戶 {sender_id} 的訊息: {message_text}")
        
        # 檢查是否為管理員用戶
        if is_admin_user(sender_id):
            logger.info(f"🔑 用戶 {sender_id} 是管理員，啟用測試模式")
            handle_admin_message(sender_id, message_text)
        else:
            logger.info(f"👤 用戶 {sender_id} 是普通用戶")
            handle_regular_message(sender_id, message_text)
            
    except Exception as e:
        logger.error(f"❌ 處理文字訊息失敗: {e}")
        send_message(sender_id, {"text": "抱歉，處理您的訊息時發生錯誤，請稍後再試。"})

def handle_admin_message(sender_id, message_text):
    """處理管理員訊息"""
    try:
        # 管理員特殊命令
        if message_text.startswith('/admin'):
            handle_admin_command(sender_id, message_text)
        elif message_text.startswith('/test'):
            handle_test_command(sender_id, message_text)
        elif message_text.startswith('/level'):
            handle_level_command(sender_id, message_text)
        else:
            # 普通訊息處理，但具有管理員權限
            handle_regular_message(sender_id, message_text)
            
    except Exception as e:
        logger.error(f"❌ 處理管理員訊息失敗: {e}")
        send_message(sender_id, {"text": "管理員功能處理失敗，請檢查命令格式。"})

def handle_admin_command(sender_id, message_text):
    """處理管理員命令"""
    try:
        # 解析管理員命令
        parts = message_text.split()
        if len(parts) < 2:
            send_message(sender_id, {
                "text": "管理員命令格式：\n/admin status - 查看狀態\n/admin users - 查看用戶列表\n/admin stats - 查看統計數據"
            })
            return
        
        command = parts[1].lower()
        
        if command == 'status':
            # 顯示管理員狀態
            admin_info = get_user_admin_permissions(sender_id)
            if admin_info:
                status_text = f"""🔑 管理員狀態
✅ 管理員權限: {admin_info.get('is_admin', False)}
✅ 測試模式: {admin_info.get('test_mode', False)}
✅ 可訪問等級: {admin_info.get('admin_levels', [])}
✅ 權限配置: {admin_info.get('admin_permissions', {})}"""
                send_message(sender_id, {"text": status_text})
            else:
                send_message(sender_id, {"text": "❌ 無法獲取管理員狀態"})
                
        elif command == 'users':
            # 顯示用戶列表
            students_data = get_real_students_data()
            if students_data:
                user_list = "👥 用戶列表:\n"
                for i, student in enumerate(students_data[:10], 1):
                    user_list += f"{i}. {student['name']} (等級{student['level']}, {student['score']}分)\n"
                send_message(sender_id, {"text": user_list})
            else:
                send_message(sender_id, {"text": "❌ 無法獲取用戶列表"})
                
        elif command == 'stats':
            # 顯示統計數據
            students_data = get_real_students_data()
            if students_data:
                total_users = len(students_data)
                total_score = sum(student['score'] for student in students_data)
                avg_score = total_score / total_users if total_users > 0 else 0
                
                stats_text = f"""📊 統計數據
👥 總用戶數: {total_users}
🏆 總分數: {total_score}
📈 平均分數: {avg_score:.1f}
🥇 最高分: {max(student['score'] for student in students_data) if students_data else 0}"""
                send_message(sender_id, {"text": stats_text})
            else:
                send_message(sender_id, {"text": "❌ 無法獲取統計數據"})
        else:
            send_message(sender_id, {"text": "❌ 未知的管理員命令"})
            
    except Exception as e:
        logger.error(f"❌ 處理管理員命令失敗: {e}")
        send_message(sender_id, {"text": "❌ 管理員命令處理失敗"})

def handle_test_command(sender_id, message_text):
    """處理測試命令"""
    try:
        # 解析測試命令
        parts = message_text.split()
        if len(parts) < 2:
            send_message(sender_id, {
                "text": "測試命令格式：\n/test level <等級> - 測試指定等級\n/test all - 測試所有等級"
            })
            return
        
        command = parts[1].lower()
        
        if command == 'level' and len(parts) >= 3:
            # 測試指定等級
            try:
                level = int(parts[2])
                if check_admin_access(sender_id, level):
                    send_message(sender_id, {
                        "text": f"✅ 您有權限訪問等級 {level} 的測試模式"
                    })
                else:
                    send_message(sender_id, {
                        "text": f"❌ 您沒有權限訪問等級 {level}"
                    })
            except ValueError:
                send_message(sender_id, {"text": "❌ 等級必須是數字"})
                
        elif command == 'all':
            # 測試所有等級
            admin_info = get_user_admin_permissions(sender_id)
            if admin_info and admin_info.get('can_access_all_levels', False):
                send_message(sender_id, {
                    "text": "✅ 您有權限訪問所有等級的測試模式"
                })
            else:
                send_message(sender_id, {
                    "text": "❌ 您沒有權限訪問所有等級"
                })
        else:
            send_message(sender_id, {"text": "❌ 未知的測試命令"})
            
    except Exception as e:
        logger.error(f"❌ 處理測試命令失敗: {e}")
        send_message(sender_id, {"text": "❌ 測試命令處理失敗"})

def handle_level_command(sender_id, message_text):
    """處理等級命令"""
    try:
        # 解析等級命令
        parts = message_text.split()
        if len(parts) < 2:
            send_message(sender_id, {
                "text": "等級命令格式：\n/level set <等級> - 設置等級\n/level check - 檢查當前等級"
            })
            return
        
        command = parts[1].lower()
        
        if command == 'set' and len(parts) >= 3:
            # 設置等級
            try:
                new_level = int(parts[2])
                if check_admin_access(sender_id, new_level):
                    if update_user_level(sender_id, new_level):
                        send_message(sender_id, {
                            "text": f"✅ 成功設置您的等級為 {new_level}"
                        })
                    else:
                        send_message(sender_id, {
                            "text": "❌ 設置等級失敗"
                        })
                else:
                    send_message(sender_id, {
                        "text": f"❌ 您沒有權限設置等級 {new_level}"
                    })
            except ValueError:
                send_message(sender_id, {"text": "❌ 等級必須是數字"})
                
        elif command == 'check':
            # 檢查當前等級
            stats = get_user_stats(sender_id)
            if stats:
                current_level = stats.get('level', 1)
                send_message(sender_id, {
                    "text": f"📊 您當前的等級是 {current_level}"
                })
            else:
                send_message(sender_id, {"text": "❌ 無法獲取您的等級信息"})
        else:
            send_message(sender_id, {"text": "❌ 未知的等級命令"})
            
    except Exception as e:
        logger.error(f"❌ 處理等級命令失敗: {e}")
        send_message(sender_id, {"text": "❌ 等級命令處理失敗"})

def handle_regular_message(sender_id, message_text):
    """處理普通用戶訊息"""
    try:
        # 直接處理普通用戶的問答邏輯
        # 注意：這裡不需要再次檢查管理員權限，因為在 handle_text_message 中已經檢查過了
        handle_normal_quiz(sender_id, message_text)
        
    except Exception as e:
        logger.error(f"❌ 處理普通訊息失敗: {e}")
        send_message(sender_id, {"text": "抱歉，處理您的訊息時發生錯誤，請稍後再試。"})

def handle_admin_quiz(sender_id, message_text):
    """處理管理員用戶的問答邏輯"""
    try:
        # 管理員可以訪問所有等級的題目
        if message_text.lower() in ['開始', 'start', '開始答題', '開始挑戰']:
            send_admin_quiz_question(sender_id)
        elif message_text.lower() in ['幫助', 'help', '指令', '命令']:
            send_admin_help_message(sender_id)
        elif message_text.lower() in ['排行榜', 'leaderboard', '排名', '排行']:
            # 發送排行榜 Flex Message
            logger.info(f"📊 管理員用戶 {sender_id} 請求查看排行榜")
            send_leaderboard_message(sender_id)
        else:
            # 檢查是否為答案選項
            if message_text.strip() in ['1', '2', '3', '4', 'A', 'B', 'C', 'D']:
                handle_admin_answer(sender_id, message_text)
            else:
                send_message(sender_id, {
                    "text": f"🔑 管理員模式已啟用！\n\n您可以使用以下指令：\n• 輸入「開始」開始答題\n• 輸入「排行榜」查看排名\n• 輸入「幫助」查看所有指令\n• 輸入「/admin status」查看管理員狀態\n• 輸入「/test level <等級>」測試特定等級\n\n您有權限訪問所有等級的題目！"
                })
        
    except Exception as e:
        logger.error(f"❌ 處理管理員問答失敗: {e}")
        send_message(sender_id, {"text": "❌ 處理問答時發生錯誤，請稍後再試。"})

def handle_normal_quiz(sender_id, message_text):
    """處理普通用戶的問答邏輯"""
    try:
        # 獲取用戶當前等級
        user_stats = get_user_stats(sender_id)
        current_level = user_stats.get('level', 1) if user_stats else 1
        
        if message_text.lower() in ['開始', 'start', '開始答題', '開始挑戰']:
            send_normal_quiz_question(sender_id, current_level)
        elif message_text.lower() in ['幫助', 'help', '指令', '命令']:
            send_normal_help_message(sender_id, current_level)
        elif message_text.lower() in ['排行榜', 'leaderboard', '排名', '排行']:
            # 發送排行榜 Flex Message
            logger.info(f"📊 普通用戶 {sender_id} 請求查看排行榜")
            send_leaderboard_message(sender_id)
        else:
            # 檢查是否為答案選項
            if message_text.strip() in ['1', '2', '3', '4', 'A', 'B', 'C', 'D']:
                handle_normal_answer(sender_id, message_text, current_level)
            else:
                send_message(sender_id, {
                    "text": f"您好！我收到了您的訊息：{message_text}\n\n這是一個解剖學問答機器人，請輸入「開始」開始學習！\n\n您當前等級：{current_level}\n\n💡 您也可以輸入「排行榜」查看排名！"
                })
        
    except Exception as e:
        logger.error(f"❌ 處理普通問答失敗: {e}")
        send_message(sender_id, {"text": "抱歉，處理您的訊息時發生錯誤，請稍後再試。"})

def send_admin_quiz_question(sender_id):
    """發送管理員問答題目（所有等級）"""
    try:
        import random
        
        # 管理員可以訪問所有等級的題目
        all_questions = get_all_questions()
        
        if not all_questions:
            send_message(sender_id, {"text": "❌ 目前沒有可用的題目，請稍後再試。"})
            return
        
        # 隨機選擇一道題目
        question = random.choice(all_questions)
        
        # 儲存當前題目到會話中
        session_data = {
            'current_question': question,
            'question_type': 'admin',
            'timestamp': datetime.datetime.now().isoformat()
        }
        set_user_session(sender_id, session_data)
        
        # 發送題目
        question_text = f"""🔑 管理員模式 - 隨機題目

📚 題目：{question['question']}
🎯 等級：{question['level']}
📖 類別：{question['category']}

選項：
1️⃣ {question['options'][0]}
2️⃣ {question['options'][1]}
3️⃣ {question['options'][2]}
4️⃣ {question['options'][3]}

請輸入答案編號 (1-4) 或字母 (A-D)"""
        
        send_message(sender_id, {"text": question_text})
        
    except Exception as e:
        logger.error(f"❌ 發送管理員題目失敗: {e}")
        send_message(sender_id, {"text": "❌ 發送題目時發生錯誤，請稍後再試。"})

def send_normal_quiz_question(sender_id, level):
    """發送普通用戶問答題目（當前等級）"""
    try:
        # 獲取指定等級的題目
        level_questions = get_questions_by_level(level)
        
        if not level_questions:
            send_message(sender_id, {"text": f"❌ 等級 {level} 目前沒有可用的題目，請稍後再試。"})
            return
        
        import random
        question = random.choice(level_questions)
        
        # 儲存當前題目到會話中
        session_data = {
            'current_question': question,
            'question_type': 'normal',
            'level': level,
            'timestamp': datetime.datetime.now().isoformat()
        }
        set_user_session(sender_id, session_data)
        
        # 發送題目
        question_text = f"""📚 等級 {level} 題目

題目：{question['question']}
類別：{question['category']}

選項：
1️⃣ {question['options'][0]}
2️⃣ {question['options'][1]}
3️⃣ {question['options'][2]}
4️⃣ {question['options'][3]}

請輸入答案編號 (1-4) 或字母 (A-D)"""
        
        send_message(sender_id, {"text": question_text})
        
    except Exception as e:
        logger.error(f"❌ 發送普通題目失敗: {e}")
        send_message(sender_id, {"text": "❌ 發送題目時發生錯誤，請稍後再試。"})

def get_all_questions():
    """從 Supabase 獲取所有等級的真實題目"""
    try:
        if supabase is None:
            logger.error("❌ Supabase 未連接，無法獲取題目")
            return []
        
        logger.info("📚 正在從 Supabase 獲取真實題目數據...")
        
        # 從 anatomy_questions_v2 表格獲取所有題目
        response = supabase.table('anatomy_questions_v2').select('*').execute()
        
        if not response.data:
            logger.warning("⚠️ 沒有找到任何題目數據")
            return []
        
        # 轉換數據格式以符合現有系統
        questions = []
        for item in response.data:
            question = {
                "id": item.get('id'),
                "question": item.get('question'),
                "options": [
                    item.get('option_1', ''),
                    item.get('option_2', ''),
                    item.get('option_3', ''),
                    item.get('option_4', '')
                ],
                "correct_answer": (item.get('correct_option', 1) - 1) if item.get('correct_option') else 0,  # 轉換為 0-based 索引
                "level": item.get('level', 1),
                "category": "解剖學",  # 統一類別
                "explanation": item.get('explanation', ''),
                "image_url": item.get('image_url', ''),
                "qimage_url": item.get('qimage_url', '')
            }
            questions.append(question)
        
        logger.info(f"✅ 成功獲取 {len(questions)} 道真實題目")
        return questions
        
    except Exception as e:
        logger.error(f"❌ 從 Supabase 獲取題目失敗: {e}")
        return []

def get_questions_by_level(level):
    """獲取指定等級的題目"""
    all_questions = get_all_questions()
    return [q for q in all_questions if q['level'] == level]

def send_admin_help_message(sender_id):
    """發送管理員幫助訊息"""
    help_text = """🔑 管理員指令幫助

📚 問答指令：
• 開始 / start - 開始隨機答題（所有等級）
• 幫助 / help - 顯示此幫助訊息

🔧 管理員指令：
• /admin status - 查看管理員狀態
• /admin users - 查看用戶列表
• /admin stats - 查看統計數據
• /test level <等級> - 測試特定等級權限
• /test all - 測試所有等級權限
• /level set <等級> - 設置用戶等級
• /level check - 檢查當前等級

🎯 特殊功能：
• 您有權限訪問所有等級的題目
• 可以測試任何等級的內容
• 可以查看系統統計數據

開始答題吧！"""
    
    send_message(sender_id, {"text": help_text})

def send_normal_help_message(sender_id, level):
    """發送普通用戶幫助訊息"""
    help_text = f"""📚 問答指令幫助

🎯 當前等級：{level}

📚 問答指令：
• 開始 / start - 開始答題（等級 {level}）
• 幫助 / help - 顯示此幫助訊息

💡 提示：
• 輸入答案時可以使用數字 (1-4) 或字母 (A-D)
• 答對題目可以獲得積分
• 累積足夠積分可以升級到下一等級

開始學習吧！"""
    
    send_message(sender_id, {"text": help_text})

# 會話管理 - 儲存用戶當前題目狀態
user_sessions = {}

def get_user_session(user_id):
    """獲取用戶會話狀態"""
    return user_sessions.get(user_id, {})

def set_user_session(user_id, session_data):
    """設置用戶會話狀態"""
    user_sessions[user_id] = session_data

def clear_user_session(user_id):
    """清除用戶會話狀態"""
    if user_id in user_sessions:
        del user_sessions[user_id]

def handle_admin_answer(sender_id, answer):
    """處理管理員答案 - 完整版本"""
    try:
        # 獲取用戶當前會話
        session = get_user_session(sender_id)
        current_question = session.get('current_question')
        
        if not current_question:
            send_message(sender_id, {
                "text": "❌ 沒有找到當前題目，請輸入「開始」重新開始答題。"
            })
            return
        
        # 轉換答案格式 (A-D 轉為 1-4)
        answer_mapping = {'A': '1', 'B': '2', 'C': '3', 'D': '4'}
        normalized_answer = answer_mapping.get(answer, answer)
        
        # 檢查答案是否正確
        correct_answer_index = current_question.get('correct_answer', 0)
        correct_answer = str(correct_answer_index + 1)  # 轉為 1-based
        is_correct = normalized_answer == correct_answer
        
        # 發送解說訊息（包含圖片）
        send_explanation_with_image(sender_id, current_question, is_correct)
        
        # 更新用戶統計
        update_user_stats_after_answer(sender_id, is_correct)
        
        # 清除當前會話
        clear_user_session(sender_id)
        
    except Exception as e:
        logger.error(f"❌ 處理管理員答案失敗: {e}")
        send_message(sender_id, {"text": "❌ 處理答案時發生錯誤，請稍後再試。"})

def handle_normal_answer(sender_id, answer, level):
    """處理普通用戶答案 - 完整版本"""
    try:
        # 獲取用戶當前會話
        session = get_user_session(sender_id)
        current_question = session.get('current_question')
        
        if not current_question:
            send_message(sender_id, {
                "text": "❌ 沒有找到當前題目，請輸入「開始」重新開始答題。"
            })
            return
        
        # 轉換答案格式 (A-D 轉為 1-4)
        answer_mapping = {'A': '1', 'B': '2', 'C': '3', 'D': '4'}
        normalized_answer = answer_mapping.get(answer, answer)
        
        # 檢查答案是否正確
        correct_answer_index = current_question.get('correct_answer', 0)
        correct_answer = str(correct_answer_index + 1)  # 轉為 1-based
        is_correct = normalized_answer == correct_answer
        
        # 發送解說訊息（包含圖片）
        send_explanation_with_image(sender_id, current_question, is_correct)
        
        # 更新用戶統計
        update_user_stats_after_answer(sender_id, is_correct)
        
        # 檢查是否需要升級
        check_and_handle_level_up(sender_id, level, is_correct)
        
        # 清除當前會話
        clear_user_session(sender_id)
        
    except Exception as e:
        logger.error(f"❌ 處理普通答案失敗: {e}")
        send_message(sender_id, {"text": "❌ 處理答案時發生錯誤，請稍後再試。"})

def send_explanation_with_image(user_id, question_data, is_correct):
    """發送解說訊息（包含圖片）"""
    try:
        # 獲取解說文字
        explanation = question_data.get('explanation', '暫無詳細解說')
        
        # 獲取正確答案
        correct_answer_index = question_data.get('correct_answer', 0)
        correct_option = question_data.get('options', [''])[correct_answer_index]
        
        # 獲取解說圖片 URL
        explanation_image_url = get_explanation_image_url(question_data)
        
        # 發送結果訊息
        result_text = "✅ 答對了！" if is_correct else "❌ 答錯了！"
        explanation_text = f"""{result_text}

📚 正確答案：{correct_option}

💡 解說：
{explanation}

輸入「開始」繼續答題！"""
        
        # 先發送文字解說
        send_message(user_id, {"text": explanation_text})
        
        # 如果有解說圖片，嘗試發送圖片
        if explanation_image_url:
            try:
                image_message = {
                    "type": "image",
                    "originalContentUrl": explanation_image_url,
                    "previewImageUrl": explanation_image_url
                }
                send_message(user_id, image_message)
                logger.info(f"✅ 成功發送解說圖片給用戶 {user_id}")
            except Exception as e:
                logger.warning(f"⚠️ 發送解說圖片失敗: {e}")
                # 圖片發送失敗不影響整體流程
        
    except Exception as e:
        logger.error(f"❌ 發送解說訊息失敗: {e}")
        # 備用方案：只發送簡單文字
        fallback_text = "✅ 答對了！" if is_correct else "❌ 答錯了！"
        send_message(user_id, {"text": f"{fallback_text}\n\n輸入「開始」繼續答題！"})

def get_explanation_image_url(question_data):
    """獲取解說圖片 URL（包含錯誤處理）"""
    try:
        # 優先使用資料庫中的圖片 URL
        image_url = question_data.get('image_url', '')
        if image_url and image_url.strip():
            return image_url
        
        # 嘗試使用題目圖片 URL
        qimage_url = question_data.get('qimage_url', '')
        if qimage_url and qimage_url.strip():
            return qimage_url
        
        # 構建預設圖片路徑
        level = question_data.get('level', 1)
        question_id = question_data.get('id', 1)
        
        # 嘗試特定題目的解說圖片
        specific_url = f"https://ciqlfqfgzqqgdrogedxg.supabase.co/storage/v1/object/public/linebot/explanations/level_{level}_q{question_id}.png"
        
        # 檢查圖片是否存在
        try:
            import requests
            response = requests.head(specific_url, timeout=5)
            if response.status_code == 200:
                return specific_url
        except:
            pass
        
        # 使用預設解說圖片
        default_url = "https://ciqlfqfgzqqgdrogedxg.supabase.co/storage/v1/object/public/linebot/default_explanation.png"
        return default_url
        
    except Exception as e:
        logger.error(f"❌ 獲取解說圖片 URL 失敗: {e}")
        return None

def update_user_stats_after_answer(user_id, is_correct):
    """更新用戶統計資料"""
    try:
        if supabase is None:
            logger.warning("⚠️ Supabase 未連接，無法更新統計資料")
            return
        
        # 獲取當前統計資料
        current_stats = get_user_stats(user_id)
        
        if current_stats:
            # 更新現有統計
            new_correct = current_stats.get('correct', 0) + (1 if is_correct else 0)
            new_wrong = current_stats.get('wrong', 0) + (0 if is_correct else 1)
            
            update_data = {
                'user_id': user_id,
                'correct': new_correct,
                'wrong': new_wrong,
                'last_update': datetime.datetime.now().isoformat()
            }
        else:
            # 創建新統計資料
            update_data = {
                'user_id': user_id,
                'correct': 1 if is_correct else 0,
                'wrong': 0 if is_correct else 1,
                'level': 1,
                'last_update': datetime.datetime.now().isoformat()
            }
        
        # 更新資料庫
        result = supabase.table('user_stats').upsert(update_data).execute()
        
        if result.data:
            logger.info(f"✅ 成功更新用戶 {user_id} 統計資料")
        else:
            logger.warning(f"⚠️ 更新用戶 {user_id} 統計資料失敗")
            
    except Exception as e:
        logger.error(f"❌ 更新用戶統計資料失敗: {e}")

def check_and_handle_level_up(user_id, current_level, is_correct):
    """檢查並處理等級提升"""
    try:
        if not is_correct:
            return  # 只有答對才可能升級
        
        # 獲取用戶統計資料
        stats = get_user_stats(user_id)
        if not stats:
            return
        
        correct_answers = stats.get('correct', 0)
        
        # 計算應該的等級（每10題正確答案升一級）
        expected_level = min(14, (correct_answers // 10) + 1)
        
        if expected_level > current_level:
            # 等級提升
            update_user_level(user_id, expected_level)
            send_level_up_celebration(user_id, current_level, expected_level)
            logger.info(f"🎉 用戶 {user_id} 從等級 {current_level} 提升到 {expected_level}")
            
    except Exception as e:
        logger.error(f"❌ 檢查等級提升失敗: {e}")

def handle_postback(sender_id, postback):
    """處理按鈕點擊"""
    payload = postback['payload']
    
    if payload == 'CONTINUE_CHALLENGE':
        # 處理繼續挑戰邏輯
        send_message(sender_id, {"text": "讓我們繼續挑戰下一題！"})
    
    elif payload == 'VIEW_LEADERBOARD':
        # 處理查看排行榜邏輯
        logger.info(f"📊 用戶 {sender_id} 請求查看排行榜")
        send_leaderboard_message(sender_id)
    
    elif payload == 'RESTART_CHALLENGE':
        # 處理重新挑戰邏輯
        logger.info(f"🔄 用戶 {sender_id} 請求重新挑戰")
        send_message(sender_id, {"text": "好的！讓我們重新開始挑戰，鞏固你的解剖學知識！"})

@app.route('/leaderboard')
def leaderboard():
    """排行榜頁面 - 顯示學生排名"""
    logger.info("🏆 正在獲取排行榜數據...")
    
    # 優先使用真實數據
    students_data = get_real_students_data()
    
    # 如果沒有真實數據，才使用模擬數據
    if not students_data:
        logger.warning("⚠️ 無法獲取真實數據，使用模擬數據")
        students_data = [
            {"user_id": "user_008", "name": "吳建國", "level": 8, "score": 2100, "questions_answered": 150, "correct_answers": 135, "last_active": "2024-09-01 18:00"},
            {"user_id": "user_004", "name": "陳大強", "level": 7, "score": 1800, "questions_answered": 120, "correct_answers": 105, "last_active": "2024-09-01 17:15"},
            {"user_id": "user_006", "name": "黃志明", "level": 6, "score": 1450, "questions_answered": 89, "correct_answers": 76, "last_active": "2024-09-01 17:30"},
            {"user_id": "user_002", "name": "李小華", "level": 5, "score": 1200, "questions_answered": 78, "correct_answers": 65, "last_active": "2024-09-01 16:45"},
            {"user_id": "user_005", "name": "林小芳", "level": 4, "score": 920, "questions_answered": 56, "correct_answers": 48, "last_active": "2024-09-01 16:00"},
            {"user_id": "user_001", "name": "張小明", "level": 3, "score": 850, "questions_answered": 45, "correct_answers": 38, "last_active": "2024-09-01 15:30"},
            {"user_id": "user_003", "name": "王美美", "level": 2, "score": 450, "questions_answered": 23, "correct_answers": 18, "last_active": "2024-09-01 14:20"},
            {"user_id": "user_007", "name": "劉雅婷", "level": 1, "score": 200, "questions_answered": 12, "correct_answers": 8, "last_active": "2024-09-01 13:45"}
        ]
    
    logger.info(f"📊 排行榜數據準備完成，共 {len(students_data)} 條記錄")
    
    html_content = """
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>What's Up Anatomy X 每日咬一口解剖 - 排行榜</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #f5f5dc 0%, #d2b48c 100%);
                min-height: 100vh;
                color: #2c1810;
            }
            .container {
                max-width: 1000px;
                margin: 0 auto;
            }
            .header {
                text-align: center;
                margin-bottom: 30px;
                background: rgba(210, 180, 140, 0.9);
                border-radius: 20px;
                padding: 30px;
                box-shadow: 0 8px 32px rgba(44, 24, 16, 0.1);
                border: 2px solid #8b4513;
            }
            .logo-section {
                margin-bottom: 20px;
            }
            .logo {
                width: 80px;
                height: 80px;
                margin: 0 auto 15px;
                background: linear-gradient(45deg, #d2b48c, #8b4513);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 40px;
                color: #2c1810;
                border: 3px solid #8b4513;
                box-shadow: 0 4px 15px rgba(44, 24, 16, 0.3);
            }
            .header h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(44, 24, 16, 0.2);
                color: #2c1810;
                font-weight: bold;
            }
            .nav {
                display: flex;
                justify-content: center;
                gap: 20px;
                margin-bottom: 30px;
            }
            .nav a {
                background: rgba(139, 69, 19, 0.8);
                padding: 12px 24px;
                border-radius: 25px;
                text-decoration: none;
                color: #f5f5dc;
                transition: all 0.3s;
                border: 2px solid #8b4513;
                font-weight: bold;
            }
            .nav a:hover {
                background: rgba(139, 69, 19, 1);
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(44, 24, 16, 0.3);
            }
            .nav a.active {
                background: #d2b48c;
                color: #2c1810;
                border-color: #8b4513;
            }
            .leaderboard {
                background: rgba(245, 245, 220, 0.9);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 30px;
                margin-bottom: 30px;
                border: 2px solid #8b4513;
                box-shadow: 0 8px 32px rgba(44, 24, 16, 0.1);
            }
            .rank-item {
                display: flex;
                align-items: center;
                padding: 20px;
                margin: 10px 0;
                background: rgba(210, 180, 140, 0.3);
                border-radius: 15px;
                transition: all 0.3s;
                border: 1px solid #d2b48c;
            }
            .rank-item:hover {
                transform: translateX(10px);
                background: rgba(210, 180, 140, 0.5);
                box-shadow: 0 4px 15px rgba(44, 24, 16, 0.2);
            }
            .rank-number {
                font-size: 2em;
                font-weight: bold;
                width: 80px;
                text-align: center;
            }
            .rank-1 { color: #d4af37; }
            .rank-2 { color: #c0c0c0; }
            .rank-3 { color: #cd7f32; }
            .rank-other { color: #8b4513; }
            .student-info {
                flex: 1;
                margin-left: 20px;
            }
            .student-name {
                font-size: 1.3em;
                font-weight: bold;
                margin-bottom: 5px;
                color: #2c1810;
            }
            .student-details {
                display: flex;
                gap: 20px;
                font-size: 0.9em;
                opacity: 0.8;
                color: #8b4513;
            }
            .score-section {
                text-align: right;
                margin-left: 20px;
            }
            .score {
                font-size: 2em;
                font-weight: bold;
                color: #d4af37;
            }
            .level-badge {
                background: #8b4513;
                color: #f5f5dc;
                padding: 4px 12px;
                border-radius: 15px;
                font-size: 0.9em;
                font-weight: bold;
                display: inline-block;
                margin-top: 5px;
            }
            .accuracy {
                font-size: 0.9em;
                opacity: 0.8;
                margin-top: 5px;
                color: #8b4513;
            }
            .stats-summary {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            .stat-card {
                background: rgba(245, 245, 220, 0.9);
                backdrop-filter: blur(10px);
                border-radius: 15px;
                padding: 20px;
                text-align: center;
                border-left: 5px solid #8b4513;
                border: 2px solid #d2b48c;
                box-shadow: 0 4px 15px rgba(44, 24, 16, 0.1);
            }
            .stat-number {
                font-size: 2em;
                font-weight: bold;
                color: #d4af37;
                margin-bottom: 10px;
            }
            .stat-label {
                font-size: 1em;
                opacity: 0.9;
                color: #2c1810;
            }
            .score-explanation {
                background: rgba(245, 245, 220, 0.9);
                backdrop-filter: blur(10px);
                border-radius: 15px;
                padding: 25px;
                margin-bottom: 30px;
                border-left: 5px solid #d4af37;
                border: 2px solid #d2b48c;
                box-shadow: 0 4px 15px rgba(44, 24, 16, 0.1);
            }
            .score-explanation h3 {
                margin: 0 0 20px 0;
                color: #8b4513;
                font-size: 1.4em;
                text-align: center;
            }
            .explanation-content {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 15px;
            }
            .explanation-item {
                display: flex;
                align-items: center;
                padding: 12px 15px;
                background: rgba(210, 180, 140, 0.3);
                border-radius: 10px;
                transition: all 0.3s ease;
                border: 1px solid #d2b48c;
            }
            .explanation-item:hover {
                background: rgba(210, 180, 140, 0.5);
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(44, 24, 16, 0.2);
            }
            .explanation-icon {
                font-size: 1.5em;
                margin-right: 12px;
                min-width: 30px;
                text-align: center;
            }
            .explanation-text {
                font-size: 0.95em;
                line-height: 1.4;
                color: #2c1810;
            }
            .explanation-text strong {
                color: #8b4513;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo-section">
                    <div class="logo">💀📚</div>
                </div>
                <h1>🏆 What's Up Anatomy<br>X<br>解剖咬一口排行榜</h1>
                <p>每天累積一點點；解剖力提高一點點</p>
            </div>
            
            <div class="nav">
                <a href="/">🏠 首頁</a>
                <a href="/dashboard">📊 數據儀表板</a>
                <a href="/leaderboard" class="active">🏆 排行榜</a>
                <a href="/score_manager">🎯 積分管理</a>
                <a href="/webhook">🔗 Webhook</a>
            </div>
    """
    
    # 添加統計摘要
    if students_data:
        total_students = len(students_data)
        top_score = students_data[0]["score"] if students_data else 0
        avg_score = sum(s["score"] for s in students_data) / total_students if total_students > 0 else 0
        total_questions = sum(s["questions_answered"] for s in students_data)
        total_correct = sum(s["correct_answers"] for s in students_data)
        accuracy_rate = (total_correct / total_questions * 100) if total_questions > 0 else 0
        
        html_content += f"""
            <div class="stats-summary">
                <div class="stat-card">
                    <div class="stat-number">{total_students}</div>
                    <div class="stat-label">參與學生</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{top_score}</div>
                    <div class="stat-label">最高分數</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{avg_score:.0f}</div>
                    <div class="stat-label">平均分數</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{accuracy_rate:.1f}%</div>
                    <div class="stat-label">整體正確率</div>
                </div>
            </div>
            
            <div class="score-explanation">
                <h3>📊 分數計算方法</h3>
                <div class="explanation-content">
                    <div class="explanation-item">
                        <span class="explanation-icon">✅</span>
                        <span class="explanation-text"><strong>正確答案</strong>：每題 +10 分</span>
                    </div>
                    <div class="explanation-item">
                        <span class="explanation-icon">❌</span>
                        <span class="explanation-text"><strong>錯誤答案</strong>：0 分</span>
                    </div>
                    <div class="explanation-item">
                        <span class="explanation-icon">📈</span>
                        <span class="explanation-text"><strong>等級提升</strong>：每提升一級 +50 分獎勵</span>
                    </div>
                    <div class="explanation-item">
                        <span class="explanation-icon">🔥</span>
                        <span class="explanation-text"><strong>連續答對</strong>：連續答對 5 題 +20 分獎勵</span>
                    </div>
                    <div class="explanation-item">
                        <span class="explanation-icon">🎯</span>
                        <span class="explanation-text"><strong>總分公式</strong>：正確題數 × 10 + 等級獎勵 + 連續獎勵</span>
                    </div>
                </div>
            </div>
        """
    
    html_content += """
            <div class="leaderboard">
                <h2>🏅 分數排行榜</h2>
    """
    
    # 添加排行榜項目
    for i, student in enumerate(students_data, 1):
        rank_class = f"rank-{i}" if i <= 3 else "rank-other"
        accuracy = (student["correct_answers"] / student["questions_answered"] * 100) if student["questions_answered"] > 0 else 0
        
        html_content += f"""
                <div class="rank-item">
                    <div class="rank-number {rank_class}">{i}</div>
                    <div class="student-info">
                        <div class="student-name">{student["name"]}</div>
                        <div class="student-details">
                            <span>答題: {student["questions_answered"]} 題</span>
                            <span>正確: {student["correct_answers"]} 題</span>
                            <span>最後活躍: {student["last_active"]}</span>
                        </div>
                        <div class="level-badge">等級 {student["level"]}</div>
                        <div class="accuracy">正確率: {accuracy:.1f}%</div>
                    </div>
                    <div class="score-section">
                        <div class="score">{student["score"]}</div>
                        <div>分數</div>
                    </div>
                </div>
        """
    
    html_content += """
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_content

@app.route('/dashboard')
def dashboard():
    """後台管理儀表板 - 顯示學生數據和統計"""
    logger.info("📊 正在獲取儀表板數據...")
    
    # 優先使用真實數據
    students_data = get_real_students_data()
    
    # 如果沒有真實數據，才使用模擬數據
    if not students_data:
        logger.warning("⚠️ 無法獲取真實數據，使用模擬數據")
        students_data = [
            {"user_id": "user_008", "name": "吳建國", "level": 8, "score": 2100, "questions_answered": 150, "correct_answers": 135, "last_active": "2024-09-01 18:00"},
            {"user_id": "user_004", "name": "陳大強", "level": 7, "score": 1800, "questions_answered": 120, "correct_answers": 105, "last_active": "2024-09-01 17:15"},
            {"user_id": "user_006", "name": "黃志明", "level": 6, "score": 1450, "questions_answered": 89, "correct_answers": 76, "last_active": "2024-09-01 17:30"},
            {"user_id": "user_002", "name": "李小華", "level": 5, "score": 1200, "questions_answered": 78, "correct_answers": 65, "last_active": "2024-09-01 16:45"},
            {"user_id": "user_005", "name": "林小芳", "level": 4, "score": 920, "questions_answered": 56, "correct_answers": 48, "last_active": "2024-09-01 16:00"},
            {"user_id": "user_001", "name": "張小明", "level": 3, "score": 850, "questions_answered": 45, "correct_answers": 38, "last_active": "2024-09-01 15:30"},
            {"user_id": "user_003", "name": "王美美", "level": 2, "score": 450, "questions_answered": 23, "correct_answers": 18, "last_active": "2024-09-01 14:20"},
            {"user_id": "user_007", "name": "劉雅婷", "level": 1, "score": 200, "questions_answered": 12, "correct_answers": 8, "last_active": "2024-09-01 13:45"}
        ]
    
    logger.info(f"📊 儀表板數據準備完成，共 {len(students_data)} 條記錄")
    
    # 計算統計數據
    total_students = len(students_data)
    avg_level = sum(s["level"] for s in students_data) / total_students if total_students > 0 else 0
    avg_score = sum(s["score"] for s in students_data) / total_students if total_students > 0 else 0
    total_questions = sum(s["questions_answered"] for s in students_data)
    total_correct = sum(s["correct_answers"] for s in students_data)
    accuracy_rate = (total_correct / total_questions * 100) if total_questions > 0 else 0
    
    # 等級分布
    level_distribution = {}
    for student in students_data:
        level = student["level"]
        level_distribution[level] = level_distribution.get(level, 0) + 1
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>學生數據儀表板 - 解剖學測驗機器人</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: white;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
            }}
            .header {{
                text-align: center;
                margin-bottom: 30px;
            }}
            .header h1 {{
                font-size: 2.5em;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            }}
            .nav {{
                display: flex;
                justify-content: center;
                gap: 20px;
                margin-bottom: 30px;
            }}
            .nav a {{
                background: rgba(255, 255, 255, 0.2);
                padding: 10px 20px;
                border-radius: 25px;
                text-decoration: none;
                color: white;
                transition: all 0.3s;
            }}
            .nav a:hover {{
                background: rgba(255, 255, 255, 0.3);
                transform: translateY(-2px);
            }}
            .nav a.active {{
                background: #FFD700;
                color: #333;
            }}
            .stats-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }}
            .stat-card {{
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border-radius: 15px;
                padding: 20px;
                text-align: center;
                border-left: 5px solid #4CAF50;
            }}
            .stat-number {{
                font-size: 2.5em;
                font-weight: bold;
                color: #FFD700;
                margin-bottom: 10px;
            }}
            .stat-label {{
                font-size: 1.1em;
                opacity: 0.9;
            }}
            .level-distribution {{
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border-radius: 15px;
                padding: 20px;
                margin-bottom: 30px;
            }}
            .level-bars {{
                display: flex;
                align-items: end;
                gap: 10px;
                height: 200px;
                margin-top: 20px;
            }}
            .level-bar {{
                flex: 1;
                background: linear-gradient(to top, #4CAF50, #8BC34A);
                border-radius: 5px 5px 0 0;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: flex-end;
                padding-bottom: 10px;
                min-width: 40px;
            }}
            .level-label {{
                font-weight: bold;
                margin-bottom: 5px;
            }}
            .students-table {{
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border-radius: 15px;
                padding: 20px;
                overflow-x: auto;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
            }}
            th, td {{
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid rgba(255, 255, 255, 0.2);
            }}
            th {{
                background: rgba(255, 255, 255, 0.2);
                font-weight: bold;
            }}
            .level-badge {{
                background: #4CAF50;
                color: white;
                padding: 4px 8px;
                border-radius: 12px;
                font-size: 0.9em;
                font-weight: bold;
            }}
            .score-high {{
                color: #4CAF50;
                font-weight: bold;
            }}
            .score-medium {{
                color: #FF9800;
                font-weight: bold;
            }}
            .score-low {{
                color: #f44336;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📊 學生數據儀表板</h1>
                <p>解剖學測驗機器人後台管理系統</p>
            </div>
            
            <div class="nav">
                <a href="/">🏠 首頁</a>
                <a href="/dashboard" class="active">📊 數據儀表板</a>
                <a href="/leaderboard">🏆 排行榜</a>
                <a href="/score_manager">🎯 積分管理</a>
                <a href="/webhook">🔗 Webhook</a>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">{total_students}</div>
                    <div class="stat-label">總學生數</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{avg_level:.1f}</div>
                    <div class="stat-label">平均等級</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{avg_score:.0f}</div>
                    <div class="stat-label">平均分數</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{accuracy_rate:.1f}%</div>
                    <div class="stat-label">正確率</div>
                </div>
            </div>
            
            <div class="level-distribution">
                <h2>📈 等級分布</h2>
                <div class="level-bars">
    """
    
    # 添加等級分布圖表
    max_count = max(level_distribution.values()) if level_distribution else 1
    for level in range(1, 9):
        count = level_distribution.get(level, 0)
        height_percentage = (count / max_count * 100) if max_count > 0 else 0
        html_content += f"""
                    <div class="level-bar" style="height: {height_percentage}%">
                        <div class="level-label">{count}</div>
                        <div>等級 {level}</div>
                    </div>
        """
    
    html_content += """
                </div>
            </div>
            
            <div class="students-table">
                <h2>👥 學生詳細數據</h2>
                <table>
                    <thead>
                        <tr>
                            <th>學生ID</th>
                            <th>姓名</th>
                            <th>等級</th>
                            <th>分數</th>
                            <th>答題數</th>
                            <th>正確數</th>
                            <th>正確率</th>
                            <th>最後活躍</th>
                        </tr>
                    </thead>
                    <tbody>
    """
    
    # 添加學生數據表格
    for student in students_data:
        accuracy = (student["correct_answers"] / student["questions_answered"] * 100) if student["questions_answered"] > 0 else 0
        score_class = "score-high" if student["score"] >= 1000 else "score-medium" if student["score"] >= 500 else "score-low"
        
        html_content += f"""
                        <tr>
                            <td>{student["user_id"]}</td>
                            <td>{student["name"]}</td>
                            <td><span class="level-badge">等級 {student["level"]}</span></td>
                            <td class="{score_class}">{student["score"]}</td>
                            <td>{student["questions_answered"]}</td>
                            <td>{student["correct_answers"]}</td>
                            <td>{accuracy:.1f}%</td>
                            <td>{student["last_active"]}</td>
                        </tr>
        """
    
    html_content += """
                    </tbody>
                </table>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_content

@app.route('/api/update_score', methods=['POST'])
def update_score():
    """更新用戶積分的API端點"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        new_score = data.get('score')
        
        if not user_id or new_score is None:
            return jsonify({'error': '缺少必要參數: user_id 和 score'}), 400
        
        # 驗證分數為正整數
        try:
            new_score = int(new_score)
            if new_score < 0:
                return jsonify({'error': '分數不能為負數'}), 400
        except ValueError:
            return jsonify({'error': '分數必須為整數'}), 400
        
        # 更新用戶統計數據
        if supabase is None:
            return jsonify({'error': '數據庫連接失敗'}), 500
        
        # 獲取當前用戶數據
        current_stats = get_user_stats(user_id)
        if not current_stats:
            return jsonify({'error': '用戶不存在'}), 404
        
        # 計算新的正確答案數（基於分數）
        new_correct = new_score // 10  # 每題10分
        
        # 更新數據庫
        update_data = {
            'user_id': user_id,
            'correct': new_correct,
            'last_update': datetime.datetime.now().isoformat()
        }
        
        result = supabase.table('user_stats').update(update_data).eq('user_id', user_id).execute()
        
        if result.data:
            logger.info(f"✅ 成功更新用戶 {user_id} 的積分為 {new_score}")
            return jsonify({
                'success': True,
                'message': f'成功更新用戶積分為 {new_score}',
                'user_id': user_id,
                'new_score': new_score,
                'new_correct': new_correct
            })
        else:
            return jsonify({'error': '更新失敗'}), 500
            
    except Exception as e:
        logger.error(f"❌ 更新積分失敗: {e}")
        return jsonify({'error': f'更新失敗: {str(e)}'}), 500

@app.route('/api/get_user/<user_id>')
def get_user_info(user_id):
    """獲取用戶詳細信息的API端點"""
    try:
        if supabase is None:
            return jsonify({'error': '數據庫連接失敗'}), 500
        
        # 獲取用戶統計數據
        stats = get_user_stats(user_id)
        if not stats:
            return jsonify({'error': '用戶不存在'}), 404
        
        # 獲取用戶暱稱
        nickname = get_user_nickname(user_id)
        
        # 計算當前分數
        correct_answers = stats.get('correct', 0)
        current_score = correct_answers * 10
        
        return jsonify({
            'user_id': user_id,
            'name': nickname,
            'level': stats.get('level', 1),
            'score': current_score,
            'correct_answers': correct_answers,
            'wrong_answers': stats.get('wrong', 0),
            'last_update': stats.get('last_update', stats.get('last_updated', '未知'))
        })
        
    except Exception as e:
        logger.error(f"❌ 獲取用戶信息失敗: {e}")
        return jsonify({'error': f'獲取失敗: {str(e)}'}), 500

@app.route('/score_manager')
def score_manager():
    """積分管理頁面"""
    html_content = """
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>積分管理系統 - 解剖學測驗機器人</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: white;
            }
            .container {
                max-width: 1000px;
                margin: 0 auto;
            }
            .header {
                text-align: center;
                margin-bottom: 30px;
            }
            .header h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            }
            .nav {
                display: flex;
                justify-content: center;
                gap: 20px;
                margin-bottom: 30px;
            }
            .nav a {
                background: rgba(255, 255, 255, 0.2);
                padding: 10px 20px;
                border-radius: 25px;
                text-decoration: none;
                color: white;
                transition: all 0.3s;
            }
            .nav a:hover {
                background: rgba(255, 255, 255, 0.3);
                transform: translateY(-2px);
            }
            .nav a.active {
                background: #FFD700;
                color: #333;
            }
            .score-manager {
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border-radius: 15px;
                padding: 30px;
                margin-bottom: 30px;
            }
            .form-group {
                margin-bottom: 20px;
            }
            .form-group label {
                display: block;
                margin-bottom: 8px;
                font-weight: bold;
                font-size: 1.1em;
            }
            .form-group input {
                width: 100%;
                padding: 12px;
                border: none;
                border-radius: 8px;
                font-size: 1em;
                background: rgba(255, 255, 255, 0.9);
                color: #333;
            }
            .form-group input:focus {
                outline: none;
                background: white;
                box-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
            }
            .btn {
                background: #4CAF50;
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 8px;
                font-size: 1em;
                cursor: pointer;
                transition: all 0.3s;
                margin-right: 10px;
            }
            .btn:hover {
                background: #45a049;
                transform: translateY(-2px);
            }
            .btn-secondary {
                background: #2196F3;
            }
            .btn-secondary:hover {
                background: #1976D2;
            }
            .user-info {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 20px;
                margin-top: 20px;
                display: none;
            }
            .user-info.show {
                display: block;
            }
            .info-item {
                display: flex;
                justify-content: space-between;
                margin-bottom: 10px;
                padding: 8px 0;
                border-bottom: 1px solid rgba(255, 255, 255, 0.2);
            }
            .info-item:last-child {
                border-bottom: none;
            }
            .info-label {
                font-weight: bold;
            }
            .info-value {
                color: #FFD700;
            }
            .message {
                padding: 15px;
                border-radius: 8px;
                margin: 20px 0;
                display: none;
            }
            .message.success {
                background: rgba(76, 175, 80, 0.3);
                border: 1px solid #4CAF50;
                color: #4CAF50;
            }
            .message.error {
                background: rgba(244, 67, 54, 0.3);
                border: 1px solid #f44336;
                color: #f44336;
            }
            .message.show {
                display: block;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎯 積分管理系統</h1>
                <p>手動調整學生積分</p>
            </div>
            
            <div class="nav">
                <a href="/">🏠 首頁</a>
                <a href="/dashboard">📊 數據儀表板</a>
                <a href="/leaderboard">🏆 排行榜</a>
                <a href="/score_manager" class="active">🎯 積分管理</a>
            </div>
            
            <div class="score-manager">
                <h2>📝 更新學生積分</h2>
                
                <div class="message" id="message"></div>
                
                <div class="form-group">
                    <label for="user_id">用戶ID:</label>
                    <input type="text" id="user_id" placeholder="請輸入用戶ID (例如: user_001)">
                </div>
                
                <div class="form-group">
                    <label for="new_score">新積分:</label>
                    <input type="number" id="new_score" placeholder="請輸入新的積分" min="0">
                </div>
                
                <button class="btn" onclick="getUserInfo()">🔍 查詢用戶</button>
                <button class="btn btn-secondary" onclick="updateScore()">💾 更新積分</button>
                
                <div class="user-info" id="user_info">
                    <h3>👤 用戶信息</h3>
                    <div class="info-item">
                        <span class="info-label">用戶ID:</span>
                        <span class="info-value" id="info_user_id">-</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">姓名:</span>
                        <span class="info-value" id="info_name">-</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">當前積分:</span>
                        <span class="info-value" id="info_score">-</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">正確答案數:</span>
                        <span class="info-value" id="info_correct">-</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">錯誤答案數:</span>
                        <span class="info-value" id="info_wrong">-</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">等級:</span>
                        <span class="info-value" id="info_level">-</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">最後更新:</span>
                        <span class="info-value" id="info_last_update">-</span>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            function showMessage(text, type) {
                const messageEl = document.getElementById('message');
                messageEl.textContent = text;
                messageEl.className = 'message ' + type + ' show';
                setTimeout(() => {
                    messageEl.className = 'message';
                }, 5000);
            }
            
            async function getUserInfo() {
                const userId = document.getElementById('user_id').value.trim();
                if (!userId) {
                    showMessage('請輸入用戶ID', 'error');
                    return;
                }
                
                try {
                    const response = await fetch(`/api/get_user/${userId}`);
                    const data = await response.json();
                    
                    if (response.ok) {
                        document.getElementById('info_user_id').textContent = data.user_id;
                        document.getElementById('info_name').textContent = data.name;
                        document.getElementById('info_score').textContent = data.score;
                        document.getElementById('info_correct').textContent = data.correct_answers;
                        document.getElementById('info_wrong').textContent = data.wrong_answers;
                        document.getElementById('info_level').textContent = data.level;
                        document.getElementById('info_last_update').textContent = data.last_update;
                        
                        document.getElementById('user_info').classList.add('show');
                        showMessage('用戶信息查詢成功', 'success');
                    } else {
                        showMessage(data.error || '查詢失敗', 'error');
                    }
                } catch (error) {
                    showMessage('網絡錯誤: ' + error.message, 'error');
                }
            }
            
            async function updateScore() {
                const userId = document.getElementById('user_id').value.trim();
                const newScore = document.getElementById('new_score').value;
                
                if (!userId) {
                    showMessage('請輸入用戶ID', 'error');
                    return;
                }
                
                if (!newScore || newScore < 0) {
                    showMessage('請輸入有效的積分', 'error');
                    return;
                }
                
                try {
                    const response = await fetch('/api/update_score', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            user_id: userId,
                            score: parseInt(newScore)
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        showMessage(data.message, 'success');
                        // 重新查詢用戶信息
                        setTimeout(getUserInfo, 1000);
                    } else {
                        showMessage(data.error || '更新失敗', 'error');
                    }
                } catch (error) {
                    showMessage('網絡錯誤: ' + error.message, 'error');
                }
            }
        </script>
    </body>
    </html>
    """
    return html_content

@app.route('/')
def home():
    """首頁 - 顯示友好的HTML界面"""
    html_content = """
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>解剖學測驗機器人後台系統</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: white;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            }
            h1 {
                text-align: center;
                margin-bottom: 30px;
                font-size: 2.5em;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            }
            .nav {
                display: flex;
                justify-content: center;
                gap: 20px;
                margin-bottom: 30px;
            }
            .nav a {
                background: rgba(255, 255, 255, 0.2);
                padding: 10px 20px;
                border-radius: 25px;
                text-decoration: none;
                color: white;
                transition: all 0.3s;
            }
            .nav a:hover {
                background: rgba(255, 255, 255, 0.3);
                transform: translateY(-2px);
            }
            .status-card {
                background: rgba(255, 255, 255, 0.2);
                border-radius: 15px;
                padding: 20px;
                margin: 20px 0;
                border-left: 5px solid #4CAF50;
            }
            .status-item {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 10px 0;
                border-bottom: 1px solid rgba(255, 255, 255, 0.2);
            }
            .status-item:last-child {
                border-bottom: none;
            }
            .status-label {
                font-weight: bold;
            }
            .status-value {
                padding: 5px 15px;
                border-radius: 20px;
                font-weight: bold;
            }
            .status-running {
                background: #4CAF50;
                color: white;
            }
            .status-offline {
                background: #f44336;
                color: white;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧠 解剖學測驗機器人後台系統</h1>
            
            <div class="nav">
                <a href="/">🏠 首頁</a>
                <a href="/dashboard">📊 數據儀表板</a>
                <a href="/leaderboard">🏆 排行榜</a>
                <a href="/score_manager">🎯 積分管理</a>
                <a href="/webhook">🔗 Webhook</a>
            </div>
            
            <div class="status-card">
                <h2>📊 系統狀態</h2>
                <div class="status-item">
                    <span class="status-label">運行狀態:</span>
                    <span class="status-value status-running">運行中</span>
                </div>
                <div class="status-item">
                    <span class="status-label">版本:</span>
                    <span class="status-value">v1.0</span>
                </div>
                <div class="status-item">
                    <span class="status-label">數據庫連接:</span>
                    <span class="status-value status-offline">離線模式</span>
                </div>
                <div class="status-item">
                    <span class="status-label">端口:</span>
                    <span class="status-value">5002</span>
                </div>
            </div>
            
            <div style="text-align: center; margin-top: 30px;">
                <p>💡 點擊上方導航欄查看詳細的學生數據和排行榜</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

# API 端點
@app.route('/api/leaderboard')
def api_leaderboard():
    """API: 獲取排行榜數據"""
    period = request.args.get('period', 'week')
    logger.info(f"📊 API: 正在獲取排行榜數據 (period: {period})")
    
    try:
        # 獲取真實數據
        students_data = get_real_students_data()
        
        # 如果沒有真實數據，返回空數組
        if not students_data:
            logger.warning("⚠️ 無法獲取真實數據，返回空排行榜")
            return jsonify([])
        
        # 根據期間過濾數據（這裡簡化處理，實際可以根據時間範圍過濾）
        if period == 'week':
            # 返回前20名
            filtered_data = students_data[:20]
        elif period == 'month':
            # 返回前50名
            filtered_data = students_data[:50]
        else:  # all
            # 返回所有數據
            filtered_data = students_data
        
        # 轉換為 API 格式
        leaderboard_data = []
        for i, student in enumerate(filtered_data):
            leaderboard_data.append({
                "name": student['name'],
                "answers": student['questions_answered'],
                "streak": student.get('streak', 0),  # 如果沒有連勝數據，設為0
                "score": student['score'],
                "level": student['level']
            })
        
        logger.info(f"✅ API: 成功返回 {len(leaderboard_data)} 條排行榜數據")
        return jsonify(leaderboard_data)
        
    except Exception as e:
        logger.error(f"❌ API: 獲取排行榜數據失敗: {e}")
        return jsonify({"error": "獲取排行榜數據失敗"}), 500

@app.route('/api/dashboard')
def api_dashboard():
    """API: 獲取儀表板數據"""
    logger.info("📊 API: 正在獲取儀表板數據")
    
    try:
        # 獲取真實數據
        students_data = get_real_students_data()
        
        if not students_data:
            # 返回默認數據
            return jsonify({
                "activeStudents": 0,
                "activeStudentsWoW": 0,
                "answersToday": 0,
                "answersDoD": 0,
                "accuracy": 0,
                "maxStreak": 0
            })
        
        # 計算統計數據
        total_students = len(students_data)
        total_answers = sum(student['questions_answered'] for student in students_data)
        total_correct = sum(student['correct_answers'] for student in students_data)
        accuracy = total_correct / total_answers if total_answers > 0 else 0
        max_streak = max((student.get('streak', 0) for student in students_data), default=0)
        
        # 模擬今日數據（實際應該從數據庫查詢）
        answers_today = max(1, total_answers // 30)  # 假設平均每天答題數
        answers_yesterday = max(1, answers_today - 5)  # 模擬昨日數據
        
        dashboard_data = {
            "activeStudents": total_students,
            "activeStudentsWoW": max(0, total_students - 2),  # 模擬週增長
            "answersToday": answers_today,
            "answersDoD": answers_today - answers_yesterday,
            "accuracy": accuracy,
            "maxStreak": max_streak
        }
        
        logger.info(f"✅ API: 成功返回儀表板數據 - 活躍學生: {total_students}, 正確率: {accuracy:.2%}")
        return jsonify(dashboard_data)
        
    except Exception as e:
        logger.error(f"❌ API: 獲取儀表板數據失敗: {e}")
        return jsonify({"error": "獲取儀表板數據失敗"}), 500

@app.route('/api/students')
def api_students():
    """API: 獲取學生列表"""
    logger.info("📊 API: 正在獲取學生列表")
    
    try:
        # 獲取真實數據
        students_data = get_real_students_data()
        
        if not students_data:
            return jsonify([])
        
        # 轉換為 API 格式
        students_list = []
        for student in students_data:
            students_list.append({
                "name": student['name'],
                "email": f"{student['user_id']}@example.com",  # 模擬 email
                "level": student['level'],
                "status": "活躍" if student['questions_answered'] > 0 else "未開始"
            })
        
        logger.info(f"✅ API: 成功返回 {len(students_list)} 個學生數據")
        return jsonify(students_list)
        
    except Exception as e:
        logger.error(f"❌ API: 獲取學生列表失敗: {e}")
        return jsonify({"error": "獲取學生列表失敗"}), 500

@app.route('/api/questions')
def api_questions():
    """API: 獲取題目列表"""
    logger.info("📊 API: 正在獲取題目列表")
    
    try:
        # 這裡應該從數據庫獲取題目數據
        # 暫時返回模擬數據
        questions_data = [
            {"id": 1, "title": "心臟解剖", "level": "初級", "tags": ["循環系統", "心臟"], "enabled": True},
            {"id": 2, "title": "骨骼系統", "level": "中級", "tags": ["骨骼", "運動系統"], "enabled": True},
            {"id": 3, "title": "神經系統", "level": "高級", "tags": ["神經", "腦部"], "enabled": True},
            {"id": 4, "title": "消化系統", "level": "初級", "tags": ["消化", "內臟"], "enabled": False},
        ]
        
        logger.info(f"✅ API: 成功返回 {len(questions_data)} 個題目數據")
        return jsonify(questions_data)
        
    except Exception as e:
        logger.error(f"❌ API: 獲取題目列表失敗: {e}")
        return jsonify({"error": "獲取題目列表失敗"}), 500

# --- ASGI 兼容：把 Flask(WGSI) 包成 ASGI，給 Render 目前的 `uvicorn app_supabase:app` 使用 ---
try:
    from uvicorn.middleware.wsgi import WSGIMiddleware
    _flask_app = app            # 先保留原本的 Flask app（路由都掛在這上面）
    app = WSGIMiddleware(_flask_app)  # 將 `app` 變數改指向 ASGI wrapper（給 uvicorn 匯入）
    flask_app = _flask_app      # 仍保留 flask_app 供本地開發啟動
except Exception:
    # 若未裝 uvicorn 或其他例外，至少不要壞掉本地啟動
    flask_app = app

if __name__ == "__main__":
    # 本地開發時仍用 Flask 內建伺服器（不要用 uvicorn）
    port = int(os.environ.get("PORT", 5001))
    flask_app.run(host="0.0.0.0", port=port, debug=True)

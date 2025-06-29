import schedule
import time
from datetime import datetime, date
from linebot import LineBotApi, WebhookHandler
from linebot.models import (
    TextSendMessage, TextMessage,
    FlexSendMessage
)
from linebot.exceptions import LineBotApiError
from config import LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET, USER_ID, QUESTION_TIME
from sheets_handler import get_questions
from user_stats_handler import get_user_stats, update_user_stats
from flask import current_app as app

# 初始化 LINE Bot
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 用戶每日狀態（只記錄 today_count, today_answered，跨天可重置）
user_daily_state = {}  # user_id: {"date": "2024-06-09", "today_count": int, "today_answered": [qid, ...]}
# 用戶當前題目狀態
user_states = {}  # user_id: {"current_question": {...}, "answered": bool}

def get_today():
    return date.today().isoformat()

def get_user_daily(user_id):
    today = get_today()
    daily = user_daily_state.get(user_id)
    if not daily or daily["date"] != today:
        user_daily_state[user_id] = {"date": today, "today_count": 0, "today_answered": []}
    return user_daily_state[user_id]

def get_user_question_count(user_id):
    daily = get_user_daily(user_id)
    return daily["today_count"]

def get_user_correct_wrong(user_id):
    stats = get_user_stats(user_id)
    return stats["correct"], stats["wrong"]

def create_question_message(question):
    """創建問題訊息"""
    # 創建選項按鈕
    option_buttons = []
    for i, option in enumerate(question['options'], 1):
        option_buttons.append({
            "type": "button",
            "action": {
                "type": "postback",
                "label": f"{i}. {option}",
                "data": f"answer_{i}"
            },
            "style": "primary",
            "color": "#1DB446",
            "margin": "sm"
        })
    
    flex_contents = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "今日解剖學問題",
                    "weight": "bold",
                    "size": "lg",
                    "align": "center",
                    "color": "#1DB446",
                    "margin": "md"
                },
                {
                    "type": "text",
                    "text": "點選下方選項作答",
                    "size": "sm",
                    "align": "center",
                    "color": "#666666",
                    "margin": "sm"
                },
                {
                    "type": "separator",
                    "margin": "md"
                },
                {
                    "type": "text",
                    "text": question['question'],
                    "wrap": True,
                    "size": "md",
                    "margin": "lg",
                    "color": "#333333"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": option_buttons
                }
            ]
        }
    }
    
    return FlexSendMessage(alt_text="今日解剖學問題", contents=flex_contents)

def send_question(user_id):
    print(f"[DEBUG] send_question 開始，user_id={user_id}", flush=True)
    daily = get_user_daily(user_id)
    stats = get_user_stats(user_id)
    print(f"[DEBUG] daily={daily}, stats={stats}", flush=True)
    
    if daily["today_count"] >= 5:
        print(f"[DEBUG] 今日已達上限: {daily['today_count']}", flush=True)
        line_bot_api.push_message(
            user_id,
            TextSendMessage(text="今天已經完成五題，明天再來挑戰吧！")
        )
        return
    
    print("[DEBUG] 開始獲取題目", flush=True)
    questions = get_questions()
    print(f"[DEBUG] 總題目數: {len(questions)}", flush=True)
    
    available = [q for q in questions if q["qid"] not in stats["correct_qids"]]
    print(f"[DEBUG] 未答對題目數: {len(available)}", flush=True)
    
    today_answered = set(daily["today_answered"])
    print(f"[DEBUG] 今日已回答: {today_answered}", flush=True)
    
    available = [q for q in available if q["qid"] not in today_answered]
    print(f"[DEBUG] 最終可用題目數: {len(available)}", flush=True)
    
    if not available:
        print("[DEBUG] send_question: no available questions", flush=True)
        line_bot_api.push_message(
            user_id,
            TextSendMessage(text="今天沒有新題目了，明天再來挑戰吧！")
        )
        return
    
    import random
    question = random.choice(available)
    print(f"[DEBUG] 選中題目: qid={question['qid']}, 題目={question['question'][:30]}...", flush=True)
    
    daily["today_answered"].append(question["qid"])
    user_states[user_id] = {
        'current_question': question,
        'answered': False
    }
    
    print("[DEBUG] 準備發送題目", flush=True)
    try:
        question_message = create_question_message(question)
        line_bot_api.push_message(
            user_id,
            question_message
        )
        print(f"[DEBUG] 問題已發送給用戶 {user_id}: {datetime.now()}", flush=True)
    except Exception as e:
        print(f"[ERROR] 發送題目失敗: {e}", flush=True)

def handle_answer(user_id, answer_number):
    if user_id not in user_states or user_states[user_id]['answered']:
        return
    question = user_states[user_id]['current_question']
    correct_answer = int(question['answer'])
    user_answer = answer_number
    user_states[user_id]['answered'] = True
    daily = get_user_daily(user_id)
    stats = get_user_stats(user_id)
    # 增加今日題數
    daily["today_count"] += 1
    # 判斷答對/錯
    if user_answer == correct_answer:
        stats["correct"] += 1
        if question["qid"] not in stats["correct_qids"]:
            stats["correct_qids"].append(question["qid"])
        message = "哇窩！你的解剖真好！\n\n"
    else:
        stats["wrong"] += 1
        message = f"殘念啊！正確答案是{correct_answer}. {question['options'][correct_answer - 1]}\n\n"
    update_user_stats(user_id, stats["correct"], stats["wrong"], stats["correct_qids"])
    message += f"補充說明：\n{question['explanation']}"
    # 先推送補充資料
    line_bot_api.push_message(
        user_id,
        TextSendMessage(text=message)
    )
    # 再推送繼續每日問答選單
    line_bot_api.push_message(
        user_id,
        create_continue_menu_message(stats["correct"])
    )

def create_menu_message():
    flex_contents = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "解剖學問答",
                    "weight": "bold",
                    "size": "xl",
                    "align": "center",
                    "margin": "md"
                },
                {
                    "type": "text",
                    "text": "請選擇操作：",
                    "size": "md",
                    "align": "center",
                    "margin": "md"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "開始",
                                "text": "開始"
                            },
                            "style": "primary",
                            "color": "#1DB446"
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "停止每日問答",
                                "text": "停止每日問答"
                            },
                            "style": "secondary"
                        }
                    ]
                }
            ]
        }
    }
    return FlexSendMessage(
        alt_text="解剖學問答選單",
        contents=flex_contents
    )

def create_continue_menu_message(correct_count):
    flex_contents = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "每日問答",
                    "weight": "bold",
                    "size": "lg",
                    "align": "center",
                    "color": "#1DB446",
                    "margin": "md"
                },
                {
                    "type": "separator",
                    "margin": "md"
                },
                {
                    "type": "text",
                    "text": f"繼續每日問答；目前累積的積分是{correct_count}題正確",
                    "wrap": True,
                    "size": "md",
                    "align": "center",
                    "margin": "lg",
                    "color": "#333333"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "postback",
                                "label": "繼續每日問答",
                                "data": "continue_quiz"
                            },
                            "style": "primary",
                            "color": "#1DB446"
                        }
                    ]
                }
            ]
        }
    }
    return FlexSendMessage(
        alt_text="繼續每日問答",
        contents=flex_contents
    )

def create_daily_reminder_message(correct_count):
    flex_contents = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "早安！解剖學問答時間",
                    "weight": "bold",
                    "size": "lg",
                    "align": "center",
                    "color": "#1DB446",
                    "margin": "md"
                },
                {
                    "type": "separator",
                    "margin": "md"
                },
                {
                    "type": "text",
                    "text": f"目前累積總共 🔥【{correct_count} 次】解剖出擊！",
                    "wrap": True,
                    "size": "md",
                    "align": "center",
                    "margin": "lg",
                    "color": "#333333"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "開始今日問答",
                                "text": "開始"
                            },
                            "style": "primary",
                            "color": "#1DB446"
                        }
                    ]
                }
            ]
        }
    }
    return FlexSendMessage(
        alt_text="早安！解剖學問答時間",
        contents=flex_contents
    )

def send_daily_reminder(user_id):
    """發送每日提醒訊息"""
    print(f"[DEBUG] 發送每日提醒給 user_id={user_id}", flush=True)
    try:
        stats = get_user_stats(user_id)
        correct_count = stats["correct"]
        print(f"[DEBUG] 用戶 {user_id} 累積正確次數: {correct_count}", flush=True)
        
        reminder_message = create_daily_reminder_message(correct_count)
        line_bot_api.push_message(
            user_id,
            reminder_message
        )
        print(f"[DEBUG] 每日提醒已發送給用戶 {user_id}: {datetime.now()}", flush=True)
    except Exception as e:
        print(f"[ERROR] 發送每日提醒失敗: {e}", flush=True)

def main():
    print("Anatomy Quiz Bot 已啟動...")
    schedule.every().day.at(QUESTION_TIME).do(send_daily_reminder, USER_ID)
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main() 
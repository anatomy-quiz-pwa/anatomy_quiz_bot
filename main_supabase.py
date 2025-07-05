import os
import schedule
import time
from datetime import datetime, date
from linebot.v3.webhook import WebhookHandler
from linebot.v3.messaging.models import TextMessage, FlexMessage
from dotenv import load_dotenv
from supabase_quiz_handler import get_questions
from supabase_user_stats_handler import get_user_stats, update_user_stats, add_correct_answer, add_wrong_answer
from line_bot_utils import send_line_message, send_line_flex_message

# 載入環境變數
load_dotenv()

# 從環境變數讀取設定
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
USER_ID = os.getenv('USER_ID')
QUESTION_TIME = os.getenv('QUESTION_TIME', '09:00')

# 本地測試模式
LOCAL_TEST_MODE = os.getenv('LOCAL_TEST_MODE', 'false').lower() == 'true'

def safe_push_message(user_id, message):
    """安全地發送推送訊息"""
    if LOCAL_TEST_MODE:
        print(f"[LOCAL_TEST] 模擬推送訊息到 {user_id}: {message}")
        return True
    else:
        try:
            if isinstance(message, TextMessage):
                return send_line_message(user_id, message.text)
            elif isinstance(message, FlexMessage):
                return send_line_flex_message(user_id, message)
            else:
                print(f"[ERROR] 不支援的訊息類型: {type(message)}")
                return False
        except Exception as e:
            print(f"[ERROR] 推送訊息失敗: {str(e)}")
            return False

# 初始化 LINE Bot
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

def create_question_message(question, user_id=None):
    """創建問題訊息"""
    # 獲取用戶積分
    correct_count = 0
    if user_id:
        stats = get_user_stats(user_id)
        correct_count = stats['correct']
    
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
                    "text": f"目前累積：{correct_count} 題正確",
                    "size": "sm",
                    "align": "center",
                    "color": "#666666",
                    "margin": "sm"
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
    
    return FlexMessage(alt_text="今日解剖學問題", contents=flex_contents)

def send_question(user_id):
    print(f"🔍 進入 send_question function - user_id: {user_id}", flush=True)
    try:
        # 取得所有題目
        print(f"🔍 send_question: 開始獲取題目", flush=True)
        questions = get_questions()
        print(f"🔍 send_question: 總題目數: {len(questions)}", flush=True)
        
        if not questions:
            print(f"🔍 send_question: 沒有題目可用", flush=True)
            safe_push_message(
                user_id,
                TextMessage(text="暫時沒有題目，請稍後再試！")
            )
            return
        
        # 允許題目重複出現，從所有題目中隨機選擇
        import random
        question = random.choice(questions)
        print(f"🔍 send_question: 選中題目: qid={question['qid']}, 題目={question['question'][:30]}...", flush=True)
        
        user_states[user_id] = {
            'current_question': question,
            'answered': False
        }
        print(f"🔍 send_question: 已設置用戶狀態", flush=True)
        
        print(f"🔍 send_question: 準備發送題目", flush=True)
        question_message = create_question_message(question, user_id)
        print(f"🔍 send_question: 題目訊息已創建", flush=True)
        
        safe_push_message(
            user_id,
            question_message
        )
        print(f"🔍 send_question: 問題已發送給用戶 {user_id}: {datetime.now()}", flush=True)
        
    except Exception as e:
        print(f"🛑 send_question 發生錯誤: {e}", flush=True)
        import traceback
        traceback.print_exc()
        # 發送錯誤訊息給用戶
        try:
            safe_push_message(
                user_id,
                TextMessage(text="抱歉，發送題目時發生錯誤，請稍後再試！")
            )
        except Exception as push_error:
            print(f"🛑 send_question: 發送錯誤訊息也失敗: {push_error}", flush=True)

def handle_answer(user_id, answer_number):
    print(f"🔍 進入 handle_answer function - user_id: {user_id}, answer: {answer_number}", flush=True)
    
    # 檢查用戶狀態，防止重複回答
    if user_id not in user_states:
        print(f"🔍 handle_answer: 用戶 {user_id} 沒有當前題目狀態", flush=True)
        return
    
    if user_states[user_id]['answered']:
        print(f"🔍 handle_answer: 用戶 {user_id} 已經回答過此題", flush=True)
        # 回覆用戶已經回答過
        safe_push_message(
            user_id,
            TextMessage(text="你已經回答過這題了！請等待下一題。")
        )
        return
    
    # 立即標記為已回答，防止重複點擊
    user_states[user_id]['answered'] = True
    print(f"🔍 handle_answer: 已標記用戶 {user_id} 為已回答", flush=True)
    
    # 立即回覆確認訊息
    try:
        print(f"🔍 handle_answer: 準備發送確認訊息", flush=True)
        safe_push_message(
            user_id,
            TextMessage(text="收到你的答案！正在處理中...")
        )
        print(f"🔍 handle_answer: 確認訊息已發送", flush=True)
    except Exception as e:
        print(f"🛑 handle_answer: 發送確認訊息失敗: {e}", flush=True)
    
    question = user_states[user_id]['current_question']
    correct_answer = int(question['answer'])
    user_answer = answer_number
    
    print(f"🔍 handle_answer: 處理答案 - 正確答案={correct_answer}, 用戶答案={user_answer}", flush=True)
    print(f"🔍 handle_answer: question['qid'] = {question['qid']}", flush=True)
    print(f"🔍 handle_answer: question 完整資料 = {question}", flush=True)
    
    print(f"🔍 handle_answer: 準備獲取用戶每日狀態", flush=True)
    daily = get_user_daily(user_id)
    print(f"🔍 handle_answer: 每日狀態 = {daily}", flush=True)
    
    print(f"🔍 handle_answer: 準備獲取用戶統計資料", flush=True)
    stats = get_user_stats(user_id)
    print(f"🔍 handle_answer: 統計資料更新前 = {stats}", flush=True)
    
    # 檢查答案是否正確
    is_correct = (user_answer == correct_answer)
    print(f"🔍 handle_answer: 答案檢查結果 - is_correct = {is_correct}", flush=True)
    
    # 更新統計到 Supabase
    if is_correct:
        # 使用 Supabase 函數更新正確答案
        print(f"🔍 handle_answer: 準備呼叫 add_correct_answer(user_id={user_id}, question_id={question['qid']})", flush=True)
        success = add_correct_answer(user_id, question['qid'])
        print(f"🔍 handle_answer: add_correct_answer 結果 = {success}", flush=True)
        if not success:
            print(f"🛑 handle_answer: Failed to add correct answer for user {user_id}", flush=True)
    else:
        # 使用 Supabase 函數更新錯誤答案
        print(f"🔍 handle_answer: 準備呼叫 add_wrong_answer(user_id={user_id})", flush=True)
        success = add_wrong_answer(user_id)
        print(f"🔍 handle_answer: add_wrong_answer 結果 = {success}", flush=True)
        if not success:
            print(f"🛑 handle_answer: Failed to add wrong answer for user {user_id}", flush=True)
    
    # 重新查詢最新 stats（確保顯示最新積分）
    print(f"🔍 handle_answer: 準備重新查詢最新統計資料", flush=True)
    latest_stats = get_user_stats(user_id)
    print(f"🔍 handle_answer: 更新後統計資料 = {latest_stats}", flush=True)

    # 創建結果訊息
    if is_correct:
        result_text = f"🎉 答對了！\n\n正確答案：{correct_answer}. {question['options'][correct_answer-1]}\n\n"
        
        # 使用新的 answer_feedback 欄位
        if question.get('answer_feedback'):
            result_text += f"💡 {question['answer_feedback']}\n\n"
        elif question.get('explanation'):
            result_text += f"💡 {question['explanation']}\n\n"
        
        # 使用新的 emotion_response 欄位
        if question.get('emotion_response'):
            result_text += f"💬 {question['emotion_response']}\n\n"
        
        result_text += f"你的解剖力：{latest_stats['correct']} 次正確"
    else:
        result_text = f"❌ 答錯了！\n\n正確答案：{correct_answer}. {question['options'][correct_answer-1]}\n你的答案：{user_answer}. {question['options'][user_answer-1]}\n\n"
        
        # 使用新的 answer_feedback 欄位
        if question.get('answer_feedback'):
            result_text += f"💡 {question['answer_feedback']}\n\n"
        elif question.get('explanation'):
            result_text += f"💡 {question['explanation']}\n\n"
        
        # 使用新的 emotion_response 欄位
        if question.get('emotion_response'):
            result_text += f"💬 {question['emotion_response']}\n\n"
        
        result_text += f"你的解剖力：{latest_stats['correct']} 次正確"
    
    # 發送結果訊息
    try:
        print(f"🔍 handle_answer: 準備發送結果訊息", flush=True)
        safe_push_message(
            user_id,
            TextMessage(text=result_text)
        )
        print(f"🔍 handle_answer: 結果訊息已發送給用戶 {user_id}", flush=True)
    except Exception as e:
        print(f"🛑 handle_answer: 發送結果訊息失敗: {e}", flush=True)

def create_menu_message(user_id=None):
    """創建主選單訊息，會自動查詢最新積分"""
    correct_count = 0
    if user_id is not None:
        stats = get_user_stats(user_id)
        correct_count = stats['correct']
    flex_contents = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "解剖學問答 Bot",
                    "weight": "bold",
                    "size": "lg",
                    "align": "center",
                    "color": "#1DB446",
                    "margin": "md"
                },
                {
                    "type": "text",
                    "text": f"每天挑戰 100 題解剖學問題，提升你的醫學知識！\n目前累積：{correct_count} 題正確",
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
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "postback",
                                "label": "開始每日問答",
                                "data": "continue_quiz"
                            },
                            "style": "primary",
                            "color": "#1DB446",
                            "margin": "sm"
                        }
                    ]
                }
            ]
        }
    }
    return FlexMessage(alt_text="解剖學問答 Bot 主選單", contents=flex_contents)

def create_continue_menu_message(user_id):
    """創建繼續選單訊息，會自動查詢最新積分"""
    stats = get_user_stats(user_id)
    correct_count = stats['correct']
    flex_contents = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "繼續挑戰",
                    "weight": "bold",
                    "size": "lg",
                    "align": "center",
                    "color": "#1DB446",
                    "margin": "md"
                },
                {
                    "type": "text",
                    "text": f"目前累積：{correct_count} 題正確",
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
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "postback",
                                "label": "下一題",
                                "data": "continue_quiz"
                            },
                            "style": "primary",
                            "color": "#1DB446",
                            "margin": "sm"
                        }
                    ]
                }
            ]
        }
    }
    return FlexMessage(alt_text="繼續挑戰選單", contents=flex_contents)

def create_daily_reminder_message(correct_count):
    """創建每日提醒訊息"""
    flex_contents = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "🌅 早安！",
                    "weight": "bold",
                    "size": "lg",
                    "align": "center",
                    "color": "#1DB446",
                    "margin": "md"
                },
                {
                    "type": "text",
                    "text": "新的一天開始了，準備好挑戰今天的解剖學問題了嗎？",
                    "size": "sm",
                    "align": "center",
                    "color": "#666666",
                    "margin": "sm"
                },
                {
                    "type": "text",
                    "text": f"目前累積：{correct_count} 次正確",
                    "size": "sm",
                    "align": "center",
                    "color": "#1DB446",
                    "margin": "sm"
                },
                {
                    "type": "separator",
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
                                "type": "postback",
                                "label": "開始今日挑戰",
                                "data": "continue_quiz"
                            },
                            "style": "primary",
                            "color": "#1DB446",
                            "margin": "sm"
                        }
                    ]
                }
            ]
        }
    }
    
    return FlexMessage(alt_text="每日提醒", contents=flex_contents)

def send_daily_reminder(user_id):
    """發送每日提醒"""
    try:
        stats = get_user_stats(user_id)
        reminder_message = create_daily_reminder_message(stats['correct'])
        line_bot_api.push_message(user_id, reminder_message)
        print(f"[DEBUG] 每日提醒已發送給用戶 {user_id}: {datetime.now()}", flush=True)
    except Exception as e:
        print(f"[ERROR] 發送每日提醒失敗: {e}", flush=True)

def create_evening_reminder_message(correct_count):
    """創建晚間提醒訊息"""
    flex_contents = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "🌙 晚安！",
                    "weight": "bold",
                    "size": "lg",
                    "align": "center",
                    "color": "#1DB446",
                    "margin": "md"
                },
                {
                    "type": "text",
                    "text": "今天還沒完成題目嗎？快來挑戰一下吧！",
                    "size": "sm",
                    "align": "center",
                    "color": "#666666",
                    "margin": "sm"
                },
                {
                    "type": "text",
                    "text": f"目前累積：{correct_count} 次正確",
                    "size": "sm",
                    "align": "center",
                    "color": "#1DB446",
                    "margin": "sm"
                },
                {
                    "type": "separator",
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
                                "type": "postback",
                                "label": "現在挑戰",
                                "data": "continue_quiz"
                            },
                            "style": "primary",
                            "color": "#1DB446",
                            "margin": "sm"
                        }
                    ]
                }
            ]
        }
    }
    
    return FlexMessage(alt_text="晚間提醒", contents=flex_contents)

def check_and_remind_incomplete_users():
    """檢查並提醒未完成今日題目的用戶"""
    try:
        # 這裡可以實現檢查未完成用戶的邏輯
        # 目前先發送給指定用戶
        if USER_ID:
            daily = get_user_daily(USER_ID)
            if daily["today_count"] < 5:
                stats = get_user_stats(USER_ID)
                reminder_message = create_evening_reminder_message(stats['correct'])
                line_bot_api.push_message(USER_ID, reminder_message)
                print(f"[DEBUG] 晚間提醒已發送給用戶 {USER_ID}: {datetime.now()}", flush=True)
    except Exception as e:
        print(f"[ERROR] 檢查未完成用戶失敗: {e}", flush=True)

def main():
    """主函數"""
    print("Starting LINE Bot with Supabase integration...")
    
    # 設定排程任務
    schedule.every().day.at(QUESTION_TIME).do(send_daily_reminder, USER_ID)
    schedule.every().day.at("21:00").do(check_and_remind_incomplete_users)
    
    print(f"Bot started. Daily reminder scheduled at {QUESTION_TIME}")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        print("Bot stopped by user")

if __name__ == "__main__":
    main() 
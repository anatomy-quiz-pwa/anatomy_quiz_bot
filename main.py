import schedule

import time
from datetime import datetime
from linebot import LineBotApi, WebhookHandler
from linebot.models import (
    TextSendMessage, TemplateSendMessage, ButtonsTemplate,
    PostbackAction, MessageAction, TextMessage
)
from linebot.exceptions import LineBotApiError
from config import LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET, USER_ID, QUESTION_TIME
from sheets_handler import get_random_question




# 初始化 LINE Bot
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 用戶狀態字典
user_states = {}

# 用戶答題計數字典
user_question_count = {}

def create_question_message(question):
    """創建問題訊息"""
    buttons = []
    for i, option in enumerate(question['options'], 1):
        buttons.append(
            PostbackAction(
                label=f"{i}. {option}",
                data=f"answer_{i}"
            )
        )
    
    template = ButtonsTemplate(
        title="今日解剖學問題",
        text=question['question'],
        actions=buttons
    )
    
    return TemplateSendMessage(alt_text="今日解剖學問題", template=template)

def send_question(user_id):
    """發送每日問題"""
    try:
        question = get_random_question()
        if not question:
            line_bot_api.push_message(
                user_id,
                TextSendMessage(text="抱歉，目前無法獲取問題。")
            )
            return
        
        # 保存用戶的當前問題
        user_states[user_id] = {
            'current_question': question,
            'answered': False
        }
        
        # 發送問題
        line_bot_api.push_message(
            user_id,
            create_question_message(question)
        )
        print(f"問題已發送給用戶 {user_id}: {datetime.now()}")
    except Exception as e:
        print(f"發送問題時出錯: {str(e)}")

def get_user_question_count(user_id):
    """獲取用戶的答題計數"""
    return user_question_count.get(user_id, 0)

def handle_answer(user_id, answer_number):
    """處理用戶答案"""
    if user_id not in user_states or user_states[user_id]['answered']:
        return
    
    question = user_states[user_id]['current_question']
    correct_answer = int(question['answer'])
    user_answer = answer_number
    
    # 標記用戶已回答
    user_states[user_id]['answered'] = True
    
    # 增加用戶答題計數
    user_question_count[user_id] = user_question_count.get(user_id, 0) + 1
    
    # 準備回覆訊息
    if user_answer == correct_answer:
        message = "哇窩！你的解剖真好！\n\n"
    else:
        # 顯示正確答案的選項文字
        correct_option_text = question['options'][correct_answer - 1]  # 因為選項索引從0開始
        message = f"殘念啊！正確答案是{correct_answer}. {correct_option_text}\n\n"
    
    message += f"補充說明：\n{question['explanation']}"
    
    # 發送回覆
    line_bot_api.push_message(
        user_id,
        TextSendMessage(text=message)
    )

def create_menu_message():
    """創建主選單"""
    template = ButtonsTemplate(
        title="解剖學問答",
        text="請選擇操作：",
        actions=[
            MessageAction(
                label="開始每日問答",
                text="開始每日問答"
            ),
            MessageAction(
                label="停止每日問答",
                text="停止每日問答"
            )
        ]
    )
    return TemplateSendMessage(alt_text="解剖學問答選單", template=template)

def main():
    """主程序"""
    print("Anatomy Quiz Bot 已啟動...")
    
    # 設置定時任務
    schedule.every().day.at(QUESTION_TIME).do(send_question, USER_ID)
    
    # 運行定時任務
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main() 
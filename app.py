import os 
from flask import Flask, request, abort, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    PostbackEvent, FlexSendMessage
)
from dotenv import load_dotenv
from main import send_question, handle_answer, create_menu_message, get_user_question_count, get_user_correct_wrong

# 載入環境變量
load_dotenv()

app = Flask(__name__)

# 直接從環境變數讀取
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')

app.logger.info(f"Token loaded: {LINE_CHANNEL_ACCESS_TOKEN[:20] if LINE_CHANNEL_ACCESS_TOKEN else 'None'}...")
app.logger.info(f"Secret loaded: {LINE_CHANNEL_SECRET[:10] if LINE_CHANNEL_SECRET else 'None'}...")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['GET', 'POST'])
def callback():
    app.logger.info(f"Received {request.method} request to /callback")
    
    if request.method == 'GET':
        # 處理 LINE 的驗證請求
        return 'OK'
    
    # 處理 POST 請求
    try:
        # 獲取 X-Line-Signature 標頭值
        signature = request.headers.get('X-Line-Signature', '')
        app.logger.info(f"Signature: {signature}")
        
        # 如果沒有簽名，直接返回 OK
        if not signature:
            app.logger.warning("No signature provided, returning OK")
            return 'OK'
        
        # 獲取請求內容
        body = request.get_data(as_text=True)
        app.logger.info(f"Request body: {body}")
        
        # 暫時跳過簽名驗證來測試
        if not LINE_CHANNEL_SECRET:
            app.logger.warning("No LINE_CHANNEL_SECRET found, skipping signature verification")
            return 'OK'
        
        # 驗證簽名
        handler.handle(body, signature)
        
        return 'OK'
        
    except InvalidSignatureError as e:
        app.logger.error(f"Invalid signature: {str(e)}")
        # 暫時返回 200 來測試
        return 'OK'
    except Exception as e:
        app.logger.error(f"Error handling webhook: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route("/", methods=['GET'])
def index():
    return "LINE Bot is running!"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("收到訊息", flush=True)
    app.logger.info(f"[DEBUG] 收到 MessageEvent: {event}")
    text = event.message.text
    user_id = event.source.user_id

    app.logger.info(f"Received message from {user_id}: {text}")

    # 處理特定指令
    if text == "開始":
        try:
            count = get_user_question_count(user_id)
            correct, wrong = get_user_correct_wrong(user_id)
            welcome_message = f"你今天已經挑戰了 🌟【{count} 次】\n目前累積總共 🔥【{correct} 次】解剖出擊！"
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=welcome_message)
            )
            import time
            time.sleep(1)
            send_question(user_id)
        except Exception as e:
            app.logger.error(f"[ERROR] handle_message: {str(e)}")
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="抱歉，目前無法獲取問題。")
            )
    elif text == "停止每日問答":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="已停止每日問答。")
        )
    else:
        # 只要不是答題流程，回覆主選單
        try:
            line_bot_api.reply_message(
                event.reply_token,
                create_menu_message()
            )
        except Exception as e:
            app.logger.error(f"[ERROR] handle_message menu: {str(e)}")
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="收到您的訊息！請選擇「開始每日問答」來測試問題。")
            )

@handler.add(PostbackEvent)
def handle_postback(event):
    print("收到Postback", flush=True)
    app.logger.info(f"[DEBUG] 收到 PostbackEvent: {event}")
    user_id = event.source.user_id
    data = event.postback.data
    
    app.logger.info(f"[DEBUG] Postback data: {data}")
    app.logger.info(f"[DEBUG] User ID: {user_id}")

    if data == "continue_quiz":
        app.logger.info("[DEBUG] 處理 continue_quiz")
        count = get_user_question_count(user_id)
        app.logger.info(f"[DEBUG] 今日題數: {count}")
        if count < 5:
            app.logger.info("[DEBUG] 發送下一題")
            send_question(user_id)
        else:
            app.logger.info("[DEBUG] 今日已達上限")
            line_bot_api.push_message(
                user_id,
                TextSendMessage(text="今日已經達到上限！明天再來增加解剖力！")
            )
        return

    if data.startswith("answer_"):
        app.logger.info(f"[DEBUG] 處理答案: {data}")
        try:
            answer_number = int(data.split("_")[1])
            app.logger.info(f"[DEBUG] 答案編號: {answer_number}")
            handle_answer(user_id, answer_number)
        except Exception as e:
            app.logger.error(f"[ERROR] handle_postback: {str(e)}")
            app.logger.error(f"[ERROR] 完整錯誤: {e}")
    
    app.logger.info("[DEBUG] Postback 處理完成")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port) 
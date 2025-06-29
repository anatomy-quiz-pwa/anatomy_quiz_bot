import os 
from flask import Flask, request, abort, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    PostbackEvent, TemplateSendMessage, ButtonsTemplate
)
from dotenv import load_dotenv
from main import send_question, handle_answer, create_menu_message, get_user_question_count

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
    text = event.message.text
    user_id = event.source.user_id

    app.logger.info(f"Received message from {user_id}: {text}")

    # 處理特定指令
    if text == "開始每日問答":
        try:
            # 獲取用戶的答題計數
            count = get_user_question_count(user_id)
            
            # 發送歡迎訊息
            welcome_message = f"歡迎來到今天的解剖咬一口，這是你完成的第{count + 1}個解剖題目！溫馨提醒～本帳號只能進行機器人解剖題目練習，沒有小編回覆您喔！我們開始今天的練習吧！"
            
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=welcome_message)
            )
            
            # 延遲一下再發送問題，避免訊息順序混亂
            import time
            time.sleep(1)
            
            # 發送問題
            send_question(user_id)
            
        except Exception as e:
            app.logger.error(f"Error sending question: {str(e)}")
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="抱歉，目前無法獲取問題。")
            )
    elif text == "停止每日問答":
        # TODO: 實現停止功能
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="已停止每日問答。")
        )
    else:
        # 發送主選單
        try:
            line_bot_api.reply_message(
                event.reply_token,
                create_menu_message()
            )
        except Exception as e:
            app.logger.error(f"Error sending menu: {str(e)}")
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="收到您的訊息！請選擇「開始每日問答」來測試問題。")
            )

@handler.add(PostbackEvent)
def handle_postback(event):
    user_id = event.source.user_id
    data = event.postback.data

    if data.startswith("answer_"):
        answer_number = int(data.split("_")[1])
        handle_answer(user_id, answer_number)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port) 
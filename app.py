import os 
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    PostbackEvent, TemplateSendMessage, ButtonsTemplate
)
from config import LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET
from main import send_question, handle_answer, create_menu_message

app = Flask(__name__)

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # 獲取 X-Line-Signature 標頭值
    signature = request.headers.get('X-Line-Signature', '')

    # 獲取請求內容
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.error("Invalid signature")
        abort(400)
    except Exception as e:
        app.logger.error(f"Error handling webhook: {str(e)}")
        abort(500)

    return 'OK'

@app.route("/", methods=['GET'])
def index():
    return "LINE Bot is running!"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    user_id = event.source.user_id

    if text == "開始每日問答":
        send_question(user_id)
    elif text == "停止每日問答":
        # TODO: 實現停止功能
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="已停止每日問答。")
        )
    else:
        # 發送主選單
        line_bot_api.reply_message(
            event.reply_token,
            create_menu_message()
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
import os 
from flask import Flask, request, abort, jsonify
from linebot.v3.webhook import WebhookHandler
from linebot.v3.messaging import Configuration, MessagingApi
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent, PostbackEvent
from linebot.v3.messaging.models import TextMessage, FlexMessage
from dotenv import load_dotenv
from main_supabase import send_question, handle_answer, create_menu_message, get_user_question_count, get_user_correct_wrong
from supabase import create_client, Client

# 載入環境變量
load_dotenv()

# 本地測試模式：設為 True 時不會發送實際 LINE 訊息，只記錄 log
LOCAL_TEST_MODE = os.getenv('LOCAL_TEST_MODE', 'false').lower() == 'true'

if LOCAL_TEST_MODE:
    print("🔧 本地測試模式已啟用 - 不會發送實際 LINE 訊息")

app = Flask(__name__)

# 直接從環境變數讀取
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')

app.logger.info(f"Token loaded: {LINE_CHANNEL_ACCESS_TOKEN[:20] if LINE_CHANNEL_ACCESS_TOKEN else 'None'}...")
app.logger.info(f"Secret loaded: {LINE_CHANNEL_SECRET[:10] if LINE_CHANNEL_SECRET else 'None'}...")

configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
line_bot_api = MessagingApi(configuration)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

def log_user_answer(supabase, user_id, question, chosen_option):
    """
    紀錄學生作答行為到 quiz_logs 表格中

    question: 一筆題目 dict，需含 id, answer, tags, level
    chosen_option: 學生選擇的選項編號（1～4）
    """
    is_correct = (chosen_option == question["answer"])  # 注意: 你的題目正確答案 key 可能是 'answer'
    supabase.table("quiz_logs").insert({
        "user_id": user_id,
        "question_id": question["id"],
        "chosen_option": chosen_option,
        "is_correct": is_correct,
        "tags": question.get("tags", []),
        "level": question.get("level", 1)
    }).execute()

# 在 log_user_answer 函數之後添加本地測試模式的輔助函數
def safe_reply_message(reply_token, message):
    """安全地發送回覆訊息，在本地測試模式下只記錄 log"""
    if LOCAL_TEST_MODE:
        app.logger.info(f"[LOCAL_TEST] 模擬發送訊息到 {reply_token}: {message}")
        return True
    else:
        try:
            # 使用 v3 API 的回覆訊息方法
            from linebot.v3.messaging import ReplyMessageRequest
            request = ReplyMessageRequest(
                reply_token=reply_token,
                messages=[message]
            )
            line_bot_api.reply_message(request)
            return True
        except Exception as e:
            app.logger.error(f"[ERROR] 發送訊息失敗: {str(e)}")
            return False

def safe_push_message(user_id, message):
    """安全地發送推送訊息，在本地測試模式下只記錄 log"""
    if LOCAL_TEST_MODE:
        app.logger.info(f"[LOCAL_TEST] 模擬推送訊息到 {user_id}: {message}")
        return True
    else:
        try:
            # 使用 v3 API 的推送訊息方法
            from linebot.v3.messaging import PushMessageRequest
            request = PushMessageRequest(
                to=user_id,
                messages=[message]
            )
            line_bot_api.push_message(request)
            return True
        except Exception as e:
            app.logger.error(f"[ERROR] 推送訊息失敗: {str(e)}")
            return False

@app.route("/callback", methods=['GET', 'POST'])
def callback():
    if request.method == 'GET':
        # 處理 LINE 的驗證請求
        return 'OK'
    
    # 處理 POST 請求
    try:
        # 獲取 X-Line-Signature 標頭值
        signature = request.headers.get('X-Line-Signature', '')
        app.logger.info(f"Signature: {signature}")
        
        # 獲取請求內容
        body = request.get_data(as_text=True)
        app.logger.info(f"Request body: {body}")
        
        # 如果沒有簽名，但我們在開發環境中，仍然處理 webhook
        if not signature:
            app.logger.warning("No signature provided, but processing webhook for development")
            try:
                # 直接處理 webhook，跳過簽名驗證
                handler.handle(body, '')  # 空簽名
                app.logger.info("Webhook processed successfully without signature")
            except Exception as e:
                app.logger.error(f"Error processing webhook without signature: {str(e)}")
                # 即使有錯誤，也返回 OK 避免 LINE 重試
            return 'OK'
        
        # 有簽名的正常處理
        if not LINE_CHANNEL_SECRET:
            app.logger.warning("No LINE_CHANNEL_SECRET found, skipping signature verification")
            try:
                handler.handle(body, '')
                app.logger.info("Webhook processed successfully without secret")
            except Exception as e:
                app.logger.error(f"Error processing webhook without secret: {str(e)}")
            return 'OK'
        
        # 驗證簽名並處理
        try:
            handler.handle(body, signature)
            app.logger.info("Webhook processed successfully with signature")
        except InvalidSignatureError as e:
            app.logger.error(f"Invalid signature: {str(e)}")
            # 在開發環境中，即使簽名無效也嘗試處理
            app.logger.warning("Development mode: attempting to process webhook despite invalid signature")
            try:
                handler.handle(body, '')
                app.logger.info("Webhook processed successfully in development mode")
            except Exception as dev_e:
                app.logger.error(f"Error processing webhook in development mode: {str(dev_e)}")
        
        return 'OK'
        
    except Exception as e:
        app.logger.error(f"Error handling webhook: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route("/", methods=['GET'])
def index():
    return "LINE Bot with Supabase is running!"

@app.route("/test", methods=['GET'])
def test():
    """測試 Supabase 連線"""
    try:
        from supabase_quiz_handler import test_supabase_connection
        from supabase_user_stats_handler import test_supabase_user_stats
        
        quiz_ok = test_supabase_connection()
        stats_ok = test_supabase_user_stats()
        
        return jsonify({
            'status': 'success',
            'supabase_quiz': 'OK' if quiz_ok else 'FAILED',
            'supabase_user_stats': 'OK' if stats_ok else 'FAILED'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("收到訊息", flush=True)
    app.logger.info(f"[DEBUG] 收到 MessageEvent: {event}")
    text = event.message.text
    user_id = event.source.user_id

    # 每次收到訊息都印出用戶 ID
    print(f"🔍 收到訊息 - 用戶 ID: {user_id}")
    print(f"📝 訊息內容: {text}")
    app.logger.info(f"Received message from {user_id}: {text}")

    # 新增：查詢 user_id
    if text == "我的ID":
        safe_reply_message(
            event.reply_token,
            TextMessage(text=f"你的 user_id 是：{user_id}")
        )
        return

    # 新增：查詢積分
    if text == "積分":
        correct, wrong = get_user_correct_wrong(user_id)
        app.logger.info(f"[DEBUG] 積分查詢 - user_id: {user_id}, correct: {correct}, wrong: {wrong}")
        safe_reply_message(
            event.reply_token,
            TextMessage(text=f"你的積分：{correct}（正確）/{wrong}（錯誤）")
        )
        return

    # 新增：重置指令
    if text == "重置":
        try:
            # 清除本地快取
            from main_supabase import user_states, user_daily_state
            if user_id in user_states:
                del user_states[user_id]
            if user_id in user_daily_state:
                del user_daily_state[user_id]
            app.logger.info(f"[DEBUG] 重置指令 - 已清除用戶 {user_id} 的本地快取")
            
            # 清除 Supabase 資料庫中的用戶統計
            from supabase_user_stats_handler import reset_user_stats
            reset_success = reset_user_stats(user_id)
            
            if reset_success:
                app.logger.info(f"[DEBUG] 重置指令 - 已清除用戶 {user_id} 的 Supabase 資料")
                safe_reply_message(
                    event.reply_token,
                    TextMessage(text="✅ 重置完成！你的所有資料已完全歸零，請重新開始測驗！")
                )
            else:
                app.logger.warning(f"[DEBUG] 重置指令 - 清除 Supabase 資料失敗，但本地快取已清除")
                safe_reply_message(
                    event.reply_token,
                    TextMessage(text="⚠️ 本地快取已清除，但資料庫重置失敗。請稍後再試或聯繫管理員。")
                )
        except Exception as e:
            app.logger.error(f"[ERROR] 重置指令執行失敗: {str(e)}")
            safe_reply_message(
                event.reply_token,
                TextMessage(text="❌ 重置失敗，請稍後再試或聯繫管理員。")
            )
        return

    # 處理特定指令
    if text == "開始":
        try:
            # 獲取正確/錯誤次數（從 Supabase）
            correct, wrong = get_user_correct_wrong(user_id)
            total = correct + wrong
            
            # 獲取今日挑戰次數（從內存，可能不準確）
            today_count = get_user_question_count(user_id)
            
            app.logger.info(f"[DEBUG] 開始指令 - user_id: {user_id}, today_count: {today_count}, correct: {correct}, wrong: {wrong}, total: {total}")
            
            # 如果今日挑戰次數為 0 但累積總次數 > 0，說明應用重啟過，使用累積總次數作為今日挑戰次數
            if today_count == 0 and total > 0:
                today_count = total
                app.logger.info(f"[DEBUG] 應用重啟後，使用累積總次數作為今日挑戰次數: {today_count}")
            
            welcome_message = f"你今天已經挑戰了 🌟【{today_count} 次】\n目前累積總共 🔥【{total} 次】解剖出擊！"
            safe_reply_message(
                event.reply_token,
                TextMessage(text=welcome_message)
            )
            import time
            time.sleep(1)
            send_question(user_id)
        except Exception as e:
            app.logger.error(f"[ERROR] handle_message: {str(e)}")
            safe_reply_message(
                event.reply_token,
                TextMessage(text="抱歉，目前無法獲取問題。")
            )
    elif text == "停止每日問答":
        safe_reply_message(
            event.reply_token,
            TextMessage(text="已停止每日問答。")
        )
    elif text == "測試":
        # 測試 Supabase 連線
        try:
            from supabase_quiz_handler import test_supabase_connection
            if test_supabase_connection():
                safe_reply_message(
                    event.reply_token,
                    TextMessage(text="✅ Supabase 連線正常！")
                )
            else:
                safe_reply_message(
                    event.reply_token,
                    TextMessage(text="❌ Supabase 連線失敗！")
                )
        except Exception as e:
            safe_reply_message(
                event.reply_token,
                TextMessage(text=f"❌ 測試失敗：{str(e)}")
            )
    else:
        # 對於其他訊息，只回覆簡單的提示，不自動推送選單
        try:
            safe_reply_message(
                event.reply_token,
                TextMessage(text="輸入「開始」來開始每日問答，或輸入「積分」查看你的成績！")
            )
        except Exception as e:
            app.logger.error(f"[ERROR] handle_message default: {str(e)}")
            safe_reply_message(
                event.reply_token,
                TextMessage(text="收到您的訊息！輸入「開始」來開始每日問答。")
            )

@handler.add(PostbackEvent)
def handle_postback(event):
    print("收到Postback", flush=True)
    app.logger.info(f"[DEBUG] 收到 PostbackEvent: {event}")
    user_id = event.source.user_id
    data = event.postback.data
    
    # 每次收到按鈕點擊都印出用戶 ID
    print(f"🔘 收到按鈕點擊 - 用戶 ID: {user_id}")
    print(f"📝 按鈕資料: {data}")
    app.logger.info(f"[DEBUG] Postback data: {data}")
    app.logger.info(f"[DEBUG] User ID: {user_id}")

    if data == "continue_quiz":
        app.logger.info("[DEBUG] 處理 continue_quiz")
        # 直接發送下一題
        try:
            send_question(user_id)
        except Exception as e:
            app.logger.error(f"[ERROR] 發送下一題失敗: {str(e)}")
            safe_reply_message(
                event.reply_token,
                TextMessage(text="抱歉，無法發送下一題。請稍後再試。")
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
    port = int(os.getenv("PORT", 5001))
    app.run(host='0.0.0.0', port=port, debug=True) 
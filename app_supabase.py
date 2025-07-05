import os
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse, PlainTextResponse
from dotenv import load_dotenv
from main_supabase import send_question, handle_answer, create_menu_message, get_user_question_count, get_user_correct_wrong
from supabase import create_client, Client
from linebot.v3.webhook import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks.models import MessageEvent, PostbackEvent, TextMessageContent
from linebot.v3.messaging import TextMessage, FlexMessage
from line_bot_utils import send_line_message, send_line_flex_message, reply_line_message, reply_line_flex_message

# 載入環境變量
load_dotenv()

# 本地測試模式：設為 True 時不會發送實際 LINE 訊息，只記錄 log
LOCAL_TEST_MODE = os.getenv('LOCAL_TEST_MODE', 'false').lower() == 'true'

if LOCAL_TEST_MODE:
    print("🔧 本地測試模式已啟用 - 不會發送實際 LINE 訊息")

app = FastAPI()

# 直接從環境變數讀取
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')

print(f"Token loaded: {LINE_CHANNEL_ACCESS_TOKEN[:20] if LINE_CHANNEL_ACCESS_TOKEN else 'None'}...")
print(f"Secret loaded: {LINE_CHANNEL_SECRET[:10] if LINE_CHANNEL_SECRET else 'None'}...")

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
        print(f"[LOCAL_TEST] 模擬發送訊息到 {reply_token}: {message}")
        return True
    else:
        try:
            if isinstance(message, TextMessage):
                return reply_line_message(reply_token, message.text)
            elif isinstance(message, FlexMessage):
                return reply_line_flex_message(reply_token, message)
            else:
                print(f"[ERROR] 不支援的訊息類型: {type(message)}")
                return False
        except Exception as e:
            print(f"[ERROR] 發送訊息失敗: {str(e)}")
            return False

def safe_push_message(user_id, message):
    """安全地發送推送訊息，在本地測試模式下只記錄 log"""
    print(f"🔍 safe_push_message: 準備發送訊息到 {user_id}", flush=True)
    if LOCAL_TEST_MODE:
        print(f"🔍 safe_push_message: 本地測試模式，模擬推送訊息", flush=True)
        print(f"[LOCAL_TEST] 模擬推送訊息到 {user_id}: {message}")
        return True
    else:
        try:
            print(f"🔍 safe_push_message: 使用 LINE Bot API 發送訊息", flush=True)
            if isinstance(message, TextMessage):
                return send_line_message(user_id, message.text)
            elif isinstance(message, FlexMessage):
                return send_line_flex_message(user_id, message)
            else:
                print(f"[ERROR] 不支援的訊息類型: {type(message)}")
                return False
        except Exception as e:
            print(f"🛑 safe_push_message: 推送訊息失敗: {str(e)}", flush=True)
            print(f"[ERROR] 推送訊息失敗: {str(e)}")
            return False

@app.get("/")
def index():
    return PlainTextResponse("LINE Bot with Supabase is running!")

@app.post("/callback")
async def callback(request: Request):
    if request.method == 'POST':
        try:
            signature = request.headers.get('X-Line-Signature', '')
            body = await request.body()
            body = body.decode("utf-8")
            print(f"[FastAPI] Signature: {signature}")
            print(f"[FastAPI] Request body: {body}")
            if not signature:
                print("[FastAPI] No signature provided, but processing webhook for development")
                try:
                    handler.handle(body, '')
                    print("[FastAPI] Webhook processed successfully without signature")
                except Exception as e:
                    print(f"[FastAPI] Error processing webhook without signature: {str(e)}")
                return PlainTextResponse('OK')
            if not LINE_CHANNEL_SECRET:
                print("[FastAPI] No LINE_CHANNEL_SECRET found, skipping signature verification")
                try:
                    handler.handle(body, '')
                    print("[FastAPI] Webhook processed successfully without secret")
                except Exception as e:
                    print(f"[FastAPI] Error processing webhook without secret: {str(e)}")
                return PlainTextResponse('OK')
            try:
                handler.handle(body, signature)
                print("[FastAPI] Webhook processed successfully with signature")
            except InvalidSignatureError as e:
                print(f"[FastAPI] Invalid signature: {str(e)}")
                print("[FastAPI] Development mode: attempting to process webhook despite invalid signature")
                try:
                    handler.handle(body, '')
                    print("[FastAPI] Webhook processed successfully in development mode")
                except Exception as dev_e:
                    print(f"[FastAPI] Error processing webhook in development mode: {str(dev_e)}")
            return PlainTextResponse('OK')
        except Exception as e:
            print(f"[FastAPI] Error handling webhook: {str(e)}")
            import traceback
            traceback.print_exc()
            return JSONResponse({'error': str(e)}, status_code=500)
    return PlainTextResponse('OK')

@app.get("/test")
def test():
    """測試 Supabase 連線"""
    try:
        from supabase_quiz_handler import test_supabase_connection
        from supabase_user_stats_handler import test_supabase_user_stats
        
        quiz_ok = test_supabase_connection()
        stats_ok = test_supabase_user_stats()
        
        return JSONResponse({
            'status': 'success',
            'supabase_quiz': 'OK' if quiz_ok else 'FAILED',
            'supabase_user_stats': 'OK' if stats_ok else 'FAILED'
        })
    except Exception as e:
        return JSONResponse({
            'status': 'error',
            'message': str(e)
        }, status_code=500)

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    print("收到訊息", flush=True)
    print(f"🔍 event: {event}", flush=True)
    print(f"🔍 event.source: {event.source}", flush=True)
    print(f"🔍 event.message: {event.message}", flush=True)
    # 嘗試多種方式取得 user_id
    user_id = getattr(event.source, 'user_id', None) or getattr(event.source, 'userId', None)
    print(f"🔍 取得 user_id: {user_id}", flush=True)
    print(f"🔍 收到訊息 - 用戶 ID: {user_id}")
    print(f"📝 訊息內容: {event.message.text}")
    print(f"Received message from {user_id}: {event.message.text}")

    # 新增：查詢 user_id
    if event.message.text == "我的ID":
        print(f"🔍 收到我的ID指令，user_id: {user_id}", flush=True)
        safe_reply_message(
            event.reply_token,
            TextMessage(text=f"你的 user_id 是：{user_id}")
        )
        return

    # 新增：查詢積分
    if event.message.text == "積分":
        correct, wrong = get_user_correct_wrong(user_id)
        print(f"[DEBUG] 積分查詢 - user_id: {user_id}, correct: {correct}, wrong: {wrong}")
        safe_reply_message(
            event.reply_token,
            TextMessage(text=f"你的積分：{correct}（正確）/{wrong}（錯誤）")
        )
        return

    # 新增：重置指令
    if event.message.text == "重置":
        try:
            # 清除本地快取
            from main_supabase import user_states, user_daily_state
            if user_id in user_states:
                del user_states[user_id]
            if user_id in user_daily_state:
                del user_daily_state[user_id]
            print(f"[DEBUG] 重置指令 - 已清除用戶 {user_id} 的本地快取")
            
            # 清除 Supabase 資料庫中的用戶統計
            from supabase_user_stats_handler import reset_user_stats
            reset_success = reset_user_stats(user_id)
            
            if reset_success:
                print(f"[DEBUG] 重置指令 - 已清除用戶 {user_id} 的 Supabase 資料")
                safe_reply_message(
                    event.reply_token,
                    TextMessage(text="✅ 重置完成！你的所有資料已完全歸零，請重新開始測驗！")
                )
            else:
                print(f"[DEBUG] 重置指令 - 清除 Supabase 資料失敗，但本地快取已清除")
                safe_reply_message(
                    event.reply_token,
                    TextMessage(text="⚠️ 本地快取已清除，但資料庫重置失敗。請稍後再試或聯繫管理員。")
                )
        except Exception as e:
            print(f"[ERROR] 重置指令執行失敗: {str(e)}")
            safe_reply_message(
                event.reply_token,
                TextMessage(text="❌ 重置失敗，請稍後再試或聯繫管理員。")
            )
        return

    # 處理特定指令
    if event.message.text == "開始":
        try:
            # 獲取正確/錯誤次數（從 Supabase）
            correct, wrong = get_user_correct_wrong(user_id)
            total = correct + wrong
            
            welcome_message = f"目前累積總共 🔥【{total} 次】解剖出擊！"
            safe_reply_message(
                event.reply_token,
                TextMessage(text=welcome_message)
            )
            import time
            time.sleep(1)
            print(f"🔍 開始指令: 準備調用 send_question(user_id={user_id})", flush=True)
            send_question(user_id)
            print(f"🔍 開始指令: send_question 調用完成", flush=True)
        except Exception as e:
            print(f"[ERROR] handle_message: {str(e)}")
            safe_reply_message(
                event.reply_token,
                TextMessage(text="抱歉，目前無法獲取問題。")
            )
    elif event.message.text == "停止每日問答":
        safe_reply_message(
            event.reply_token,
            TextMessage(text="已停止每日問答。")
        )
    elif event.message.text == "測試":
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
            print(f"[ERROR] handle_message default: {str(e)}")
            safe_reply_message(
                event.reply_token,
                TextMessage(text="收到您的訊息！輸入「開始」來開始每日問答。")
            )

@handler.add(PostbackEvent)
def handle_postback(event):
    print("收到Postback", flush=True)
    print(f"[DEBUG] 收到 PostbackEvent: {event}")
    user_id = event.source.user_id
    data = event.postback.data
    
    # 每次收到按鈕點擊都印出用戶 ID
    print(f"🔘 收到按鈕點擊 - 用戶 ID: {user_id}")
    print(f"📝 按鈕資料: {data}")
    print(f"[DEBUG] Postback data: {data}")
    print(f"[DEBUG] User ID: {user_id}")

    if data == "continue_quiz":
        print("[DEBUG] 處理 continue_quiz")
        # 直接發送下一題
        try:
            send_question(user_id)
        except Exception as e:
            print(f"[ERROR] 發送下一題失敗: {str(e)}")
            safe_reply_message(
                event.reply_token,
                TextMessage(text="抱歉，無法發送下一題。請稍後再試。")
            )
        return

    if data.startswith("answer_"):
        print(f"[DEBUG] 處理答案: {data}")
        try:
            answer_number = int(data.split("_")[1])
            print(f"[DEBUG] 答案編號: {answer_number}")
            handle_answer(user_id, answer_number)
        except Exception as e:
            print(f"[ERROR] handle_postback: {str(e)}")
            print(f"[ERROR] 完整錯誤: {e}")
    
    print("[DEBUG] Postback 處理完成")

# FastAPI 啟動方式：
# uvicorn app_supabase:app --host 0.0.0.0 --port 5001 
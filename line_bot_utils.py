from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, PushMessageRequest, ReplyMessageRequest, TextMessage
import os

def get_line_configuration():
    """獲取 LINE Bot 配置"""
    line_channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
    if not line_channel_access_token:
        raise ValueError("LINE_CHANNEL_ACCESS_TOKEN 環境變數未設定")
    return Configuration(access_token=line_channel_access_token)

def send_line_message(user_id: str, message_text: str):
    """發送文字訊息到指定用戶"""
    try:
        configuration = get_line_configuration()
        with ApiClient(configuration) as api_client:
            line_bot = MessagingApi(api_client)
            line_bot.push_message(
                PushMessageRequest(
                    to=user_id,
                    messages=[
                        TextMessage(text=message_text)
                    ]
                )
            )
        return True
    except Exception as e:
        print(f"[ERROR] 發送 LINE 訊息失敗: {str(e)}")
        return False

def send_line_flex_message(user_id: str, flex_message):
    """發送 Flex 訊息到指定用戶"""
    try:
        configuration = get_line_configuration()
        with ApiClient(configuration) as api_client:
            line_bot = MessagingApi(api_client)
            line_bot.push_message(
                PushMessageRequest(
                    to=user_id,
                    messages=[flex_message]
                )
            )
        return True
    except Exception as e:
        print(f"[ERROR] 發送 LINE Flex 訊息失敗: {str(e)}")
        return False

def reply_line_message(reply_token: str, message_text: str):
    """回覆文字訊息"""
    try:
        configuration = get_line_configuration()
        with ApiClient(configuration) as api_client:
            line_bot = MessagingApi(api_client)
            line_bot.reply_message(
                ReplyMessageRequest(
                    reply_token=reply_token,
                    messages=[
                        TextMessage(text=message_text)
                    ]
                )
            )
        return True
    except Exception as e:
        print(f"[ERROR] 回覆 LINE 訊息失敗: {str(e)}")
        return False

def reply_line_flex_message(reply_token: str, flex_message):
    """回覆 Flex 訊息"""
    try:
        configuration = get_line_configuration()
        with ApiClient(configuration) as api_client:
            line_bot = MessagingApi(api_client)
            line_bot.reply_message(
                ReplyMessageRequest(
                    reply_token=reply_token,
                    messages=[flex_message]
                )
            )
        return True
    except Exception as e:
        print(f"[ERROR] 回覆 LINE Flex 訊息失敗: {str(e)}")
        return False 
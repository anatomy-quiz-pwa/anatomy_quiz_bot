
from flask import Flask, request, jsonify
import os
import logging

app = Flask(__name__)

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    """處理 webhook 訊息"""
    try:
        logger.info("📨 收到 webhook 請求")
        
        data = request.get_json()
        logger.info(f"📊 請求數據: {data}")
        
        # 基本驗證
        if not data:
            logger.warning("⚠️ 沒有收到數據")
            return 'OK', 200
        
        # 處理 LINE Bot 訊息
        if 'events' in data:
            for event in data['events']:
                if event['type'] == 'message':
                    sender_id = event['source']['userId']
                    message = event['message']
                    
                    if message['type'] == 'text':
                        message_text = message.get('text', '').strip()
                        logger.info(f"📨 收到來自用戶 {sender_id} 的訊息: {message_text}")
                        
                        # 檢查是否為排行榜請求
                        if message_text.lower() in ['排行榜', 'leaderboard', '排名', '排行']:
                            logger.info(f"📊 用戶 {sender_id} 請求查看排行榜")
                            # 這裡應該發送排行榜，但先只記錄日誌
                            logger.info("✅ 排行榜請求已識別")
        
        return 'OK', 200
        
    except Exception as e:
        logger.error(f"❌ Webhook 處理失敗: {e}")
        return 'Error', 500

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "ok", "message": "Webhook service is running"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

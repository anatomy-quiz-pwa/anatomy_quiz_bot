
from flask import Flask, request, jsonify
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        logger.info("📨 收到 webhook 請求")
        data = request.get_json()
        logger.info(f"📊 請求數據: {data}")
        
        if data and 'events' in data:
            for event in data['events']:
                if event.get('type') == 'message':
                    message = event.get('message', {})
                    if message.get('type') == 'text':
                        text = message.get('text', '')
                        logger.info(f"📨 收到文字訊息: {text}")
                        
                        if text.lower() in ['排行榜', 'leaderboard', '排名', '排行']:
                            logger.info("📊 排行榜請求已識別")
                            return jsonify({"status": "success", "message": "排行榜請求已處理"}), 200
        
        return 'OK', 200
        
    except Exception as e:
        logger.error(f"❌ 錯誤: {e}")
        return 'Error', 500

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "ok", "message": "Webhook service is running"})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

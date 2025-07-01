import os
from dotenv import load_dotenv

# 載入環境變量
load_dotenv()

# LINE Bot 配置
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')

# 用戶配置
USER_ID = os.getenv('USER_ID')

# 問題發送時間
QUESTION_TIME = os.getenv('QUESTION_TIME', '09:00')

# 問題數據庫路徑
QUESTIONS_DB = 'questions.json'

# Supabase 配置
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY') 
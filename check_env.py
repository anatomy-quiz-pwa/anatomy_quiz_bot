#!/usr/bin/env python3
import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

print("=== 環境變數檢查 ===")
print(f"LINE_CHANNEL_ACCESS_TOKEN: {'已設定' if os.getenv('LINE_CHANNEL_ACCESS_TOKEN') and os.getenv('LINE_CHANNEL_ACCESS_TOKEN') != 'your_line_channel_access_token_here' else '未設定或為預設值'}")
print(f"LINE_CHANNEL_SECRET: {'已設定' if os.getenv('LINE_CHANNEL_SECRET') and os.getenv('LINE_CHANNEL_SECRET') != 'your_line_channel_secret_here' else '未設定或為預設值'}")
print(f"USER_ID: {'已設定' if os.getenv('USER_ID') and os.getenv('USER_ID') != 'your_user_id_here' else '未設定或為預設值'}")
print(f"SUPABASE_URL: {'已設定' if os.getenv('SUPABASE_URL') and 'your-project-id' not in os.getenv('SUPABASE_URL', '') else '未設定或為預設值'}")
print(f"SUPABASE_ANON_KEY: {'已設定' if os.getenv('SUPABASE_ANON_KEY') and os.getenv('SUPABASE_ANON_KEY') != 'your_supabase_anon_key_here' else '未設定或為預設值'}")
print(f"LOCAL_TEST_MODE: {os.getenv('LOCAL_TEST_MODE', 'false')}")

# 顯示部分 token 用於驗證
token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', '')
if token and token != 'your_line_channel_access_token_here':
    print(f"Token 前20字元: {token[:20]}...")
else:
    print("Token: 未設定或為預設值")

secret = os.getenv('LINE_CHANNEL_SECRET', '')
if secret and secret != 'your_line_channel_secret_here':
    print(f"Secret 前10字元: {secret[:10]}...")
else:
    print("Secret: 未設定或為預設值") 
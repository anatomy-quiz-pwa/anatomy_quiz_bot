#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解剖學測驗網站版本 - 支援LINE登入和遊戲數據同步
"""

import os
import logging
import secrets
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, render_template, session, redirect, url_for, send_from_directory
from supabase import create_client, Client
import json
from typing import Optional, Dict, List
import requests

# 嘗試載入環境變數
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.secret_key = os.getenv('FLASK_SECRET_KEY', secrets.token_hex(32))

# 設置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 環境變數
LINE_LOGIN_CHANNEL_ID = os.getenv('LINE_LOGIN_CHANNEL_ID')
LINE_LOGIN_CHANNEL_SECRET = os.getenv('LINE_LOGIN_CHANNEL_SECRET')
LINE_LOGIN_REDIRECT_URI = os.getenv('LINE_LOGIN_REDIRECT_URI', 'http://localhost:5001/auth/callback')
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# 如果環境變數未設置，使用預設值
if not LINE_LOGIN_CHANNEL_ID:
    LINE_LOGIN_CHANNEL_ID = "2004874394"  # 需要替換為您的LINE Login Channel ID
    logger.info("🔧 使用預設 LINE_LOGIN_CHANNEL_ID")

if not LINE_LOGIN_CHANNEL_SECRET:
    LINE_LOGIN_CHANNEL_SECRET = "your_line_login_channel_secret"  # 需要替換
    logger.info("🔧 使用預設 LINE_LOGIN_CHANNEL_SECRET")

if not SUPABASE_URL:
    SUPABASE_URL = "https://ciqlfqfgzqqgdrogedxg.supabase.co"
    logger.info("🔧 使用預設 SUPABASE_URL")

if not SUPABASE_KEY:
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA"
    logger.info("🔧 使用預設 SUPABASE_KEY")

# 創建 Supabase 客戶端
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    logger.info(f"✅ Supabase 連接成功: {SUPABASE_URL}")
except Exception as e:
    logger.error(f"❌ Supabase 連接失敗: {e}")
    supabase = None

# 等級稱號對應表
LEVEL_TITLES = {
    1: "新手解剖師",
    2: "初級解剖師", 3: "初級解剖師",
    4: "中級解剖師", 5: "中級解剖師", 6: "中級解剖師", 7: "中級解剖師",
    8: "高級解剖師", 9: "高級解剖師", 10: "高級解剖師", 11: "高級解剖師",
    12: "專家解剖師", 13: "專家解剖師",
    14: "終極解剖師"
}

def get_level_title(level: int) -> str:
    """獲取等級對應的稱號"""
    return LEVEL_TITLES.get(level, "未知等級")

def get_user_nickname(user_id: str) -> str:
    """從 users 表格獲取用戶暱稱"""
    try:
        if supabase is None:
            return f"用戶_{user_id[2:10] if user_id.startswith('U') else user_id}"
        
        response = supabase.table('users').select('game_nickname').eq('line_user_id', user_id).execute()
        
        if response.data and len(response.data) > 0:
            nickname = response.data[0].get('game_nickname')
            if nickname:
                return nickname
        
        return f"用戶_{user_id[2:10] if user_id.startswith('U') else user_id}"
        
    except Exception as e:
        logger.error(f"❌ 獲取用戶 {user_id} 暱稱失敗: {e}")
        return f"用戶_{user_id[2:10] if user_id.startswith('U') else user_id}"

def get_user_stats(user_id: str) -> Dict:
    """獲取用戶統計數據"""
    try:
        if supabase is None:
            return {
                'correct': 0,
                'total': 0,
                'level': 1,
                'score': 0
            }
        
        response = supabase.table('user_stats').select('*').eq('user_id', user_id).execute()
        
        if response.data and len(response.data) > 0:
            stats = response.data[0]
            return {
                'correct': stats.get('correct', 0),
                'total': stats.get('total', 0),
                'level': stats.get('level', 1),
                'score': stats.get('correct', 0) * 10
            }
        
        # 如果沒有數據，創建默認數據
        return {
            'correct': 0,
            'total': 0,
            'level': 1,
            'score': 0
        }
        
    except Exception as e:
        logger.error(f"❌ 獲取用戶 {user_id} 統計數據失敗: {e}")
        return {
            'correct': 0,
            'total': 0,
            'level': 1,
            'score': 0
        }

def get_quiz_question(user_level: int) -> Optional[Dict]:
    """獲取指定等級的隨機題目"""
    try:
        if supabase is None:
            return get_demo_question(user_level)
        
        # 獲取該等級的題目
        response = supabase.table('questions').select('*').eq('level', user_level).execute()
        
        if response.data and len(response.data) > 0:
            import random
            question = random.choice(response.data)
            return {
                'id': question['id'],
                'question': question['question'],
                'options': question['options'],
                'correct_answer': question['correct_answer'],
                'explanation': question.get('explanation', ''),
                'level': question['level'],
                'category': question['category']
            }
        
        # 如果沒有題目，返回演示題目
        return get_demo_question(user_level)
        
    except Exception as e:
        logger.error(f"❌ 獲取等級 {user_level} 題目失敗: {e}")
        return get_demo_question(user_level)

def get_demo_question(user_level: int) -> Dict:
    """獲取演示題目（當questions表不存在時使用）"""
    demo_questions = {
        1: {
            'id': 1,
            'question': '心臟的主要功能是什麼？',
            'options': ['輸送血液', '過濾血液', '儲存血液', '製造血液'],
            'correct_answer': 0,
            'explanation': '心臟是循環系統的核心，主要功能是泵血輸送到全身。',
            'level': 1,
            'category': '循環系統'
        },
        2: {
            'id': 2,
            'question': '人體最大的器官是什麼？',
            'options': ['心臟', '肝臟', '皮膚', '肺'],
            'correct_answer': 2,
            'explanation': '皮膚是人體最大的器官，覆蓋整個身體表面。',
            'level': 2,
            'category': '器官系統'
        },
        3: {
            'id': 3,
            'question': '心臟有幾個腔室？',
            'options': ['2個', '3個', '4個', '5個'],
            'correct_answer': 2,
            'explanation': '心臟有4個腔室：左心房、左心室、右心房、右心室。',
            'level': 3,
            'category': '循環系統'
        }
    }
    
    # 根據等級返回對應的演示題目，如果沒有則返回等級1的題目
    level = min(user_level, 3)
    return demo_questions.get(level, demo_questions[1])

def update_user_stats(user_id: str, is_correct: bool) -> bool:
    """更新用戶統計數據"""
    try:
        if supabase is None:
            return False
        
        # 獲取當前統計
        current_stats = get_user_stats(user_id)
        
        # 更新統計
        new_correct = current_stats['correct'] + (1 if is_correct else 0)
        new_total = current_stats['total'] + 1
        new_level = min(14, current_stats['level'] + (1 if is_correct and new_correct % 5 == 0 else 0))
        
        # 更新到數據庫
        supabase.table('user_stats').upsert({
            'user_id': user_id,
            'correct': new_correct,
            'total': new_total,
            'level': new_level
        }).execute()
        
        logger.info(f"✅ 更新用戶 {user_id} 統計: 正確{new_correct}, 總計{new_total}, 等級{new_level}")
        return True
        
    except Exception as e:
        logger.error(f"❌ 更新用戶 {user_id} 統計失敗: {e}")
        return False

def get_leaderboard_data() -> List[Dict]:
    """獲取排行榜數據"""
    try:
        if supabase is None:
            return []
        
        response = supabase.table('user_stats').select('*').order('correct', desc=True).limit(10).execute()
        
        if not response.data:
            return []
        
        leaderboard = []
        for i, item in enumerate(response.data):
            user_id = item.get('user_id', '')
            nickname = get_user_nickname(user_id)
            
            leaderboard.append({
                'rank': i + 1,
                'name': nickname,
                'score': item.get('correct', 0) * 10,
                'correct': item.get('correct', 0),
                'total': item.get('total', 0),
                'level': item.get('level', 1)
            })
        
        return leaderboard
        
    except Exception as e:
        logger.error(f"❌ 獲取排行榜數據失敗: {e}")
        return []

@app.route('/')
def index():
    """首頁 - 使用public/index.html"""
    public_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'public')
    return send_from_directory(public_dir, 'index.html')

@app.route('/login')
def login():
    """LINE登入"""
    # 生成隨機state參數防止CSRF攻擊
    state = secrets.token_urlsafe(32)
    session['oauth_state'] = state
    
    # LINE Login授權URL
    auth_url = (
        f"https://access.line.me/oauth2/v2.1/authorize?"
        f"response_type=code&"
        f"client_id={LINE_LOGIN_CHANNEL_ID}&"
        f"redirect_uri={LINE_LOGIN_REDIRECT_URI}&"
        f"state={state}&"
        f"scope=profile%20openid"
    )
    
    return redirect(auth_url)

@app.route('/auth/callback')
def auth_callback():
    """LINE登入回調"""
    try:
        code = request.args.get('code')
        state = request.args.get('state')
        
        # 驗證state參數
        if state != session.get('oauth_state'):
            logger.error("❌ 無效的state參數")
            return redirect(url_for('index'))
        
        if not code:
            logger.error("❌ 缺少授權碼")
            return redirect(url_for('index'))
        
        # 交換access token
        token_url = "https://api.line.me/oauth2/v2.1/token"
        token_data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': LINE_LOGIN_REDIRECT_URI,
            'client_id': LINE_LOGIN_CHANNEL_ID,
            'client_secret': LINE_LOGIN_CHANNEL_SECRET
        }
        
        response = requests.post(token_url, data=token_data)
        if response.status_code != 200:
            logger.error(f"❌ 獲取access token失敗: {response.text}")
            return redirect(url_for('index'))
        
        token_info = response.json()
        access_token = token_info.get('access_token')
        
        # 獲取用戶資料
        profile_url = "https://api.line.me/v2/profile"
        headers = {'Authorization': f'Bearer {access_token}'}
        
        profile_response = requests.get(profile_url, headers=headers)
        if profile_response.status_code != 200:
            logger.error(f"❌ 獲取用戶資料失敗: {profile_response.text}")
            return redirect(url_for('index'))
        
        user_info = profile_response.json()
        user_id = user_info.get('userId')
        display_name = user_info.get('displayName', '未知用戶')
        
        # 儲存用戶資料到session
        session['user_id'] = user_id
        session['display_name'] = display_name
        session['access_token'] = access_token
        
        # 確保用戶在數據庫中存在
        try:
            if supabase:
                supabase.table('users').upsert({
                    'line_user_id': user_id,
                    'display_name': display_name,
                    'game_nickname': get_user_nickname(user_id)
                }).execute()
        except Exception as e:
            logger.error(f"❌ 更新用戶資料失敗: {e}")
        
        logger.info(f"✅ 用戶 {user_id} ({display_name}) 登入成功")
        return redirect(url_for('game'))
        
    except Exception as e:
        logger.error(f"❌ LINE登入失敗: {e}")
        return redirect(url_for('index'))

@app.route('/game')
def game():
    """遊戲主頁"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    user_stats = get_user_stats(user_id)
    nickname = get_user_nickname(user_id)
    
    return render_template('game.html', 
                         user_stats=user_stats, 
                         nickname=nickname,
                         level_title=get_level_title(user_stats['level']))

@app.route('/api/quiz/start', methods=['POST'])
def start_quiz():
    """開始測驗"""
    if 'user_id' not in session:
        return jsonify({'error': '未登入'}), 401
    
    user_id = session['user_id']
    user_stats = get_user_stats(user_id)
    
    # 獲取題目
    question = get_quiz_question(user_stats['level'])
    
    if not question:
        return jsonify({'error': '沒有可用題目'}), 404
    
    # 儲存當前題目到session
    session['current_question'] = question
    
    return jsonify({
        'success': True,
        'question': question
    })

@app.route('/api/quiz/answer', methods=['POST'])
def submit_answer():
    """提交答案"""
    if 'user_id' not in session:
        return jsonify({'error': '未登入'}), 401
    
    if 'current_question' not in session:
        return jsonify({'error': '沒有當前題目'}), 400
    
    user_id = session['user_id']
    current_question = session['current_question']
    
    data = request.get_json()
    selected_answer = data.get('answer')
    
    if selected_answer is None:
        return jsonify({'error': '缺少答案'}), 400
    
    # 檢查答案
    is_correct = int(selected_answer) == current_question['correct_answer']
    
    # 更新統計
    update_user_stats(user_id, is_correct)
    
    # 清除當前題目
    session.pop('current_question', None)
    
    return jsonify({
        'success': True,
        'is_correct': is_correct,
        'correct_answer': current_question['correct_answer'],
        'explanation': current_question['explanation']
    })

@app.route('/api/leaderboard')
def get_leaderboard():
    """獲取排行榜"""
    leaderboard = get_leaderboard_data()
    
    if 'user_id' in session:
        user_id = session['user_id']
        user_stats = get_user_stats(user_id)
        
        # 找到用戶排名
        user_rank = 0
        for i, entry in enumerate(leaderboard):
            if entry['name'] == get_user_nickname(user_id):
                user_rank = i + 1
                break
        
        if user_rank == 0:
            # 用戶不在前10名，需要計算總排名
            try:
                if supabase:
                    response = supabase.table('user_stats').select('*').order('correct', desc=True).execute()
                    if response.data:
                        for i, item in enumerate(response.data):
                            if item.get('user_id') == user_id:
                                user_rank = i + 1
                                break
            except Exception as e:
                logger.error(f"❌ 計算用戶排名失敗: {e}")
        
        return jsonify({
            'leaderboard': leaderboard,
            'user_rank': user_rank,
            'user_stats': user_stats
        })
    
    return jsonify({
        'leaderboard': leaderboard
    })

@app.route('/demo')
def demo():
    """演示模式 - 無需登入即可體驗遊戲"""
    return render_template('demo.html')

@app.route('/api/demo/quiz/start', methods=['POST'])
def start_demo_quiz():
    """開始演示測驗"""
    # 獲取演示題目
    question = get_demo_question(1)  # 使用等級1的演示題目
    
    if not question:
        return jsonify({'error': '沒有可用題目'}), 404
    
    # 儲存當前題目到session
    session['current_demo_question'] = question
    
    return jsonify({
        'success': True,
        'question': question
    })

@app.route('/api/demo/quiz/answer', methods=['POST'])
def submit_demo_answer():
    """提交演示答案"""
    if 'current_demo_question' not in session:
        return jsonify({'error': '沒有當前題目'}), 400
    
    current_question = session['current_demo_question']
    
    data = request.get_json()
    selected_answer = data.get('answer')
    
    if selected_answer is None:
        return jsonify({'error': '缺少答案'}), 400
    
    # 檢查答案
    is_correct = int(selected_answer) == current_question['correct_answer']
    
    # 清除當前題目
    session.pop('current_demo_question', None)
    
    return jsonify({
        'success': True,
        'is_correct': is_correct,
        'correct_answer': current_question['correct_answer'],
        'explanation': current_question['explanation']
    })

@app.route('/logout')
def logout():
    """登出"""
    session.clear()
    return redirect(url_for('index'))

@app.route('/static/<path:filename>')
def static_files(filename):
    """服務靜態檔案"""
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    return send_from_directory(static_dir, filename)

@app.route('/public/<path:filename>')
def public_files(filename):
    """服務public資料夾檔案"""
    public_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'public')
    return send_from_directory(public_dir, filename)

# Vercel 需要的入口點
app = app

if __name__ == '__main__':
    logger.info("🚀 啟動解剖學測驗網站")
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)

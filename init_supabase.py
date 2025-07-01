#!/usr/bin/env python3
"""
Supabase 資料庫初始化腳本
用於建立必要的表格和插入範例資料
"""

import os
from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_ANON_KEY

def init_supabase():
    """初始化 Supabase 資料庫"""
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        print("錯誤：請設定 SUPABASE_URL 和 SUPABASE_ANON_KEY 環境變數")
        return
    
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    
    print("開始初始化 Supabase 資料庫...")
    
    # 範例題目資料
    sample_questions = [
        {
            'category': '解剖學基礎',
            'question': '人體最大的器官是什麼？',
            'option1': '心臟',
            'option2': '大腦', 
            'option3': '皮膚',
            'option4': '肝臟',
            'correct_answer': 3,
            'explanation': '皮膚是人體最大的器官，佔體重的約16%。'
        },
        {
            'category': '骨骼系統',
            'question': '人體有多少塊骨頭？',
            'option1': '206塊',
            'option2': '186塊',
            'option3': '226塊', 
            'option4': '196塊',
            'correct_answer': 1,
            'explanation': '成人人體有206塊骨頭。'
        },
        {
            'category': '心血管系統',
            'question': '心臟位於胸腔的哪個位置？',
            'option1': '左側',
            'option2': '右側',
            'option3': '中央偏左',
            'option4': '中央偏右',
            'correct_answer': 3,
            'explanation': '心臟位於胸腔中央偏左的位置。'
        },
        {
            'category': '消化系統',
            'question': '人體最大的內臟器官是什麼？',
            'option1': '心臟',
            'option2': '肺臟',
            'option3': '肝臟',
            'option4': '腎臟',
            'correct_answer': 3,
            'explanation': '肝臟是人體最大的內臟器官。'
        },
        {
            'category': '神經系統',
            'question': '人體的神經系統分為哪兩大部分？',
            'option1': '中樞神經系統和周圍神經系統',
            'option2': '感覺神經系統和運動神經系統',
            'option3': '自主神經系統和體神經系統',
            'option4': '交感神經系統和副交感神經系統',
            'correct_answer': 1,
            'explanation': '人體神經系統分為中樞神經系統（腦和脊髓）和周圍神經系統。'
        }
    ]
    
    try:
        # 插入範例題目
        print("插入範例題目...")
        for question in sample_questions:
            try:
                supabase.table('questions').insert(question).execute()
                print(f"已插入題目：{question['question'][:30]}...")
            except Exception as e:
                print(f"插入題目失敗：{str(e)}")
        
        print("Supabase 資料庫初始化完成！")
        print("\n注意事項：")
        print("1. 請確保在 Supabase 中已建立以下表格：")
        print("   - questions (題目表)")
        print("   - user_stats (用戶統計表)")
        print("2. 表格結構請參考下方的 SQL 語法")
        
    except Exception as e:
        print(f"初始化失敗：{str(e)}")

def print_table_schema():
    """印出建議的表格結構"""
    print("\n" + "="*50)
    print("建議的 Supabase 表格結構")
    print("="*50)
    
    print("\n1. questions 表格 (題目表)：")
    print("""
CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    category TEXT DEFAULT '未分類',
    question TEXT NOT NULL,
    option1 TEXT NOT NULL,
    option2 TEXT NOT NULL,
    option3 TEXT NOT NULL,
    option4 TEXT NOT NULL,
    correct_answer INTEGER NOT NULL CHECK (correct_answer >= 1 AND correct_answer <= 4),
    explanation TEXT DEFAULT '',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
    """)
    
    print("\n2. user_stats 表格 (用戶統計表)：")
    print("""
CREATE TABLE user_stats (
    id SERIAL PRIMARY KEY,
    user_id TEXT UNIQUE NOT NULL,
    correct INTEGER DEFAULT 0,
    wrong INTEGER DEFAULT 0,
    correct_qids TEXT DEFAULT '', -- 逗號分隔的正確題目ID
    last_update DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
    """)
    
    print("\n3. 建立索引：")
    print("""
CREATE INDEX idx_questions_category ON questions(category);
CREATE INDEX idx_user_stats_user_id ON user_stats(user_id);
CREATE INDEX idx_user_stats_last_update ON user_stats(last_update);
    """)

if __name__ == "__main__":
    print_table_schema()
    print("\n" + "="*50)
    response = input("是否要執行初始化？(y/n): ")
    if response.lower() == 'y':
        init_supabase()
    else:
        print("取消初始化。") 
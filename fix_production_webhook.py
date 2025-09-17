#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修復生產環境 webhook 問題
"""

import os
import sys
import json

def check_production_code_issues():
    """檢查生產環境代碼可能的問題"""
    print("🔍 檢查生產環境代碼可能的問題...")
    
    production_file = "/Users/baobaoc/Dev/anatomy_quiz_bot/app_supabase.py"
    
    if not os.path.exists(production_file):
        print(f"❌ 生產環境檔案不存在: {production_file}")
        return False
    
    try:
        with open(production_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 檢查可能的問題
        issues = []
        
        # 1. 檢查是否有錯誤處理
        if 'try:' not in content or 'except' not in content:
            issues.append("缺少錯誤處理")
        
        # 2. 檢查是否有必要的導入
        required_imports = ['flask', 'requests', 'json', 'os', 'logging', 'supabase']
        for imp in required_imports:
            if f'import {imp}' not in content and f'from {imp}' not in content:
                issues.append(f"缺少導入: {imp}")
        
        # 3. 檢查 webhook 函數
        if 'def webhook():' not in content:
            issues.append("缺少 webhook 函數")
        
        # 4. 檢查環境變數處理
        if 'os.getenv' not in content:
            issues.append("缺少環境變數處理")
        
        # 5. 檢查 Supabase 連接
        if 'create_client' not in content:
            issues.append("缺少 Supabase 客戶端創建")
        
        if issues:
            print("❌ 發現以下問題:")
            for issue in issues:
                print(f"  - {issue}")
            return False
        else:
            print("✅ 代碼結構檢查通過")
            return True
            
    except Exception as e:
        print(f"❌ 檢查代碼時發生錯誤: {e}")
        return False

def create_minimal_webhook_test():
    """創建最小化的 webhook 測試"""
    print("\n🔍 創建最小化的 webhook 測試...")
    
    minimal_code = '''
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
'''
    
    # 保存最小化測試代碼
    with open('minimal_webhook_test.py', 'w', encoding='utf-8') as f:
        f.write(minimal_code)
    
    print("✅ 最小化 webhook 測試代碼已創建: minimal_webhook_test.py")
    return True

def create_environment_check():
    """創建環境檢查腳本"""
    print("\n🔍 創建環境檢查腳本...")
    
    env_check_code = '''
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
環境檢查腳本
"""

import os
import sys

def check_environment():
    """檢查環境變數"""
    print("🔍 檢查環境變數...")
    
    required_vars = [
        'SUPABASE_URL',
        'SUPABASE_ANON_KEY',
        'LINE_CHANNEL_ACCESS_TOKEN',
        'LINE_CHANNEL_SECRET'
    ]
    
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # 只顯示前20個字符
            display_value = value[:20] + "..." if len(value) > 20 else value
            print(f"✅ {var}: {display_value}")
        else:
            print(f"❌ {var}: 未設置")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\\n⚠️ 缺少環境變數: {', '.join(missing_vars)}")
        return False
    else:
        print("\\n✅ 所有必要的環境變數都已設置")
        return True

def check_imports():
    """檢查必要的導入"""
    print("\\n🔍 檢查必要的導入...")
    
    required_modules = [
        'flask',
        'requests', 
        'json',
        'os',
        'logging',
        'supabase'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}: 可用")
        except ImportError:
            print(f"❌ {module}: 不可用")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\\n⚠️ 缺少模組: {', '.join(missing_modules)}")
        return False
    else:
        print("\\n✅ 所有必要的模組都可用")
        return True

def main():
    """主函數"""
    print("🚀 開始環境檢查")
    print("=" * 50)
    
    env_ok = check_environment()
    imports_ok = check_imports()
    
    print("\\n" + "=" * 50)
    print("🏁 環境檢查完成")
    
    if env_ok and imports_ok:
        print("✅ 環境檢查通過")
        return True
    else:
        print("❌ 環境檢查失敗")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
'''
    
    # 保存環境檢查腳本
    with open('environment_check.py', 'w', encoding='utf-8') as f:
        f.write(env_check_code)
    
    print("✅ 環境檢查腳本已創建: environment_check.py")
    return True

def create_deployment_guide():
    """創建部署指南"""
    print("\n🔍 創建部署指南...")
    
    guide = '''
# 生產環境排行榜問題修復指南

## 問題診斷結果
- ✅ 本地功能正常
- ✅ 排行榜 Flex Message 創建正常
- ❌ 生產環境 webhook 返回 500 錯誤

## 可能的原因
1. 環境變數配置問題
2. 依賴項缺失
3. 代碼錯誤
4. 數據庫連接問題
5. 應用程式崩潰

## 修復步驟

### 1. 檢查 Render 部署日誌
```bash
# 在 Render Dashboard 中查看部署日誌
# 尋找錯誤訊息和異常堆疊
```

### 2. 檢查環境變數
確保以下環境變數在 Render 中正確設置：
- SUPABASE_URL
- SUPABASE_ANON_KEY
- LINE_CHANNEL_ACCESS_TOKEN
- LINE_CHANNEL_SECRET

### 3. 檢查依賴項
確保 requirements.txt 包含所有必要的依賴項：
```
flask
requests
supabase
line-bot-sdk
```

### 4. 測試最小化版本
使用 minimal_webhook_test.py 進行測試，確認基本功能正常。

### 5. 逐步添加功能
從最小化版本開始，逐步添加功能直到找到問題所在。

## 建議的修復方案

### 方案 1: 重新部署
1. 檢查代碼是否有語法錯誤
2. 確保所有依賴項都在 requirements.txt 中
3. 重新部署到 Render

### 方案 2: 使用最小化版本
1. 使用 minimal_webhook_test.py 替換當前版本
2. 確認基本 webhook 功能正常
3. 逐步添加排行榜功能

### 方案 3: 檢查數據庫連接
1. 確認 Supabase 連接正常
2. 檢查數據庫權限
3. 測試數據庫查詢

## 測試命令
```bash
# 測試環境
python environment_check.py

# 測試最小化 webhook
python minimal_webhook_test.py

# 測試生產環境
curl -X POST https://anatomy-quiz-bot.onrender.com/webhook \\
  -H "Content-Type: application/json" \\
  -d '{"events":[{"type":"message","source":{"userId":"test"},"message":{"type":"text","text":"排行榜"}}]}'
```
'''
    
    # 保存部署指南
    with open('DEPLOYMENT_FIX_GUIDE.md', 'w', encoding='utf-8') as f:
        f.write(guide)
    
    print("✅ 部署指南已創建: DEPLOYMENT_FIX_GUIDE.md")
    return True

def main():
    """主函數"""
    print("🚀 開始修復生產環境 webhook 問題")
    print("=" * 60)
    
    # 1. 檢查生產環境代碼
    code_ok = check_production_code_issues()
    
    # 2. 創建最小化測試
    create_minimal_webhook_test()
    
    # 3. 創建環境檢查腳本
    create_environment_check()
    
    # 4. 創建部署指南
    create_deployment_guide()
    
    print("\n" + "=" * 60)
    print("🏁 修復準備完成")
    
    print("\n📋 已創建的文件:")
    print("  - minimal_webhook_test.py (最小化 webhook 測試)")
    print("  - environment_check.py (環境檢查腳本)")
    print("  - DEPLOYMENT_FIX_GUIDE.md (部署修復指南)")
    
    print("\n💡 建議的修復步驟:")
    print("  1. 檢查 Render 部署日誌")
    print("  2. 確認環境變數設置")
    print("  3. 使用最小化版本測試")
    print("  4. 逐步添加功能")
    
    if not code_ok:
        print("\n⚠️ 生產環境代碼可能有問題，建議重新檢查")

if __name__ == "__main__":
    main()

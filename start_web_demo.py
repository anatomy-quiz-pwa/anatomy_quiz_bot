#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
啟動解剖學測驗網站演示版本
"""

import os
import sys
import webbrowser
import time
from threading import Timer

def open_browser():
    """延遲3秒後自動打開瀏覽器"""
    time.sleep(3)
    webbrowser.open('http://localhost:8080')

if __name__ == '__main__':
    print("🚀 啟動解剖學測驗網站演示版本...")
    print("=" * 50)
    
    # 檢查是否有其他進程在運行
    try:
        import psutil
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            if proc.info['cmdline'] and 'web_app_demo.py' in ' '.join(proc.info['cmdline']):
                print(f"⚠️  發現現有進程 {proc.info['pid']}，正在終止...")
                proc.terminate()
                time.sleep(2)
    except ImportError:
        print("ℹ️  建議安裝 psutil 以更好地管理進程")
    
    print("✅ 清理完成，啟動新實例...")
    
    # 自動打開瀏覽器
    Timer(3.0, open_browser).start()
    
    print("🌐 網站將在 http://localhost:8080 啟動")
    print("📱 瀏覽器將自動打開")
    print("🛑 按 Ctrl+C 停止服務器")
    print("=" * 50)
    
    # 導入並運行應用
    from web_app_demo import app
    
    try:
        app.run(
            host='0.0.0.0',  # 允許外部訪問
            port=8080,
            debug=True,
            use_reloader=False  # 避免重複啟動
        )
    except KeyboardInterrupt:
        print("\n👋 網站已停止")
    except Exception as e:
        print(f"❌ 啟動失敗: {e}")
        print("💡 請檢查端口8080是否被其他程序佔用")

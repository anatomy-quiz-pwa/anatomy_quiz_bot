#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
部署配置驗證腳本
檢查所有必要的文件和配置是否正確
"""

import os
import sys
import subprocess
from pathlib import Path

def check_file_exists(file_path):
    """檢查文件是否存在"""
    if Path(file_path).exists():
        print(f"✅ {file_path} 存在")
        return True
    else:
        print(f"❌ {file_path} 不存在")
        return False

def check_requirements():
    """檢查 requirements.txt 內容"""
    print("\n📦 檢查 requirements.txt...")
    if not check_file_exists("requirements.txt"):
        return False
    
    with open("requirements.txt", "r") as f:
        content = f.read()
        required_packages = [
            "flask",
            "requests", 
            "supabase",
            "line-bot-sdk",
            "python-dotenv",
            "gunicorn",
            "PyJWT"
        ]
        
        for package in required_packages:
            if package in content:
                print(f"✅ {package} 在 requirements.txt 中")
            else:
                print(f"❌ {package} 不在 requirements.txt 中")
                return False
    
    return True

def check_app_files():
    """檢查應用文件"""
    print("\n🚀 檢查應用文件...")
    app_files = ["app_supabase.py", "secure_token_manager.py", "secure_session_manager.py"]
    
    all_exist = True
    for app_file in app_files:
        if not check_file_exists(app_file):
            all_exist = False
    
    return all_exist

def check_config_files():
    """檢查配置文件"""
    print("\n⚙️ 檢查配置文件...")
    config_files = ["Procfile", "render.yaml"]
    
    all_exist = True
    for config_file in config_files:
        if not check_file_exists(config_file):
            all_exist = False
    
    return all_exist

def check_procfile_content():
    """檢查 Procfile 內容"""
    print("\n📋 檢查 Procfile 內容...")
    if not check_file_exists("Procfile"):
        return False
    
    with open("Procfile", "r") as f:
        content = f.read().strip()
        if "app_supabase:app" in content:
            print("✅ Procfile 指向正確的應用文件")
            print(f"📄 Procfile 內容: {content}")
            return True
        else:
            print("❌ Procfile 沒有指向 app_supabase:app")
            print(f"📄 Procfile 內容: {content}")
            return False

def check_render_yaml():
    """檢查 render.yaml 內容"""
    print("\n🔧 檢查 render.yaml 內容...")
    if not check_file_exists("render.yaml"):
        return False
    
    with open("render.yaml", "r") as f:
        content = f.read()
        
        checks = [
            ("app_supabase:app", "startCommand 指向正確的應用文件"),
            ("/__health", "健康檢查路徑配置"),
            ("SUPABASE_KEY", "Supabase 環境變數"),
            ("LINE_CHANNEL_ACCESS_TOKEN", "LINE Bot 環境變數"),
            ("LINE_CHANNEL_SECRET", "LINE Bot 環境變數")
        ]
        
        all_good = True
        for check_text, description in checks:
            if check_text in content:
                print(f"✅ {description}")
            else:
                print(f"❌ {description}")
                all_good = False
        
        return all_good

def test_imports():
    """測試 Python 導入"""
    print("\n🐍 測試 Python 導入...")
    try:
        import flask
        print("✅ Flask 導入成功")
    except ImportError as e:
        print(f"❌ Flask 導入失敗: {e}")
        return False
    
    try:
        import supabase
        print("✅ Supabase 導入成功")
    except ImportError as e:
        print(f"❌ Supabase 導入失敗: {e}")
        return False
    
    try:
        from linebot import LineBotApi
        print("✅ LINE Bot SDK 導入成功")
    except ImportError as e:
        print(f"❌ LINE Bot SDK 導入失敗: {e}")
        return False
    
    try:
        import jwt
        print("✅ PyJWT 導入成功")
    except ImportError as e:
        print(f"❌ PyJWT 導入失敗: {e}")
        return False
    
    return True

def main():
    """主函數"""
    print("🔍 開始部署配置驗證...")
    
    checks = [
        ("requirements.txt", check_requirements),
        ("應用文件", check_app_files),
        ("配置文件", check_config_files),
        ("Procfile 內容", check_procfile_content),
        ("render.yaml 內容", check_render_yaml),
        ("Python 導入", test_imports)
    ]
    
    all_passed = True
    for check_name, check_func in checks:
        print(f"\n{'='*50}")
        print(f"檢查: {check_name}")
        print('='*50)
        
        if not check_func():
            all_passed = False
            print(f"❌ {check_name} 檢查失敗")
        else:
            print(f"✅ {check_name} 檢查通過")
    
    print(f"\n{'='*50}")
    if all_passed:
        print("🎉 所有檢查都通過！部署配置正確。")
        print("\n📋 部署步驟:")
        print("1. 確保所有環境變數在 Render 中正確設置")
        print("2. 推送代碼到 GitHub")
        print("3. 在 Render 中觸發重新部署")
        return 0
    else:
        print("❌ 部分檢查失敗，請修復問題後重新運行。")
        return 1

if __name__ == "__main__":
    sys.exit(main())

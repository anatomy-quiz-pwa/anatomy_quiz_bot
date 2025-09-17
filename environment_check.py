
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
        print(f"\n⚠️ 缺少環境變數: {', '.join(missing_vars)}")
        return False
    else:
        print("\n✅ 所有必要的環境變數都已設置")
        return True

def check_imports():
    """檢查必要的導入"""
    print("\n🔍 檢查必要的導入...")
    
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
        print(f"\n⚠️ 缺少模組: {', '.join(missing_modules)}")
        return False
    else:
        print("\n✅ 所有必要的模組都可用")
        return True

def main():
    """主函數"""
    print("🚀 開始環境檢查")
    print("=" * 50)
    
    env_ok = check_environment()
    imports_ok = check_imports()
    
    print("\n" + "=" * 50)
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

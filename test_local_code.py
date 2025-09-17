#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試本地代碼
"""

def test_local_code():
    """測試本地代碼"""
    print("🔍 測試本地代碼...")
    
    try:
        # 導入本地代碼
        import sys
        sys.path.append('/Users/baobaoc/Dev/anatomy_quiz_bot')
        from app_supabase import app
        
        print("✅ 本地代碼可以正常導入")
        
        # 測試根路徑
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        response = client.get("/")
        print(f"📤 本地根路徑響應: {response.json()}")
        
        # 檢查是否包含版本標識符
        if "FORCE_FIX_V8_2025_09_17" in str(response.json()):
            print("✅ 本地代碼包含正確的版本標識符")
            return True
        else:
            print("❌ 本地代碼不包含正確的版本標識符")
            return False
            
    except Exception as e:
        print(f"❌ 本地代碼測試失敗: {e}")
        return False

def main():
    """主函數"""
    print("🚀 測試本地代碼")
    print("=" * 50)
    
    # 測試本地代碼
    local_ok = test_local_code()
    
    if local_ok:
        print("\n✅ 本地代碼正常，問題在於 Render 部署")
        print("💡 建議檢查 Render 配置或使用替代平台")
    else:
        print("\n❌ 本地代碼有問題，需要修復代碼")

if __name__ == "__main__":
    main()

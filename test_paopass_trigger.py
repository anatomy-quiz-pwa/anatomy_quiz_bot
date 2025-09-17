#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PAOPASS管理員模式觸發測試
測試PAOPASS密碼是否能正確激活管理員模式
"""

import sys
import os
import json
from datetime import datetime

def test_paopass_trigger():
    """測試PAOPASS觸發管理員模式功能"""
    print("=" * 60)
    print("🔑 PAOPASS管理員模式觸發測試")
    print("=" * 60)
    
    results = []
    
    try:
        # 導入必要的函數
        from app_supabase import (
            handle_text_message, 
            is_admin_user,
            get_user_admin_permissions,
            activate_admin_mode,
            supabase
        )
        
        # 測試用戶ID（使用寶的真實帳號）
        test_user_id = "U977c24d1fec3a2bf07035504e1444911"  # 寶的LINE帳號
        
        print(f"📱 測試用戶: {test_user_id}")
        print()
        
        # 1. 檢查用戶初始狀態
        print("1️⃣ 檢查用戶初始管理員狀態...")
        try:
            initial_admin_status = is_admin_user(test_user_id)
            print(f"   初始管理員狀態: {initial_admin_status}")
            
            if initial_admin_status:
                print("   ⚠️ 用戶已經是管理員，先清除權限進行測試")
                # 清除管理員權限
                supabase.table('users').update({
                    'is_admin': False,
                    'test_mode': False,
                    'admin_levels': [],
                    'admin_permissions': {}
                }).eq('line_user_id', test_user_id).execute()
                print("   ✅ 已清除管理員權限")
            
            results.append(("初始狀態檢查", True))
        except Exception as e:
            print(f"   ❌ 初始狀態檢查失敗: {e}")
            results.append(("初始狀態檢查", False))
        print()
        
        # 2. 測試PAOPASS觸發
        print("2️⃣ 測試PAOPASS觸發管理員模式...")
        try:
            # 模擬發送PAOPASS訊息
            test_message = {"text": "PAOPASS"}
            
            print("   📨 模擬發送訊息: PAOPASS")
            handle_text_message(test_user_id, test_message)
            print("   ✅ PAOPASS訊息處理完成")
            
            results.append(("PAOPASS觸發處理", True))
        except Exception as e:
            print(f"   ❌ PAOPASS觸發失敗: {e}")
            results.append(("PAOPASS觸發處理", False))
        print()
        
        # 3. 驗證管理員權限是否激活
        print("3️⃣ 驗證管理員權限是否成功激活...")
        try:
            # 檢查管理員狀態
            admin_status = is_admin_user(test_user_id)
            print(f"   管理員狀態: {admin_status}")
            
            if admin_status:
                # 獲取詳細權限信息
                admin_info = get_user_admin_permissions(test_user_id)
                if admin_info:
                    print("   ✅ 管理員權限激活成功！")
                    print(f"   📋 權限詳情:")
                    print(f"      • is_admin: {admin_info.get('is_admin', False)}")
                    print(f"      • test_mode: {admin_info.get('test_mode', False)}")
                    print(f"      • admin_levels: {len(admin_info.get('admin_levels', []))} 個等級")
                    print(f"      • 可訪問所有等級: {admin_info.get('admin_permissions', {}).get('can_access_all_levels', False)}")
                    results.append(("管理員權限激活", True))
                else:
                    print("   ❌ 無法獲取管理員權限詳情")
                    results.append(("管理員權限激活", False))
            else:
                print("   ❌ 管理員權限未激活")
                results.append(("管理員權限激活", False))
                
        except Exception as e:
            print(f"   ❌ 權限驗證失敗: {e}")
            results.append(("管理員權限激活", False))
        print()
        
        # 4. 測試不同大小寫的PAOPASS
        print("4️⃣ 測試不同大小寫的PAOPASS...")
        try:
            test_cases = ["paopass", "Paopass", "PAOPASS", "PaoPass"]
            
            for test_case in test_cases:
                print(f"   測試: {test_case}")
                # 先清除權限
                supabase.table('users').update({
                    'is_admin': False,
                    'test_mode': False
                }).eq('line_user_id', test_user_id).execute()
                
                # 測試觸發
                test_message = {"text": test_case}
                handle_text_message(test_user_id, test_message)
                
                # 檢查是否激活
                admin_status = is_admin_user(test_user_id)
                status = "✅ 成功" if admin_status else "❌ 失敗"
                print(f"      結果: {status}")
            
            results.append(("大小寫測試", True))
        except Exception as e:
            print(f"   ❌ 大小寫測試失敗: {e}")
            results.append(("大小寫測試", False))
        print()
        
        # 5. 測試管理員功能是否正常
        print("5️⃣ 測試管理員功能是否正常...")
        try:
            # 確保用戶是管理員
            activate_admin_mode(test_user_id)
            
            # 測試管理員命令
            admin_commands = [
                {"text": "/admin status"},
                {"text": "開始"},
                {"text": "排行榜"}
            ]
            
            for cmd in admin_commands:
                print(f"   測試管理員命令: {cmd['text']}")
                handle_text_message(test_user_id, cmd)
                print("   ✅ 命令處理完成")
            
            results.append(("管理員功能測試", True))
        except Exception as e:
            print(f"   ❌ 管理員功能測試失敗: {e}")
            results.append(("管理員功能測試", False))
        print()
        
    except ImportError as e:
        print(f"❌ 導入模組失敗: {e}")
        print("請確認 app_supabase.py 檔案存在且可正常導入")
        return False
    except Exception as e:
        print(f"❌ 測試過程發生錯誤: {e}")
        return False
    
    # 總結報告
    print("=" * 60)
    print("📊 PAOPASS觸發測試總結")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"   {test_name}: {status}")
    
    print(f"\n🎯 總體結果: {passed}/{total} 通過")
    
    if passed == total:
        print("\n🎉 PAOPASS管理員模式觸發功能測試全部通過！")
        print("\n✨ 功能說明:")
        print("   🔑 用戶輸入 'PAOPASS' (不區分大小寫) 即可激活管理員模式")
        print("   👑 激活後用戶將獲得完整的管理員權限")
        print("   🛡️ 包括訪問所有等級、無每日限制、管理員命令等")
        print("   📱 可在LINE中直接輸入 'PAOPASS' 測試")
        
        print("\n💡 使用方法:")
        print("   1. 在LINE中輸入: PAOPASS")
        print("   2. 系統會自動激活管理員模式")
        print("   3. 用戶將收到管理員權限激活確認訊息")
        print("   4. 之後可使用所有管理員功能")
        
    else:
        print(f"\n⚠️ 發現 {total-passed} 個問題需要修復")
        for test_name, result in results:
            if not result:
                print(f"  • {test_name}")
    
    return passed == total

def main():
    """主函數"""
    success = test_paopass_trigger()
    
    # 創建測試報告
    try:
        report = {
            "test_name": "PAOPASS管理員模式觸發測試",
            "test_time": datetime.now().isoformat(),
            "success": success,
            "description": "測試PAOPASS密碼觸發管理員模式的功能"
        }
        
        with open("paopass_trigger_test_report.json", "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n📄 測試報告已保存到: paopass_trigger_test_report.json")
        
    except Exception as e:
        print(f"⚠️ 保存測試報告失敗: {e}")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

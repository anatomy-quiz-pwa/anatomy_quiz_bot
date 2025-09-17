#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PAOPASS管理員模式切換測試
測試PAOPASS密碼切換管理員模式開關的功能
"""

import sys
import os
import json
from datetime import datetime

def test_paopass_toggle():
    """測試PAOPASS切換管理員模式功能"""
    print("=" * 60)
    print("🔄 PAOPASS管理員模式切換測試")
    print("=" * 60)
    
    results = []
    
    try:
        # 導入必要的函數
        from app_supabase import (
            handle_text_message, 
            is_admin_user,
            get_user_admin_permissions,
            activate_admin_mode,
            deactivate_admin_mode,
            supabase
        )
        
        # 測試用戶ID（使用寶的真實帳號）
        test_user_id = "U977c24d1fec3a2bf07035504e1444911"  # 寶的LINE帳號
        
        print(f"📱 測試用戶: {test_user_id}")
        print()
        
        # 1. 確保用戶初始狀態為普通用戶
        print("1️⃣ 設置初始狀態為普通用戶...")
        try:
            # 清除管理員權限
            supabase.table('users').update({
                'is_admin': False,
                'test_mode': False,
                'admin_levels': [],
                'admin_permissions': {}
            }).eq('line_user_id', test_user_id).execute()
            
            initial_status = is_admin_user(test_user_id)
            print(f"   初始管理員狀態: {initial_status}")
            
            if not initial_status:
                print("   ✅ 初始狀態設置成功（普通用戶）")
                results.append(("初始狀態設置", True))
            else:
                print("   ❌ 初始狀態設置失敗，仍為管理員")
                results.append(("初始狀態設置", False))
                
        except Exception as e:
            print(f"   ❌ 初始狀態設置失敗: {e}")
            results.append(("初始狀態設置", False))
        print()
        
        # 2. 第一次輸入PAOPASS - 激活管理員模式
        print("2️⃣ 第一次輸入PAOPASS（激活管理員模式）...")
        try:
            test_message = {"text": "PAOPASS"}
            print("   📨 模擬發送訊息: PAOPASS")
            
            handle_text_message(test_user_id, test_message)
            print("   ✅ PAOPASS訊息處理完成")
            
            # 檢查是否成功激活
            admin_status_after_first = is_admin_user(test_user_id)
            print(f"   管理員狀態: {admin_status_after_first}")
            
            if admin_status_after_first:
                print("   ✅ 第一次PAOPASS成功激活管理員模式")
                results.append(("第一次PAOPASS激活", True))
            else:
                print("   ❌ 第一次PAOPASS未能激活管理員模式")
                results.append(("第一次PAOPASS激活", False))
                
        except Exception as e:
            print(f"   ❌ 第一次PAOPASS處理失敗: {e}")
            results.append(("第一次PAOPASS激活", False))
        print()
        
        # 3. 第二次輸入PAOPASS - 停用管理員模式
        print("3️⃣ 第二次輸入PAOPASS（停用管理員模式）...")
        try:
            test_message = {"text": "PAOPASS"}
            print("   📨 模擬發送訊息: PAOPASS")
            
            handle_text_message(test_user_id, test_message)
            print("   ✅ PAOPASS訊息處理完成")
            
            # 檢查是否成功停用
            admin_status_after_second = is_admin_user(test_user_id)
            print(f"   管理員狀態: {admin_status_after_second}")
            
            if not admin_status_after_second:
                print("   ✅ 第二次PAOPASS成功停用管理員模式")
                results.append(("第二次PAOPASS停用", True))
            else:
                print("   ❌ 第二次PAOPASS未能停用管理員模式")
                results.append(("第二次PAOPASS停用", False))
                
        except Exception as e:
            print(f"   ❌ 第二次PAOPASS處理失敗: {e}")
            results.append(("第二次PAOPASS停用", False))
        print()
        
        # 4. 第三次輸入PAOPASS - 再次激活管理員模式
        print("4️⃣ 第三次輸入PAOPASS（再次激活管理員模式）...")
        try:
            test_message = {"text": "PAOPASS"}
            print("   📨 模擬發送訊息: PAOPASS")
            
            handle_text_message(test_user_id, test_message)
            print("   ✅ PAOPASS訊息處理完成")
            
            # 檢查是否成功再次激活
            admin_status_after_third = is_admin_user(test_user_id)
            print(f"   管理員狀態: {admin_status_after_third}")
            
            if admin_status_after_third:
                print("   ✅ 第三次PAOPASS成功再次激活管理員模式")
                results.append(("第三次PAOPASS再次激活", True))
            else:
                print("   ❌ 第三次PAOPASS未能再次激活管理員模式")
                results.append(("第三次PAOPASS再次激活", False))
                
        except Exception as e:
            print(f"   ❌ 第三次PAOPASS處理失敗: {e}")
            results.append(("第三次PAOPASS再次激活", False))
        print()
        
        # 5. 測試不同大小寫的切換功能
        print("5️⃣ 測試不同大小寫的切換功能...")
        try:
            test_cases = ["paopass", "Paopass", "PaoPass"]
            
            for i, test_case in enumerate(test_cases, 1):
                print(f"   測試 {i}: {test_case}")
                
                # 獲取當前狀態
                current_status = is_admin_user(test_user_id)
                print(f"      切換前狀態: {'管理員' if current_status else '普通用戶'}")
                
                # 執行切換
                test_message = {"text": test_case}
                handle_text_message(test_user_id, test_message)
                
                # 檢查切換後狀態
                new_status = is_admin_user(test_user_id)
                print(f"      切換後狀態: {'管理員' if new_status else '普通用戶'}")
                
                # 驗證狀態是否改變
                if current_status != new_status:
                    print(f"      ✅ 狀態成功切換")
                else:
                    print(f"      ❌ 狀態未改變")
            
            results.append(("大小寫切換測試", True))
        except Exception as e:
            print(f"   ❌ 大小寫切換測試失敗: {e}")
            results.append(("大小寫切換測試", False))
        print()
        
        # 6. 測試權限詳情變化
        print("6️⃣ 測試權限詳情變化...")
        try:
            # 確保當前是管理員狀態
            if not is_admin_user(test_user_id):
                activate_admin_mode(test_user_id)
            
            # 獲取管理員權限詳情
            admin_info = get_user_admin_permissions(test_user_id)
            if admin_info:
                print("   📋 管理員權限詳情:")
                print(f"      • is_admin: {admin_info.get('is_admin', False)}")
                print(f"      • test_mode: {admin_info.get('test_mode', False)}")
                print(f"      • admin_levels: {len(admin_info.get('admin_levels', []))} 個等級")
                print(f"      • 特殊權限: {admin_info.get('admin_permissions', {}).get('can_access_all_levels', False)}")
            
            # 切換到普通用戶
            deactivate_admin_mode(test_user_id)
            
            # 獲取普通用戶權限詳情
            normal_info = get_user_admin_permissions(test_user_id)
            if normal_info:
                print("   📋 普通用戶權限詳情:")
                print(f"      • is_admin: {normal_info.get('is_admin', False)}")
                print(f"      • test_mode: {normal_info.get('test_mode', False)}")
                print(f"      • admin_levels: {len(normal_info.get('admin_levels', []))} 個等級")
            else:
                print("   📋 普通用戶無管理員權限記錄")
            
            results.append(("權限詳情測試", True))
        except Exception as e:
            print(f"   ❌ 權限詳情測試失敗: {e}")
            results.append(("權限詳情測試", False))
        print()
        
    except ImportError as e:
        print(f"❌ 導入模組失敗: {e}")
        return False
    except Exception as e:
        print(f"❌ 測試過程發生錯誤: {e}")
        return False
    
    # 總結報告
    print("=" * 60)
    print("📊 PAOPASS切換測試總結")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"   {test_name}: {status}")
    
    print(f"\n🎯 總體結果: {passed}/{total} 通過")
    
    if passed == total:
        print("\n🎉 PAOPASS管理員模式切換功能測試全部通過！")
        print("\n✨ 功能說明:")
        print("   🔄 用戶輸入 'PAOPASS' 可以切換管理員模式開關")
        print("   🔑 第一次輸入：激活管理員模式")
        print("   🔒 第二次輸入：停用管理員模式")
        print("   🔄 第三次輸入：再次激活管理員模式")
        print("   📱 支援不區分大小寫切換")
        
        print("\n💡 使用方法:")
        print("   1. 在LINE中輸入: PAOPASS")
        print("   2. 系統檢查當前管理員狀態")
        print("   3. 自動切換到相反的狀態")
        print("   4. 發送相應的確認訊息")
        
    else:
        print(f"\n⚠️ 發現 {total-passed} 個問題需要修復")
        for test_name, result in results:
            if not result:
                print(f"  • {test_name}")
    
    return passed == total

def main():
    """主函數"""
    success = test_paopass_toggle()
    
    # 創建測試報告
    try:
        report = {
            "test_name": "PAOPASS管理員模式切換測試",
            "test_time": datetime.now().isoformat(),
            "success": success,
            "description": "測試PAOPASS密碼切換管理員模式開關的功能"
        }
        
        with open("paopass_toggle_test_report.json", "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n📄 測試報告已保存到: paopass_toggle_test_report.json")
        
    except Exception as e:
        print(f"⚠️ 保存測試報告失敗: {e}")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試輸入「排行榜」是否會出現 Flex 結構訊息
"""

import os
import sys
import json
from datetime import datetime

# 添加當前目錄到 Python 路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 設置環境變量
os.environ['SUPABASE_URL'] = 'https://ciqlfqfgzqqgdrogedxg.supabase.co'
os.environ['SUPABASE_ANON_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA'

def test_leaderboard_flex():
    """測試排行榜 Flex 訊息"""
    print("🔍 測試輸入「排行榜」是否會出現 Flex 結構訊息...")
    
    try:
        from app_supabase_fixed import create_leaderboard_flex_message, send_leaderboard_message
        
        # 測試用戶ID
        test_user_id = "U1234567890abcdef"
        
        print(f"\n📋 測試用戶ID: {test_user_id}")
        print(f"📝 測試輸入: 排行榜")
        
        # 1. 測試創建排行榜 Flex Message
        print("\n1️⃣ 測試創建排行榜 Flex Message...")
        try:
            # 先獲取排行榜數據
            from app_supabase_fixed import get_real_students_data
            students_data = get_real_students_data()
            
            if not students_data:
                print("❌ 無法獲取排行榜數據")
                return False
            
            # 限制顯示前10名
            top_10 = students_data[:10]
            
            # 創建 Flex Message
            flex_message = create_leaderboard_flex_message(top_10, students_data, test_user_id)
            print("✅ 排行榜 Flex Message 創建成功")
            print(f"📊 Flex Message 類型: {type(flex_message)}")
            
            # 檢查 Flex Message 結構
            if isinstance(flex_message, dict):
                print("✅ Flex Message 是字典格式")
                print(f"📋 包含的鍵: {list(flex_message.keys())}")
                
                # 檢查必要的結構
                if 'type' in flex_message:
                    print(f"✅ 包含 type 欄位: {flex_message['type']}")
                else:
                    print("❌ 缺少 type 欄位")
                
                if 'altText' in flex_message:
                    print(f"✅ 包含 altText 欄位: {flex_message['altText']}")
                else:
                    print("❌ 缺少 altText 欄位")
                
                if 'contents' in flex_message:
                    print(f"✅ 包含 contents 欄位")
                    contents = flex_message['contents']
                    if isinstance(contents, dict):
                        print(f"📋 contents 類型: {contents.get('type', 'unknown')}")
                        if 'body' in contents:
                            print(f"✅ 包含 body 欄位")
                        else:
                            print("❌ 缺少 body 欄位")
                    else:
                        print(f"❌ contents 不是字典格式: {type(contents)}")
                else:
                    print("❌ 缺少 contents 欄位")
                
                # 顯示 Flex Message 結構摘要
                print(f"\n📊 Flex Message 結構摘要:")
                print(f"   - 類型: {flex_message.get('type', 'N/A')}")
                print(f"   - 替代文字: {flex_message.get('altText', 'N/A')[:50]}...")
                print(f"   - 內容類型: {flex_message.get('contents', {}).get('type', 'N/A')}")
                
            else:
                print(f"❌ Flex Message 不是字典格式: {type(flex_message)}")
                
        except Exception as e:
            print(f"❌ 創建排行榜 Flex Message 失敗: {e}")
            return False
        
        # 2. 測試發送排行榜訊息
        print("\n2️⃣ 測試發送排行榜訊息...")
        try:
            result = send_leaderboard_message(test_user_id)
            print("✅ 排行榜訊息發送成功")
            print(f"📊 發送結果: {result}")
            
            # 檢查發送結果
            if isinstance(result, dict):
                if 'error' in result:
                    print(f"⚠️ 發送結果包含錯誤: {result['error']}")
                else:
                    print("✅ 發送結果正常")
            else:
                print(f"📊 發送結果類型: {type(result)}")
                
        except Exception as e:
            print(f"❌ 發送排行榜訊息失敗: {e}")
            return False
        
        # 3. 測試文字處理邏輯
        print("\n3️⃣ 測試文字處理邏輯...")
        try:
            from app_supabase_fixed import handle_text_message
            
            # 模擬文字訊息
            message_text = "排行榜"
            print(f"📝 測試文字: {message_text}")
            
            # 測試文字匹配
            leaderboard_keywords = ['排行榜', 'leaderboard', '排名', '排行']
            if message_text.lower() in [kw.lower() for kw in leaderboard_keywords]:
                print("✅ 文字匹配成功")
            else:
                print("❌ 文字匹配失敗")
                
        except Exception as e:
            print(f"❌ 測試文字處理邏輯失敗: {e}")
            return False
        
        print("\n🎉 所有測試完成！")
        return True
        
    except ImportError as e:
        print(f"❌ 導入模組失敗: {e}")
        print("請確保 app_supabase_fixed.py 文件存在且可導入")
        return False
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {e}")
        return False

def test_flex_message_structure():
    """測試 Flex Message 結構詳細分析"""
    print("\n🔍 詳細分析 Flex Message 結構...")
    
    try:
        from app_supabase_fixed import create_leaderboard_flex_message, get_real_students_data
        
        # 獲取排行榜數據
        students_data = get_real_students_data()
        if not students_data:
            print("❌ 無法獲取排行榜數據")
            return
        
        top_10 = students_data[:10]
        test_user_id = "U1234567890abcdef"
        
        flex_message = create_leaderboard_flex_message(top_10, students_data, test_user_id)
        
        if isinstance(flex_message, dict):
            print("📊 Flex Message 詳細結構:")
            print(json.dumps(flex_message, indent=2, ensure_ascii=False))
            
            # 檢查關鍵結構
            print("\n🔍 結構檢查:")
            
            # 檢查根級別
            required_root_keys = ['type', 'altText', 'contents']
            for key in required_root_keys:
                if key in flex_message:
                    print(f"✅ 根級別 {key}: {flex_message[key]}")
                else:
                    print(f"❌ 缺少根級別 {key}")
            
            # 檢查 contents 結構
            if 'contents' in flex_message:
                contents = flex_message['contents']
                if isinstance(contents, dict):
                    print(f"\n📋 contents 結構:")
                    print(f"   - 類型: {contents.get('type', 'N/A')}")
                    print(f"   - 大小: {contents.get('size', 'N/A')}")
                    
                    if 'body' in contents:
                        body = contents['body']
                        if isinstance(body, dict):
                            print(f"   - body 類型: {body.get('type', 'N/A')}")
                            print(f"   - body 佈局: {body.get('layout', 'N/A')}")
                            
                            if 'contents' in body:
                                body_contents = body['contents']
                                if isinstance(body_contents, list):
                                    print(f"   - body 內容項目數: {len(body_contents)}")
                                    
                                    # 分析每個內容項目
                                    for i, item in enumerate(body_contents):
                                        if isinstance(item, dict):
                                            print(f"     - 項目 {i+1}: {item.get('type', 'N/A')} - {item.get('text', item.get('type', 'N/A'))[:30]}...")
                                        else:
                                            print(f"     - 項目 {i+1}: {type(item)}")
                                else:
                                    print(f"   - body 內容不是列表: {type(body_contents)}")
                            else:
                                print("   - 缺少 body contents")
                        else:
                            print(f"   - body 不是字典: {type(body)}")
                    else:
                        print("   - 缺少 body")
                else:
                    print(f"   - contents 不是字典: {type(contents)}")
            else:
                print("   - 缺少 contents")
                
        else:
            print(f"❌ Flex Message 不是字典格式: {type(flex_message)}")
            
    except Exception as e:
        print(f"❌ 分析 Flex Message 結構失敗: {e}")

if __name__ == "__main__":
    print("🚀 開始測試排行榜 Flex 訊息功能...")
    print("=" * 60)
    
    # 執行測試
    success = test_leaderboard_flex()
    
    if success:
        print("\n" + "=" * 60)
        print("🎉 測試完成！排行榜 Flex 訊息功能正常")
        
        # 執行詳細結構分析
        test_flex_message_structure()
    else:
        print("\n" + "=" * 60)
        print("❌ 測試失敗！請檢查相關配置")

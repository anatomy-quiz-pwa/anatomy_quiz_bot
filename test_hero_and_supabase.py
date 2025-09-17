#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
from dotenv import load_dotenv
from supabase import create_client

# 載入環境變數
load_dotenv()

def test_supabase_connection():
    """測試Supabase連線"""
    print("🔍 測試Supabase連線...")
    
    try:
        SUPABASE_URL = os.getenv("SUPABASE_URL")
        SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
        
        print(f"SUPABASE_URL: {SUPABASE_URL}")
        print(f"SUPABASE_KEY: {SUPABASE_KEY[:20] if SUPABASE_KEY else 'None'}...")
        
        if not SUPABASE_URL or not SUPABASE_KEY:
            print("❌ 環境變數未設置")
            return False
        
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # 測試連線
        result = supabase.table('user_stats').select('*').limit(1).execute()
        
        if result.data:
            print("✅ Supabase連線成功")
            return True
        else:
            print("⚠️ Supabase連線成功但沒有數據")
            return True
            
    except Exception as e:
        print(f"❌ Supabase連線失敗: {e}")
        return False

def test_hero_images():
    """測試hero圖片URL"""
    print("\n🔍 測試hero圖片URL...")
    
    # 測試等級海報
    base_url = "https://ciqlfqfgzqqgdrogedxg.supabase.co/storage/v1/object/public"
    level_posters = {
        1: f"{base_url}/linebot/level_1_poster.png",
        2: f"{base_url}/linebot/level_2_poster.png",
        3: f"{base_url}/linebot/level_3_poster.png",
        4: f"{base_url}/linebot/level_4_poster.png",
        5: f"{base_url}/linebot/level_5_poster.png",
    }
    
    success_count = 0
    total_count = len(level_posters)
    
    for level, url in level_posters.items():
        try:
            print(f"測試 Level {level} 海報: {url}")
            response = requests.head(url, timeout=5)
            
            if response.status_code == 200:
                content_type = response.headers.get('Content-Type', '')
                if content_type.startswith('image/'):
                    print(f"✅ Level {level} 海報正常")
                    success_count += 1
                else:
                    print(f"⚠️ Level {level} 海報內容類型異常: {content_type}")
            else:
                print(f"❌ Level {level} 海報HTTP錯誤: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Level {level} 海報請求失敗: {e}")
    
    print(f"\n📊 Hero圖片測試結果: {success_count}/{total_count} 成功")
    return success_count == total_count

def test_level_up_image():
    """測試升級圖片"""
    print("\n🔍 測試升級圖片...")
    
    level_up_url = "https://ciqlfqfgzqqgdrogedxg.supabase.co/storage/v1/object/public/linebot/levelup.png"
    
    try:
        print(f"測試升級圖片: {level_up_url}")
        response = requests.head(level_up_url, timeout=5)
        
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', '')
            if content_type.startswith('image/'):
                print("✅ 升級圖片正常")
                return True
            else:
                print(f"⚠️ 升級圖片內容類型異常: {content_type}")
                return False
        else:
            print(f"❌ 升級圖片HTTP錯誤: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 升級圖片請求失敗: {e}")
        return False

def test_question_images():
    """測試題目圖片"""
    print("\n🔍 測試題目圖片...")
    
    try:
        from supabase_quiz_handler import get_questions
        
        questions = get_questions()
        if not questions:
            print("❌ 無法獲取題目數據")
            return False
        
        # 檢查前5個題目的圖片
        image_count = 0
        valid_image_count = 0
        
        for i, question in enumerate(questions[:5]):
            image_url = question.get('image_url') or question.get('Q_image_url') or question.get('qimage_url')
            
            if image_url:
                image_count += 1
                print(f"題目 {i+1} 圖片: {image_url}")
                
                try:
                    response = requests.head(image_url, timeout=5)
                    if response.status_code == 200:
                        content_type = response.headers.get('Content-Type', '')
                        if content_type.startswith('image/'):
                            print(f"✅ 題目 {i+1} 圖片正常")
                            valid_image_count += 1
                        else:
                            print(f"⚠️ 題目 {i+1} 圖片內容類型異常: {content_type}")
                    else:
                        print(f"❌ 題目 {i+1} 圖片HTTP錯誤: {response.status_code}")
                except Exception as e:
                    print(f"❌ 題目 {i+1} 圖片請求失敗: {e}")
            else:
                print(f"題目 {i+1} 沒有圖片")
        
        print(f"\n📊 題目圖片測試結果: {valid_image_count}/{image_count} 有效")
        return valid_image_count > 0
        
    except Exception as e:
        print(f"❌ 題目圖片測試失敗: {e}")
        return False

def main():
    """主測試函數"""
    print("🚀 開始測試LINE bot的hero圖片和Supabase連線...")
    print("=" * 60)
    
    # 測試Supabase連線
    supabase_ok = test_supabase_connection()
    
    # 測試hero圖片
    hero_ok = test_hero_images()
    
    # 測試升級圖片
    level_up_ok = test_level_up_image()
    
    # 測試題目圖片
    question_images_ok = test_question_images()
    
    # 總結
    print("\n" + "=" * 60)
    print("📋 測試總結:")
    print(f"Supabase連線: {'✅ 正常' if supabase_ok else '❌ 異常'}")
    print(f"Hero圖片: {'✅ 正常' if hero_ok else '❌ 異常'}")
    print(f"升級圖片: {'✅ 正常' if level_up_ok else '❌ 異常'}")
    print(f"題目圖片: {'✅ 正常' if question_images_ok else '❌ 異常'}")
    
    if supabase_ok and hero_ok and level_up_ok and question_images_ok:
        print("\n🎉 所有測試通過！LINE bot應該可以正常顯示hero圖片。")
    else:
        print("\n⚠️ 部分測試失敗，可能需要檢查相關配置。")

if __name__ == "__main__":
    main()

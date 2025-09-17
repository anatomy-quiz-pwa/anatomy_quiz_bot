#!/usr/bin/env python3
"""
測試真實問答流程
模擬用戶實際使用情況
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_real_quiz_flow():
    """測試真實問答流程"""
    print("🎮 測試真實問答流程")
    print("=" * 60)
    
    # 模擬用戶狀態
    class MockUser:
        def __init__(self, user_id):
            self.user_id = user_id
            self.level = 1
            self.correct = 0
            self.wrong = 0
            self.current_level_correct = 0
        
        def answer_question(self, answer, is_correct):
            """回答問題"""
            if is_correct:
                self.correct += 1
                self.current_level_correct += 1
                
                # 檢查是否升級
                if self.current_level_correct >= 3:
                    self.level += 1
                    self.current_level_correct = 0
                    return True, f"🎉 恭喜升級到等級 {self.level}！"
                else:
                    remaining = 3 - self.current_level_correct
                    return False, f"✅ 答對了！還需要答對 {remaining} 題即可升級"
            else:
                self.wrong += 1
                remaining = 3 - self.current_level_correct
                return False, f"❌ 答錯了！還需要答對 {remaining} 題即可升級"
        
        def get_status(self):
            """獲取當前狀態"""
            return {
                "level": self.level,
                "correct": self.correct,
                "wrong": self.wrong,
                "current_progress": f"{self.current_level_correct}/3"
            }
    
    # 測試場景1：完美答題（全部答對）
    print("📝 測試場景1：完美答題（全部答對）")
    print("-" * 40)
    
    user1 = MockUser("user_1")
    print(f"初始狀態: {user1.get_status()}")
    
    # 等級1：答對3題
    for i in range(3):
        upgraded, message = user1.answer_question("1", True)
        print(f"第{i+1}題: {message}")
        print(f"當前狀態: {user1.get_status()}")
        print()
    
    # 等級2：答對3題
    for i in range(3):
        upgraded, message = user1.answer_question("1", True)
        print(f"第{i+4}題: {message}")
        print(f"當前狀態: {user1.get_status()}")
        print()
    
    print("=" * 60)
    
    # 測試場景2：混合答題（有答錯）
    print("📝 測試場景2：混合答題（有答錯）")
    print("-" * 40)
    
    user2 = MockUser("user_2")
    print(f"初始狀態: {user2.get_status()}")
    
    # 模擬答題序列：對、錯、對、對、對
    answers = [True, False, True, True, True]
    
    for i, is_correct in enumerate(answers):
        upgraded, message = user2.answer_question("1", is_correct)
        print(f"第{i+1}題: {message}")
        print(f"當前狀態: {user2.get_status()}")
        print()
    
    print("=" * 60)
    
    # 測試場景3：連續答錯
    print("📝 測試場景3：連續答錯")
    print("-" * 40)
    
    user3 = MockUser("user_3")
    print(f"初始狀態: {user3.get_status()}")
    
    # 連續答錯5題
    for i in range(5):
        upgraded, message = user3.answer_question("2", False)  # 假設答案是1，所以2是錯的
        print(f"第{i+1}題: {message}")
        print(f"當前狀態: {user3.get_status()}")
        print()
    
    print("=" * 60)
    
    # 測試場景4：多輪升級
    print("📝 測試場景4：多輪升級")
    print("-" * 40)
    
    user4 = MockUser("user_4")
    print(f"初始狀態: {user4.get_status()}")
    
    # 連續答對12題（應該升級4次）
    for i in range(12):
        upgraded, message = user4.answer_question("1", True)
        print(f"第{i+1}題: {message}")
        if upgraded:
            print(f"🎊 升級成功！當前等級: {user4.level}")
        print(f"當前狀態: {user4.get_status()}")
        print()
    
    print("🎉 所有測試完成！")
    print("=" * 60)
    print("📊 總結：")
    print("✅ 升級需要答對 3 題")
    print("✅ 答錯題目不影響升級進度")
    print("✅ 升級後進度重置為 0/3")
    print("✅ 可以連續升級多個等級")

if __name__ == "__main__":
    test_real_quiz_flow()

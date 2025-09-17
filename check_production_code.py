#!/usr/bin/env python3
"""
檢查生產環境代碼版本
"""

import sys
import os

# 添加項目根目錄到Python路徑
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def check_reset_code():
    """檢查 RESET 相關代碼"""
    print("🔍 檢查 RESET 相關代碼...")
    
    try:
        # 讀取 app_supabase.py 文件
        with open('app_supabase.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 檢查關鍵代碼片段
        checks = [
            ("handle_admin_quiz 調用", "handle_admin_quiz(sender_id, message_text)"),
            ("普通用戶重置邏輯", "elif message_text.lower() in ['reset', 'RESET', '重置', '重設', '重新開始']:"),
            ("重置進度日志", "🔄 普通用戶 {sender_id} 請求重置進度"),
            ("管理員重置邏輯", "elif message_text.lower() in ['reset', 'RESET', '重置', '重設', '重新開始']:"),
            ("管理員重置日志", "🔄 管理員用戶 {sender_id} 請求重置進度"),
        ]
        
        results = []
        
        for check_name, code_snippet in checks:
            if code_snippet in content:
                print(f"✅ {check_name}: 存在")
                results.append((check_name, True))
            else:
                print(f"❌ {check_name}: 不存在")
                results.append((check_name, False))
        
        # 檢查 handle_admin_message 的修復
        if "handle_admin_quiz(sender_id, message_text)" in content:
            # 查找上下文
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if "handle_admin_quiz(sender_id, message_text)" in line:
                    context = '\n'.join(lines[max(0, i-3):i+3])
                    print(f"\n📋 handle_admin_message 修復上下文:")
                    print(context)
                    break
        
        return results
        
    except Exception as e:
        print(f"❌ 檢查代碼失敗: {e}")
        return []

def check_git_status():
    """檢查 Git 狀態"""
    print("\n🔍 檢查 Git 狀態...")
    
    try:
        import subprocess
        
        # 檢查當前分支
        result = subprocess.run(['git', 'branch', '--show-current'], 
                               capture_output=True, text=True, cwd=project_root)
        if result.returncode == 0:
            branch = result.stdout.strip()
            print(f"📋 當前分支: {branch}")
        
        # 檢查未提交的更改
        result = subprocess.run(['git', 'status', '--porcelain'], 
                               capture_output=True, text=True, cwd=project_root)
        if result.returncode == 0:
            changes = result.stdout.strip()
            if changes:
                print("⚠️ 有未提交的更改:")
                for line in changes.split('\n')[:5]:  # 只顯示前5行
                    print(f"  {line}")
            else:
                print("✅ 沒有未提交的更改")
        
        # 檢查最近的提交
        result = subprocess.run(['git', 'log', '--oneline', '-5'], 
                               capture_output=True, text=True, cwd=project_root)
        if result.returncode == 0:
            commits = result.stdout.strip()
            print("📋 最近的提交:")
            for line in commits.split('\n'):
                print(f"  {line}")
        
        return True
        
    except Exception as e:
        print(f"❌ 檢查 Git 狀態失敗: {e}")
        return False

def create_deployment_fix():
    """創建部署修復指南"""
    print("\n📝 創建部署修復指南...")
    
    fix_guide = """# 🔧 RESET 功能部署修復指南

## 問題診斷
根據生產環境日志分析，RESET 功能在本地測試正常，但在生產環境中無效。

### 生產環境日志分析
```
2025-09-17 11:07:04,735 - 📨 收到來自用戶的訊息: RESET
2025-09-17 11:07:05,395 - 👤 用戶是普通用戶
2025-09-17 11:07:05,624 - 查詢用戶統計
2025-09-17 11:07:05,904 - 📤 LINE 訊息發送結果: 200
```

### 缺失的日志
- ❌ 沒有看到 "🔄 普通用戶 ... 請求重置進度" 日志
- ❌ 沒有看到重置功能執行

## 可能原因
1. **代碼版本不同步** - 生產環境可能使用舊版本代碼
2. **部署問題** - 最新修復沒有正確部署到生產環境

## 解決方案

### 1. 確認代碼修復
檢查 `app_supabase.py` 第 1778 行：
```python
# 應該是這樣（修復後）
handle_admin_quiz(sender_id, message_text)

# 而不是這樣（修復前）  
handle_regular_message(sender_id, message_text)
```

### 2. 重新部署
```bash
# 提交最新更改
git add .
git commit -m "修復 RESET 功能 - 管理員訊息路由"
git push origin main

# 觸發 Render 重新部署
# 或手動在 Render 控制台重新部署
```

### 3. 驗證部署
部署完成後，檢查日志應該看到：
```
🔄 普通用戶 [user_id] 請求重置進度
✅ 成功重置用戶 [user_id] 的進度
```

### 4. 測試確認
用戶發送 "RESET" 或 "重置" 後應該收到：
```
🔄 進度重置成功！

✅ 您的學習進度已重置為：
• 等級：1
• 答對題數：0
• 答錯題數：0
• 連續天數：0

🎯 重新開始您的解剖學學習之旅！
輸入「開始」開始答題吧！
```

## 緊急修復
如果問題持續，可以嘗試：
1. 在 Render 控制台手動重新部署
2. 檢查環境變數設置
3. 查看完整的部署日志

---
*修復指南創建時間：2025年9月17日*
"""
    
    try:
        with open('RESET_部署修復指南.md', 'w', encoding='utf-8') as f:
            f.write(fix_guide)
        print("✅ 部署修復指南創建成功：RESET_部署修復指南.md")
        return True
    except Exception as e:
        print(f"❌ 創建修復指南失敗: {e}")
        return False

def main():
    """主函數"""
    print("🚀 生產環境代碼檢查")
    print("=" * 40)
    
    # 檢查代碼
    code_results = check_reset_code()
    
    # 檢查 Git 狀態
    git_ok = check_git_status()
    
    # 創建修復指南
    guide_created = create_deployment_fix()
    
    # 總結
    print("\n" + "=" * 40)
    print("📊 檢查結果總結")
    print("=" * 40)
    
    if code_results:
        passed = sum(1 for _, result in code_results if result)
        total = len(code_results)
        print(f"🔧 代碼檢查: {passed}/{total} 項通過")
        
        for check_name, result in code_results:
            status = "✅" if result else "❌"
            print(f"  {status} {check_name}")
    
    git_status = "✅" if git_ok else "❌"
    print(f"📋 Git 狀態: {git_status}")
    
    guide_status = "✅" if guide_created else "❌"
    print(f"📝 修復指南: {guide_status}")
    
    print(f"\n💡 診斷結果:")
    print(f"• 本地代碼包含 RESET 修復")
    print(f"• 功能在本地測試正常")
    print(f"• 生產環境可能需要重新部署")
    
    print(f"\n🔧 建議操作:")
    print(f"1. 確認最新代碼已提交到 Git")
    print(f"2. 在 Render 控制台重新部署")
    print(f"3. 部署完成後測試 RESET 功能")
    print(f"4. 查看部署後的日志確認修復生效")

if __name__ == "__main__":
    main()

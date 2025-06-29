# Anatomy Quiz Bot

這是一個自動發送解剖學問題的 LINE Bot 專案。

## 功能特點

- 每日自動發送解剖學問題
- 支援多種題型（選擇題、是非題等）
- 自動評分和回饋
- 從 Google Sheets 讀取題庫

## 安裝說明

1. 克隆此專案
2. 安裝依賴：
   ```bash
   pip install -r requirements.txt
   ```
3. 設置 Google Sheets API：
   - 前往 Google Cloud Console
   - 創建一個新專案
   - 啟用 Google Sheets API
   - 下載憑證文件並重命名為 `credentials.json`，放在專案根目錄

4. 設置 LINE Bot：
   - 在 LINE Developers Console 創建一個新的 Channel
   - 獲取 Channel Secret 和 Channel Access Token
   - 複製 `.env.example` 到 `.env` 並填入必要的配置信息

5. 運行程序：
   ```bash
   python app.py
   ```

## 配置說明

在 `.env` 文件中配置以下參數：
- LINE_CHANNEL_ACCESS_TOKEN：LINE Bot 的 Channel Access Token
- LINE_CHANNEL_SECRET：LINE Bot 的 Channel Secret
- USER_ID：接收問題的用戶 ID
- QUESTION_TIME：每日發送問題的時間（格式：HH:MM）

## 使用說明

1. 將機器人加入為好友
2. 發送任何訊息，機器人會顯示主選單
3. 點擊「開始每日問答」來啟動每日問答
4. 點擊「停止每日問答」來暫停問答
5. 回答問題時，點擊選項即可提交答案 
>>>>>>> f5f0a01 (feat: upload all project files)

# Supabase 後台數據抓取邏輯詳解

## 🔄 數據流程圖

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            Supabase 數據抓取流程                              │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   環境變數檢查   │───▶│   Supabase 連接  │───▶│   數據庫查詢     │
│                 │    │     測試        │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ SUPABASE_URL    │    │ 連接成功/失敗    │    │ user_stats 表   │
│ SUPABASE_KEY    │    │ 狀態記錄        │    │ select('*')     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ 變數存在檢查     │    │ 全局狀態更新     │    │ 原始數據獲取     │
│ 長度驗證        │    │ 錯誤信息記錄     │    │ response.data   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ 連接測試函數    │    │ 診斷端點可用    │    │ 數據處理函數     │
│ test_supabase_  │    │ /diagnostics    │    │ get_students_   │
│ connection()    │    │ 實時狀態查詢     │    │ data()          │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📊 詳細數據處理邏輯

### 1. 初始化階段
```python
# 環境變數配置
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# 連接狀態跟踪
supabase_connection_status = {
    'connected': False,
    'last_check': None,
    'error_message': None,
    'url': SUPABASE_URL,
    'key_length': len(SUPABASE_KEY) if SUPABASE_KEY else 0
}
```

### 2. 連接測試邏輯
```python
def test_supabase_connection():
    # 1. 檢查環境變數
    if not SUPABASE_URL or not SUPABASE_KEY:
        return False
    
    # 2. 創建客戶端
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # 3. 測試查詢
    test_response = supabase.table('user_stats').select('count', count='exact').limit(1).execute()
    
    # 4. 更新狀態
    supabase_connection_status.update({
        'connected': True,
        'last_check': datetime.datetime.now(),
        'error_message': None
    })
```

### 3. 數據獲取邏輯
```python
def get_students_data():
    if supabase is not None:
        # 真實數據路徑
        response = supabase.table('user_stats').select('*').execute()
        students_data = response.data
        
        # 數據處理和字段標準化
        processed_data = []
        for student in students_data:
            processed_student = {
                "user_id": student.get("user_id", "unknown"),
                "name": student.get("name", f"用戶 {student.get('user_id', 'unknown')}"),
                "level": student.get("level", 1),
                "score": student.get("score", 0),
                "questions_answered": student.get("questions_answered", 0),
                "correct_answers": student.get("correct_answers", 0),
                "last_active": student.get("last_active", "未知")
            }
            processed_data.append(processed_student)
    else:
        # 模擬數據路徑
        students_data = [模擬數據...]
    
    return students_data
```

## 🎯 數據抓取端點

### 1. 排行榜端點 (`/leaderboard`)
```python
@app.route('/leaderboard')
def leaderboard():
    # 獲取數據
    students_data = get_students_data()
    
    # 排序處理
    if supabase is None:
        students_data = sorted(students_data, key=lambda x: x["score"], reverse=True)
    
    # 渲染頁面
    return html_content
```

### 2. 儀表板端點 (`/dashboard`)
```python
@app.route('/dashboard')
def dashboard():
    # 獲取數據
    students_data = get_students_data()
    
    # 計算統計
    total_students = len(students_data)
    avg_score = sum(s["score"] for s in students_data) / total_students
    
    # 渲染頁面
    return html_content
```

### 3. 診斷端點 (`/diagnostics`)
```python
@app.route('/diagnostics')
def diagnostics():
    # 重新測試連接
    connection_test_result = test_supabase_connection()
    
    # 返回系統狀態
    return jsonify({
        'timestamp': datetime.datetime.now().isoformat(),
        'supabase_connection': supabase_connection_status,
        'environment_variables': {
            'SUPABASE_URL_set': bool(SUPABASE_URL),
            'SUPABASE_KEY_set': bool(SUPABASE_KEY)
        },
        'connection_test_result': connection_test_result
    })
```

## 🔍 錯誤處理機制

### 1. 連接失敗處理
```python
# 連接失敗時的回退邏輯
if supabase is None:
    logger.warning("⚠️ Supabase 未連接，使用模擬數據")
    students_data = [模擬數據...]
```

### 2. 數據字段缺失處理
```python
# 使用 get() 方法提供默認值
processed_student = {
    "user_id": student.get("user_id", "unknown"),
    "name": student.get("name", f"用戶 {student.get('user_id', 'unknown')}"),
    "level": student.get("level", 1),
    "score": student.get("score", 0),
    # ...
}
```

### 3. 異常捕獲處理
```python
try:
    response = supabase.table('user_stats').select('*').execute()
    students_data = response.data
except Exception as e:
    logger.error(f"❌ 獲取學生數據失敗: {e}")
    students_data = []
```

## 📈 數據流程狀態

### 當前狀態：
- ✅ **連接狀態**：離線模式（環境變數未設置）
- ✅ **數據來源**：模擬數據
- ✅ **數據一致性**：排行榜和儀表板完全一致
- ✅ **錯誤處理**：完整的回退機制
- ✅ **日誌記錄**：詳細的操作日誌

### 真實數據模式：
- 🔄 **連接狀態**：連接正常
- 🔄 **數據來源**：Supabase user_stats 表
- 🔄 **數據處理**：字段標準化和驗證
- 🔄 **排序處理**：按分數降序排列

## 🛠️ 技術實現細節

### 1. Supabase 查詢語法
```python
# 獲取所有用戶數據
response = supabase.table('user_stats').select('*').execute()

# 獲取計數
response = supabase.table('user_stats').select('count', count='exact').limit(1).execute()

# 按分數排序
response = supabase.table('user_stats').select('*').order('score', desc=True).execute()
```

### 2. 數據標準化
```python
# 確保所有必要字段存在
required_fields = [
    'user_id', 'name', 'level', 'score', 
    'questions_answered', 'correct_answers', 'last_active'
]

# 使用 get() 方法提供默認值
for field in required_fields:
    if field not in student:
        student[field] = get_default_value(field)
```

### 3. 日誌記錄
```python
# 詳細的操作日誌
logger.info("📊 正在獲取學生數據...")
logger.info("📡 從 Supabase 獲取真實數據...")
logger.info(f"✅ 成功獲取 {len(students_data)} 條真實數據")
logger.info(f"✅ 數據處理完成，共 {len(students_data)} 條記錄")
```

## 🎯 優化建議

### 1. 性能優化
- 添加數據緩存機制
- 實現分頁查詢
- 添加查詢結果緩存

### 2. 錯誤處理
- 實現自動重連機制
- 添加數據驗證
- 實現數據備份

### 3. 監控改進
- 添加性能指標
- 實現實時監控
- 添加告警機制


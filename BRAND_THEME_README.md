# 解剖咬一口 Anatomy Bite - 品牌風格指南

## 品牌色彩 🎨

### 主要色彩
- **骨色背景** `#F4E8D8` - 溫暖的米白色，營造出復古手繪的氛圍
- **深黑線條** `#1C1C1C` - 用於邊框、文字和陰影，增強視覺對比
- **主要色調** `#C57B57` - 柔和的棕色，代表溫暖與專業
- **輔助色調** `#B85C38` - 較深的棕色，用於強調和按鈕

### 次要色彩
- **淺色背景** `#fffaf5` - 卡片和容器背景
- **成功色** `#88B04B` - 正確答案提示
- **錯誤色** `#DC3545` - 錯誤答案提示

## 字體設計 ✍️

### 英文標題字體
- **Playfair Display** (400, 700, 900)
- 特點：優雅的襯線字體，適合標題和品牌名稱
- 用途：所有標題 (h1-h6)

### 中文內文字體
- **Noto Sans TC** (400, 500, 700)
- 特點：清晰易讀的無襯線字體
- 用途：正文內容、按鈕文字、表單

## 設計特色 🎯

### 1. 美式復古手繪風格
- **黑線條邊框**：所有卡片和按鈕都有 2-3px 的深黑邊框
- **平面陰影**：使用 `box-shadow: 4px 4px 0 #1C1C1C` 創造立體效果
- **圓角設計**：適度的圓角 (8-16px) 保持友善感

### 2. 互動效果
- **懸停效果**：元素向左上方移動 `translate(-2px, -2px)`
- **陰影增強**：懸停時陰影變大 `box-shadow: 6px 6px 0 #1C1C1C`
- **顏色變化**：按鈕從 `#C57B57` 變為 `#B85C38`

### 3. 紙質紋理
- 使用細微的網格紋理模擬紙張質感
- 透過 `repeating-linear-gradient` 創造

## 已更新的檔案 📝

### 核心樣式檔案
1. **`/static/brand-theme.css`** - 新建的品牌主題檔案
2. **`/static/style.css`** - 更新現有樣式以符合品牌風格

### HTML 模板
1. **`/public/index.html`** - 主遊戲頁面
2. **`/templates/base.html`** - 基礎模板
3. **`/public_leaderboard.html`** - 排行榜頁面

## 使用方式 🚀

### 在 HTML 中引入品牌主題

```html
<!-- Google Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Noto+Sans+TC:wght@400;500;700&display=swap" rel="stylesheet">

<!-- Brand Theme -->
<link href="/static/brand-theme.css" rel="stylesheet">
```

### CSS 變數使用

```css
/* 在自訂樣式中使用品牌色彩 */
.my-element {
    background: var(--brand-bg);
    color: var(--brand-dark);
    border: 2px solid var(--brand-dark);
    box-shadow: 4px 4px 0 var(--brand-dark);
}
```

## 組件樣式範例 🧩

### 按鈕
```css
button {
    background: #C57B57;
    color: #fffaf5;
    border: 2px solid #1C1C1C;
    border-radius: 8px;
    box-shadow: 3px 3px 0 #1C1C1C;
    font-weight: bold;
    padding: 0.75rem 1.5rem;
}

button:hover {
    background: #B85C38;
    transform: translate(-2px, -2px);
    box-shadow: 5px 5px 0 #1C1C1C;
}
```

### 卡片
```css
.card {
    background: #fffaf5;
    border: 2px solid #1C1C1C;
    border-radius: 12px;
    box-shadow: 4px 4px 0 #1C1C1C;
    padding: 2rem;
}

.card:hover {
    transform: translate(-2px, -2px);
    box-shadow: 6px 6px 0 #1C1C1C;
}
```

### 選項按鈕
```css
.option-btn {
    background: #fffaf5;
    border: 2px solid #1C1C1C;
    box-shadow: 3px 3px 0 #1C1C1C;
}

.option-btn.selected {
    background: #C57B57;
    color: #fffaf5;
}
```

## 響應式設計 📱

在小螢幕上，部分效果會被簡化：
- 移除懸停的位移效果
- 縮小邊框寬度
- 調整陰影大小

```css
@media (max-width: 768px) {
    .game-container {
        border-width: 2px;
        box-shadow: 4px 4px 0 var(--brand-dark);
    }
}
```

## 品牌理念 💡

「解剖咬一口」的視覺設計靈感來自：
- 📚 **復古醫學插圖**：經典的解剖學教科書風格
- ✏️ **手繪質感**：溫暖且具有人文關懷
- 🎨 **美式復古**：簡潔有力的視覺語言
- 📖 **紙本閱讀**：紙質紋理喚起學習記憶

這個品牌風格旨在創造一個既專業又溫暖的學習環境，讓解剖學習變得更加親切和有趣。

---

**最後更新日期：2025-10-09**


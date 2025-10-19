// test_vercel_functions.js
// 測試 Vercel Functions 是否正確建立

const fs = require('fs');
const path = require('path');

console.log('🧪 Vercel Functions 測試');
console.log('======================');

// 檢查必要的檔案是否存在
const requiredFiles = [
  'api/auth/line/login.ts',
  'api/auth/line/callback.ts',
  'api/auth/line/verify.ts',
  'api/me/stats.ts'
];

console.log('\n📁 檢查 Vercel Functions 檔案結構...');
let allFilesExist = true;

requiredFiles.forEach(file => {
  const filePath = path.join(__dirname, file);
  if (fs.existsSync(filePath)) {
    console.log(`✅ ${file}`);
    
    // 檢查檔案內容是否包含必要的函數
    const content = fs.readFileSync(filePath, 'utf8');
    if (content.includes('VercelRequest') && content.includes('VercelResponse')) {
      console.log(`  ✅ 使用 Vercel Functions 類型`);
    } else {
      console.log(`  ❌ 缺少 Vercel Functions 類型`);
      allFilesExist = false;
    }
    
    if (content.includes('export default async function handler')) {
      console.log(`  ✅ 包含 handler 函數`);
    } else {
      console.log(`  ❌ 缺少 handler 函數`);
      allFilesExist = false;
    }
  } else {
    console.log(`❌ ${file} - 檔案不存在`);
    allFilesExist = false;
  }
});

// 檢查目錄結構
console.log('\n📂 檢查目錄結構...');
const requiredDirs = [
  'api',
  'api/auth',
  'api/auth/line',
  'api/me'
];

requiredDirs.forEach(dir => {
  const dirPath = path.join(__dirname, dir);
  if (fs.existsSync(dirPath)) {
    console.log(`✅ ${dir}/`);
  } else {
    console.log(`❌ ${dir}/ - 目錄不存在`);
    allFilesExist = false;
  }
});

// 檢查是否在根目錄
console.log('\n📍 檢查檔案位置...');
const rootApiPath = path.join(__dirname, 'api');
if (fs.existsSync(rootApiPath)) {
  console.log('✅ api/ 目錄位於專案根目錄');
} else {
  console.log('❌ api/ 目錄不在專案根目錄');
  allFilesExist = false;
}

// 總結
console.log('\n📊 測試結果:');
if (allFilesExist) {
  console.log('🎉 所有 Vercel Functions 都已正確建立！');
  console.log('\n🚀 部署後測試路徑:');
  console.log('1. OIDC 登入: https://anatomy-quiz-bot.vercel.app/api/auth/line/login');
  console.log('2. 用戶統計: https://anatomy-quiz-bot.vercel.app/api/me/stats');
  console.log('3. LIFF 驗證: POST https://anatomy-quiz-bot.vercel.app/api/auth/line/verify');
  console.log('\n🔍 Debug 清單:');
  console.log('✅ 檔案確實位於根目錄 api/');
  console.log('✅ 使用 Vercel Functions 類型 (VercelRequest, VercelResponse)');
  console.log('✅ 所有檔案都包含 handler 函數');
  console.log('\n📝 下一步:');
  console.log('1. 重新部署到 Vercel');
  console.log('2. 在 Vercel Deployment 面板的「Functions」看到 4 支函式');
  console.log('3. 測試 https://anatomy-quiz-bot.vercel.app/api/auth/line/login');
  console.log('4. 確認 LINE Console 的 Callback URL 設定正確');
} else {
  console.log('❌ 部分檢查失敗，請修復後重新測試。');
  process.exit(1);
}

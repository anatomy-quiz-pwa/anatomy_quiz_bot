// test_pages_api.js
// 測試 Pages API 路由是否正確建立

const fs = require('fs');
const path = require('path');

console.log('🧪 Pages API 路由測試');
console.log('====================');

// 檢查必要的檔案是否存在
const requiredFiles = [
  'pages/api/auth/line/login.ts',
  'pages/api/auth/line/callback.ts',
  'pages/api/auth/line/verify.ts',
  'pages/api/me/stats.ts'
];

console.log('\n📁 檢查 Pages API 檔案結構...');
let allFilesExist = true;

requiredFiles.forEach(file => {
  const filePath = path.join(__dirname, file);
  if (fs.existsSync(filePath)) {
    console.log(`✅ ${file}`);
    
    // 檢查檔案內容是否包含必要的函數
    const content = fs.readFileSync(filePath, 'utf8');
    if (file.includes('login.ts')) {
      if (content.includes('export default async function handler')) {
        console.log(`  ✅ 包含 handler 函數`);
      } else {
        console.log(`  ❌ 缺少 handler 函數`);
        allFilesExist = false;
      }
    } else if (file.includes('callback.ts')) {
      if (content.includes('export default async function handler') && content.includes('jwtVerify')) {
        console.log(`  ✅ 包含 handler 函數和 JWT 驗證`);
      } else {
        console.log(`  ❌ 缺少必要功能`);
        allFilesExist = false;
      }
    } else if (file.includes('verify.ts')) {
      if (content.includes('export default async function handler') && content.includes('SignJWT')) {
        console.log(`  ✅ 包含 handler 函數和 JWT 簽章`);
      } else {
        console.log(`  ❌ 缺少必要功能`);
        allFilesExist = false;
      }
    } else if (file.includes('stats.ts')) {
      if (content.includes('export default async function handler') && content.includes('jwtVerify')) {
        console.log(`  ✅ 包含 handler 函數和 JWT 驗證`);
      } else {
        console.log(`  ❌ 缺少必要功能`);
        allFilesExist = false;
      }
    }
  } else {
    console.log(`❌ ${file} - 檔案不存在`);
    allFilesExist = false;
  }
});

// 檢查目錄結構
console.log('\n📂 檢查目錄結構...');
const requiredDirs = [
  'pages',
  'pages/api',
  'pages/api/auth',
  'pages/api/auth/line',
  'pages/api/me'
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

// 總結
console.log('\n📊 測試結果:');
if (allFilesExist) {
  console.log('🎉 所有 Pages API 路由都已正確建立！');
  console.log('\n🚀 測試路徑:');
  console.log('1. OIDC 登入: https://anatomy-quiz-bot.vercel.app/api/auth/line/login');
  console.log('2. 用戶統計: https://anatomy-quiz-bot.vercel.app/api/me/stats');
  console.log('3. LIFF 驗證: POST https://anatomy-quiz-bot.vercel.app/api/auth/line/verify');
  console.log('\n📝 注意事項:');
  console.log('- 確保 Vercel 環境變數已正確設定');
  console.log('- 確保 LINE Console 的 Callback URL 設定正確');
  console.log('- 部署後測試 OIDC 登入流程');
} else {
  console.log('❌ 部分檢查失敗，請修復後重新測試。');
  process.exit(1);
}

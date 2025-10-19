// test_line_login_integration.js
// 簡單的整合測試腳本

const fs = require('fs');
const path = require('path');

console.log('🧪 LINE Login 整合測試');
console.log('====================');

// 檢查必要的檔案是否存在
const requiredFiles = [
  'lib/supabase.ts',
  'lib/session.ts', 
  'lib/users.ts',
  'lib/line_oidc.ts',
  'app/api/auth/line/login/route.ts',
  'app/api/auth/line/callback/route.ts',
  'app/api/auth/line/verify/route.ts',
  'app/api/auth/logout/route.ts',
  'app/api/me/stats/route.ts',
  'app/game-new/page.tsx',
  'app/test-login/page.tsx'
];

console.log('\n📁 檢查檔案結構...');
let allFilesExist = true;

requiredFiles.forEach(file => {
  const filePath = path.join(__dirname, file);
  if (fs.existsSync(filePath)) {
    console.log(`✅ ${file}`);
  } else {
    console.log(`❌ ${file} - 檔案不存在`);
    allFilesExist = false;
  }
});

// 檢查 package.json 依賴
console.log('\n📦 檢查依賴...');
const packageJson = JSON.parse(fs.readFileSync('package.json', 'utf8'));
const requiredDeps = ['@supabase/supabase-js', 'jose', 'next'];

requiredDeps.forEach(dep => {
  if (packageJson.dependencies[dep]) {
    console.log(`✅ ${dep}: ${packageJson.dependencies[dep]}`);
  } else {
    console.log(`❌ ${dep} - 依賴缺失`);
    allFilesExist = false;
  }
});

// 檢查環境變數範例
console.log('\n🔧 檢查環境變數設定...');
if (fs.existsSync('env_example_new.txt')) {
  console.log('✅ 環境變數範例檔案存在');
  const envContent = fs.readFileSync('env_example_new.txt', 'utf8');
  const requiredEnvVars = [
    'LINE_LOGIN_CHANNEL_ID',
    'LINE_LOGIN_CHANNEL_SECRET', 
    'LIFF_ID',
    'APP_SESSION_SECRET',
    'SUPABASE_URL',
    'SUPABASE_SERVICE_KEY',
    'NEXT_PUBLIC_LIFF_ID'
  ];
  
  requiredEnvVars.forEach(envVar => {
    if (envContent.includes(envVar)) {
      console.log(`✅ ${envVar}`);
    } else {
      console.log(`❌ ${envVar} - 環境變數範例缺失`);
      allFilesExist = false;
    }
  });
} else {
  console.log('❌ 環境變數範例檔案不存在');
  allFilesExist = false;
}

// 檢查部署指南
console.log('\n📚 檢查文件...');
if (fs.existsSync('LINE_LOGIN_DEPLOYMENT_GUIDE.md')) {
  console.log('✅ 部署指南存在');
} else {
  console.log('❌ 部署指南不存在');
  allFilesExist = false;
}

if (fs.existsSync('setup_line_login.sh')) {
  console.log('✅ 設定腳本存在');
} else {
  console.log('❌ 設定腳本不存在');
  allFilesExist = false;
}

// 總結
console.log('\n📊 測試結果:');
if (allFilesExist) {
  console.log('🎉 所有檢查都通過！整合準備就緒。');
  console.log('\n🚀 下一步:');
  console.log('1. 在 Vercel Dashboard 設定環境變數');
  console.log('2. 在 LINE Console 設定 Callback URL 和 LIFF');
  console.log('3. 部署到 Vercel');
  console.log('4. 測試 A/B 兩條登入路徑');
} else {
  console.log('❌ 部分檢查失敗，請修復後重新測試。');
  process.exit(1);
}

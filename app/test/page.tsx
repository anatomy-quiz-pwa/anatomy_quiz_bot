export default function TestPage() {
  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>測試頁面</h1>
      <p>如果您能看到這個頁面，說明 Next.js 部署成功！</p>
      <p>時間：{new Date().toLocaleString()}</p>
    </div>
  );
}

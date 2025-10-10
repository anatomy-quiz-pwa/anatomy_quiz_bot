import './globals.css'

export const metadata = {
  title: '解剖咬一口 - Anatomy Bite',
  description: '遊戲化解剖學問答系統，每天學一點解剖、咬一口文獻！',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="zh-TW">
      <body className="font-sans">{children}</body>
    </html>
  )
}

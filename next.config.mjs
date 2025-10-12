/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // 配置靜態文件路由
  async rewrites() {
    return [
      // 直接訪問 HTML 文件
      {
        source: '/leaderboard.html',
        destination: '/public/leaderboard.html',
      },
      {
        source: '/test-simple.html',
        destination: '/public/test-simple.html',
      },
      {
        source: '/game.html',
        destination: '/public/game.html',
      },
      {
        source: '/index.html',
        destination: '/public/index.html',
      },
      // 靜態資源
      {
        source: '/public/:path*',
        destination: '/public/:path*',
      },
      {
        source: '/static/:path*',
        destination: '/static/:path*',
      },
    ];
  },
  async headers() {
    return [
      {
        source: '/public/:path*',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
      {
        source: '/(.*\\.html)',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=3600',
          },
        ],
      },
    ];
  },
};
export default nextConfig;

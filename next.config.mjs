/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // 簡化配置，讓 public/index.html 成為默認首頁
  async rewrites() {
    return [
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
    ];
  },
};
export default nextConfig;

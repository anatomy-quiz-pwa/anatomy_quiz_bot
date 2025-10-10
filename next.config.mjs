/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
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
      {
        source: '/index.html',
        destination: '/public/index.html',
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

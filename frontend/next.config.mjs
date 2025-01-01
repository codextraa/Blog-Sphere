/** @type {import('next').NextConfig} */
const nextConfig = {
  // Set the output configuration to 'standalone'
  output: 'standalone',

  // Add headers to be sent with every response
  async headers() {
    return [
      {
        source: "/(.*)", // Apply to all routes
        headers: [
          { key: "X-Forwarded-Proto", value: "https" }, // Tell Next.js the request is secure
        ],
      },
    ];
  },

  // Enable redirects and rewrites if needed (optional)
  // async redirects() {
  //   return [
  //     {
  //       source: "/old-page",
  //       destination: "/new-page",
  //       permanent: true,
  //     },
  //   ];
  // },

  // // Configure image optimization if you're using Next.js Image component (optional)
  // images: {
  //   domains: ['example.com'], // Add your image domains here
  // },
};

export default nextConfig;

// next.config.mjs
import withPWA from 'next-pwa';

const isProd = process.env.NODE_ENV === 'production';
// Habilita PWA se for produção ou se ENABLE_PWA=true no .env.local
const enablePWA = process.env.ENABLE_PWA === 'true' || isProd;

const nextConfig = {
  reactStrictMode: true,
  experimental: {
    serverActions: { allowedOrigins: ['*'] },
  },
  // (opcional) liberar imagens externas
  // images: { remotePatterns: [{ protocol: 'https', hostname: '**' }] },
};

export default withPWA({
  dest: 'public',
  disable: !enablePWA, // ← chave para ligar/desligar no dev
  register: true,
  skipWaiting: true,
})(nextConfig);

import { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.okastudio.app',          // mude para seu ID de pacote
  appName: 'Oka Studio',
  webDir: 'dist',                      // não será usado, pois vamos apontar para a URL
  server: {
    url: 'https://SEU-PROJETO.vercel.app', // <<< sua URL do Vercel aqui
    cleartext: false                    // HTTPS
  },
  android: {
    allowMixedContent: false
  }
};

export default config;

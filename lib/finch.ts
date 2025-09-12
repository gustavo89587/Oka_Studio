// lib/finch.ts
export type Platform = "LinkedIn" | "Instagram" | "YouTube shorts" | "TikTok";

export function generateCopy(topic: string, platform: Platform) {
  const hooks: Record<Platform, string[]> = {
    LinkedIn: [
      `${topic} pode mudar o futuro das empresas — e quase ninguém percebe.`,
      `Você já parou pra pensar em como ${topic} afeta o seu trabalho?`,
    ],
    Instagram: [
      `⚡ ${topic} em 30 segundos — ninguém te contou isso.`,
      `🚨 O que ninguém fala sobre ${topic}...`,
    ],
    "YouTube shorts": [
      `🔥 ${topic} explicado como nunca antes.`,
      `O segredo por trás de ${topic} que quase ninguém sabe.`,
    ],
    TikTok: [
      `👀 Se você ignorar ${topic}, pode se arrepender depois.`,
      `💡 O truque que muda tudo sobre ${topic}...`,
    ],
  };

  const story = `Imagine um cenário onde ${topic} muda tudo. Poucos acreditam, mas é aí que surge a oportunidade.`;
  const ctas: Record<Platform, string> = {
    LinkedIn: "👉 Me siga e acompanhe insights reais sobre tecnologia e segurança.",
    Instagram: "🔥 Segue a Oka IA e compartilha pra não esquecer!",
    "YouTube shorts": "📌 Inscreva-se no canal e descubra mais hacks de tecnologia.",
    TikTok: "⚡ Curte e segue a Oka IA para mais conteúdos assim!",
  };

  const list = hooks[platform];
  const hook = list[Math.floor(Math.random() * list.length)];
  return `${hook}\n\n${story}\n\n${ctas[platform]}`;
}

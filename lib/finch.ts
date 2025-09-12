// lib/finch.ts

export type Platform = 'LinkedIn' | 'Instagram' | 'YouTube shorts' | 'TikTok';

type CopyOpts = {
  cta?: string;
  tags?: string[];
};

function normalizeHashtags(tags: string[] = []) {
  return tags.map(t => (t.startsWith('#') ? t : `#${t}`)).join(' ');
}

function baseCTA(platform: Platform) {
  switch (platform) {
    case 'LinkedIn':
      return 'Comente "quero" para receber o template completo.';
    case 'Instagram':
      return 'Salve este post e compartilhe com alguém que precisa ver!';
    case 'YouTube shorts':
      return 'Inscreva-se para mais hacks como este.';
    case 'TikTok':
      return 'Segue pra não perder os próximos!';
  }
}

function defaultTags(platform: Platform) {
  switch (platform) {
    case 'LinkedIn':
      return ['ciberseguranca', 'devops', 'carreira', 'okastudio'];
    case 'Instagram':
      return ['reels', 'conteudodigital', 'okastudio', 'marketingdigital'];
    case 'YouTube shorts':
      return ['shorts', 'ai', 'automation', 'okastudio'];
    case 'TikTok':
      return ['fy', 'fyp', 'tech', 'okastudio'];
  }
}

/**
 * Gera uma copy curta no estilo “hook > contexto > prova/valor > CTA + hashtags”
 */
export function generateCopy(topic: string, platform: Platform, opts: CopyOpts = {}): string {
  const cta = opts.cta ?? baseCTA(platform);
  const tags = opts.tags ?? defaultTags(platform);

  const hook = `⚡ ${topic}: o que ninguém te contou`;
  const contexto = `Em ${platform}, quem executa rápido sai na frente. Aqui vai um atalho prático.`;
  const valor = `• O que fazer: explique em 3 passos.\n• O erro comum: a armadilha que trava 90% das pessoas.\n• O truque: um detalhe que dobra seus resultados.`;
  const call = `👉 ${cta}`;
  const hashtags = normalizeHashtags(tags);

  return [hook, '', contexto, '', valor, '', call, '', hashtags].join('\n');
}

// Se em algum lugar você importar default:
export default { generateCopy };

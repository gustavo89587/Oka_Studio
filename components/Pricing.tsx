export default function Pricing() {
  return (
    <section className="relative isolate overflow-hidden bg-neutral-50 py-20">
      <div className="mx-auto max-w-7xl px-6">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-3xl font-bold tracking-tight text-neutral-900 sm:text-4xl">
            Planos do{" "}
            <span className="bg-gradient-to-r from-yellow-600 via-amber-500 to-yellow-400 bg-clip-text text-transparent">
              Oka Studio
            </span>
          </h2>
          <p className="mt-3 text-neutral-600">
            Crie vídeos no padrão Finch com IA, legendas premium e automações —
            do primeiro post ao scale.
          </p>
        </div>

        <div className="mt-12 grid grid-cols-1 gap-6 sm:mt-16 lg:grid-cols-3">
          {/* Free */}
          <div className="rounded-2xl border border-neutral-200 bg-white p-6 shadow-sm">
            <h3 className="text-xl font-semibold text-neutral-900">Free</h3>
            <p className="mt-3 text-sm text-neutral-600">
              Ideal para testar o fluxo e validar criativos.
            </p>
            <div className="mt-6 flex items-end gap-1">
              <span className="text-4xl font-bold text-neutral-900">R$ 0</span>
              <span className="pb-1 text-neutral-500">/ mês</span>
            </div>
            <ul className="mt-6 space-y-2 text-sm text-neutral-700">
              <li>Até 5 vídeos/mês com marca d’água dourada</li>
              <li>Legendas estilo Finch (básico)</li>
              <li>Voz IA padrão</li>
              <li>Backgrounds automáticos (básico)</li>
            </ul>
          </div>

          {/* Pro */}
          <div className="relative rounded-2xl border-2 border-yellow-400 bg-white p-6 shadow-xl">
            <div className="absolute -top-3 right-4 rounded-full bg-gradient-to-r from-yellow-600 via-amber-500 to-yellow-400 px-3 py-1 text-xs font-semibold text-white shadow">
              Mais popular
            </div>
            <h3 className="text-xl font-semibold text-neutral-900">Pro</h3>
            <p className="mt-3 text-sm text-neutral-600">
              Crie em escala sem marca d’água, com vozes premium e exportação
              rápida.
            </p>
            <div className="mt-6 flex items-end gap-1">
              <span className="text-4xl font-bold text-neutral-900">R$ 29</span>
              <span className="pb-1 text-neutral-500">/ mês</span>
            </div>
            <ul className="mt-6 space-y-2 text-sm text-neutral-700">
              <li>Até 50 vídeos/mês, sem marca d’água</li>
              <li>Legendas avançadas (Finch, Impacto, custom)</li>
              <li>Vozes ElevenLabs/Play.ht</li>
              <li>Marca d’água personalizada</li>
              <li>Exportação 1080×1920 acelerada</li>
            </ul>
          </div>

          {/* Business */}
          <div className="rounded-2xl border border-neutral-200 bg-white p-6 shadow-sm">
            <h3 className="text-xl font-semibold text-neutral-900">Business</h3>
            <p className="mt-3 text-sm text-neutral-600">
              Para operações com alto volume, integrações e suporte prioritário.
            </p>
            <div className="mt-6 flex items-end gap-1">
              <span className="text-4xl font-bold text-neutral-900">R$ 99</span>
              <span className="pb-1 text-neutral-500">/ mês</span>
            </div>
            <ul className="mt-6 space-y-2 text-sm text-neutral-700">
              <li>Vídeos ilimitados</li>
              <li>Upload de BGs próprios (vídeo/imagem)</li>
              <li>Integração Instagram/TikTok/YouTube</li>
              <li>API para automação e equipes</li>
              <li>Suporte prioritário</li>
            </ul>
          </div>
        </div>
      </div>
    </section>
  );
}

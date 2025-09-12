import random

def generate_copy(topic: str, platform: str) -> str:
    hooks = {
        "LinkedIn": [
            f"{topic} pode mudar o futuro das empresas — e quase ninguém percebe.",
            f"Você já parou pra pensar em como {topic} afeta o seu trabalho?"
        ],
        "Instagram": [
            f"⚡ {topic} em 30 segundos — ninguém nunca te contou isso.",
            f"🚨 O que ninguém fala sobre {topic}..."
        ],
        "YouTube shorts": [
            f"🔥 {topic} explicado como nunca antes.",
            f"Esse é o segredo por trás de {topic} que quase ninguém sabe."
        ],
        "TikTok": [
            f"👀 Se você ignorar {topic}, pode se arrepender depois.",
            f"💡 O truque que muda tudo sobre {topic}..."
        ]
    }

    story = f"Imagine um cenário onde {topic} muda tudo. Poucos acreditam, mas é aí que surge a oportunidade."
    cta = {
        "LinkedIn": "👉 Me siga e acompanhe insights reais sobre tecnologia e segurança.",
        "Instagram": "🔥 Segue a Oka IA e compartilha pra não esquecer!",
        "YouTube shorts": "📌 Inscreva-se no canal e descubra mais hacks de tecnologia.",
        "TikTok": "⚡ Curte e segue a Oka IA para mais conteúdos assim!"
    }

    hook = random.choice(hooks[platform])
    return f"{hook}\n\n{story}\n\n{cta[platform]}"

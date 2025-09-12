import streamlit as st
import streamlit as st
from pathlib import Path
from oka_core.eleven import list_voices
from oka_core.render import render_video

BUILD_DIR = Path.cwd() / "oka_webui" / "build"

st.set_page_config(page_title="Oka Studio", page_icon="🎬", layout="centered")
st.title("🎬 Oka Studio — Reels/TikTok com ElevenLabs")

@st.cache_data(ttl=600, show_spinner=False)
def fetch_voices():
    try:
        voices = list_voices()  # precisa da permissão voices_read
        # monta rótulo amigável: "Rachel (21m00T...)"
        options = []
        for v in voices:
            vid = v.get("voice_id", "")
            name = v.get("name", "Unknown")
            label = f"{name} ({vid[:7]}…)"
            options.append({"label": label, "voice_id": vid})
        return options
    except Exception as e:
        return st.session_state.get("_voices_cache", []), str(e)

voices_error = None
voices_options = []
try:
    voices_options = fetch_voices()
    st.session_state["_voices_cache"] = voices_options
except Exception as e:
    voices_error = str(e)

with st.form("form"):
    texto = st.text_area(
        "Texto da narração (PT-BR)",
        height=160,
        value="Fala, Gustavo! Este é um teste do Oka Studio."
    )

    # Dropdown de vozes
    if voices_options:
        default_idx = 0  # primeira como padrão
        selected = st.selectbox(
            "Escolha a voz",
            options=list(range(len(voices_options))),
            format_func=lambda i: voices_options[i]["label"],
            index=default_idx
        )
        voice_id = voices_options[selected]["voice_id"]
        st.caption(f"Voice ID selecionado: `{voice_id}`")
    else:
        st.warning("Não consegui carregar a lista de vozes. "
                   "Confira sua API Key e a permissão **voices_read**. "
                   "Você pode colar um Voice ID manualmente abaixo.")
        voice_id = st.text_input(
            "Voice ID (manual, ex.: 21m00Tcm4TLvDq8ikWAM)",
            value="21m00Tcm4TLvDq8ikWAM"
        )

    bg_video = st.text_input("Caminho do vídeo de fundo (opcional)")
    bg_image = st.text_input("Caminho da imagem de fundo (opcional)")

    submitted = st.form_submit_button("Gerar Vídeo")

if submitted:
    if not voice_id.strip():
        st.error("Informe/seleciona uma voz válida.")
    elif not texto.strip():
        st.error("Texto da narração não pode estar vazio.")
    else:
        try:
            with st.spinner("Gerando vídeo..."):
                out_path = render_video(
                    texto=texto.strip(),
                    voice_id=voice_id.strip(),
                    build_dir=BUILD_DIR,
                    bg_video=bg_video.strip() or None,
                    bg_image=bg_image.strip() or None
                )
            st.success("✅ Vídeo pronto!")
            st.video(out_path)
            st.download_button(
                "⬇️ Baixar MP4",
                data=open(out_path, "rb").read(),
                file_name="video.mp4",
                mime="video/mp4"
            )
        except Exception as e:
            st.error(f"Erro: {e}")
            st.stop()

st.divider()
st.caption(f"Saída: {BUILD_DIR}")

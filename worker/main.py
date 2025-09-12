# main.py
import os
import io
import uuid
from typing import Optional, Tuple

from fastapi import FastAPI, Header, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic_settings import BaseSettings

import requests
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from moviepy.editor import ImageClip, ColorClip, CompositeVideoClip


# ===================== Settings =====================
class Settings(BaseSettings):
    # Auth
    WORKER_TOKEN: str = "change-me"

    # ElevenLabs (opcional — TTS real se setar a API key)
    ELEVEN_API_KEY: Optional[str] = None
    ELEVENLABS_VOICE_ID: str = "21m00Tcm4TlvDq8ikWAM"  # Rachel
    ELEVENLABS_MODEL: str = "eleven_multilingual_v2"

    # Saída & URLs
    OUTPUT_DIR: str = "/app/out"
    PUBLIC_BASE_URL: Optional[str] = None  # ex: https://seu-dominio/files

    # App
    DEBUG: bool = False
    ALLOW_ORIGINS: str = "*"  # em produção: defina o domínio do seu app

    class Config:
        env_file = ".env"


settings = Settings()
os.makedirs(settings.OUTPUT_DIR, exist_ok=True)


# ===================== App =====================
app = FastAPI(title="Oka Worker", version="1.3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.ALLOW_ORIGINS.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir arquivos gerados se PUBLIC_BASE_URL não for usado
app.mount("/files", StaticFiles(directory=settings.OUTPUT_DIR), name="files")


# ===================== Helpers =====================
PRESETS = {
    "VERTICAL_9_16": (1080, 1920),
    "SQUARE_1_1": (1080, 1080),
    "PORTRAIT_4_5": (1080, 1350),
    "LANDSCAPE_16_9": (1920, 1080),
}


def require_token(token_header: Optional[str]):
    if not token_header:
        raise HTTPException(401, "Missing worker token")
    if token_header != settings.WORKER_TOKEN:
        raise HTTPException(401, "Invalid worker token")


def resolve_dims(
    width: Optional[int], height: Optional[int], preset: Optional[str]
) -> Tuple[int, int]:
    if preset and preset in PRESETS:
        return PRESETS[preset]
    return (width or 1080, height or 1920)


def public_url(filename: str) -> str:
    """
    Retorna URL pública para um arquivo no OUTPUT_DIR.
    Se PUBLIC_BASE_URL estiver setado, usa ela; caso contrário, usa /files/filename.
    """
    if settings.PUBLIC_BASE_URL:
        base = settings.PUBLIC_BASE_URL.rstrip("/")
        return f"{base}/{filename}"
    return f"/files/{filename}"


def save_bytes(name: str, data: bytes) -> Tuple[str, str]:
    """Salva bytes em OUTPUT_DIR e devolve (path, url)."""
    path = os.path.join(settings.OUTPUT_DIR, name)
    with open(path, "wb") as f:
        f.write(data)
    return path, public_url(name)


# ===================== Rotas básicas =====================
@app.get("/")
def root():
    return {"ok": True, "service": "Oka Worker"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/whoami")
def whoami():
    return {
        "debug": settings.DEBUG,
        "has_eleven": bool(settings.ELEVEN_API_KEY),
        "output_dir": settings.OUTPUT_DIR,
        "public_base_url": settings.PUBLIC_BASE_URL,
    }


# ===================== /tts (ElevenLabs) =====================
@app.post("/tts")
def tts(
    text: str = Form(...),
    x_worker_token: Optional[str] = Header(None),
):
    require_token(x_worker_token)

    if not settings.ELEVEN_API_KEY:
        # modo mock, útil para teste
        mock_name = f"tts_{uuid.uuid4().hex}.txt"
        path, url = save_bytes(mock_name, f"[MOCK TTS] {text}".encode("utf-8"))
        return {"ok": True, "engine": "mock", "audio_url": url, "audio_path": path}

    voice = settings.ELEVENLABS_VOICE_ID
    model = settings.ELEVENLABS_MODEL
    api = f"https://api.elevenlabs.io/v1/text-to-speech/{voice}"

    payload = {"text": text, "model_id": model, "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}}
    headers = {"xi-api-key": settings.ELEVEN_API_KEY, "accept": "audio/mpeg", "content-type": "application/json"}

    r = requests.post(api, json=payload, headers=headers, timeout=180)
    if r.status_code != 200:
        raise HTTPException(r.status_code, r.text)

    name = f"tts_{uuid.uuid4().hex}.mp3"
    path, url = save_bytes(name, r.content)
    return {"ok": True, "engine": "elevenlabs", "audio_url": url, "audio_path": path}


# ===================== /image (PIL) =====================
def draw_prompt_image(prompt: str, w: int, h: int) -> bytes:
    """
    Gera uma imagem simples com fundo gradiente e o prompt escrito (placeholder).
    Substitua por um gerador real quando quiser.
    """
    img = Image.new("RGB", (w, h), (18, 18, 18))
    drw = ImageDraw.Draw(img)

    # gradiente vertical suave
    for y in range(h):
        c = int(18 + (y / max(1, h)) * 40)
        drw.line([(0, y), (w, y)], fill=(c, c, c))

    # moldura
    drw.rectangle([8, 8, w - 9, h - 9], outline=(255, 215, 0), width=3)

    # texto
    try:
        font = ImageFont.truetype("arial.ttf", size=max(20, w // 20))
    except Exception:
        font = ImageFont.load_default()

    # Quebra linha simples
    max_chars = max(10, w // 18)
    words = prompt.split()
    lines = []
    curr = []
    for word in words:
        if len(" ".join(curr + [word])) <= max_chars:
            curr.append(word)
        else:
            lines.append(" ".join(curr))
            curr = [word]
    if curr:
        lines.append(" ".join(curr))

    text = "\n".join(lines[:10])
    tw, th = drw.multiline_textsize(text, font=font, spacing=6)
    pos = ((w - tw) // 2, (h - th) // 2)
    drw.multiline_text(pos, text, font=font, fill=(255, 255, 255), align="center", spacing=6)

    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


@app.post("/image")
def image(
    prompt: str = Form(...),
    width: Optional[int] = Form(None),
    height: Optional[int] = Form(None),
    preset: Optional[str] = Form(None),
    x_worker_token: Optional[str] = Header(None),
):
    require_token(x_worker_token)
    w, h = resolve_dims(width, height, preset)
    png = draw_prompt_image(prompt, w, h)
    name = f"img_{w}x{h}_{uuid.uuid4().hex}.png"
    path, url = save_bytes(name, png)
    return {"ok": True, "image_url": url, "image_path": path, "width": w, "height": h, "preset": preset}


# ===================== /video (MoviePy) =====================
def render_video(
    text: str, w: int, h: int, bg_path: Optional[str], seconds: int = 6
) -> Tuple[str, str]:
    """
    Render simples:
    - BG a partir da imagem enviada (redimensiona) ou cor sólida dark
    - Texto central desenhado via PIL para evitar dependência do ImageMagick
    """
    if bg_path:
        bg_clip = ImageClip(bg_path).resize(newsize=(w, h)).set_duration(seconds)
    else:
        bg_clip = ColorClip(size=(w, h), color=(15, 15, 15)).set_duration(seconds)

    # cria uma "faixa" de texto com PIL -> np.ndarray
    def make_text_frame() -> np.ndarray:
        pad = 40
        canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        drw = ImageDraw.Draw(canvas)
        try:
            font = ImageFont.truetype("arial.ttf", size=max(28, w // 18))
        except Exception:
            font = ImageFont.load_default()

        # quebra linhas
        max_chars = max(10, w // 16)
        words = str(text).split()
        lines, curr = [], []
        for word in words:
            if len(" ".join(curr + [word])) <= max_chars:
                curr.append(word)
            else:
                lines.append(" ".join(curr))
                curr = [word]
        if curr:
            lines.append(" ".join(curr))
        block = "\n".join(lines[:10])

        tw, th = drw.multiline_textsize(block, font=font, spacing=6)
        x = (w - tw) // 2
        y = (h - th) // 2
        # fundo semi-transparente
        drw.rectangle([x - pad, y - pad, x + tw + pad, y + th + pad], fill=(0, 0, 0, 140))
        drw.multiline_text((x, y), block, font=font, fill=(255, 255, 255, 255), align="center", spacing=6)
        return np.array(canvas)

    txt_clip = ImageClip(make_text_frame()).set_duration(seconds)
    final = CompositeVideoClip([bg_clip, txt_clip])

    name = f"video_{w}x{h}_{uuid.uuid4().hex}.mp4"
    out_path = os.path.join(settings.OUTPUT_DIR, name)
    final.write_videofile(
        out_path,
        fps=30,
        codec="libx264",
        audio=False,        # plugue o áudio do TTS aqui quando quiser
        preset="medium",
        verbose=False,
        logger=None,
    )
    return out_path, public_url(name)


@app.post("/video")
async def video(
    text: str = Form(...),
    width: Optional[int] = Form(None),
    height: Optional[int] = Form(None),
    preset: Optional[str] = Form(None),
    bg_image: UploadFile | None = File(None),
    x_worker_token: Optional[str] = Header(None),
):
    require_token(x_worker_token)
    w, h = resolve_dims(width, height, preset)

    tmp_bg_path = None
    try:
        if bg_image is not None:
            raw = await bg_image.read()
            tmp_bg_name = f"bg_{uuid.uuid4().hex}.png"
            tmp_bg_path = os.path.join(settings.OUTPUT_DIR, tmp_bg_name)
            with open(tmp_bg_path, "wb") as f:
                f.write(raw)

        out_path, url = render_video(text, w, h, tmp_bg_path)
        return {"ok": True, "video_url": url, "video_path": out_path, "width": w, "height": h, "preset": preset}
    finally:
        try:
            if tmp_bg_path and os.path.exists(tmp_bg_path):
                os.remove(tmp_bg_path)
        except Exception:
            pass

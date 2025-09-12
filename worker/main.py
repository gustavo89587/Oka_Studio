import os
from fastapi import FastAPI, Header, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    WORKER_TOKEN: str = "troque-por-um-token-forte-aqui"
    DEBUG: bool = True

settings = Settings()

app = FastAPI(title="Oka Worker", version="1.0.0")

# Libera o frontend (Vercel / app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # se quiser restringir depois, troque por seu domínio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def check_token(x_worker_token: str | None):
    if not x_worker_token or x_worker_token != settings.WORKER_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid worker token")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/tts")
async def tts(text: str = Form(...), x_worker_token: str | None = Header(None)):
    check_token(x_worker_token)
    # TODO: chamar ElevenLabs/Play.ht aqui e devolver URL/bytes do áudio
    return {"ok": True, "audio_url": "https://exemplo.com/narracao.mp3"}

@app.post("/image")
async def image(prompt: str = Form(...), x_worker_token: str | None = Header(None)):
    check_token(x_worker_token)
    # TODO: gerar imagem (ou chamar seu serviço) e devolver URL
    return {"ok": True, "image_url": "https://exemplo.com/imagem.png"}

@app.post("/video")
async def video(
    text: str = Form(...),
    bg_video: UploadFile | None = File(None),
    bg_image: UploadFile | None = File(None),
    x_worker_token: str | None = Header(None)
):
    check_token(x_worker_token)
    # TODO: montar pipeline (TTS -> legendas -> FFmpeg/MoviePy), salvar e devolver URL
    return {"ok": True, "video_url": "https://exemplo.com/video.mp4"}

import os, json, requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY") or ""
BASE_URL = "https://api.elevenlabs.io/v1"

DEFAULT_MODEL_ID = "eleven_turbo_v2_5"
DEFAULT_VOICE_SETTINGS = {
    "stability": 0.45,
    "similarity_boost": 0.85,
    "style": 0.15,
    "use_speaker_boost": True
}

def _headers(accept: str | None = None) -> dict:
    if not ELEVEN_API_KEY:
        raise RuntimeError("ELEVEN_API_KEY não encontrada (.env).")
    h = {"xi-api-key": ELEVEN_API_KEY}
    if accept:
        h["accept"] = accept
    return h

def list_voices() -> list[dict]:
    r = requests.get(f"{BASE_URL}/voices", headers=_headers())
    r.raise_for_status()
    data = r.json()
    return data.get("voices", data)

def generate_tts(
    text: str,
    voice_id: str,
    out_path: str | Path,
    model_id: str = DEFAULT_MODEL_ID,
    voice_settings: dict = None
) -> str:
    if not text.strip():
        raise ValueError("Texto vazio.")
    if not voice_id.strip():
        raise ValueError("voice_id vazio.")
    out_path = Path(out_path).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    url = f"{BASE_URL}/text-to-speech/{voice_id}"
    payload = {
        "model_id": model_id,
        "text": text,
        "voice_settings": voice_settings or DEFAULT_VOICE_SETTINGS
    }
    headers = _headers(accept="audio/mpeg")
    headers["Content-Type"] = "application/json"

    r = requests.post(url, headers=headers, data=json.dumps(payload), stream=True, timeout=120)
    if r.status_code != 200:
        try:
            detail = r.json()
        except Exception:
            detail = r.text
        raise RuntimeError(f"TTS {r.status_code}: {detail}")

    with open(out_path, "wb") as f:
        for chunk in r.iter_content(8192):
            if chunk:
                f.write(chunk)
    return str(out_path)

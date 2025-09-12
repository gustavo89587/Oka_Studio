import os
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="OKA Worker")

class Narration(BaseModel):
    text: str

@app.get("/healthz")
def healthz():
    return {
        "status": "ok",
        "engine": "oka-worker",
        "env": {
            "ELEVENLABS_API_KEY": bool(os.getenv("ELEVENLABS_API_KEY")),
            "OPENAI_API_KEY": bool(os.getenv("OPENAI_API_KEY")),
        },
    }

@app.post("/narrate")
def narrate(n: Narration):
    return {"ok": True, "preview": n.text.upper()}

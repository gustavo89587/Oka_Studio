from pathlib import Path
from typing import List, Tuple
from moviepy.editor import (
    ColorClip, ImageClip, VideoFileClip, AudioFileClip,
    TextClip, CompositeVideoClip, vfx
)
from .eleven import generate_tts

W, H = 1080, 1920
FONT = "Arial-Bold"
FG_COLOR = "white"
STROKE_COLOR = "black"
STROKE_WIDTH = 4
BOX_PAD = 16
LINE_GAP = 18
POP_SCALE = 1.08
EMPHASIS_COLOR = "#FFD400"

def chunk_text(text: str) -> List[str]:
    import re
    words = re.findall(r"\w+[\w’']*|[.,!?;:]", text, flags=re.UNICODE)
    chunks, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) >= 5 or (w in [".", "!", "?", ";", ":"] and len(cur) >= 2):
            chunks.append(" ".join(cur))
            cur = []
    if cur: chunks.append(" ".join(cur))
    return chunks

def distribute_times(chunks: List[str], audio_dur: float) -> List[Tuple[float, float]]:
    weights = [max(1, len(c)) for c in chunks]
    total = sum(weights)
    times, t = [], 0.0
    for w in weights:
        dur = max(0.6, audio_dur * (w / total))
        times.append((t, t + dur))
        t += dur
    if times:
        s, _ = times[-1]
        times[-1] = (s, audio_dur)
    return times

def make_caption_clip(text: str, start: float, end: float):
    words = text.split()
    styled = []
    for w in words:
        raw = w.strip()
        is_emph = (len(raw) >= 6) or raw.isupper()
        if is_emph:
            styled.append(f"<span backgroundcolor='{EMPHASIS_COLOR}'>{raw.upper()}</span>")
        else:
            styled.append(raw.upper())
    html = " ".join(styled)

    txt = TextClip(
        txt=html, method="caption", size=(W - 160, None),
        font=FONT, color=FG_COLOR, stroke_color=STROKE_COLOR, stroke_width=STROKE_WIDTH,
        fontsize=72, align="center", interline=LINE_GAP, bg_color=None
    )
    box = ColorClip(size=(int(txt.w + 2*BOX_PAD), int(txt.h + 2*BOX_PAD)), color=(0, 0, 0)).set_opacity(0.35)
    x = (W - box.w)//2; y = int(H*0.70) - box.h//2
    boxed = CompositeVideoClip([box.set_position((x,y)), txt.set_position((x+BOX_PAD, y+BOX_PAD))])

    pop = boxed.fx(vfx.resize, POP_SCALE).set_start(start).set_end(min(end, start+0.2))
    normal = boxed.set_start(min(end, start+0.2)).set_end(end)
    return CompositeVideoClip([pop, normal])

def render_video(
    texto: str,
    voice_id: str,
    build_dir: Path,
    bg_video: str | None = None,
    bg_image: str | None = None
) -> str:
    build_dir = Path(build_dir)
    build_dir.mkdir(parents=True, exist_ok=True)
    mp3_path = build_dir / "narracao.mp3"
    video_out = build_dir / "video.mp4"

    generate_tts(texto, voice_id=voice_id, out_path=mp3_path)

    if bg_video and Path(bg_video).exists():
        base = VideoFileClip(bg_video).without_audio().resize(height=H)
        base = base.crop(width=W, height=H, x_center=base.w/2, y_center=base.h/2)
    elif bg_image and Path(bg_image).exists():
        base = ImageClip(bg_image).resize(height=H).crop(width=W, height=H, x_center=W/2, y_center=H/2).set_duration(1)
    else:
        base = ColorClip(size=(W,H), color=(12,12,16)).set_duration(1)

    audio = AudioFileClip(str(mp3_path))
    dur = audio.duration
    base = base.set_duration(dur)

    chunks = chunk_text(texto)
    times = distribute_times(chunks, dur)
    captions = [make_caption_clip(c, t0, t1) for c, (t0,t1) in zip(chunks, times)]

    final = CompositeVideoClip([base] + captions).set_audio(audio)
    final.write_videofile(
        str(video_out),
        fps=30, codec="libx264", audio_codec="aac",
        bitrate="6000k", preset="medium", threads=4
    )
    return str(video_out)

# main_all.py — Oka Studio: render rápido sem TTS
# Dependências: moviepy, pillow
# pip install moviepy pillow




import os
import random
import subprocess
from pathlib import Path

def add_bg_music(input_video: str, output_video: str, music_dir: str = "assets/music"):
    """
    Adiciona música de fundo com leve ducking (abaixa a trilha quando há narração).
    Se não encontrar músicas, apenas copia o vídeo de entrada para a saída.
    """
    # coleta faixas
    tracks = [str(Path(music_dir)/f) for f in os.listdir(music_dir)
              if f.lower().endswith((".mp3", ".wav", ".m4a"))] if os.path.isdir(music_dir) else []

    if not tracks:
        # Sem trilha? Copia o vídeo
        subprocess.run(["ffmpeg","-y","-i",input_video,"-c","copy",output_video], check=True)
        return

    music = random.choice(tracks)

    # Mix: vídeo (0) + música (1)
    # - Música reduzida ~ -18 dB
    # - amix faz a mistura; dropout_transition suaviza alternância
    # Obs.: Se sua narração já está embutida no vídeo (pista 0:a), o ducking simples funciona bem.
    subprocess.run([
        "ffmpeg","-y",
        "-i", input_video,
        "-i", music,
        "-filter_complex",
        "[1:a]volume=-18dB[a1];"              # abaixa volume da música
        "[0:a][a1]amix=inputs=2:duration=first:dropout_transition=2,volume=1.0[aout]",
        "-map", "0:v",                         # usa o vídeo original
        "-map", "[aout]",                      # usa o áudio mixado
        "-c:v", "copy",                        # não reencodeia o vídeo
        "-c:a", "aac", "-b:a", "160k",         # áudio AAC
        output_video
    ], check=True)


import subprocess

def add_watermark(input_video, output_video, watermark="assets/logo/oka_watermark.png"):
    cmd = [
        "ffmpeg", "-i", input_video, "-i", watermark,
        "-filter_complex", "overlay=W-w-20:H-h-20",
        "-codec:a", "copy", output_video
    ]
    subprocess.run(cmd, check=True)

def add_watermark(input_video, output_video, watermark="assets/logo/oka_watermark.png"):
    subprocess.run([
        "ffmpeg","-y",
        "-i", input_video, "-i", watermark,
        "-filter_complex","overlay=W-w-20:H-h-20",
        "-c:a","copy",
        output_video
    ], check=True)

import argparse, os, sys, textwrap
from pathlib import Path
from datetime import datetime

from moviepy.editor import (
    VideoFileClip, ImageClip, ColorClip, CompositeVideoClip, vfx
)

try:
    from PIL import Image, ImageDraw, ImageFont
except Exception as e:
    print("[ERRO] Pillow não instalado. Rode: pip install pillow")
    sys.exit(1)

def parse_size(s: str):
    try:
        w, h = s.lower().split("x")
        return int(w), int(h)
    except:
        raise argparse.ArgumentTypeError("Use o formato LARGURAxALTURA, ex: 1080x1920")

def wrap_text(text, width=22):
    # quebra agressiva pra caber em 1080x1920 com fonte grande
    return "\n".join(textwrap.wrap(text, width=width, break_long_words=True))

def make_text_image(
    text: str,
    size: tuple[int, int],
    font_path: str | None = None,
    base_color=(255, 255, 255),
    stroke_color=(0, 0, 0),
    stroke=4,
    style="finch",
):
    W, H = size
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # tenta achar uma fonte boa; senão usa default
    font = None
    if font_path and Path(font_path).exists():
        try:
            font = ImageFont.truetype(font_path, size=72)
        except:
            font = None
    if font is None:
        # tenta Arial comum do Windows
        for candidate in [
            r"C:\Windows\Fonts\arialbd.ttf",
            r"C:\Windows\Fonts\arial.ttf",
            r"C:\Windows\Fonts\segoeuib.ttf",
            r"C:\Windows\Fonts\segoeui.ttf",
        ]:
            if Path(candidate).exists():
                try:
                    font = ImageFont.truetype(candidate, size=72)
                    break
                except:
                    pass
    if font is None:
        font = ImageFont.load_default()

    # estilos rápidos
    KEY_RED = (255, 59, 48)
    KEY_YEL = (255, 214, 10)

    wrapped = wrap_text(text, width=22 if style == "finch" else 28)
    lines = wrapped.split("\n")

    # mede bloco
    line_h = int(font.size * 1.25)
    block_h = line_h * len(lines)
    y = (H - block_h) // 2  # centralizado vertical

    # realce de algumas palavras (Finch vibe)
    keywords_yel = {"AGORA", "AGORA MESMO", "DADOS", "2FA", "AÇÃO"}
    keywords_red = {"ROUBADOS", "ATAQUES", "95%", "PERIGO", "ALERTA"}

    for line in lines:
        w, _ = draw.textbbox((0, 0), line, font=font)[2:]
        x = (W - w) // 2  # centralizado horizontal
        # desenha com stroke
        # para realce simples: pinta palavras-chave dentro da linha
        if style == "finch":
            # separa por espaços mantendo posições
            cursor_x = x
            for token in line.split(" "):
                token_disp = token.strip()
                color = base_color
                up = token_disp.upper().strip(",.?!…")
                if up in keywords_yel:
                    color = KEY_YEL
                elif up in keywords_red:
                    color = KEY_RED
                # medida do token
                tw, th = draw.textbbox((0, 0), token + " ", font=font)[2:]
                # stroke
                if stroke > 0:
                    draw.text((cursor_x, y), token + " ", font=font, fill=stroke_color, stroke_width=stroke, stroke_fill=stroke_color)
                # frente
                draw.text((cursor_x, y), token + " ", font=font, fill=color)
                cursor_x += tw
        else:
            if stroke > 0:
                draw.text((x, y), line, font=font, fill=stroke_color, stroke_width=stroke, stroke_fill=stroke_color)
            draw.text((x, y), line, font=font, fill=base_color)
        y += line_h

    return img

def load_background(size, bg_video, bg_image, duration):
    W, H = size
    if bg_video and Path(bg_video).exists():
        clip = VideoFileClip(bg_video).fx(vfx.loop, duration=duration)
        # letterbox/cover
        clip = clip.resize(width=W) if clip.h <= H else clip.resize(height=H)
        clip = clip.crop(x_center=clip.w/2, y_center=clip.h/2, width=W, height=H)
        return clip.set_duration(duration).set_fps(30)
    if bg_image and Path(bg_image).exists():
        img = ImageClip(bg_image).set_duration(duration)
        img = img.resize(height=H) if img.w < W else img.resize(width=W)
        return img.crop(x_center=img.w/2, y_center=img.h/2, width=W, height=H)
    # fallback sólido
    return ColorClip(size=(W, H), color=(11, 18, 33), duration=duration).set_fps(30)

def main():
    ap = argparse.ArgumentParser(description="Oka Studio — render rápido (sem TTS)")
    ap.add_argument("--text", required=True, help="Texto/Copy para sobrepor")
    ap.add_argument("--bg-video", dest="bg_video", default=None, help="Caminho do vídeo de fundo")
    ap.add_argument("--bg-image", dest="bg_image", default=None, help="Caminho da imagem de fundo")
    ap.add_argument("--size", type=parse_size, default="1080x1920", help="Ex.: 1080x1920 (padrão)")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--duration", type=int, default=15, help="Duração em segundos (padrão: 15)")
    ap.add_argument("--sub-style", default="finch", choices=["finch", "impacto", "basic"])
    ap.add_argument("--out", required=False, default=None, help="Arquivo de saída .mp4")
    # argumentos ignorados (compatibilidade com seus BATs)
    ap.add_argument("--tts-engine", default="", help=argparse.SUPPRESS)
    ap.add_argument("--voice-id", default="", help=argparse.SUPPRESS)

    args = ap.parse_args()

    W, H = args.size if isinstance(args.size, tuple) else parse_size(str(args.size))
    out = Path(args.out) if args.out else Path("out") / f"shorts_{datetime.now():%Y%m%d_%H%M%S}.mp4"
    out.parent.mkdir(parents=True, exist_ok=True)

    print("[OKA] Iniciando render")
    print("[OKA] Texto:", args.text[:120] + ("..." if len(args.text) > 120 else ""))
    print("[OKA] Saída:", out.resolve())

    # fundo
    bg = load_background((W, H), args.bg_video, args.bg_image, args.duration)

    # camada de texto (imagem RGBA -> ImageClip)
    txt_img = make_text_image(
        text=args.text,
        size=(W, H),
        style=args.sub_style
    )
    txt_clip = ImageClip(txt_img).set_duration(min(8, args.duration))\
                                 .set_position(("center", "center"))\
                                 .crossfadein(0.3).crossfadeout(0.3)

    # leve vignette fake (overlay sem precisar filtros do ffmpeg)
    overlay = ColorClip((W, H), color=(0,0,0)).set_opacity(0.15).set_duration(args.duration)

    final = CompositeVideoClip([bg, overlay, txt_clip]).set_duration(args.duration)

    # exporta
    try:
        final.write_videofile(
            str(out),
            codec="libx264",
            audio=False,
            fps=args.fps,
            preset="medium",
            threads=4,
            verbose=True,
        )
        print("[OKA] Concluído em:", out.resolve())
    except Exception as e:
        print("[ERRO] Falha ao exportar:", e)
        sys.exit(1)

if __name__ == "__main__":
    main()

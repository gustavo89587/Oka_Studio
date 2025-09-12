import os
import subprocess
from oka_copybot import generate_copy
from main_all import add_watermark
from main_all import add_watermark, add_bg_music  # <— importe aqui

def run_video(text: str, platform: str):
    bg = build_bg_mix(duration=30.0, out=Path("build/bg_mix.mp4"))
    tmp = f"out/oka_{platform.lower()}.mp4"
    with_music = f"out/oka_{platform.lower()}_music.mp4"
    final = f"out/oka_{platform.lower()}_final.mp4"

    subprocess.run([
        "python","main_all.py",
        "--text", text,
        "--sub-style","finch",
        "--bg-video", str(bg),
        "--size","1080x1920",
        "--duration","30",
        "--out", tmp
    ], check=True)

    # Música de fundo
    add_bg_music(tmp, with_music, "assets/music")

    # Watermark
    add_watermark(with_music, final)
    print("✅ Vídeo pronto:", final)

from oka_bg import build_bg_mix
from pathlib import Path



def run_video(text: str, platform: str):
    bg_mix = build_bg_mix(duration=30.0, out_path=Path("build/bg_mix.mp4"))
    temp_video = f"out/oka_{platform.lower()}.mp4"
    final_video = f"out/oka_{platform.lower()}_final.mp4"

    cmd = [
        "python", "main_all.py",
        "--text", text,
        "--sub-style", "finch",
        "--bg-video", str(bg_mix),
        "--size", "1080x1920",
        "--duration", "30",
        "--out", temp_video
    ]

    subprocess.run(cmd, check=True)
    add_watermark(temp_video, final_video)
    print(f"✅ Vídeo final pronto: {final_video}")

def main():
    platforms = ["LinkedIn", "Instagram", "YouTube shorts", "TikTok"]
    for i, p in enumerate(platforms, start=1):
        print(f"{i}. {p}")

    choice = int(input("\nEscolha a plataforma: "))
    platform = platforms[choice - 1]
    topic = input("\nDigite o tema: ")

    text = generate_copy(topic, platform)
    print("\n📝 Copy gerada:\n", text)

    if input("\nGerar vídeo? (s/n): ").lower() == "s":
        run_video(text, platform)

if __name__ == "__main__":
    main()

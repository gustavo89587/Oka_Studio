import os, random, shutil, subprocess
from pathlib import Path
SUP_V = (".mp4",".mov",".mkv",".webm")
SUP_I = (".png",".jpg",".jpeg",".webp")
BG_ROOT = Path("assets/bg"); TMP = Path("build/tmp_bg"); TMP.mkdir(parents=True, exist_ok=True)
def ff(*a): subprocess.run(["ffmpeg","-y",*a], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
def collect():
    vids, imgs = [], []
    for base,_,files in os.walk(BG_ROOT) if BG_ROOT.exists() else []:
        for f in files:
            p = Path(base)/f; ext = p.suffix.lower()
            (vids if ext in SUP_V else imgs if ext in SUP_I else []).append(p)
    return vids, imgs
def make_from_img(img, out, length=6.0):
    ff("-loop","1","-t",str(length),"-i",str(img),
       "-filter_complex","scale=1080:1920:force_original_aspect_ratio=cover,zoompan=z='min(zoom+0.0015,1.05)':d=900:s=1080x1920:fps=30",
       "-pix_fmt","yuv420p","-an",str(out))
def transcode_clip(src, out, length=6.0):
    ff("-t",str(length),"-i",str(src),
       "-vf","scale=1080:1920:force_original_aspect_ratio=cover,fps=30",
       "-pix_fmt","yuv420p","-an","-c:v","libx264","-preset","veryfast","-crf","20",str(out))
def build_bg_mix(duration=30.0, out=Path("build/bg_mix.mp4"), minc=4, maxc=8):
    if out.exists(): out.unlink()
    if TMP.exists(): shutil.rmtree(TMP); TMP.mkdir(parents=True, exist_ok=True)
    vids, imgs = collect(); srcs = vids + imgs
    if not srcs: raise RuntimeError("Adicione vídeos/imagens em assets/bg")
    total=0.0; chunks=[]; i=0
    while total < duration + minc:
        s = random.choice(srcs); seg = float(random.randint(minc, maxc)); tmp = TMP/f"seg_{i:02d}.mp4"
        (transcode_clip if s.suffix.lower() in SUP_V else make_from_img)(s, tmp, seg)
        chunks.append(tmp); total += seg; i += 1
    lst = TMP/"list.txt"
    with open(lst,"w",encoding="utf-8") as f:
        for c in chunks: f.write(f\"file '{c.as_posix()}'\\n\")
    concat = TMP/"concat.mp4"; ff("-f","concat","-safe","0","-i",str(lst),"-c","copy",str(concat))
    ff("-t",str(duration),"-i",str(concat),"-vf","gblur=sigma=0.1","-pix_fmt","yuv420p","-c:v","libx264","-preset","veryfast","-crf","20","-an",str(out))
    return out
if __name__ == "__main__": print("[OK]", build_bg_mix())

from moviepy.editor import TextClip, CompositeVideoClip, ColorClip
from pathlib import Path

# Texto de teste
texto = "Abertura de impacto"

# Arquivo de saída
out = Path("out/test_ok.mp4")
out.parent.mkdir(parents=True, exist_ok=True)

# Fundo sólido 1080x1920 (15s)
bg = ColorClip(size=(1080,1920), color=(11,18,33), duration=15).set_fps(30)

# Texto central
txt = TextClip(texto, fontsize=70, color='white', size=(1000, None), method='caption')
txt = txt.set_position('center').set_duration(5)

# Monta vídeo
final = CompositeVideoClip([bg, txt])

print("[OKA] Salvando em:", out.resolve())
final.write_videofile(str(out), codec="libx264", audio=False, fps=30, preset="medium")

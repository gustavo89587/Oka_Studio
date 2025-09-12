# Oka Worker - Dockerfile
FROM python:3.11-slim

# Dependências do sistema (FFmpeg p/ vídeo/áudio)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código
COPY . .

# Railway expõe a porta em $PORT (variável já definida lá)
ENV PORT=8000

# Sobe o servidor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]

@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"

if not exist "out" mkdir "out"
if not exist "assets\bg" mkdir "assets\bg"

rem ---> AJUSTE o caminho do seu ffmpeg aqui, se precisar
set "IMAGEIO_FFMPEG_EXE=C:\ProgramData\chocolatey\bin\ffmpeg.exe"

echo [OKA] Verificando FFmpeg...
"%IMAGEIO_FFMPEG_EXE%" -hide_banner -version >nul 2>&1 || (
  echo [ERRO] FFmpeg nao encontrado em: %IMAGEIO_FFMPEG_EXE%
  pause & exit /b 1
)

set /p COPY=Digite/cole a copy: 

for /f %%i in ('powershell -NoProfile -Command "(Get-Date).ToString(\"yyyyMMdd_HHmmss\")"') do set "TS=%%i"
set "OUT=%cd%\out\shorts_%TS%.mp4"

set /p BGP=Arraste/cole o caminho ABSOLUTO do fundo (video .mp4 ou imagem .jpg/.png): 

echo [OKA] Saida: %OUT%
echo [OKA] Fundo: %BGP%
echo [OKA] Iniciando...

set "PY=python"
if exist "venv\Scripts\python.exe" set "PY=venv\Scripts\python.exe"

set LOG=out\log_%TS%.txt
echo [OKA] Log: %LOG%

"%PY%" "main_all.py" ^
  --text "%COPY%" ^
  --tts-engine elevenlabs ^
  --voice-id "21m00Tcm4TLvDq8ikWAM" ^
  --sub-style finch ^
  --size 1080x1920 ^
  --fps 30 ^
  --out "%OUT%" ^
  --bg-video "%BGP%" > "%LOG%" 2>&1

if errorlevel 1 (
  echo [ERRO] Falhou. Veja o log: %LOG%
) else (
  if exist "%OUT%" (
    echo [OK] Video gerado: "%OUT%"
  ) else (
    echo [WARN] Sem erro, mas o arquivo nao apareceu. Abra o log: %LOG%
  )
)
pause

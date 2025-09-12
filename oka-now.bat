@echo off
title Oka Studio - NOW
cd /d "%~dp0"

if not exist "out" mkdir "out"

:: Python (usa venv se existir)
set "PY=python"
if exist "venv\Scripts\python.exe" set "PY=venv\Scripts\python.exe"

echo =======================================
echo   Oka Studio - Gerador RÁPIDO
echo =======================================
echo.

set /p COPY=Digite/cole a copy: 

:: Timestamp simples (yyyyMMdd_HHmmss)
for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd_HHmmss"') do set "TS=%%i"
if "%TS%"=="" set "TS=default"

set "OUT=out\shorts_%TS%.mp4"

echo.
echo ====== RENDER ======
echo Copy   : %COPY%
echo Saida  : %OUT%
echo.

"%PY%" "main_all.py" ^
  --text "%COPY%" ^
  --tts-engine elevenlabs ^
  --voice-id "21m00Tcm4TLvDq8ikWAM" ^
  --sub-style finch ^
  --bg-video "assets\bg\cyber_glow.mp4" ^
  --size 1080x1920 ^
  --fps 30 ^
  --out "%OUT%"

echo.
if exist "%OUT%" (
  echo ✅ Video gerado: "%OUT%"
) else (
  echo ⚠ Nenhum arquivo encontrado em %OUT%.
)
pause

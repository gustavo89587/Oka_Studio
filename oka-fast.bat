@echo off
setlocal EnableExtensions EnableDelayedExpansion
title Oka Studio - FAST
cd /d "%~dp0"

:: Pastas
if not exist "out" mkdir "out"
if not exist "assets\bg" mkdir "assets\bg"

:: Python preferencial do venv
set "PY=python"
if exist "venv\Scripts\python.exe" set "PY=venv\Scripts\python.exe"

:: === Carrega config padrão ===
set "CFG=oka-studio.config"
if not exist "%CFG%" (
  echo [ERRO] Nao achei %CFG%. Crie o arquivo oka-studio.config
  pause & exit /b 1
)

for /f "usebackq tokens=* delims=" %%L in ("%CFG%") do (
  set "LINE=%%L"
  if not "!LINE!"=="" if /i not "!LINE:~0,1!"=="#" (
    for /f "tokens=1,2 delims==" %%A in ("!LINE!") do (
      set "%%A=%%B"
    )
  )
)

:: === Mostra resumo ===
echo =======================================
echo  Oka Studio - FAST (Defaults do config)
echo =======================================
echo TTS      : %TTS%
echo VOICE_ID : %VOICE_ID%
echo SUB      : %SUB_STYLE%
echo MODE     : %MODE%
echo BG PATH  : %BG_PATH%
echo SIZE/FPS : %SIZE% / %FPS%
echo =======================================
echo.

:: === Copy ===
set /p COPY=Digite/cole a copy: 

:: === Timestamp seguro ===
for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd_HHmmss"') do set "TS=%%i"

if "%TS%"=="" (
  echo [WARN] Nao consegui gerar timestamp, usando nome default.
  set "OUT=%cd%\out\shorts_default.mp4"
) else (
  set "OUT=%cd%\out\shorts_%TS%.mp4"
)

:: === Define flag de fundo ===
if /i "%MODE%"=="image" (
  set "BGFLAG=--bg-image"
) else (
  set "BGFLAG=--bg-video"
)

:: === Execucao ===
echo.
echo ====== RENDER ======
echo TTS    : %TTS%   (VOICE_ID=%VOICE_ID%)
echo SUB    : %SUB_STYLE%
echo BG     : %BGFLAG% "%BG_PATH%"
echo SIZE   : %SIZE%  FPS=%FPS%
echo OUT    : %OUT%
echo.

set "TTSARGS="
if not "%TTS%"=="" set "TTSARGS=--tts-engine %TTS%"
set "VOICEARGS="
if not "%VOICE_ID%"=="" set "VOICEARGS=--voice-id %VOICE_ID%"

"%PY%" "main_all.py" ^
  --text "%COPY%" ^
  %TTSARGS% ^
  %VOICEARGS% ^
  --sub-style %SUB_STYLE% ^
  %BGFLAG% "%BG_PATH%" ^
  --size %SIZE% ^
  --fps %FPS% ^
  --out "%OUT%"

echo.
if exist "%OUT%" (
  echo ✅ Video gerado com sucesso: "%OUT%"
) else (
  echo ⚠ Concluiu sem erro, mas o arquivo nao apareceu.
)

pause

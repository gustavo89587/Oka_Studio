@echo off
REM Ativa ambiente e roda o Oka Studio no Streamlit

cd /d "C:\Users\GUSTAVO\Desktop\Oka video Maker\Oka_Studio"

echo ========================================
echo 🚀 Iniciando Oka Studio em localhost:8501
echo ========================================

REM se quiser forçar o Python do sistema use "py" no lugar de "python"
python -m streamlit run app.py

pause

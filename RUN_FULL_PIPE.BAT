@echo off
echo 🕒 Iniciando pipeline de análisis de vacantes...

cd /d C:\Users\aviau\DEV\ai-job-analyzer

REM Activar entorno virtual
call .venv\Scripts\activate.bat

REM Ejecutar el pipeline completo
echo 🚀 Ejecutando run_pipeline.py ...
python run_full_pipe.py

echo ✅ Pipeline finalizado.
pause


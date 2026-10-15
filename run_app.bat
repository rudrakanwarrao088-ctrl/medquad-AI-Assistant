@echo off
title MedQuAD AI Medical Assistant
echo =======================================================
echo         MedQuAD AI Medical Assistant Launcher
echo =======================================================
echo.
echo Launching Streamlit Medical QA Web Application...
echo.

python -m streamlit run app.py --server.port 8501 --browser.gatherUsageStats false

pause

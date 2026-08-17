@echo off
title Forecasting Mutual Funds

echo ============================================================
echo   Forecasting Mutual Funds - Starting Application
echo ============================================================
echo.

:: ── Check Python venv ──────────────────────────────────────────────────────
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
    echo [Python] Virtual env activated
) else (
    echo [Python] No .venv found — using system Python
)
echo.
echo [Application] Starting Server on http://localhost:5000
echo.
echo Press Ctrl+C to stop the servers.
echo ============================================================
echo.
python app.py
echo Open http://localhost:5000 in your browser.
pause


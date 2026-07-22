@echo off
cd /d %~dp0
set "BUNDLED_PY=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
if exist "%BUNDLED_PY%" (
    "%BUNDLED_PY%" desktop_app.py
) else (
    python desktop_app.py
)
pause

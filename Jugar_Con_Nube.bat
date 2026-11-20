@echo off
cd /d "%~dp0"
title Pokemon Reloaded - Modo Nube Automatico

set LOCAL_PY=C:\Users\Profe Juanito\AppData\Roaming\uv\python\cpython-3.12-windows-x86_64-none\python.exe
if exist "%LOCAL_PY%" (
    "%LOCAL_PY%" sync_nube.py play
    goto :done
)

where python >nul 2>&1
if %errorlevel% equ 0 (
    python sync_nube.py play
    goto :done
)

where py >nul 2>&1
if %errorlevel% equ 0 (
    py sync_nube.py play
    goto :done
)

echo [ERROR] No se encontro Python en este PC.
:done
echo.
pause

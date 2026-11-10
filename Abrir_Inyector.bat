@echo off
cd /d "%~dp0"

:: 1. Probar ruta especifica local si existe
set LOCAL_PYW=C:\Users\Profe Juanito\AppData\Roaming\uv\python\cpython-3.12-windows-x86_64-none\pythonw.exe
if exist "%LOCAL_PYW%" (
    start "" "%LOCAL_PYW%" gui_inyector.pyw
    exit /b
)

:: 2. Probar comandos del sistema (para cuando se copie a otro PC)
where pythonw >nul 2>&1
if %errorlevel% equ 0 (
    start "" pythonw gui_inyector.pyw
    exit /b
)

where pyw >nul 2>&1
if %errorlevel% equ 0 (
    start "" pyw gui_inyector.pyw
    exit /b
)

where python >nul 2>&1
if %errorlevel% equ 0 (
    start "" python gui_inyector.pyw
    exit /b
)

where py >nul 2>&1
if %errorlevel% equ 0 (
    start "" py gui_inyector.pyw
    exit /b
)

echo [ERROR] No se encontro Python en este equipo.
echo Por favor instala Python o asegurate de marcar "Add Python to PATH" durante la instalacion.
echo Puedes descargarlo gratis desde https://www.python.org/
pause

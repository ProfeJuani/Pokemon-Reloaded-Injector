@echo off
cd /d "%~dp0"
echo ========================================================
echo   Subiendo Inyector a GitHub (ProfeJuani)
echo ========================================================
echo.
git push -u origin main
echo.
if %errorlevel% equ 0 (
    echo [EXITO] Los archivos se subieron correctamente a GitHub:
    echo https://github.com/ProfeJuani/Pokemon-Reloaded-Injector
) else (
    echo [ERROR] Hubo un problema al subir los archivos.
)
echo.
pause


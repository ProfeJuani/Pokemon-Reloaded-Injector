@echo off
:: Comprobar privilegios de Administrador
net session >nul 2>&1
if %errorLevel% neq 0 (
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

echo ========================================================
echo   Reparando conexion con GitHub en Windows...
echo ========================================================
echo.
powershell -NoProfile -Command "(Get-Content -Path $env:SystemRoot\System32\drivers\etc\hosts) -notmatch 'api\.github\.com' | Set-Content -Path $env:SystemRoot\System32\drivers\etc\hosts -Force"
ipconfig /flushdns >nul
echo [OK] Hosts reparado correctamente.
echo.
echo ========================================================
echo   Subiendo archivos a tu repositorio de GitHub...
echo ========================================================
echo.
cd /d "%~dp0"
git push -u origin main
echo.
if %errorlevel% equ 0 (
    echo ========================================================
    echo   [EXITO TOTAL] El inyector ya esta en tu GitHub:
    echo   https://github.com/ProfeJuani/Pokemon-Reloaded-Injector
    echo ========================================================
) else (
    echo [AVISO] Si te pidio iniciar sesion en el navegador, autorizalo y vuelve a ejecutar este archivo.
)
echo.
pause

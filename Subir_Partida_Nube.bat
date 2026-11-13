@echo off
cd /d "%~dp0"
echo ========================================================
echo   Subiendo Partida a la Nube (ProfeJuani)
echo ========================================================
echo.
set TEMP_DIR=%TEMP%\pkm_saves_sync
if exist "%TEMP_DIR%" rd /s /q "%TEMP_DIR%"

git clone https://github.com/ProfeJuani/pokemon-reloated-saves.git "%TEMP_DIR%"
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] No se pudo conectar con el repositorio.
    pause
    exit /b
)

copy /y "Proyecto Reloaded The Last Beta 1.9.2.2 Full\data\partidas\reloaded*.*" "%TEMP_DIR%\" >nul
cd /d "%TEMP_DIR%"
git add .
git commit -m "Partida sincronizada" >nul 2>&1
git push origin main
cd /d "%~dp0"
rd /s /q "%TEMP_DIR%"
echo.
echo ========================================================
echo   [EXITO] Tu partida actual ha sido subida a GitHub!
echo ========================================================
echo.
pause

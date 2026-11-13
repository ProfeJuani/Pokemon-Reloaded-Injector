@echo off
cd /d "%~dp0"
echo ========================================================
echo   Sincronizando Partida desde GitHub (ProfeJuani)
echo ========================================================
echo.
set TEMP_DIR=%TEMP%\pkm_saves_sync
if exist "%TEMP_DIR%" rd /s /q "%TEMP_DIR%"

git clone https://github.com/ProfeJuani/pokemon-reloated-saves.git "%TEMP_DIR%"
if %errorlevel% equ 0 (
    copy /y "%TEMP_DIR%\reloaded*.*" "Proyecto Reloaded The Last Beta 1.9.2.2 Full\data\partidas\" >nul
    rd /s /q "%TEMP_DIR%"
    echo.
    echo ========================================================
    echo   [EXITO] Partida descargada y sincronizada al 100%%!
    echo ========================================================
) else (
    echo.
    echo [ERROR] No se pudo descargar la partida desde GitHub.
)
echo.
pause

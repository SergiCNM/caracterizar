@echo off
echo ==============================================
echo    LANZADOR DE ACTUALIZACION CARACTERIZAR
echo ==============================================
echo.
echo Iniciando PowerShell con permisos de ejecucion temporal...
powershell.exe -ExecutionPolicy Bypass -NoProfile -File "%~dp0update_caracterizar.ps1"
echo.
pause

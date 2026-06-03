@echo off
echo Iniciando backend Flask (porta 5000)...
start "Backend Flask" cmd /k "cd /d "%~dp0backend-tde" && python main.py"

echo Iniciando frontend (porta 4200)...
start "Frontend" cmd /k "cd /d "%~dp0" && python -m http.server 4200"

timeout /t 2 /nobreak >nul
echo Abrindo navegador...
start http://localhost:4200

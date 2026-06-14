@echo off
setlocal
cd /d "%~dp0"

echo ============================================
echo   Jett-Events - iniciando projeto
echo ============================================

REM ---------- Backend (Python / Flask) ----------
if not exist ".venv" (
    echo [setup] Criando ambiente virtual .venv...
    python -m venv .venv
)

echo [setup] Instalando dependencias do backend...
call ".venv\Scripts\activate.bat"
python -m pip install --upgrade pip
pip install -r "backend-tde\requirements.txt"

echo [setup] Criando super usuario (CPF 1234)...
pushd "backend-tde"
python "database\seed_admin.py"
popd

REM ---------- Frontend (Angular / npm) ----------
echo [setup] Instalando dependencias do frontend...
pushd "frontend-tde"
call npm install
popd

REM ---------- Subindo os servidores em consoles separados ----------
echo [run] Abrindo consoles do backend e do frontend...

start "Jett-Events BACKEND" cmd /k "cd /d "%~dp0backend-tde" && call "%~dp0.venv\Scripts\activate.bat" && python main.py"

start "Jett-Events FRONTEND" cmd /k "cd /d "%~dp0frontend-tde" && npm start"

echo.
echo Pronto! Backend em http://localhost:5000 e Frontend em http://localhost:4200
echo Esta janela pode ser fechada.
endlocal

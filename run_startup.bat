@echo off
:: Script de execução do modo Startup do SAS-Caema
:: Simula o checkup automático que roda na inicialização do Windows

echo ========================================
echo         SAS - Caema
echo   Verificacao Automatica (Startup)
echo ========================================
echo.

:: Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo Por favor, instale o Python 3.8 ou superior.
    exit /b 1
)

:: Executa o módulo de startup
echo Iniciando verificacao automatica...
python app/modules/checkup/startup/main.py

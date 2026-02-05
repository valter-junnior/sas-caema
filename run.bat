@echo off
:: Script de inicialização rápida do SAS-Caema
:: Executa a aplicação principal

echo ========================================
echo         SAS - Caema
echo   Sistema de Automacao de Suporte
echo ========================================
echo.

:: Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo Por favor, instale o Python 3.8 ou superior.
    exit /b 1
)

:: Executa a aplicação
echo Iniciando aplicacao...
cd app
python app.py

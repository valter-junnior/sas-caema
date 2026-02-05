@echo off
:: Script para gerar executável .exe do SAS-Caema

echo ========================================
echo      SAS-Caema - Build Executavel
echo ========================================
echo.

:: Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo Por favor, instale o Python 3.8 ou superior.
    exit /b 1
)

echo Iniciando processo de build...
echo Isso pode levar alguns minutos...
echo.

python build_exe.py

if errorlevel 1 (
    echo.
    echo [ERRO] Falha ao gerar executavel!
    exit /b 1
)

echo.
echo ========================================
echo    Build concluido com sucesso!
echo ========================================
echo.
echo O executavel esta em: releases\SAS-Caema.exe
echo.
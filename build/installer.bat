@echo off
REM Script para gerar instalador do SAS-Caema
REM Requer Inno Setup instalado

echo ========================================
echo   SAS-Caema - Build do Instalador
echo ========================================
echo.

echo.
echo ========================================
echo   Gerando Executaveis...
echo ========================================
echo.

python build_exe.py

if errorlevel 1 (
    echo.
    echo ERRO ao gerar executaveis!
    echo Verifique os logs acima.
    exit /b 1
)

echo.
echo Executaveis gerados com sucesso!
echo Continuando com o instalador...
echo.
timeout /t 2 /nobreak >nul

REM Procura pelo Inno Setup
set INNO_PATH=""
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    set INNO_PATH="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
) else if exist "C:\Program Files\Inno Setup 6\ISCC.exe" (
    set INNO_PATH="C:\Program Files\Inno Setup 6\ISCC.exe"
) else if exist "%LOCALAPPDATA%\Programs\Inno Setup 6\ISCC.exe" (
    set INNO_PATH="%LOCALAPPDATA%\Programs\Inno Setup 6\ISCC.exe"
)

if %INNO_PATH%=="" (
    echo ERRO: Inno Setup nao encontrado!
    echo.
    echo Por favor, instale o Inno Setup 6:
    echo https://jrsoftware.org/isdl.php
    echo.
    exit /b 1
)

echo Gerando instalador...
echo.

REM Cria diretório de saída
if not exist "..\releases\installer" mkdir "..\releases\installer"

REM Compila o script
%INNO_PATH% "..\installer\setup.iss"

if %ERRORLEVEL%==0 (
    echo.
    echo ========================================
    echo   Instalador criado com sucesso!
    echo ========================================
    echo.
    echo Instalador: ..\releases\installer\SAS-Caema-Setup.exe
    echo.
) else (
    echo.
    echo ERRO ao gerar instalador!
    echo.
)
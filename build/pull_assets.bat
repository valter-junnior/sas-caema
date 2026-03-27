@echo off
:: Baixa app/assets/apps da pasta espelhada para ambiente local

echo ========================================
echo      SAS-Caema - Pull de Assets
echo ========================================
echo.

cd /d "%~dp0\.."
python build\supabase_assets.py pull

if errorlevel 1 (
    echo.
    echo [ERRO] Falha ao baixar assets da pasta espelhada.
    exit /b 1
)

echo.
echo [OK] Assets baixados com sucesso.

# Guia de Operacao

## 1. Execucao local (desenvolvimento)

Pre-requisitos:
- Python 3.8+
- Windows 10/11

Comandos:

```powershell
cd app
pip install -r requirements.txt
python app.py
```

## 2. Executar checkup startup manualmente

```powershell
cd app
python modules/checkup/startup/main.py
```

## 3. Build de executaveis

```powershell
build/build.bat
```

Resultado esperado:
- releases/SAS-Caema.exe
- releases/SAS-Caema-Startup.exe

## 4. Build do instalador

```powershell
build/installer.bat
```

Resultado esperado:
- releases/SAS-Caema-Setup.exe

## 5. Operacao do catalogo de apps

Catalogo local:
- app/assets/apps/catalog.csv (script/dev)
- %LOCALAPPDATA%/SAS-Caema/apps/catalog.csv (exe)

Fluxo operacional recomendado:
1. Publicar instalador em GitHub Releases ou repositorio raw.
2. Atualizar catalog.csv com id, installer_filename e opcional download_url.
3. Validar download na tela Instalar Aplicativos.

Exemplo de catalog.csv:

```csv
id,installer_filename,download_url
anydesk,AnyDesk.exe,
chrome,ChromeSetup.exe,https://github.com/SEU_USUARIO/SEU_REPO/releases/download/apps-v1/ChromeSetup.exe
```

Regra de resolucao:
- com download_url: usa URL direta;
- sem download_url: usa raw base + installer_filename.

## 6. Logs e diagnostico

Locais de log:
- app/logs/sas_caema.log (modo script)
- %LOCALAPPDATA%/SAS-Caema/logs/sas_caema.log (modo exe)

Quando investigar falhas:
- erros no download de catalogo/apps;
- erros de permissao no proxy/registro;
- falha de aplicacao do wallpaper;
- erro de inicializacao do wizard de rede/proxy.

## 7. Checklist rapido para suporte

- Aplicativo abre sem erro?
- Checkup conclui?
- Solucao de rede executa as 3 etapas?
- Proxy esperado esta ativo (10.39.192.11:3128)?
- Catalogo de apps atualiza?
- Instalador baixa e abre com elevacao?

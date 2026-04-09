# SAS Caema

Sistema de automacao de suporte para TI da Caema.

## Principais funcionalidades

- Checkup do sistema com validacoes e correcoes guiadas.
- Modo startup para rodar verificacoes automaticamente ao iniciar o Windows.
- Instalador de aplicativos com catalogo remoto (GitHub) e download sob demanda.
- Solucoes rapidas para problemas comuns de suporte.
- Papel de parede com informacoes tecnicas do equipamento.

## Instalacao rapida

### Usuario final (recomendado)

```powershell
.\build\installer.bat
installer\Output\SAS-Caema-Setup.exe
```

### Executavel portatil

```powershell
.\build\build.bat
releases\SAS-Caema.exe
```

### Modo desenvolvimento (Python)

```powershell
cd app
pip install -r requirements.txt
python app.py
```

## Como funciona o instalador de apps

- O app baixa o `catalog.csv` ao iniciar.
- Quando o usuario clica em instalar, o executavel do app e baixado naquele momento.
- Isso evita aumentar o tamanho do executavel principal.

Formato do catalogo:

```csv
id,installer_filename
anydesk,AnyDesk.exe
chrome,ChromeSetup.exe
```

Regra:
- Se o arquivo ainda nao existir localmente, o app baixa direto do repositorio remoto usando `installer_filename`.
- A URL base remota fica centralizada em `app/config.py` (`GITHUB_APPS_BASE_URL`).

## Requisitos

- Windows 10/11 (64-bit)
- Python 3.8+ para desenvolvimento

## Estrutura resumida

```text
app/        codigo-fonte
build/      scripts de build
installer/  instalador Inno Setup
releases/   executaveis gerados
docs/       documentacao
```

## Documentacao

- [docs/documentacao.md](docs/documentacao.md)
- [docs/diagramas.md](docs/diagramas.md)
- [docs/operacao.md](docs/operacao.md)
- [docs/changelogs/](docs/changelogs/)

## Suporte

- Log principal: `app/logs/sas_caema.log`

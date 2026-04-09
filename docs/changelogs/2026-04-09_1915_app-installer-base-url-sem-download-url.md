# Changelog - 2026-04-09 19:15 - App Installer sem download_url

## Resumo
Ajustado o fluxo de download de aplicativos para usar uma URL base centralizada no config e baixar sempre por installer_filename.

## Alteracoes
- Criada configuracao global GITHUB_APPS_BASE_URL em app/config.py.
- github_assets_service passou a usar GITHUB_APPS_BASE_URL para:
  - download do catalog.csv;
  - download de instaladores por nome de arquivo.
- CatalogService removido de download_url no modelo/parse.
- AppsDialog passou a baixar sempre por installer_filename quando o app nao existe localmente.
- Catalogo local simplificado para colunas:
  - id
  - installer_filename

## Documentacao atualizada
- README.md
- docs/documentacao.md
- docs/diagramas.md
- docs/operacao.md

## Resultado funcional
- Se o instalador ainda nao existe na maquina, o app baixa diretamente do repositorio remoto usando apenas o nome do arquivo no catalog.csv.

# Texto de Release - IMM

## SAS-Caema - Atualizacao de Distribuicao de Apps

Nesta release, o fluxo de distribuicao de aplicativos foi atualizado para usar um host remoto dedicado de assets.

### O que mudou

- O download de catalogo e instaladores deixou de depender do GitHub.
- A origem dos arquivos agora utiliza a base:
  - https://sas.areadoaluno.tec.br/assets/apps
- O servico de download foi renomeado para refletir a nova arquitetura:
  - de: app/common/services/github_assets_service.py
  - para: app/common/services/assets_service.py
- A documentacao tecnica e operacional foi atualizada para o novo fluxo.

### Ajustes de repositorio

- A pasta app/assets/apps passou a ser ignorada no versionamento.
- Os arquivos dessa pasta foram removidos do indice Git local (cached), evitando novo envio para o GitHub.

### Beneficios

- Repositorio principal mais leve.
- Publicacao de instaladores desacoplada do ciclo de release de codigo.
- Manutencao simplificada do catalogo e dos binarios.

### Impacto para o usuario final

- Nenhuma mudanca de uso na interface.
- O usuario continua clicando em Instalar Aplicativos normalmente.
- O download passa a ocorrer a partir do novo host remoto.

### Observacao

- Para efetivar a remocao no GitHub, e necessario concluir com commit e push destas alteracoes.

# Texto de Release - IMM

## SAS-Caema v1.0.1-beta

Release baseada nos 2 ultimos commits:
- feat: update app distribution flow to use dedicated remote assets host
- feat: update catalog CSV structure and enhance metadata extraction in CatalogService

### O que mudou

- O fluxo de distribuicao de aplicativos passou a usar host remoto dedicado para assets.
- Download de catalogo e instaladores padronizado para a base:
  - https://sas.areadoaluno.tec.br/assets/apps
- O catalogo foi evoluido para o formato:
  - id,nome,installer_filename
- A aplicacao agora considera o campo `nome` do catalogo para exibir o nome correto do app.
- A extracao de metadados dos executaveis foi aprimorada, mantendo fallback quando necessario.

### Beneficios

- Melhora de governanca no catalogo de apps com nome exibido controlado por CSV.
- Distribuicao de binarios desacoplada do ciclo de release do codigo.
- Experiencia de instalacao mais consistente para o usuario final.

### Impacto para o usuario final

- Nenhuma mudanca de fluxo na interface.
- O usuario continua instalando aplicativos pelo mesmo modulo.
- A lista de aplicativos fica mais precisa e padronizada.

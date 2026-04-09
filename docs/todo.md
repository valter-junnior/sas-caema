Resolvido: distribuição de aplicativos sem aumentar o executável

Decisão adotada (gratuita)
- Catálogo: manter o catalog.csv em repositório GitHub público (raw).
- Instaladores: publicar em GitHub Releases (assets dos releases) ou manter em raw quando pequeno.
- Aplicativo SAS: baixa catalog.csv ao iniciar e baixa o instalador somente quando o usuário clicar em Instalar.

Motivo da decisão
- Custo zero.
- Fácil de manter (upload simples no GitHub).
- Evita inflar o executável principal.
- Suporta atualização sem novo build do SAS.

Formato do catalog.csv
- Colunas:
	- id (obrigatório)
	- installer_filename (obrigatório; nome local salvo em app/assets/apps)
	- download_url (opcional; quando informado, usa URL direta)

Exemplo:
id,installer_filename,download_url
anydesk,AnyDesk.exe,https://github.com/SEU_USUARIO/SEU_REPO/releases/download/apps-v1/AnyDesk.exe
chrome,ChromeSetup.exe,

Regras de download implementadas
- Se download_url existir, o app usa essa URL.
- Se download_url estiver vazio, usa o padrão legado no repositório de assets via raw.

Fluxo operacional
1. Subir novo instalador no GitHub (preferencialmente em Releases).
2. Atualizar catalog.csv com novo app/versão/url.
3. Commit/push do catalog.csv.
4. Usuários recebem o catálogo atualizado automaticamente ao abrir o SAS.

Observação
- Supabase não é necessário para este cenário público.

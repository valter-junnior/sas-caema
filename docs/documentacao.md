# SAS-Caema - Documentacao Tecnica

## 1. Visao geral

O SAS-Caema e uma aplicacao desktop (PyQt5) para suporte tecnico com foco em automacao de tarefas recorrentes.

Objetivos principais:
- reduzir tempo de atendimento;
- padronizar diagnostico e correcoes;
- facilitar operacao para tecnico e usuario final;
- manter o executavel principal leve, baixando assets sob demanda.

## 2. Arquitetura do projeto

Estrutura base:
- app/: codigo-fonte principal.
- app/common/: componentes compartilhados (tema, widgets, servicos, views).
- app/modules/: modulos de negocio (checkup, wallpaper, rede, proxy, app_installer).
- build/: scripts de build com PyInstaller.
- installer/: script do instalador Inno Setup.
- releases/: saida dos executaveis e instalador.

Padrao geral:
- UI em PyQt5 nas pastas views.
- Regras de negocio em services.
- Entradas dos modulos em main.py de cada modulo.
- Configuracoes centralizadas em app/config.py e config.py de cada modulo.

## 3. Fluxo principal da aplicacao

Entrada:
- app/app.py cria QApplication, aplica tema global e abre MainWindow.
- Ao iniciar, o app tenta baixar o catalog.csv em background para o modulo de instalacao de apps.

Janela principal:
- app/common/views/main_window.py exibe 3 acoes:
  - Rodar Checkup
  - Executar Solucao
  - Instalar Aplicativos

## 4. Modulos e responsabilidades

### 4.1 Checkup

Arquivos-chave:
- app/modules/checkup/services/checkup_service.py
- app/modules/checkup/threads/checkup_thread.py
- app/modules/checkup/startup/main.py
- app/modules/checkup/startup/startup_feedback.py

Comportamento:
- executa verificacoes por modulos registrados;
- hoje o checkup carrega principalmente o modulo de wallpaper;
- pode aplicar correcao automatica quando encontra problema;
- no modo startup, mostra janela de feedback com progresso e status final.

### 4.2 Solucoes guiadas

Orquestracao:
- app/common/services/solutions_service.py
- app/common/views/solutions_dialog.py

Solucoes registradas:
- Verificacao de Cabos de Rede (wizard 3 etapas)
- Corrigir Papel de Parede
- Configurar Proxy (wizard 3 etapas)

### 4.3 Network Troubleshoot

Arquivos-chave:
- app/modules/network_troubleshoot/views/wizard_window.py
- app/modules/network_troubleshoot/views/step_widgets.py
- app/modules/network_troubleshoot/services/network_checker.py

Etapas:
1) verificar cabos e equipamento;
2) reiniciar modem/roteador;
3) testar conectividade com ping para hosts configurados.

### 4.4 Proxy Setup

Arquivos-chave:
- app/modules/proxy_setup/views/wizard_window.py
- app/modules/proxy_setup/views/step_widgets.py
- app/modules/proxy_setup/services/proxy_service.py

Comportamento:
- aplica proxy no registro do Windows (Internet Settings);
- tenta aplicar tambem via netsh winhttp;
- valida se o proxy atual corresponde ao esperado.

Proxy padrao:
- 10.39.192.11:3128

### 4.5 Wallpaper

Arquivos-chave:
- app/modules/wallpaper/main.py
- app/modules/wallpaper/services/system_info.py
- app/modules/wallpaper/services/image_generator.py
- app/modules/wallpaper/services/wallpaper_setter.py

Fluxo:
- coleta dados do sistema (usuario, host, IP, MAC etc.);
- gera imagem com texto sobre wallpaper base;
- aplica no Windows via API/registro.

### 4.6 Instalador de aplicativos

Arquivos-chave:
- app/modules/app_installer/views/apps_dialog.py
- app/modules/app_installer/services/catalog_service.py
- app/common/services/assets_service.py

Fluxo:
- le catalog.csv local;
- atualiza catalog.csv em background via host remoto;
- exibe grid de apps;
- se app nao existe localmente, baixa ao clicar em Instalar;
- baixa sempre por installer_filename usando a base configurada em app/config.py.

Schema do catalog.csv:
- id (obrigatorio)
- installer_filename (obrigatorio)

## 5. Design system e UI

Arquivos-chave:
- app/common/theme.py
- app/common/widgets.py
- app/common/views/dialogs.py

Elementos principais:
- paleta central em Colors;
- tipografia central em Fonts;
- estilos QSS reutilizaveis em Styles;
- componentes reutilizaveis para botoes, cards e dialogos.

## 6. Build e distribuicao

Arquivos-chave:
- build/build_exe.py
- build/build.bat
- build/installer.bat
- installer/setup.iss

Saidas principais:
- releases/SAS-Caema.exe
- releases/SAS-Caema-Startup.exe
- releases/SAS-Caema-Setup.exe

Resumo:
- build_exe.py gera os dois executaveis via PyInstaller;
- installer.bat compila o setup via Inno Setup;
- setup.iss define tarefas de atalho e startup.

## 7. Operacao e observabilidade

Logs:
- em modo script: app/logs/
- em modo executavel: %LOCALAPPDATA%/SAS-Caema/logs/

Assets de apps:
- em modo script: app/assets/apps/
- em modo executavel: %LOCALAPPDATA%/SAS-Caema/apps/

## 8. Pontos de atencao conhecidos

- Existem blocos com except Exception: pass em alguns pontos de download/atualizacao, o que dificulta diagnostico de falhas.
- O download de instaladores nao valida checksum/assinatura no fluxo atual.
- O arquivo app/common/views/main_window.py contem trecho legado adicional apos a classe principal, o que aumenta custo de manutencao.

## 9. Referencias rapidas

- Fluxo geral e diagramas: docs/diagramas.md
- Guia operacional e comandos: docs/operacao.md

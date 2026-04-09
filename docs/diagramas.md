# Diagramas da Aplicacao

Este arquivo concentra diagramas Mermaid para entendimento rapido do sistema.

## 1. Arquitetura de alto nivel

```mermaid
flowchart TB
    U[Usuario/Tecnico] --> UI[MainWindow - PyQt5]

    UI --> C[Checkup]
    UI --> S[Solucoes]
    UI --> A[Instalador de Apps]

    C --> CS[CheckupService]
    CS --> WM[WallpaperModule]

    S --> SS[SolutionsService]
    SS --> NT[NetworkTroubleshootModule]
    SS --> PM[ProxySetupModule]
    SS --> WF[WallpaperModule]

    A --> AD[AppsDialog]
    AD --> CAT[CatalogService]
    AD --> GHS[GitHubAssetsService]

    GHS --> GH[(GitHub Raw / Releases)]

    WM --> WIN[(Windows API + Registro)]
    PM --> REG[(Registro + netsh)]

    CS --> LOG[LoggerService]
    SS --> LOG
    AD --> LOG
```

## 2. Fluxo da aplicacao principal

```mermaid
sequenceDiagram
    participant User as Usuario
    participant App as app.py
    participant Main as MainWindow
    participant Git as github_assets_service

    User->>App: inicia aplicacao
    App->>Main: cria janela principal
    App->>Git: thread background download_catalog()
    Main-->>User: exibe 3 acoes principais

    alt Rodar Checkup
        User->>Main: clicar Rodar Checkup
        Main->>Main: inicia CheckupThread
    else Executar Solucao
        User->>Main: clicar Executar Solucao
        Main->>Main: abre SolutionsDialog
    else Instalar Aplicativos
        User->>Main: clicar Instalar Aplicativos
        Main->>Main: abre AppsDialog
    end
```

## 3. Fluxo do checkup

```mermaid
flowchart TD
    A[MainWindow - Rodar Checkup] --> B[CheckupThread]
    B --> C[CheckupService.run_full_checkup]
    C --> D[run_checks]
    D --> E[WallpaperModule.check]
    E --> F{status ok?}
    F -- Sim --> G[ResultDialogs sucesso]
    F -- Nao --> H[fix_issues]
    H --> I[WallpaperModule.execute]
    I --> J[ResultDialogs com problemas/correcao]
```

## 4. Fluxo do instalador de aplicativos

```mermaid
flowchart TD
    A[AppsDialog abre] --> B[CatalogService carrega catalog.csv local]
    A --> C[_CatalogUpdateThread baixa catalog.csv remoto]
    B --> D[Renderiza grid de apps]

    D --> E{App disponivel localmente?}
    E -- Sim --> F[launch_installer ShellExecute runas]
    E -- Nao --> G[_DownloadThread]

    G --> H{download_url preenchido?}
    H -- Sim --> I[download_app por URL direta]
    H -- Nao --> J[download_app por raw base + filename]

    I --> K[Salva em APPS_DIR]
    J --> K
    K --> F
```

## 5. Fluxo de solucao de rede

```mermaid
flowchart LR
    S1[Etapa 1: cabos/equipamento] --> S2[Etapa 2: reiniciar modem]
    S2 --> S3[Etapa 3: testar conexao]
    S3 --> T{Conectividade OK?}
    T -- Sim --> OK[Conexao restabelecida]
    T -- Nao --> NOK[Orienta abrir chamado]
```

## 6. Fluxo de configuracao de proxy

```mermaid
flowchart LR
    P1[Etapa 1: revisar proxy] --> P2[Etapa 2: aplicar]
    P2 --> P3[Etapa 3: verificar]

    P2 --> REG1[Registro Internet Settings]
    P2 --> N1[netsh winhttp set proxy]
    P3 --> V{Proxy esperado ativo?}
    V -- Sim --> Y[Conclui com sucesso]
    V -- Nao --> Z[Concluir com aviso]
```

## 7. Build e instalador

```mermaid
flowchart TD
    A[build/build.bat] --> B[build/build_exe.py]
    B --> C[PyInstaller - SAS-Caema.exe]
    B --> D[PyInstaller - SAS-Caema-Startup.exe]
    C --> E[releases]
    D --> E
    E --> F[build/installer.bat]
    F --> G[ISCC + installer/setup.iss]
    G --> H[releases/SAS-Caema-Setup.exe]
```

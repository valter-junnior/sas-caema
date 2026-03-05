; Script de instalação para SAS-Caema
; Usa Inno Setup 6 ou superior
; https://jrsoftware.org/isinfo.php

#define MyAppName "SAS-Caema"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Caema"
#define MyAppURL "https://caema.com.br"
#define MyAppExeName "SAS-Caema.exe"
#define MyStartupExeName "SAS-Caema-Startup.exe"

[Setup]
; Informações da aplicação
AppId={{8F9E5A2C-1D4B-4E3F-9A7C-6B8D5E4F3A2C}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

; Diretórios
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes

; Saída
OutputDir=..\releases
OutputBaseFilename=SAS-Caema-Setup
Compression=lzma
SolidCompression=yes

; Privilégios e compatibilidade
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

; Ícones e visual
SetupIconFile=..\app\assets\icon.ico
; WizardImageFile=.\wizard-image.bmp
; WizardSmallImageFile=.\wizard-small.bmp

; Desinstalador
UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na área de trabalho"; GroupDescription: "Atalhos adicionais:"
Name: "startupauto"; Description: "Iniciar automaticamente com o Windows (executará verificação do sistema)"; GroupDescription: "Inicialização:"

[Files]
; Executável principal
Source: "..\releases\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
; Executável de startup (com feedback visual)
Source: "..\releases\{#MyStartupExeName}"; DestDir: "{app}"; Flags: ignoreversion
; Logs (cria diretório vazio - fica comentado se não existir)
; Source: "..\app\logs\.gitkeep"; DestDir: "{app}\logs"; Flags: ignoreversion

[Icons]
; Atalho no Menu Iniciar
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
; Atalho na Área de Trabalho (opcional)
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
; Atalho no Startup (inicialização automática)
Name: "{userstartup}\{#MyAppName} Checkup"; Filename: "{app}\{#MyStartupExeName}"; Tasks: startupauto

[Run]
; Opção para executar após instalação
Filename: "{app}\{#MyAppExeName}"; Description: "Executar {#MyAppName}"; Flags: nowait postinstall skipifsilent

[Code]
// Código Pascal Script para customizações

function InitializeSetup(): Boolean;
var
  ResultCode: Integer;
  UninstallPath: String;
begin
  Result := True;
  
  // Verifica se já existe uma instalação
  if RegQueryStringValue(HKLM, 'Software\Microsoft\Windows\CurrentVersion\Uninstall\{#SetupSetting("AppId")}_is1', 'UninstallString', UninstallPath) then
  begin
    // Versão já instalada encontrada
    if MsgBox('Uma versão do {#MyAppName} já está instalada. Deseja desinstalar a versão anterior?', mbConfirmation, MB_YESNO) = IDYES then
    begin
      // Executa o desinstalador
      Exec(RemoveQuotes(UninstallPath), '/SILENT', '', SW_SHOW, ewWaitUntilTerminated, ResultCode);
    end
    else
    begin
      Result := False;
    end;
  end;
end;

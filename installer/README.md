# Guia de Instalação - Inno Setup

Para gerar o instalador do SAS-Caema, você precisa ter o Inno Setup instalado.

## Download e Instalação

1. **Baixe o Inno Setup 6:**
   - Acesse: https://jrsoftware.org/isdl.php
   - Baixe: `innosetup-6.x.x.exe` (versão estável mais recente)

2. **Instale:**
   - Execute o instalador
   - Siga o assistente de instalação
   - Aceite as configurações padrão

3. **Verifique a instalação:**
   ```bash
   # O instalador será instalado em:
   C:\Program Files (x86)\Inno Setup 6\
   ```

## Uso

Após instalar o Inno Setup, você pode gerar o instalador:

```bash
# Opção 1: Usar script batch
.\build\installer.bat
# (Gera executáveis automaticamente se necessário)

# Opção 2: Manual
python build\build_exe.py      # 1. Gerar executáveis
.\build\installer.bat           # 2. Gerar instalador
```

O instalador será criado em: `releases\installer\SAS-Caema-Setup.exe`

## Estrutura de Arquivos Necessária

```
sas-caema/
├── releases/
│   ├── SAS-Caema.exe           ← Gerado por build_exe.py
│   └── SAS-Caema-Startup.exe   ← Gerado por build_exe.py
├── build/
│   ├── build_exe.py            ← Gera executáveis
│   └── installer.bat           ← Gera instalador
├── installer/
│   └── setup.iss               ← Script do instalador
└── ...
```

## Customização (Opcional)

Para customizar o instalador, edite `installer/setup.iss`:

- **Ícone da aplicação:** Linha com `SetupIconFile=`
- **Imagens do wizard:** Linhas com `WizardImageFile=` e `WizardSmallImageFile=`
- **Informações da empresa:** Seção `[Setup]`
- **Arquivos incluídos:** Seção `[Files]`
- **Atalhos:** Seção `[Icons]`

## Troubleshooting

**Erro: "Inno Setup não encontrado"**
- Verifique se instalou na pasta padrão: `C:\Program Files (x86)\Inno Setup 6\`
- Se instalou em outro local, edite `build\installer.bat` e adicione o caminho

**Erro: "Executáveis não encontrados"**
- Execute `python build\build_exe.py` primeiro
- Verifique se `releases\SAS-Caema.exe` e `releases\SAS-Caema-Startup.exe` existem

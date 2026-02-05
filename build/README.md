# Scripts de Build

Esta pasta contém todos os scripts relacionados à geração de executáveis e instalador do SAS-Caema.

## 📁 Arquivos

- **`build_exe.py`** - Script Python que gera os executáveis usando PyInstaller
- **`build.bat`** - Wrapper batch para `build_exe.py` (Windows)
- **`installer.bat`** - Gera instalador usando Inno Setup 6

## 🚀 Uso Rápido

### Gerar Executáveis

```powershell
# Opção 1: Usar build.bat (recomendado)
.\build\build.bat

# Opção 2: Executar diretamente o Python script
python build\build_exe.py
```

**Resultado:**
- `releases\SAS-Caema.exe` - Aplicação principal
- `releases\SAS-Caema-Startup.exe` - Modo startup (com feedback visual)

### Gerar Instalador

```powershell
.\build\installer.bat
```

**Requisito:** Inno Setup 6 instalado
**Resultado:** `installer\Output\SAS-Caema-Setup.exe`

> **Nota:** O `installer.bat` verifica automaticamente se os executáveis existem e oferece gerá-los se necessário.

## 📝 Detalhes Técnicos

### build_exe.py

- Usa PyInstaller para criar executáveis standalone
- Gera 2 arquivos `.exe` separados:
  - **SAS-Caema.exe:** Interface gráfica principal
  - **SAS-Caema-Startup.exe:** Execução em segundo plano com janela de progresso
- Inclui todos os assets, módulos e dependências automaticamente
- Limpa arquivos temporários após build

### build.bat

- Verifica se Python está instalado
- Chama `build_exe.py` do mesmo diretório
- Exibe mensagens de progresso e erros

### installer.bat

- Verifica se executáveis existem
- Oferece gerar executáveis automaticamente se necessário
- Procura Inno Setup 6 em locais padrão
- Compila o script `installer\setup.iss`
- Cria instalador profissional com:
  - Assistente de instalação em português
  - Opção de desktop icon
  - Configuração automática de startup
  - Desinstalador completo

## 🔧 Configuração

### Personalizar Build

Edite `build_exe.py` para:
- Adicionar/remover arquivos incluídos
- Modificar hidden imports
- Alterar ícone da aplicação
- Ajustar configurações do PyInstaller

### Personalizar Instalador

Edite `..\installer\setup.iss` para:
- Mudar informações da empresa
- Adicionar/remover arquivos
- Customizar atalhos
- Modificar mensagens do wizard

## 🐛 Troubleshooting

**Erro: "PyInstaller não encontrado"**
```powershell
pip install pyinstaller
```

**Erro: "Inno Setup não encontrado"**
- Instale: https://jrsoftware.org/isdl.php
- Ou edite `installer.bat` para apontar para localização customizada

**Build falha com erro de imports**
- Verifique se todas as dependências estão em `app\requirements.txt`
- Adicione hidden imports em `build_exe.py` se necessário

**Executável não roda**
- Verifique logs em: `releases\logs\`
- Execute no terminal para ver mensagens de erro
- Verifique se caminhos relativos estão corretos

## 📦 Output

Após execução bem-sucedida:

```
releases/
├── SAS-Caema.exe              # ~50-60 MB
├── SAS-Caema-Startup.exe      # ~50-60 MB
└── logs/                       # Logs da aplicação

installer/
└── Output/
    └── SAS-Caema-Setup.exe    # ~110-120 MB
```

## 🔄 Fluxo Completo

```powershell
# 1. Desenvolver código em app/
cd app
python app.py  # Testar

# 2. Gerar executáveis
cd ..
.\build\build.bat

# 3. Testar executáveis
.\releases\SAS-Caema.exe
.\releases\SAS-Caema-Startup.exe

# 4. Gerar instalador
.\build\installer.bat

# 5. Testar instalador
.\installer\Output\SAS-Caema-Setup.exe

# 6. Distribuir SAS-Caema-Setup.exe
```

---

**Organização:** Esta pasta mantém todos os scripts de build organizados separadamente do código-fonte, facilitando manutenção e evitando confusão com arquivos temporários de build.

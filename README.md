# SAS - Caema
Sistema de Automação de Suporte para TI da Caema

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Windows](https://img.shields.io/badge/Platform-Windows%2010%2F11-blue.svg)](https://www.microsoft.com/windows)

---

## 📋 Sobre

Sistema automatizado para facilitar o trabalho de suporte de TI através de:
- 🔍 Checkup automático do sistema
- 🖼️ Papel de parede com informações para suporte (IP, MAC, usuário, etc.)
- ⚙️ Execução de soluções automatizadas
- 🚀 **Inicialização automática com Windows** (checkup em segundo plano)

---

## ⚡ Instalação Rápida

### Opção 1: Instalador (Recomendado para Usuários)
```powershell
# Gerar instalador profissional
.\build\installer.bat

# Executar instalador
installer\Output\SAS-Caema-Setup.exe

# Durante instalação:
# ✓ Marque "Iniciar com Windows" para checkup automático
# ✓ Escolha "Criar ícone na Área de Trabalho" (opcional)
```

### Opção 2: Executável Portátil
```powershell
# Gerar executáveis
.\build\build.bat
# ou: python build\build_exe.py

# Executar aplicação principal
releases\SAS-Caema.exe

# Executar em modo startup (checkup silencioso)
releases\SAS-Caema-Startup.exe
```

### Opção 3: Com Python (Para Desenvolvimento)
```powershell
# Instalar dependências
cd app
pip install -r requirements.txt

# Executar aplicação principal
python app.py

# Testar modo startup
python modules\checkup\startup\main.py
```

---

## 🚀 Como Usar

### Executar Aplicação
```powershell
# Com instalador (após instalar)
# Procurar "SAS-Caema" no Menu Iniciar

# Executável portátil
releases\SAS-Caema.exe

# Com Python (dev)
python app\app.py
```

### Inicialização Automática com Windows
A funcionalidade de startup é configurada automaticamente durante a instalação.

**Durante instalação:**
- ✓ Marque "Iniciar com Windows" no assistente
- Sistema adicionará entrada no Registro do Windows
- Toda inicialização: janela visual no canto inferior direito mostra progresso

**Após instalação:**
- Startup configurado em: `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`
- Executável: `SAS-Caema-Startup.exe` (checkup silencioso com feedback visual)
- Desinstalar remove automaticamente do startup

### Build e Distribuição
```powershell
# Gerar executáveis (2 arquivos: app principal + startup)
.\build\build.bat
# ou: python build\build_exe.py

# Gerar instalador Windows (recomendado)
.\build\installer.bat
# Nota: Roda build_exe.py automaticamente se necessário

# Resultado:
releases\                          # Executáveis portáteis
├── SAS-Caema.exe
└── SAS-Caema-Startup.exe

installer\Output\                 # Instalador profissional
└── SAS-Caema-Setup.exe
```

### Testar Módulos
```powershell
cd app

# Módulo de wallpaper
python modules\wallpaper\main.py

# Módulo de checkup
python modules\checkup\main.py

# Modo startup (com feedback visual)
python modules\checkup\startup\main.py
```

---

## 📁 Estrutura

```
sas-caema/
├── app/                              # Código-fonte
│   ├── common/                       # Componentes compartilhados
│   │   ├── services/                # Serviços (checkup, logging, config)
│   │   └── views/                   # Janelas e componentes visuais
│   ├── modules/                      # Módulos funcionais
│   │   ├── checkup/                 # Verificação e correção do sistema
│   │   │   ├── startup/             # Modo startup (execução automática)
│   │   │   │   ├── main.py         # Entry point do startup
│   │   │   │   └── startup_feedback.py  # Janela visual de progresso
│   │   │   ├── threads/             # Threads de checkup
│   │   │   └── main.py              # Checkup principal
│   │   └── wallpaper/               # Papel de parede com info do sistema
│   ├── app.py                        # Entry point da aplicação principal
│   └── config.py                     # Configurações
├── build/                            # Scripts de build
│   ├── build_exe.py                 # Gerar executáveis (PyInstaller)
│   ├── build.bat                    # Wrapper para build_exe.py
│   └── installer.bat                # Gerar instalador (Inno Setup)
├── installer/                        # Instalador Windows
│   ├── setup.iss                    # Script Inno Setup
│   └── Output/                       # Instalador gerado
│       └── SAS-Caema-Setup.exe
├── releases/                         # Executáveis gerados
│   ├── SAS-Caema.exe                # Aplicação principal
│   └── SAS-Caema-Startup.exe        # Modo startup
├── docs/                             # Documentação
│   ├── changelogs/                  # Histórico de mudanças
│   └── bugs.md                       # Issues conhecidos
└── run.bat                           # Executar com Python (desenvolvimento)
```

---

## ⚙️ Configuração

Edite `app/config.py` para personalizar:
- Cor do texto do papel de parede
- Posição das informações
- Configurações de checkup

---

## 🛠️ Desenvolvimento

### Instalar Dependências
```powershell
cd app
pip install -r requirements.txt
```

### Executar em Modo Dev
```powershell
cd app
python app.py
```

---

## 📝 Documentação

- [docs/documentacao.md](docs/documentacao.md) - Documentação técnica completa
- [docs/todo.md](docs/todo.md) - Tarefas e roadmap
- [docs/changelogs/](docs/changelogs/) - Histórico de mudanças

---

## 🔧 Requisitos

### Para Usuários (Instalador)
- **Windows:** 10/11 (64-bit)
- **Espaço:** ~150 MB
- **Privilégios:** Administrador (para instalação em Program Files)

### Para Desenvolvedores
- **Python:** 3.13+ (3.8+ compatível)
- **PyInstaller:** Para gerar executáveis
- **Inno Setup 6:** Para gerar instalador (opcional)
- **Dependências:** `pip install -r app/requirements.txt`

---

## Suporte

Problemas? Verifique:
1. Logs em `app/logs/sas_caema.log`

---

**Desenvolvido para Caema** | Versão 1.0.0

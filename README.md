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

### Opção 1: Executável (Recomendado para Usuários)
```powershell
# Gerar executável
.\build.bat

# Executar (não precisa Python!)
releases\SAS-Caema.exe
```

### Opção 2: Com Python (Para Desenvolvimento)
```powershell
# Instalar dependências
cd app
pip install -r requirements.txt

# Executar aplicação
python app.py

# Configurar startup (opcional - use menu na GUI)
python app.py
# Menu → Configurações → Iniciar com Windows
```

---

## 🚀 Como Usar

### Executar Aplicação
```powershell
# Com executável
releases\SAS-Caema.exe

# Com Python
.\run.bat
```

### Ativar Inicialização Automática
```powershell
# 1. Abrir aplicação
releases\SAS-Caema.exe

# 2. Menu → Configurações → Marcar "Iniciar com Windows"
# 3. Confirmar
# ✓ Sistema fará checkup automático toda vez que ligar o PC!
```

### Gerar Executável
```powershell
.\build.bat
```

### Testar Módulos
```powershell
cd app

# Módulo de wallpaper
python modules\wallpaper\main.py

# Módulo de checkup
python mapp.py        # Aplicação principal (com startup)
```

---

## 📁 Estrutura

```
sas-caema/
├── app/              # Código-fonte
│   ├── install.py   # Configurar sistema
│   └── ...
├── docs/             # Documentação
├── releases/         # Executáveis .exe
├── build.bat         # Gerar executável
└── run.bat           # Executar com Python (dev)
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

- **Windows:** 10/11 (64-bit)
- **Python:** 3.8+ (apenas para desenvolvimento)
- **Espaço:** ~100 MB

---

## 📞 Suporte

Problemas? Verifique:
1. Logs em `app/logs/sas_caema.log`
2. Documentação em `docs/`
3. Issues reportados em `docs/bugs.md`

---

**Desenvolvido para Caema** | Versão 1.0.0

# SAS-Caema - Sistema de Automação de Suporte

Sistema desktop para automação de tarefas de TI na Caema.

## Stack Tecnológica

**Linguagem:** Python 3.8+
**Framework GUI:** PyQt5 5.15.10
**Plataforma:** Windows 10/11

## Bibliotecas Utilizadas

**Interface e Sistema:**
- PyQt5 - Framework para interface gráfica desktop
- psutil 5.9.8 - Coleta de informações do sistema (CPU, memória, disco, rede)
- winotify 1.1.0 - Notificações nativas do Windows

**Processamento de Imagens:**
- Pillow 10.2.0 - Geração e manipulação de imagens (papel de parede)

**Utilitários:**
- colorlog 6.8.2 - Sistema de logging com cores no terminal

## Ferramentas de Build e Distribuição

**Compilação:**
- PyInstaller 6.3.0 - Converte aplicação Python em executáveis Windows (.exe)
- Gera dois executáveis: aplicação principal e modo startup

**Instalador:**
- Inno Setup 6 - Gerador de instalador Windows profissional
- Cria setup.exe com wizard de instalação
- Configuração automática de startup no registro do Windows

**Scripts de Build:**
- build_exe.py - Automação da compilação com PyInstaller
- build.bat - Script batch para build rápido
- installer.bat - Compilação do instalador

## Funcionalidades Principais

**1. Checkup Automático**
- Executa verificações automáticas no sistema
- Detecta e corrige problemas comuns
- Modo startup: executa silenciosamente ao iniciar Windows
- Feedback visual com janela de progresso
- Auto-fix de problemas detectados

**2. Troubleshooting de Rede**
- Wizard passo a passo para diagnóstico de rede
- Validação de conectividade
- Testes de DNS e gateway
- Interface guiada para usuários não técnicos

**3. Papel de Parede Informativo**
- Gera papel de parede com informações do sistema
- Exibe: nome do computador, usuário, IP, MAC address, data/hora
- Útil para suporte remoto identificar rapidamente a máquina
- Atualização automática das informações

**4. Sistema de Soluções**
- Interface para executar scripts e soluções automatizadas
- Organizado em categorias
- Execução em background de scripts batch
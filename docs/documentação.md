# SAS - Caema
## Sistema de Automação de Suporte

### 📋 Visão Geral
Sistema desenvolvido para automatizar tarefas rotineiras do setor de suporte de TI da Caema, incluindo instalação de aplicativos, configurações de proxy, instalação de impressoras e guias de resolução de problemas.

### 🛠️ Stack Tecnológica
- **Linguagens**: Python, Batch
- **Plataforma**: Windows 11
- **Interface**: UI/UX moderna e intuitiva

### 📐 Arquitetura do Projeto

```
sas-caema/
│
├── app.py                 # Aplicação principal
├── assets/                # Recursos estáticos (imagens, ícones, etc.)
│
├── common/                # Componentes compartilhados
│   ├── views/            # Visualizações comuns
│   └── services/         # Serviços compartilhados
│
├── modules/              # Módulos específicos
│   └── nome_do_modulo/
│       ├── views/        # Visualizações do módulo
│       ├── services/     # Serviços do módulo
│       └── batchs/       # Scripts batch do módulo
│
└── docs/                 # Documentação
    ├── prompt.md
    ├── documentação.md
    └── todo.md
```

### 🚀 Funcionalidades Principais

#### 1. Aplicação Principal
- **Menu intuitivo** com opções fáceis de navegar
- **Rodar Checkup**: Executa verificações de rotina do sistema
- **Executar Solução**: Executa soluções disponíveis para problemas detectados

#### 2. Módulo de Checkup
- **Inicialização automática**: Roda junto com o sistema operacional
- **Verificações automáticas**: Scripts de verificação ao iniciar
- **Feedback visual**: Notificações na área inferior direita da tela
- **Tratamento de erros**: Abre aplicação principal quando há problemas
- **Execução automática**: Resolve problemas automaticamente quando possível
- **Sistema de chamados**: Alerta o usuário para abrir chamado quando necessário

### 📦 Módulos Implementados

#### Módulo: Papel de Parede
**Objetivo**: Configurar automaticamente o papel de parede com informações úteis para o suporte.

**Funcionalidades**:
- Coleta informações do sistema:
  - Nome do usuário
  - Endereço MAC
  - Endereço IP
  - Outras informações relevantes para suporte
- Sobrepõe as informações em uma imagem personalizada
- Posiciona o texto no canto superior direito
- Permite configuração fácil da cor do texto (adaptável para fundos claros ou escuros)
- Define automaticamente como papel de parede do Windows

**Benefícios**:
- Facilita o atendimento de chamados
- Usuário tem acesso rápido às informações do sistema
- Reduz tempo de diagnóstico do suporte

### 🔧 Configuração e Instalação

#### Requisitos
- Windows 11
- Python 3.8+
- Permissões administrativas (para algumas operações)

#### Instalação
```bash
# Clone o repositório
git clone <repository-url>

# Entre no diretório
cd sas-caema

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
python app.py
```

#### Configuração de Inicialização Automática
O sistema deve ser configurado para iniciar junto com o Windows através do Registro do Windows ou da pasta de inicialização.

### 🎨 Design e UX
- Interface moderna e intuitiva
- Feedback visual para todas as operações
- Notificações não intrusivas
- Cores e layout configuráveis

### 🔄 Fluxo de Execução

1. **Inicialização do Sistema**
   - Sistema Windows inicia
   - SAS-Caema inicia automaticamente em segundo plano
   - Módulo de checkup é executado

2. **Execução do Checkup**
   - Scripts de verificação são executados
   - Feedback visual é exibido na tela
   - Problemas são detectados e registrados

3. **Tratamento de Problemas**
   - Problemas simples: Resolução automática
   - Problemas complexos: Abre aplicação principal
   - Problemas críticos: Solicita abertura de chamado

4. **Interação do Usuário**
   - Usuário pode executar checkup manualmente
   - Usuário pode executar soluções específicas
   - Usuário recebe feedback claro sobre todas as operações

### 📝 Notas de Desenvolvimento
- Todo código deve seguir as boas práticas do Python (PEP 8)
- Módulos devem ser independentes e reutilizáveis
- Tratamento de erros robusto em todas as operações
- Logs detalhados para diagnóstico
- Testes unitários para funcionalidades críticas

### 🔐 Segurança
- Execução com privilégios mínimos necessários
- Validação de entrada de usuário
- Proteção contra execução de código malicioso
- Logs de auditoria para operações críticas

### 🤝 Contribuição
- Siga a estrutura de pastas estabelecida
- Documente novas funcionalidades
- Atualize o todo.md com novas tarefas
- Mantenha a documentação sincronizada com o código

### 📞 Suporte
Para problemas ou dúvidas sobre o sistema, entre em contato com a equipe de desenvolvimento da Caema.


# TODO - SAS Caema

## 🎯 Prioridade Alta

### [ ] Módulo: Papel de Parede
**Descrição**: Implementar sistema de papel de parede personalizado com informações do sistema.

**Subtarefas**:
- [ ] Criar estrutura do módulo `wallpaper/`
  - [ ] Criar pasta `modules/wallpaper/`
  - [ ] Criar subpastas: `views/`, `services/`, `batchs/`
  
- [ ] Implementar coleta de informações do sistema
  - [ ] Coletar nome do usuário do Windows
  - [ ] Obter endereço MAC da interface de rede principal
  - [ ] Obter endereço IP (IPv4)
  - [ ] Coletar informações adicionais relevantes (hostname, domínio, etc.)
  
- [ ] Implementar geração do papel de parede
  - [ ] Carregar imagem base personalizada
  - [ ] Adicionar texto com informações no canto superior direito
  - [ ] Implementar sistema de cores configurável (para fundos claros/escuros)
  - [ ] Gerar imagem final com as informações sobrepostas
  
- [ ] Implementar configuração do papel de parede
  - [ ] Salvar imagem gerada em local apropriado
  - [ ] Configurar imagem como papel de parede do Windows via registro
  - [ ] Aplicar configurações de exibição (ajustar, preencher, etc.)
  
- [ ] Integrar com módulo de checkup
  - [ ] Adicionar verificação de papel de parede no checkup
  - [ ] Implementar lógica para atualizar apenas quando necessário
  - [ ] Adicionar tratamento de erros e logs

**Arquivos a criar**:
- `modules/wallpaper/services/system_info.py` - Coleta de informações
- `modules/wallpaper/services/image_generator.py` - Geração da imagem
- `modules/wallpaper/services/wallpaper_setter.py` - Configuração do papel de parede
- `modules/wallpaper/config.py` - Configurações do módulo
- `assets/wallpaper_base.png` - Imagem base (a ser fornecida)

---

## 🚀 Implementação da Estrutura Base

### [ ] Estrutura de Pastas
- [ ] Criar pasta `assets/`
- [ ] Criar pasta `common/views/`
- [ ] Criar pasta `common/services/`
- [ ] Criar pasta `modules/`

### [ ] Aplicação Principal (app.py)
- [ ] Criar arquivo `app.py`
- [ ] Implementar interface gráfica principal
  - [ ] Menu com opção "Rodar Checkup"
  - [ ] Menu com opção "Executar Solução"
- [ ] Implementar sistema de navegação entre módulos
- [ ] Adicionar gerenciamento de tema/estilo da UI

### [ ] Módulo de Checkup
- [ ] Criar estrutura do módulo `checkup/`
  - [ ] Pasta `modules/checkup/views/`
  - [ ] Pasta `modules/checkup/services/`
  - [ ] Pasta `modules/checkup/batchs/`
  
- [ ] Implementar lógica de checkup
  - [ ] Sistema de execução de verificações
  - [ ] Registro de resultados
  - [ ] Sistema de notificações visuais
  
- [ ] Criar notificação visual (canto inferior direito)
  - [ ] Exibir status atual da execução
  - [ ] Mostrar progresso das verificações
  - [ ] Alertas de erro com opções de ação
  
- [ ] Implementar tratamento de erros
  - [ ] Detectar tipo de problema
  - [ ] Execução automática de soluções quando possível
  - [ ] Abrir aplicação principal para problemas que requerem interação
  - [ ] Solicitar abertura de chamado para problemas críticos

### [ ] Sistema de Inicialização Automática
- [ ] Implementar registro no Windows Startup
  - [ ] Adicionar entrada no registro do Windows
  - [ ] OU adicionar atalho na pasta de inicialização
- [ ] Criar script de instalação/configuração
- [ ] Implementar modo silencioso para inicialização
- [ ] Garantir que checkup roda automaticamente ao iniciar

---

## 📦 Dependências e Configuração

### [ ] Configuração do Ambiente
- [ ] Criar `requirements.txt` com dependências Python
  - [ ] Biblioteca para UI (PyQt5, tkinter, etc.)
  - [ ] Pillow (PIL) para manipulação de imagens
  - [ ] psutil para informações do sistema
  - [ ] requests (se necessário para APIs)
  
- [ ] Criar arquivo de configuração global
  - [ ] Configurações de cores
  - [ ] Caminhos de arquivos
  - [ ] Configurações de checkup
  
- [ ] Criar `.gitignore` apropriado
- [ ] Documentar processo de instalação

---

## 🎨 Interface e UX

### [ ] Design da Interface Principal
- [ ] Escolher/criar biblioteca de UI
- [ ] Definir paleta de cores
- [ ] Criar layout responsivo
- [ ] Implementar ícones e recursos visuais

### [ ] Sistema de Notificações
- [ ] Notificações toast no Windows
- [ ] Popup de status de checkup
- [ ] Indicadores visuais de progresso
- [ ] Animações e transições suaves

## 📝 Notas

- Priorizar funcionalidades básicas antes de adicionar complexidade
- Manter código modular e reutilizável
- Documentar cada módulo à medida que é desenvolvido
- Testar extensivamente em ambiente de produção da Caema
- Coletar feedback dos usuários do suporte para melhorias contínuas

---

**Última atualização**: 05/02/2026

# Changelog - Módulo de Verificação de Cabos de Rede

**Data**: 2026-02-05  
**Hora**: 20:43  
**Tipo**: Nova Funcionalidade - Planejamento

## Resumo

Criação da documentação e planejamento completo para o novo módulo **"Verificação de Cabos de Rede"**, um wizard interativo de troubleshooting que será integrado ao botão "Executar Solução" da aplicação SAS-Caema.

## Objetivo

Implementar uma solução de autoatendimento que permita aos usuários diagnosticar e resolver problemas básicos de conectividade de rede antes de acionar o suporte técnico, reduzindo chamados desnecessários e aumentando a eficiência do suporte.

## Arquivos Criados

### Documentação
- **`docs/documentação.md`** - Documentação técnica completa do módulo
  - Visão geral e objetivos
  - Arquitetura detalhada
  - Estrutura de diretórios
  - Descrição de todos os componentes
  - Fluxo de uso com diagrama Mermaid
  - Integração com aplicação principal
  - Considerações de UX
  - Tecnologias utilizadas
  - Planos de extensibilidade

- **`docs/todo.md`** - Lista completa de tarefas de implementação
  - 8 fases de desenvolvimento
  - Mais de 100 tarefas detalhadas
  - Checklist organizado por componente
  - Dependências entre fases
  - Notas sobre testes e deploy

- **`docs/changelogs/2026-02-05_2043_network-troubleshoot-planning.md`** - Este arquivo

## Características do Módulo Planejado

### Wizard Passo-a-Passo (5 Etapas)

1. **Etapa 1**: Verificação física do cabo de rede
   - Checklist interativo
   - Imagem ilustrativa

2. **Etapa 2**: Verificação do roteador/modem
   - Verificação de alimentação
   - Checklist de status

3. **Etapa 3**: Verificação de LEDs de conexão
   - Identificação de status visual
   - Checklist de indicadores

4. **Etapa 4**: Reinício de equipamentos
   - Instruções passo a passo
   - Timer de 2 minutos para aguardar reinicialização

5. **Etapa 5**: Teste de conectividade
   - Botão de teste automático
   - Ping para múltiplos servidores
   - Resultado claro (sucesso/falha)

### Tela de Conclusão

- **Sucesso**: Mensagem de confirmação, internet restabelecida
- **Falha**: Orientação para abertura de chamado ao suporte

## Estrutura Técnica

### Novos Diretórios (a serem criados)
```
app/modules/network_troubleshoot/
├── services/
│   ├── network_checker.py      # Testes de conectividade
│   └── step_validator.py       # Validação de etapas
├── views/
│   ├── wizard_window.py        # Janela principal do wizard
│   └── step_widgets.py         # Widgets de cada etapa
└── assets/
    ├── step1_placeholder.png   # 5 imagens placeholder
    ├── step2_placeholder.png
    ├── step3_placeholder.png
    ├── step4_placeholder.png
    └── step5_placeholder.png
```

### Novos Componentes Principais
- `NetworkTroubleshootModule`: Classe principal do módulo
- `WizardWindow`: Interface PyQt5 do wizard
- `NetworkChecker`: Serviço de verificação de rede
- `StepValidator`: Controle de fluxo entre etapas
- `SolutionsService`: Novo serviço para gerenciar soluções disponíveis
- `SolutionsDialog`: Dialog de seleção de soluções

## Integrações com Sistema Existente

### Arquivos que Serão Modificados
- `app/common/views/main_window.py`
  - Método `show_solutions()` será implementado
  - Integração com novo SolutionsService

### Novos Serviços Comuns
- `app/common/services/solutions_service.py`
- `app/common/views/solutions_dialog.py`

## Tecnologias

- **PyQt5**: Interface gráfica (QDialog, QStackedWidget, QCheckBox)
- **subprocess**: Execução de comandos ping
- **pathlib**: Manipulação de arquivos
- **Logger**: Registro de diagnósticos

## Benefícios Esperados

1. **Redução de chamados**: Problemas simples resolvidos pelo usuário
2. **Padronização**: Processo uniforme de troubleshooting
3. **Educação**: Usuários aprendem procedimentos básicos
4. **Eficiência**: Suporte foca em problemas complexos
5. **Diagnóstico**: Coleta automática de informações relevantes

## Padrão de Design

O módulo segue o padrão já estabelecido no projeto:
- Estrutura similar aos módulos `checkup` e `wallpaper`
- Separação clara entre serviços (backend) e views (frontend)
- Uso de logger para rastreamento
- Configurações centralizadas em `config.py`
- Estilo visual consistente com aplicação principal

## Extensibilidade

O sistema de soluções é projetado para ser extensível. Futuros módulos podem incluir:
- Verificação de impressora
- Diagnóstico de VPN
- Limpeza de cache/temporários
- Reset de configurações de rede
- Diagnóstico de performance

## Próximos Passos

1. Revisar documentação com stakeholders
2. Validar fluxo de etapas com usuários finais
3. Obter imagens reais para substituir placeholders
4. Iniciar implementação seguindo o `todo.md`
5. Realizar testes com usuários reais antes do deploy

## Notas

- As imagens serão criadas como placeholders e deverão ser substituídas por imagens reais e contextualizadas
- O módulo não faz parte do checkup automático, apenas é executado sob demanda
- Logging detalhado para facilitar diagnóstico remoto pelo suporte
- Interface não-invasiva: não executa ações sem consentimento do usuário

## Impacto

- **Código novo**: ~1500 linhas estimadas
- **Arquivos novos**: ~15 arquivos
- **Arquivos modificados**: ~3 arquivos existentes
- **Assets**: 5 imagens placeholder

---

*Documentação criada como parte do planejamento inicial. Implementação seguirá conforme todo.md.*
